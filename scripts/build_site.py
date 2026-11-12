import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'
REPO = 'https://github.com/lla86/lei-analytics-portfolio'
CLAIMS = json.loads((ROOT / 'provenance' / 'resume_claims.json').read_text())
RESULTS = json.loads((SITE / 'assets' / 'results.json').read_text())


def escape(value):
    return html.escape(str(value))


def percent(value):
    return f'{value:.1%}'


PROJECTS = {
    'delivery': dict(number='01', category='OPERATIONS & SYSTEMS', short='From orders to operational clarity.', question='Where does delivery performance vary, and how can a small analytics service make planning easier?', summary='A Python and SQLite workflow turns fictional order records into validated service metrics. A local Flask API exposes the results, with a routing heuristic to illustrate planning trade-offs.', stack=['Python', 'Flask', 'SQLite'], methods=[('Validate the operational grain', 'Use one row per order, unique IDs, explicit cancellation status, and nullable duration for cancelled work. Keep cancellations visible outside the delivered-order denominator.'), ('Aggregate before presenting', 'Run the versioned SQL by zone. Calculate on-time rates from on-time and delivered counts, then reconcile them to all orders. Publish the same outputs to the website and local API.'), ('Explore a planning heuristic', 'Compare input order with nearest-neighbour routing on a fixed 12-stop synthetic batch. Use Euclidean round-trip distance with a depot at (0,0). The heuristic is feasible for this simplified geometry, not a proven optimum.')], metrics=[('On-time rate', 'On-time delivered orders / all delivered orders', 'Cancelled orders excluded; promise = 50 minutes.'), ('Mean service time', 'Sum of actual minutes / delivered orders', 'Minutes; cancelled orders have no duration.'), ('Cancellation rate', 'Cancelled orders / all orders', 'Separate reliability indicator.'), ('Route distance', 'Sum of Euclidean legs including depot return', 'Fictional kilometres; one fixed 12-stop batch.')], limits='No traffic, vehicle capacities, time windows, address data or production monitoring. Synthetic zone differences are generator assumptions. There is no observed before/after operational improvement.', next_step='With approved real data: validate timestamps, profile late delivery tails, add vehicle and time-window constraints, and test scheduling decisions prospectively.', artifact='Local Flask API + SQL metrics + route heuristic', deliverable='Run the analytics API locally; the public site is a static case study.'),
    'retention': dict(number='02', category='COHORTS & EXPERIMENTS', short='Ask better questions of retention.', question='How do D1 and D7 retention differ across cohorts, and does variant B have evidence of a D7 effect?', summary='Exact-day cohort analysis and a prespecified D7 comparison, built around eligible denominators, a sample-ratio check and an honest view of statistical uncertainty.', stack=['SQL', 'Python', 'Statistics'], methods=[('Define eligibility first', 'Use an observation end of September 30, 2025. Require signup + 7 days to fall within that window. The 353 newer synthetic players are excluded from both reported D1 and D7 denominators.'), ('Build player-level flags', 'Left join activity to the eligible player population, deduplicate at player-day grain, and create exact-day D1 and D7 indicators. Aggregate the flags by signup cohort and randomized variant.'), ('Evaluate the primary comparison', 'Use a two-sided pooled two-proportion z test for D7 at alpha 0.05. Report B minus A with an unpooled Wald 95% confidence interval. Check 50:50 sample-ratio mismatch; D1 is descriptive.')], metrics=[('D1 retention', 'Players active exactly day 1 / D7-mature players', 'Same eligible denominator as D7 for comparability.'), ('D7 retention', 'Players active exactly day 7 / D7-mature players', 'Primary endpoint; exact-day, not rolling retention.'), ('Absolute difference', 'D7 rate B - D7 rate A', 'Percentage points, not relative percent.'), ('95% interval', 'Difference ± 1.96 × unpooled standard error', 'Approximate interval; assumptions in data dictionary.')], limits='The assignment and activity are simulated. Independent Bernoulli activity by day is a simplification, so this is not a realistic churn model or evidence of real player behavior. No long-term churn prediction or multiple-endpoint causal claim is made.', next_step='With real event logs: audit assignment and exposure, freeze the observation window, assess experiment power, inspect guardrails and estimate long-term retention only after cohorts mature.', artifact='Cohort SQL + A/B readout + maturity checks', deliverable='Reproduce the exact-day cohort table and experiment calculation with Python.'),
    'campaign': dict(number='03', category='CUSTOMERS & CAMPAIGNS', short='Make customer behaviour legible.', question='How can simple lifecycle segments make campaign response easier to inspect without confusing association with lift?', summary='A transparent customer segmentation workflow, an inspectable SQL response analysis, and a Power BI model guide for carrying the same definitions into a dashboard.', stack=['SQL', 'Python', 'Power BI'], methods=[('Freeze a pre-campaign snapshot', 'Use recency, 180-day purchase count and historical spend from before the fictional September campaign. Assign each of 800 synthetic customers exactly one recipient record.'), ('Apply interpretable segment rules', 'Loyal: recency ≤ 60 days and purchases ≥ 8; At risk: recency > 90 days; Developing: everyone else. Profile spend by segment; no hidden clustering or asserted optimal thresholds.'), ('Prepare a dashboard model', 'Join one customer to one campaign record, aggregate response counts, and recalculate the response ratio. Supply CSV inputs, explicit DAX measures and a Power BI build guide; no original .pbix file is included.')], metrics=[('Response rate', 'Responses within 14 days / assigned recipients', 'A response is not assumed to be a purchase.'), ('Segment share', 'Customers in segment / all 800 customers', 'Mutually exclusive snapshot segments.'), ('Historical spend', 'Sum of pre-campaign spend_cad', 'CAD over prior 180 days; not campaign revenue.'), ('Spend per customer', 'Historical spend / customers in segment', 'Descriptive value profile, not lifetime value.')], limits='Synthetic response probabilities depend on the segment by construction. This is observational segmentation, with no control group, incremental lift, ROI or customer lifetime value estimate. The resume reports 2,000+ customer records; this separate demo uses 800.', next_step='With consented customer data: confirm source provenance, validate stable segment definitions, run a randomized campaign holdout and measure incremental conversion with complete follow-up.', artifact='Segmentation SQL + dashboard model + DAX', deliverable='Import the synthetic CSVs into Power BI using the included model guide.')
}


