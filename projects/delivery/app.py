import sys
from pathlib import Path

from flask import Flask, abort, jsonify


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from generate_demo import analyze, generate_rows


app = Flask(__name__)


@app.get('/')
def home():
    return '<h1>Delivery analytics demo</h1><p>Portfolio reconstruction / synthetic data.</p><p><a href="/api/delivery">View operational metrics</a></p>'


@app.get('/api/delivery')
@app.get('/api/delivery/<zone>')
def metrics(zone=None):
    results = analyze(generate_rows())
    rows = results['delivery']
    if zone is not None:
        rows = [row for row in rows if row['zone'].lower() == zone.lower()]
        if not rows:
            abort(404)
    return jsonify(provenance=results['provenance'], period='2025-09-01 to 2025-09-30', rows=rows, route=results['route'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
