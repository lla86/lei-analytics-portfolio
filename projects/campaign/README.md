# Customer Behavior & Campaign Analytics

**Portfolio reconstruction / demo / synthetic data.** All code in this directory is newly authored. Displayed results are not original project achievements.

## Resume-declared scope

- Analyzed engagement and campaign response data across 2,000+ customer records using SQL and Python.
- Developed customer segments using recency, purchase behavior, and spending patterns to identify high-value groups.
- Built Power BI dashboards to monitor conversion, retention, campaign performance, and customer behavior metrics.
- Generated data-driven recommendations to improve customer targeting and lifecycle marketing initiatives.

These self-reported bullets were transcribed from the source resume; see [provenance](../../provenance/README.md).

## Question

How can simple lifecycle segments make campaign response easier to inspect without confusing association with lift?

## Technology

SQL · Python · Power BI

## Reconstruction method

### Freeze a pre-campaign snapshot

Use recency, 180-day purchase count and historical spend from before the fictional September campaign. Assign each of 800 synthetic customers exactly one recipient record.

### Apply interpretable segment rules

Loyal: recency ≤ 60 days and purchases ≥ 8; At risk: recency > 90 days; Developing: everyone else. Profile spend by segment; no hidden clustering or asserted optimal thresholds.

### Prepare a dashboard model

Join one customer to one campaign record, aggregate response counts, and recalculate the response ratio. Supply CSV inputs, explicit DAX measures and a Power BI build guide; no original .pbix file is included.

## Demonstration findings

The 800 synthetic customers are assigned to three mutually exclusive lifecycle segments. Response differences illustrate an inspectable reporting workflow; segment response probabilities were deliberately encoded in the generator. Historical spending is a customer profile measure and cannot be interpreted as attributed campaign revenue.

## Metric definitions

| Metric | Definition | Scope |
| --- | --- | --- |
| Response rate | Responses within 14 days / assigned recipients | A response is not assumed to be a purchase. |
| Segment share | Customers in segment / all 800 customers | Mutually exclusive snapshot segments. |
| Historical spend | Sum of pre-campaign spend_cad | CAD over prior 180 days; not campaign revenue. |
| Spend per customer | Historical spend / customers in segment | Descriptive value profile, not lifetime value. |

## Limitations

Synthetic response probabilities depend on the segment by construction. This is observational segmentation, with no control group, incremental lift, ROI or customer lifetime value estimate. The resume reports 2,000+ customer records; this separate demo uses 800.

## Next step

With consented customer data: confirm source provenance, validate stable segment definitions, run a randomized campaign holdout and measure incremental conversion with complete follow-up.

## Run and inspect

From the repository root:

```sh
python3 scripts/generate_demo.py
python3 scripts/build_site.py
python3 -m unittest discover -s tests
```

See [CSV dictionary](../../data/README.md), [SQL](metrics.sql), [computed outputs](../../docs/assets/results.json), and [website source](../../docs/projects/campaign.html).

See the [Power BI build guide](POWER_BI.md) and [DAX measures](measures.dax). No `.pbix` file is included or claimed. Existing public work: [customer-campaign-analysis](https://github.com/lla86/customer-campaign-analysis), inspected read-only; its calculations were not audited or reused.
