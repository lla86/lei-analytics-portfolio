# Player Retention & Experimentation Analytics

**Portfolio reconstruction / demo / synthetic data.** All code in this directory is newly authored. Displayed results are not original project achievements.

## Resume-declared scope

- Conducted cohort analysis to evaluate D1 and D7 retention metrics and identify engagement trends across player segments.
- Performed A/B testing analysis to measure the impact of product changes on engagement, retention, and player behavior.
- Identified behavioral indicators associated with churn and long-term engagement to support product quality insights.
- Automated KPI reporting and translated findings into dashboard-ready metrics for stakeholder communication.

These self-reported bullets were transcribed from the source resume; see [provenance](../../provenance/README.md).

## Question

How do D1 and D7 retention differ across cohorts, and does variant B have evidence of a D7 effect?

## Technology

SQL · Python · Statistics

## Reconstruction method

### Define eligibility first

Use an observation end of September 30, 2025. Require signup + 7 days to fall within that window. The 353 newer synthetic players are excluded from both reported D1 and D7 denominators.

### Build player-level flags

Left join activity to the eligible player population, deduplicate at player-day grain, and create exact-day D1 and D7 indicators. Aggregate the flags by signup cohort and randomized variant.

### Evaluate the primary comparison

Use a two-sided pooled two-proportion z test for D7 at alpha 0.05. Report B minus A with an unpooled Wald 95% confidence interval. Check 50:50 sample-ratio mismatch; D1 is descriptive.

## Demonstration findings

Of 2,400 synthetic players, 2,047 have complete D7 follow-up. D7 is 29.9% in A and 30.2% in B. The estimated difference is +0.38 percentage points (95% CI -3.59 to +4.35; p=0.851). The interval includes zero: there is insufficient evidence of a D7 effect in this simulation. SRM p=0.707; this check alone does not validate an experiment.

## Metric definitions

| Metric | Definition | Scope |
| --- | --- | --- |
| D1 retention | Players active exactly day 1 / D7-mature players | Same eligible denominator as D7 for comparability. |
| D7 retention | Players active exactly day 7 / D7-mature players | Primary endpoint; exact-day, not rolling retention. |
| Absolute difference | D7 rate B - D7 rate A | Percentage points, not relative percent. |
| 95% interval | Difference ± 1.96 × unpooled standard error | Approximate interval; assumptions in data dictionary. |

## Limitations

The assignment and activity are simulated. Independent Bernoulli activity by day is a simplification, so this is not a realistic churn model or evidence of real player behavior. No long-term churn prediction or multiple-endpoint causal claim is made.

## Next step

With real event logs: audit assignment and exposure, freeze the observation window, assess experiment power, inspect guardrails and estimate long-term retention only after cohorts mature.

## Run and inspect

From the repository root:

```sh
python3 scripts/generate_demo.py
python3 scripts/build_site.py
python3 -m unittest discover -s tests
```

See [CSV dictionary](../../data/README.md), [SQL](metrics.sql), [computed outputs](../../docs/assets/results.json), and [website source](../../docs/projects/retention.html).
