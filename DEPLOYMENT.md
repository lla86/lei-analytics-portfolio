# GitHub Pages deployment

The intended independent repository is `lla86/lei-analytics-portfolio`. Existing repositories should not be overwritten. Deployment status and verified links are recorded separately in `output/deployment-status.json` in the local handoff package, not assumed by these instructions.

## Browser

1. Create a new **public** repository named `lei-analytics-portfolio` under `lla86`. Public is intended for this recruiting portfolio. Do not upload the original PDF, phone number or private DeliveryTool source.
2. Upload the **contents** of this repository, preserving folders; do not add an extra enclosing directory. Include `docs/.nojekyll`. A Git client is preferable to browser drag-and-drop if hidden files are omitted.
3. Open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**. Choose **main** and **/docs**, then **Save**.
4. Wait for the **pages build and deployment** workflow to finish. Open the URL reported by Pages and check home plus all three project pages.

Expected URL **only after successful activation**: `https://lla86.github.io/lei-analytics-portfolio/`. This expected address is not proof of a live deployment.

Official instructions: [Configure a GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Optional GitHub CLI path

Only use this in this new portfolio directory, after checking the target does not exist. `gh` needs to be installed and authenticated with permission to create repositories and manage Pages; the connected chat GitHub app does not automatically authenticate a local CLI.

```sh
git init -b main
git add .
git commit -m "Create analytics portfolio with reproducible synthetic demos"
gh repo create lla86/lei-analytics-portfolio --public --source=. --remote=origin --push
gh api --method POST repos/lla86/lei-analytics-portfolio/pages -f 'source[branch]=main' -f 'source[path]=/docs'
gh api repos/lla86/lei-analytics-portfolio/pages
```

If the repository already exists, inspect its contents and permissions first. Do not force-push. To update an established portfolio, regenerate data and pages, run validation, then make an ordinary commit and push to main. The configured branch source republishes changes to `docs/`.

GitHub Pages serves static content. It cannot run the Flask API or an interactive Power BI workbook. Their local run and rebuild instructions are in the project directories.