def bar_chart(rows, label, numerator, denominator, title):
    chart_rows = []
    for row in rows:
        rate = row[numerator] / row[denominator]
        chart_rows.append(f'<div class="bar-row"><span>{escape(row[label])}</span><div class="bar-track"><div class="bar-fill" style="width:{rate * 100:.4f}%"></div></div><strong>{percent(rate)}</strong><small>{row[numerator]:,} / {row[denominator]:,}</small></div>')
    return f'<div class="bar-chart" role="img" aria-label="{escape(title)}. Exact values and denominators follow."><div class="chart-scale"><span>0%</span><span>50%</span><span>100%</span></div>{"".join(chart_rows)}</div>'


def data_table(headers, rows, caption):
    return '<div class="table-wrap"><table><caption>' + escape(caption) + '</caption><thead><tr>' + ''.join(f'<th scope="col">{escape(header)}</th>' for header in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{escape(value)}</td>' for value in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def page(title, body, depth=0, description='Data analytics portfolio of Lei Liu, SFU Statistics graduate and former VFX Compositor.'):
    prefix = '../' * depth
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{escape(description)}"><meta name="theme-color" content="#172b34"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><title>{escape(title)}</title><link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}assets/style.css"><script src="{prefix}assets/site.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="wordmark" href="{prefix}index.html" aria-label="Lei Liu home">LL<span> / </span>LEI LIU</a><nav aria-label="Main navigation"><a href="{prefix}index.html#work">Work</a><a href="{prefix}index.html#about">About</a><a href="{prefix}index.html#skills">Skills</a><a href="{prefix}index.html#contact">Contact <span aria-hidden="true">↗</span></a></nav></header>
<main id="main">{body}</main><footer><a class="wordmark" href="{prefix}index.html">LEI LIU<span> / </span>ANALYTICS</a><p>Vancouver, BC · Statistics × visual craft</p><a href="{REPO}/blob/main/provenance/README.md">Evidence & reconstruction notes ↗</a></footer></body></html>'''


def home():
    cards = []
    for source in CLAIMS['projects']:
        project_id = source['id']
        project = PROJECTS[project_id]
        if project_id == 'delivery':
            mini = bar_chart(RESULTS['delivery'], 'zone', 'on_time', 'delivered', 'Synthetic delivery on-time rate by zone')
        elif project_id == 'retention':
            groups = [dict(variant=variant, **values) for variant, values in RESULTS['experiment']['groups'].items()]
            mini = bar_chart(groups, 'variant', 'retained_d7', 'players', 'Synthetic exact-day D7 retention by variant')
        else:
            mini = bar_chart(RESULTS['campaign'], 'segment', 'responses', 'customers', 'Synthetic response rate by segment')
        cards.append(f'''<article class="project-card"><div class="project-card-copy"><p class="eyebrow">{project['number']} / {project['category']}</p><h3><a href="projects/{project_id}.html">{escape(source['title'])}<span aria-hidden="true"> ↗</span></a></h3><p>{escape(project['summary'])}</p><ul class="tags">{"".join(f'<li>{escape(tag)}</li>' for tag in project['stack'])}</ul><a class="text-link" href="projects/{project_id}.html">Explore case study <span aria-hidden="true">→</span></a></div><div class="project-preview"><p class="chart-kicker">SYNTHETIC DATA / REPRODUCIBLE PREVIEW</p>{mini}</div></article>''')
    body = f'''<section class="hero"><div class="hero-copy"><p class="eyebrow light">LEI LIU / DATA ANALYTICS PORTFOLIO</p><h1>Clear thinking.<br>Careful analysis.<br><em>A visual edge.</em></h1><p class="hero-intro">I bring a statistics foundation and a compositor’s eye for detail to data, systems and the stories they tell.</p><div class="hero-actions"><a class="button primary" href="#work">Explore selected work <span aria-hidden="true">↓</span></a><a class="button outline" href="https://github.com/lla86">GitHub ↗</a></div><p class="hero-meta">VANCOUVER, BC <span> / </span> SFU BSc STATISTICS · DEC 2025</p></div><div class="hero-art" aria-hidden="true"><div class="art-top"><span>FROM SIGNAL TO UNDERSTANDING</span><span>LL / 01</span></div><svg viewBox="0 0 420 380"><defs><pattern id="grid" width="42" height="38" patternUnits="userSpaceOnUse"><path d="M 42 0 L 0 0 0 38" fill="none" stroke="#47606a" stroke-width="0.7"/></pattern></defs><rect width="420" height="380" fill="url(#grid)"/><path d="M0 310 Q60 305 90 250 T170 220 T250 150 T330 115 T420 30" fill="none" stroke="#e6a881" stroke-width="3"/><path d="M0 310 Q60 305 90 250 T170 220 T250 150 T330 115 T420 30 L420 90 Q360 170 330 160 T250 210 T170 280 T90 300 T0 350 Z" fill="#e6a881" opacity=".09"/><circle cx="250" cy="150" r="7" fill="#e6a881"/><circle cx="250" cy="150" r="18" fill="none" stroke="#e6a881" opacity=".4"/><path d="M250 0V380M0 150H420" stroke="#94a7ab" stroke-dasharray="3 7" opacity=".45"/></svg><div class="art-bottom"><span>STATISTICAL REASONING</span><span>VISUAL PRECISION</span></div><div class="art-note">Concept illustration · not measured data</div></div></section>
<section class="intro-strip"><p><strong>Statistics</strong><span>Simon Fraser University</span></p><p><strong>Visual craft</strong><span>VFX Compositor · 2019–2023</span></p><p><strong>Practical tools</strong><span>Python · SQL · Power BI</span></p></section>
<section class="work section" id="work"><div class="section-head"><div><p class="eyebrow">01 / SELECTED WORK</p><h2>Questions worth<br>getting right.</h2></div><p>Three case studies connecting operational systems, player behaviour and customer insight.</p></div><aside class="disclosure"><strong>About this portfolio</strong><p>These case studies expand projects listed on my resume. All new code and displayed results are <b>portfolio reconstruction / demo / synthetic data</b>. Resume statements and demo findings are identified separately. <a href="{REPO}/blob/main/provenance/README.md">Read the evidence notes ↗</a></p></aside>{''.join(cards)}</section>
<section class="about section" id="about"><div><p class="eyebrow">02 / A DIFFERENT PERSPECTIVE</p><h2>Precision, from<br>pixels to patterns.</h2></div><div class="about-copy"><p class="large-copy">My background combines visual effects production with a BSc in Statistics from Simon Fraser University.</p><p>As a VFX Compositor from 2019 to 2023, I worked with supervisors, artists and production teams to complete shots on schedule. That work built habits of quality control, careful observation and clear communication.</p><p>I completed my statistics degree in December 2025. This portfolio brings that foundation into practical Python, SQL and reporting workflows.</p><div class="timeline"><div><span>2019–2023</span><strong>Visual Effects Artist / Compositor</strong><small>Vancouver, BC</small></div><div><span>2023–2025</span><strong>BSc, Statistics</strong><small>Simon Fraser University · completed December 2025</small></div></div></div></section>
<section class="skills section" id="skills"><div class="section-head"><div><p class="eyebrow">03 / TOOLKIT</p><h2>Analytical rigour.<br>Useful outputs.</h2></div><p>Skills listed on my resume, with selected methods illustrated in the demos above.</p></div><div class="skill-grid"><div><span>01</span><h3>Analysis & statistics</h3><p>Exploratory analysis · hypothesis testing · regression analysis · cohort analysis · retention analysis</p></div><div><span>02</span><h3>Code & data</h3><p>Python · SQL · R · Pandas · NumPy · scikit-learn · MySQL · SQLite · Git</p></div><div><span>03</span><h3>Reporting & communication</h3><p>Power BI · Tableau · Excel · dashboard development · KPI reporting · data visualisation</p></div></div></section>
<section class="contact section" id="contact"><p class="eyebrow light">04 / GET IN TOUCH</p><h2>Let’s make the<br>next question clearer.</h2><p>For opportunities in data analysis, research and technical collaboration.</p><div class="hero-actions"><a class="button primary" href="mailto:leisfu2020@gmail.com">Email Lei ↗</a><a class="button outline" href="https://github.com/lla86">Explore GitHub ↗</a></div><p class="contact-address">leisfu2020@gmail.com</p></section>'''
    (SITE / 'index.html').write_text(page('Lei Liu | Data Analytics Portfolio', body))


def findings(project_id):
    if project_id == 'delivery':
        delivered = sum(row['delivered'] for row in RESULTS['delivery'])
        on_time = sum(row['on_time'] for row in RESULTS['delivery'])
        route = RESULTS['route']
        text = f'Across 900 synthetic orders, {on_time} of {delivered} delivered orders met the 50-minute promise ({percent(on_time / delivered)}). The fixed 12-stop geometry measures {route["baseline_km"]:.1f} km in input order and {route["heuristic_km"]:.1f} km with nearest-neighbour ordering. This is an illustrative route comparison, not a business saving.'
        chart = bar_chart(RESULTS['delivery'], 'zone', 'on_time', 'delivered', 'September synthetic on-time rate by zone')
        table = data_table(['Zone', 'All orders', 'Delivered', 'Cancelled', 'On time', 'On-time rate', 'Mean minutes'], [[row['zone'], row['orders'], row['delivered'], row['cancelled'], row['on_time'], percent(row['on_time_rate']), row['mean_minutes']] for row in RESULTS['delivery']], 'Synthetic operational metrics · September 1–30, 2025')
        return text, chart, table
    if project_id == 'retention':
        experiment = RESULTS['experiment']
        groups = [dict(variant=variant, **values) for variant, values in experiment['groups'].items()]
        text = f'Of 2,400 synthetic players, 2,047 have complete D7 follow-up. D7 is {percent(experiment["d7_control"])} in A and {percent(experiment["d7_treatment"])} in B. The estimated difference is {experiment["difference"] * 100:+.2f} percentage points (95% CI {experiment["ci_low"] * 100:+.2f} to {experiment["ci_high"] * 100:+.2f}; p={experiment["p_value"]:.3f}). The interval includes zero: there is insufficient evidence of a D7 effect in this simulation. SRM p={experiment["srm_p_value"]:.3f}; this check alone does not validate an experiment.'
        chart = bar_chart(groups, 'variant', 'retained_d7', 'players', 'Synthetic exact-day D7 retention by variant')
        table = data_table(['Variant', 'Eligible players', 'D1 retained', 'D1 rate', 'D7 retained', 'D7 rate'], [[row['variant'], row['players'], row['retained_d1'], percent(row['retained_d1'] / row['players']), row['retained_d7'], percent(row['retained_d7'] / row['players'])] for row in groups], 'Synthetic experiment · same D7-mature denominator for both days')
        cohort_rows = []
        for cohort in sorted(set(row['cohort'] for row in RESULTS['retention'])):
            rows = [row for row in RESULTS['retention'] if row['cohort'] == cohort]
            cohort_rows.append([cohort, sum(row['players'] for row in rows), percent(sum(row['retained_d1'] for row in rows) / sum(row['players'] for row in rows)), percent(sum(row['retained_d7'] for row in rows) / sum(row['players'] for row in rows))])
        table += '<details><summary>Inspect all 23 mature signup cohorts</summary>' + data_table(['Signup date', 'Eligible players', 'D1 rate', 'D7 rate'], cohort_rows, 'Synthetic cohort rates · variants pooled using player counts') + '</details>'
        return text, chart, table
    text = 'The 800 synthetic customers are assigned to three mutually exclusive lifecycle segments. Response differences illustrate an inspectable reporting workflow; segment response probabilities were deliberately encoded in the generator. Historical spending is a customer profile measure and cannot be interpreted as attributed campaign revenue.'
    chart = bar_chart(RESULTS['campaign'], 'segment', 'responses', 'customers', 'Synthetic response rate by pre-campaign segment')
    table = data_table(['Segment', 'Recipients', 'Responses', 'Response rate', 'Historical spend (CAD)'], [[row['segment'], row['customers'], row['responses'], percent(row['response_rate']), f'{row["historical_spend_cad"]:,.2f}'] for row in RESULTS['campaign']], 'Synthetic 14-day campaign response · 800 fully observed recipients')
    return text, chart, table


def case_study(source):
    project_id = source['id']
    project = PROJECTS[project_id]
    text, chart, table = findings(project_id)
    methods = ''.join(f'<article><span class="step-number">0{index + 1}</span><div><h3>{escape(title)}</h3><p>{escape(copy)}</p></div></article>' for index, (title, copy) in enumerate(project['methods']))
    metrics = data_table(['Metric', 'Definition', 'Scope'], project['metrics'], 'Metric contract for this reconstruction')
    source_link = f'{REPO}/tree/main/projects/{project_id}'
    extra = f'<a class="text-link" href="{REPO}/blob/main/projects/campaign/POWER_BI.md">Power BI build guide ↗</a>' if project_id == 'campaign' else ''
    body = f'''<section class="case-hero section"><a class="back-link" href="../index.html#work">← All projects</a><p class="eyebrow">CASE STUDY {project['number']} / {project['category']}</p><h1>{escape(source['title'])}</h1><p class="case-tagline">{escape(project['short'])}</p><ul class="tags">{''.join(f'<li>{escape(tag)}</li>' for tag in project['stack'])}</ul><aside class="disclosure"><strong>Portfolio reconstruction / demo / synthetic data</strong><p>New implementation inspired by a resume-listed project. Every displayed metric below comes from generated data. No historical impact or original analysis is claimed.</p></aside></section>
<div class="case-layout section"><aside class="case-nav"><p class="eyebrow">IN THIS CASE STUDY</p><a href="#question">The question</a><a href="#scope">Resume scope</a><a href="#method">Method</a><a href="#results">Demo results</a><a href="#metrics">Data & definitions</a><a href="#limits">Limits & next steps</a><a href="#reproduce">Reproduce</a></aside><div class="case-content">
<section id="question"><p class="eyebrow">THE QUESTION</p><h2>{escape(project['question'])}</h2><p class="large-copy">{escape(project['summary'])}</p></section>
<section id="scope"><p class="eyebrow">SOURCE / RESUME-DECLARED SCOPE</p><h2>What the resume states.</h2><p>The following bullets are transcribed from the original resume. They are self-reported statements, separate from the reconstruction below.</p><ul class="resume-claims">{''.join(f'<li>{escape(claim)}</li>' for claim in source['claims'])}</ul><p class="small-copy">No numeric business improvement is stated in the resume. <a href="{REPO}/blob/main/provenance/resume_claims.json">Inspect source transcription ↗</a></p></section>
<section id="method"><p class="eyebrow">RECONSTRUCTION / APPROACH</p><h2>A traceable workflow.</h2><div class="method-steps">{methods}</div></section>
<section id="results"><p class="eyebrow">OUTPUT / SYNTHETIC DATA ONLY</p><h2>What the demo shows.</h2><p>{escape(text)}</p><div class="evidence-panel"><div class="evidence-heading"><h3>{'On-time delivery by zone' if project_id == 'delivery' else 'Exact-day D7 retention' if project_id == 'retention' else 'Response rate by lifecycle segment'}</h3><span>DEMO / SEPTEMBER 2025</span></div>{chart}<p class="small-copy">Bars use a shared 0–100% scale. Counts and exact denominator definitions are available below.</p>{table}</div><p><strong>Practical output:</strong> {escape(project['artifact'])}. {escape(project['deliverable'])}</p></section>
<section id="metrics"><p class="eyebrow">DATA / MEASUREMENT CONTRACT</p><h2>Definitions before conclusions.</h2>{metrics}<p><a href="{REPO}/blob/main/data/README.md">Full data dictionary ↗</a> · <a href="{REPO}/tree/main/data/synthetic">Synthetic CSV inputs ↗</a> · <a href="../assets/results.json">Computed results JSON ↗</a></p><p class="small-copy">Fixed seed 20261112. Synthetic dataset snapshot: September 2025. Data-generation assumptions are inspectable in the source.</p></section>
<section id="limits"><p class="eyebrow">INTERPRETATION</p><h2>Where the evidence ends.</h2><p>{escape(project['limits'])}</p><div class="next-step"><h3>A meaningful next step</h3><p>{escape(project['next_step'])}</p></div></section>
<section id="reproduce"><p class="eyebrow">CODE / REPRODUCIBILITY</p><h2>Open the workflow.</h2><p>The analysis uses Python’s standard library and SQLite. Flask is optional for the local delivery API. The public website is static and requires no backend or visitor tracking.</p><pre><code>python3 scripts/generate_demo.py\npython3 scripts/build_site.py\npython3 -m unittest discover -s tests\npython3 -m http.server 8000 --directory docs</code></pre><a class="button dark-button" href="{source_link}">View project source ↗</a> {extra}</section>
</div></div><section class="case-end section"><p class="eyebrow">KEEP EXPLORING</p><h2>Another angle on the data.</h2><div class="next-projects">{''.join(f'<a href="{other_id}.html">{escape(other["short"])} ↗</a>' for other_id, other in PROJECTS.items() if other_id != project_id)}</div></section>'''
    (SITE / 'projects' / f'{project_id}.html').write_text(page(f'{source["title"]} | Lei Liu', body, depth=1, description=project['summary']))
    markdown = f'# {source["title"]}\n\n**Portfolio reconstruction / demo / synthetic data.** All code in this directory is newly authored. Displayed results are not original project achievements.\n\n## Resume-declared scope\n\n' + '\n'.join('- ' + claim for claim in source['claims']) + f'\n\nThese self-reported bullets were transcribed from the source resume; see [provenance](../../provenance/README.md).\n\n## Question\n\n{project["question"]}\n\n## Technology\n\n' + ' · '.join(project['stack']) + '\n\n## Reconstruction method\n\n' + '\n\n'.join(f'### {title}\n\n{copy}' for title, copy in project['methods']) + '\n\n## Demonstration findings\n\n' + text + '\n\n## Metric definitions\n\n| Metric | Definition | Scope |\n| --- | --- | --- |\n' + '\n'.join('| ' + ' | '.join(row) + ' |' for row in project['metrics']) + f'\n\n## Limitations\n\n{project["limits"]}\n\n## Next step\n\n{project["next_step"]}\n\n## Run and inspect\n\nFrom the repository root:\n\n```sh\npython3 scripts/generate_demo.py\npython3 scripts/build_site.py\npython3 -m unittest discover -s tests\n```\n\nSee [CSV dictionary](../../data/README.md), [SQL](metrics.sql), [computed outputs](../../docs/assets/results.json), and [website source](../../docs/projects/{project_id}.html).\n'
    if project_id == 'delivery':
        markdown += '\nOptional local API:\n\n```sh\npython3 -m pip install -r requirements.txt\npython3 projects/delivery/app.py\n```\n\nOpen `http://127.0.0.1:5000/api/delivery` or `/api/delivery/north`. It is not hosted by GitHub Pages.\n'
    if project_id == 'campaign':
        markdown += '\nSee the [Power BI build guide](POWER_BI.md) and [DAX measures](measures.dax). No `.pbix` file is included or claimed. Existing public work: [customer-campaign-analysis](https://github.com/lla86/customer-campaign-analysis), inspected read-only; its calculations were not audited or reused.\n'
    (ROOT / 'projects' / project_id / 'README.md').write_text(markdown)


def main():
    (SITE / 'projects').mkdir(parents=True, exist_ok=True)
    home()
    for source in CLAIMS['projects']:
        case_study(source)
    (SITE / '.nojekyll').touch()
    (SITE / '404.html').write_text(page('Page not found | Lei Liu', '<section class="section case-hero"><p class="eyebrow">404</p><h1>Let’s find the right page.</h1><a class="button dark-button" href="/lei-analytics-portfolio/">Back to the portfolio →</a></section>'))
    print('Built home, three case studies, project READMEs and 404 page.')


if __name__ == '__main__':
    main()
