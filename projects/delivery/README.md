# Delivery Operations Analytics Platform

**Portfolio reconstruction / demo / synthetic data.** All code in this directory is newly authored. Displayed results are not original project achievements.

## Resume-declared scope

- Designed and developed a Python-based analytics platform to support operational planning, route optimization, and reporting.
- Built data workflows to clean, validate, and structure operational datasets for analysis and dashboard monitoring.
- Applied optimization logic to improve scheduling visibility, resource allocation, and operational decision-making.

These self-reported bullets were transcribed from the source resume; see [provenance](../../provenance/README.md).

## Question

Where does delivery performance vary, and how can a small analytics service make planning easier?

## Technology

Python · Flask · SQLite

## Reconstruction method

### Validate the operational grain

Use one row per order, unique IDs, explicit cancellation status, and nullable duration for cancelled work. Keep cancellations visible outside the delivered-order denominator.

### Aggregate before presenting

Run the versioned SQL by zone. Calculate on-time rates from on-time and delivered counts, then reconcile them to all orders. Publish the same outputs to the website and local API.

### Explore a planning heuristic

Compare input order with nearest-neighbour routing on a fixed 12-stop synthetic batch. Use Euclidean round-trip distance with a depot at (0,0). The heuristic is feasible for this simplified geometry, not a proven optimum.

## Demonstration findings

Across 900 synthetic orders, 698 of 865 delivered orders met the 50-minute promise (80.7%). The fixed 12-stop geometry measures 166.4 km in input order and 91.7 km with nearest-neighbour ordering. This is an illustrative route comparison, not a business saving.

## Metric definitions

| Metric | Definition | Scope |
| --- | --- | --- |
| On-time rate | On-time delivered orders / all delivered orders | Cancelled orders excluded; promise = 50 minutes. |
| Mean service time | Sum of actual minutes / delivered orders | Minutes; cancelled orders have no duration. |
| Cancellation rate | Cancelled orders / all orders | Separate reliability indicator. |
| Route distance | Sum of Euclidean legs including depot return | Fictional kilometres; one fixed 12-stop batch. |

## Limitations

No traffic, vehicle capacities, time windows, address data or production monitoring. Synthetic zone differences are generator assumptions. There is no observed before/after operational improvement.

## Next step

With approved real data: validate timestamps, profile late delivery tails, add vehicle and time-window constraints, and test scheduling decisions prospectively.

## Run and inspect

From the repository root:

```sh
python3 scripts/generate_demo.py
python3 scripts/build_site.py
python3 -m unittest discover -s tests
```

See [CSV dictionary](../../data/README.md), [SQL](metrics.sql), [computed outputs](../../docs/assets/results.json), and [website source](../../docs/projects/delivery.html).

Optional local API:

```sh
python3 -m pip install -r requirements.txt
python3 projects/delivery/app.py
```

Open `http://127.0.0.1:5000/api/delivery` or `/api/delivery/north`. It is not hosted by GitHub Pages.
