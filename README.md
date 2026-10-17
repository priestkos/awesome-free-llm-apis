# awesome-free-llm-apis website

A bold Riso-Zine (dark mode) directory of **every provider API and inference
provider** listed in [`mnfst/awesome-free-llm-apis`](https://github.com/mnfst/awesome-free-llm-apis) —
each provider gets a collapsible section with a one-click copy box for its base
URL. All provider text is copied **verbatim** from the source README (CC0-1.0);
only the presentation and page chrome are added.

## How it updates

- `.github/workflows/refresh.yml` runs **every Monday 09:00 UTC** (and
  manually via *Run workflow*), fetches the latest `README.md` from the source
  repo over the network, runs `build.py --remote`, and commits `index.html`
  only when it actually changed.
- GitHub Pages deploys from `main`, so the push above auto-redeploys the site.
- The local `source-README.md` used for the very first build is a one-off
  read-only copy and is not part of the scheduled pipeline (and is deleted by
  the workflow, never read by it).

## Local build (one-off, not the update path)

```bash
python build.py          # reads ./source-README.md
python build.py --remote # fetches the latest README over the network
```

Files: `template.html` (shell), `build.py` (README → static HTML),
`index.html` (generated, committed), `DESIGN.md` (design record).
