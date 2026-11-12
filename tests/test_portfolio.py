import csv
import hashlib
import importlib.util
import json
import math
import sys
import unittest
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from generate_demo import analyze, generate_rows, load_database, query


def read_csv(name):
    with (ROOT / 'data' / 'synthetic' / f'{name}.csv').open() as handle:
        return list(csv.DictReader(handle))


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if 'id' in attributes:
            self.ids.add(attributes['id'])
        for field in ['href', 'src']:
            if field in attributes:
                self.links.append(attributes[field])


class AnalyticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = json.loads((ROOT / 'docs' / 'assets' / 'results.json').read_text())

    def test_delivery_counts_and_denominators_from_csv(self):
        orders = read_csv('deliveries')
        self.assertEqual(len({row['order_id'] for row in orders}), len(orders))
        for metric in self.results['delivery']:
            zone = [row for row in orders if row['zone'] == metric['zone']]
            delivered = [row for row in zone if row['status'] == 'delivered']
            on_time = sum(int(row['actual_minutes']) <= int(row['promised_minutes']) for row in delivered)
            self.assertEqual(metric['orders'], len(zone))
            self.assertEqual(metric['delivered'], len(delivered))
            self.assertEqual(metric['on_time'], on_time)
            self.assertAlmostEqual(metric['on_time_rate'], on_time / len(delivered), places=6)
        self.assertTrue(all(row['actual_minutes'] == '' for row in orders if row['status'] == 'cancelled'))

    def test_retention_eligibility_and_exact_day_independently(self):
        players = read_csv('players')
        sessions = {(row['player_id'], int(row['day_number'])) for row in read_csv('sessions')}
        end = date.fromisoformat(self.results['observation_end'])
        mature = [row for row in players if date.fromisoformat(row['signup_date']) + timedelta(days=7) <= end]
        self.assertEqual(len(mature), 2047)
        self.assertEqual(len(players) - len(mature), 353)
        for variant, values in self.results['experiment']['groups'].items():
            selected = [row for row in mature if row['variant'] == variant]
            self.assertEqual(values['players'], len(selected))
            self.assertEqual(values['retained_d1'], sum((row['player_id'], 1) in sessions for row in selected))
            self.assertEqual(values['retained_d7'], sum((row['player_id'], 7) in sessions for row in selected))

    def test_maturity_boundary_and_no_session_player(self):
        tables = generate_rows()
        tables['players'] = [dict(player_id='edge', signup_date='2025-09-23', variant='A'), dict(player_id='new', signup_date='2025-09-24', variant='B'), dict(player_id='zero', signup_date='2025-09-22', variant='A')]
        tables['sessions'] = [dict(player_id='edge', day_number=7), dict(player_id='edge', day_number=3), dict(player_id='new', day_number=1)]
        rows = query(load_database(tables), 'retention')
        self.assertEqual(sum(row['players'] for row in rows), 2)
        self.assertEqual(sum(row['retained_d7'] for row in rows), 1)
        self.assertEqual(sum(row['retained_d1'] for row in rows), 0)

    def test_campaign_join_and_response_from_csv(self):
        customers = {row['customer_id']: row for row in read_csv('customers')}
        campaigns = read_csv('campaigns')
        self.assertEqual(len(customers), 800)
        self.assertEqual(len({row['customer_id'] for row in campaigns}), len(campaigns))
        self.assertEqual(set(customers), {row['customer_id'] for row in campaigns})
        for metric in self.results['campaign']:
            recipients = [row for row in campaigns if customers[row['customer_id']]['segment'] == metric['segment']]
            responses = sum(int(row['responded']) for row in recipients)
            self.assertEqual(metric['customers'], len(recipients))
            self.assertEqual(metric['responses'], responses)
            self.assertAlmostEqual(metric['response_rate'], responses / len(recipients))

    def test_statistical_interval_and_p_value(self):
        experiment = self.results['experiment']
        control, treatment = experiment['groups']['A'], experiment['groups']['B']
        control_rate, treatment_rate = 303 / 1015, 312 / 1032
        difference = treatment_rate - control_rate
        variance = control_rate * (1 - control_rate) / 1015 + treatment_rate * (1 - treatment_rate) / 1032
        self.assertAlmostEqual(experiment['difference'], difference)
        self.assertAlmostEqual(experiment['ci_low'], difference - 1.96 * math.sqrt(variance))
        self.assertAlmostEqual(experiment['ci_high'], difference + 1.96 * math.sqrt(variance))
        self.assertAlmostEqual(experiment['p_value'], 0.8511348541553908)
        self.assertLess(experiment['ci_low'], 0)
        self.assertGreater(experiment['ci_high'], 0)

    def test_deterministic_manifest(self):
        self.assertEqual(generate_rows(), generate_rows())
        manifest = json.loads((ROOT / 'data' / 'synthetic' / 'manifest.json').read_text())
        for filename, expected_hash in manifest['files'].items():
            self.assertEqual(hashlib.sha256((ROOT / 'data' / 'synthetic' / filename).read_bytes()).hexdigest(), expected_hash)
        self.assertEqual(analyze(generate_rows()), self.results)

    def test_local_links_fragments_and_private_content(self):
        site = ROOT / 'docs'
        for path in site.rglob('*.html'):
            content = path.read_text()
            self.assertNotIn('778-896', content)
            self.assertNotIn('Product Manager', content)
            parser = LinkParser()
            parser.feed(content)
            for target in parser.links:
                url = urlsplit(target)
                if url.scheme or url.netloc or target.startswith('/'):
                    continue
                destination = path.parent / unquote(url.path) if url.path else path
                self.assertTrue(destination.is_file(), f'{path}: broken link {target}')
                if url.fragment:
                    other = LinkParser()
                    other.feed(destination.read_text())
                    self.assertIn(url.fragment, other.ids, f'{path}: missing fragment {target}')

    def test_flask_api_when_available(self):
        try:
            import flask
        except ImportError:
            self.skipTest('Optional Flask dependency is not installed')
        spec = importlib.util.spec_from_file_location('delivery_app', ROOT / 'projects' / 'delivery' / 'app.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        client = module.app.test_client()
        self.assertEqual(client.get('/api/delivery').status_code, 200)
        filtered = client.get('/api/delivery/north').get_json()
        self.assertEqual([row['zone'] for row in filtered['rows']], ['North'])
        self.assertEqual(client.get('/api/delivery/unknown').status_code, 404)


if __name__ == '__main__':
    unittest.main()
