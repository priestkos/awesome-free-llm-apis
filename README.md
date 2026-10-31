# Awesome Free LLM APIs

A directory of every free LLM API in
[`mnfst/awesome-free-llm-apis`](https://github.com/mnfst/awesome-free-llm-apis):
collapsible provider cards, one-click copy of each base URL, filter and search.

**Live:** https://priestkos.github.io/awesome-free-llm-apis/

All provider text is copied verbatim from the source README (CC0-1.0) — only the
presentation and page chrome are added here.

## Updates

`.github/workflows/refresh.yml` runs every Monday 09:00 UTC (or manually via
*Run workflow*): it fetches the source README, rebuilds `index.html` and commits
it only when it changed. GitHub Pages serves `main`, so that push redeploys the
site.

## Build

```bash
python build.py   # fetches the source README, writes index.html
```

Files: `build.py` (README → static HTML), `template.html` (page shell),
`index.html` (generated, committed).

## Credits

Content: [mnfst/awesome-free-llm-apis](https://github.com/mnfst/awesome-free-llm-apis) (CC0-1.0).
