# Lei Liu · Data Analytics Portfolio

Statistics, operational analytics and visual communication. Vancouver, BC.

**[Explore the live portfolio →](https://lla86.github.io/lei-analytics-portfolio/)** · [Validation workflow](https://github.com/lla86/lei-analytics-portfolio/actions/workflows/validate.yml)

**BSc Statistics, Simon Fraser University — completed December 2025.** Previously **Visual Effects Artist / Compositor, 2019–2023**.

This repository expands three resume-listed projects into clear case studies and runnable examples. **Every new implementation is a portfolio reconstruction / demo, and every generated dataset and displayed number is synthetic.** Resume claims are explicitly separated from reconstructed findings. No real business improvement, production deployment, original experiment result or original Power BI workbook is implied.

## Selected work

| Project | Focus | Implementation |
| --- | --- | --- |
| [Delivery Operations Analytics Platform](projects/delivery/README.md) | Operational definitions, validation, on-time delivery, planning | Python, Flask, SQLite; synthetic route heuristic and local JSON API |
| [Player Retention & Experimentation Analytics](projects/retention/README.md) | Exact-day D1/D7, mature cohorts, experiment uncertainty | SQL, Python, statistics; two-proportion test, 95% interval, SRM |
| [Customer Behavior & Campaign Analytics](projects/campaign/README.md) | Lifecycle segmentation, response rates, dashboard modeling | SQL, Python; Power BI guide and DAX examples, no `.pbix` supplied |

The customer resume bullet reports **2,000+ records**; the separate reconstruction uses **800 synthetic customers**. The experiment intentionally reports its observed, non-significant simulation result without claiming a successful real intervention.

## Run everything

Python 3.10+; the analysis and static website build require only the standard library. No accounts, secrets, external data or paid services are needed.

```sh
python3 scripts/generate_demo.py
python3 scripts/build_site.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000`. Home and three project pages are complete HTML and remain readable with JavaScript disabled. The optional JavaScript only highlights the current case-study section.

For the optional Flask demo:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 projects/delivery/app.py
```

Open `http://127.0.0.1:5000/api/delivery` or `/api/delivery/north`. This is a local demonstration, not a public service hosted by GitHub Pages.

## Repository map

```text
docs/                    GitHub Pages publish directory
  index.html             Portfolio home, background, skills and contact
  projects/              Three case-study pages
  assets/                CSS, optional JS, computed results
projects/
  delivery/              Case study, SQL and local Flask API
  retention/             Case study and cohort SQL
  campaign/              Case study, SQL, Power BI guide and DAX
scripts/                 Deterministic generator, analysis and site builder
data/synthetic/          Generated CSVs and SHA-256 manifest
provenance/              Exact resume bullets and evidence boundaries
tests/                   Independent metric checks and static-link validation
.github/workflows/       Reproducibility checks
```

Edit case-study narrative and presentation structure in `scripts/build_site.py`, style in `docs/assets/style.css`, and the analytical logic in `scripts/generate_demo.py` plus project SQL files. Rebuild generated HTML and project READMEs after changes. Do not hand-edit the generated files.

## Evidence and existing work

See the [source transcription](provenance/resume_claims.json), [evidence notes](provenance/README.md), [data dictionary](data/README.md) and [computed output](docs/assets/results.json). Existing GitHub repositories were checked read-only and remain untouched. The original private DeliveryTool code is not republished. The existing public [customer campaign repository](https://github.com/lla86/customer-campaign-analysis) contains earlier work; this repository does not assert its calculations or data license have been independently verified.

## Publish on GitHub Pages

Use **Settings → Pages → Deploy from a branch → main → /docs → Save**. See [deployment instructions](DEPLOYMENT.md). The website is buildless at serving time; committed `docs/` files are the deployment output.

## Contact

[GitHub](https://github.com/lla86) · [leisfu2020@gmail.com](mailto:leisfu2020@gmail.com) · Vancouver, BC

No phone number, client records, private delivery source, external tracking scripts or contact form submissions are included. No license has been selected on the owner's behalf.
