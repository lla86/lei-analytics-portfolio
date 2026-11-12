import csv
import hashlib
import json
import math
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'synthetic'
SEED = 20261112
OBSERVATION_END = '2025-09-30'


def write_csv(name, rows):
    with (DATA / f'{name}.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def generate_rows():
    generator = random.Random(SEED)
    deliveries = []
    for order_number in range(900):
        zone = generator.choice(['Central', 'North', 'South'])
        cancelled = generator.random() < 0.045
        actual = max(8, round(generator.gauss({'Central': 35, 'North': 46, 'South': 40}[zone], 12)))
        deliveries.append(dict(order_id=f'D{order_number:04d}', service_date=str(date(2025, 9, 1) + timedelta(days=order_number % 30)), zone=zone, status='cancelled' if cancelled else 'delivered', promised_minutes=50, actual_minutes='' if cancelled else actual, x_km=round(generator.uniform(0, 20), 3), y_km=round(generator.uniform(0, 20), 3)))
    players, sessions = [], []
    for player_number in range(2400):
        variant = 'B' if generator.random() < 0.5 else 'A'
        players.append(dict(player_id=f'P{player_number:04d}', signup_date=str(date(2025, 9, 1) + timedelta(days=player_number % 27)), variant=variant))
        for day_number in [0, 1, 3, 7, 14]:
            probability = {0: 1, 1: 0.53, 3: 0.38, 7: 0.27 + (0.035 if variant == 'B' else 0), 14: 0.19}[day_number]
            if generator.random() < probability:
                sessions.append(dict(player_id=f'P{player_number:04d}', day_number=day_number))
    customers, campaigns = [], []
    for customer_number in range(800):
        recency = generator.randint(1, 180)
        purchases = generator.randint(1, 16)
        spend = round(purchases * generator.uniform(20, 100), 2)
        segment = 'Loyal' if recency <= 60 and purchases >= 8 else 'At risk' if recency > 90 else 'Developing'
        customers.append(dict(customer_id=f'C{customer_number:04d}', recency_days=recency, purchases_180d=purchases, spend_cad=spend, segment=segment))
        campaigns.append(dict(customer_id=f'C{customer_number:04d}', campaign='September demo', responded=int(generator.random() < {'Loyal': 0.26, 'At risk': 0.07, 'Developing': 0.13}[segment])))
    return dict(deliveries=deliveries, players=players, sessions=sessions, customers=customers, campaigns=campaigns)


def load_database(tables):
    connection = sqlite3.connect(':memory:')
    connection.row_factory = sqlite3.Row
    connection.executescript('''
        CREATE TABLE deliveries(order_id TEXT PRIMARY KEY, service_date TEXT, zone TEXT, status TEXT, promised_minutes INTEGER, actual_minutes INTEGER, x_km REAL, y_km REAL);
        CREATE TABLE players(player_id TEXT PRIMARY KEY, signup_date TEXT, variant TEXT);
        CREATE TABLE sessions(player_id TEXT REFERENCES players, day_number INTEGER, PRIMARY KEY(player_id, day_number));
        CREATE TABLE customers(customer_id TEXT PRIMARY KEY, recency_days INTEGER, purchases_180d INTEGER, spend_cad REAL, segment TEXT);
        CREATE TABLE campaigns(customer_id TEXT PRIMARY KEY REFERENCES customers, campaign TEXT, responded INTEGER CHECK(responded IN (0, 1)));
    ''')
    for name, rows in tables.items():
        values = [tuple(None if value == '' else value for value in row.values()) for row in rows]
        placeholders = ','.join('?' for field in rows[0])
        connection.executemany(f'INSERT INTO {name} VALUES ({placeholders})', values)
    return connection


def query(connection, project):
    sql = (ROOT / 'projects' / project / 'metrics.sql').read_text()
    return [dict(row) for row in connection.execute(sql, dict(observation_end=OBSERVATION_END))]


def experiment(cohorts):
    totals = {variant: dict(players=0, retained_d1=0, retained_d7=0) for variant in ['A', 'B']}
    for row in cohorts:
        for field in totals[row['variant']]:
            totals[row['variant']][field] += row[field]
    control, treatment = totals['A'], totals['B']
    control_rate = control['retained_d7'] / control['players']
    treatment_rate = treatment['retained_d7'] / treatment['players']
    difference = treatment_rate - control_rate
    standard_error = math.sqrt(control_rate * (1 - control_rate) / control['players'] + treatment_rate * (1 - treatment_rate) / treatment['players'])
    pooled = (control['retained_d7'] + treatment['retained_d7']) / (control['players'] + treatment['players'])
    null_error = math.sqrt(pooled * (1 - pooled) * (1 / control['players'] + 1 / treatment['players']))
    total = control['players'] + treatment['players']
    chi_square = sum((group['players'] - total / 2) ** 2 / (total / 2) for group in totals.values())
    result = dict(groups=totals, d7_control=control_rate, d7_treatment=treatment_rate, difference=difference, ci_low=difference - 1.96 * standard_error, ci_high=difference + 1.96 * standard_error, p_value=math.erfc(abs(difference / null_error) / math.sqrt(2)), srm_p_value=math.erfc(math.sqrt(chi_square / 2)), primary_metric='Exact-day D7 retention', method='Two-sided pooled two-proportion z test; unpooled Wald 95% CI; SRM chi-square df=1; alpha=0.05')
    return {key: round(value, 12) if isinstance(value, float) else value for key, value in result.items()}


def route_distance(points):
    origin = (0, 0)
    previous = origin
    distance = 0
    for point in points + [origin]:
        distance += math.dist(previous, point)
        previous = point
    return distance


def route_demo(deliveries):
    batch = [row for row in deliveries if row['service_date'] == '2025-09-01' and row['status'] == 'delivered'][:12]
    remaining = [(row['x_km'], row['y_km']) for row in batch]
    baseline = route_distance(remaining)
    ordered, previous = [], (0, 0)
    while remaining:
        selected = min(remaining, key=lambda point: math.dist(previous, point))
        remaining.remove(selected)
        ordered.append(selected)
        previous = selected
    return dict(stops=len(batch), baseline_km=round(baseline, 6), heuristic_km=round(route_distance(ordered), 6), assumption='Synthetic Euclidean coordinates, one vehicle, depot (0,0), round trip; input-order baseline; no traffic, capacity or time windows. Not a real dispatch saving or a proven optimum.')


def analyze(tables):
    connection = load_database(tables)
    cohorts = query(connection, 'retention')
    delivery = query(connection, 'delivery')
    return dict(provenance='portfolio reconstruction / demo / synthetic data', seed=SEED, observation_end=OBSERVATION_END, delivery=delivery, route=route_demo(tables['deliveries']), retention=cohorts, experiment=experiment(cohorts), campaign=query(connection, 'campaign'), counts={name: len(rows) for name, rows in tables.items()})


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    tables = generate_rows()
    for name, rows in tables.items():
        write_csv(name, rows)
    result = analyze(tables)
    (ROOT / 'docs' / 'assets').mkdir(parents=True, exist_ok=True)
    (ROOT / 'docs' / 'assets' / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    manifest = dict(seed=SEED, provenance=result['provenance'], files={path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(DATA.glob('*.csv'))})
    (DATA / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(dict(counts=result['counts'], experiment=result['experiment'], route=result['route']), indent=2))


if __name__ == '__main__':
    main()
