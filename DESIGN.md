# DESIGN.md — Awesome Free LLM APIs · Riso-Zine Directory (dark)

## Brief
- Product/page type: single-file static directory site (index.html), GitHub Pages, rebuilt weekly by GitHub Actions from the source repo's README.
- Target user: developers scanning free-tier LLM APIs; primary job = grab a base URL fast via copy box; full context available in collapsible sections.
- Scope and constraints: every word of provider content copied verbatim from `mnfst/awesome-free-llm-apis` (repo is CC0-1.0); no content authored. Bold Riso-Zine style modelled on `chat-log-styles/07-riso-zine`, dark mode.
- Assumptions: folder `D:\Hermes Projects\awesome-llm-website`; repo name decided at push time (user confirms before push); Chrome text (UI labels) is the only non-source copy.

## Two-pass plan
**Pass 1 tokens (dark riso):**
- Palette: desk `#0f0c0a` (fixed body market behind the sheet), paper `#191412` (sheet), paper-raised `#1f1915` (cards), ink `#e8e1d4` (warm off-white, tinted — never pure white), muted `#998c7e`, riso-pink `#ff4d6d`, riso-blue `#4f6dff`. Fluid pink-and-blue as the two ink passes, everything else discipline.
- Type: Bricolage Grotesque 700–800 (display, uppercase, tight), Atkinson Hyperlegible (body), Courier New stack (URL boxes, tables). No Inter/Roboto/Arial.
- Layout concept: a xeroxed sheet floating on a darker desk — inset darkened edges like the reference — cover (imprint row / giant misregistered title / spec strip) → sticky toolbar (filters, search, open–collapse all) → directory of numbered riso cards → glossary → contributing → footnotes as "small print" colophon. Flush-left; halftone grain overlay over everything.
- Alignment: flush-left throughout; monospace numerals for the seq badges.

**Pass 2 revisions against the brief:**
- A plain directory of cards reads generic → fixed: two ink passes by group (Provider APIs stamped blue, Inference providers stamped pink/cyan-split), numbered stamp badges `01–16` with hard offset shadows, crop-registration marks in the cover, halftone screen, and the one load moment: the title's pink shadow misregistes from `14px` to its resting `5px` offset, once, ~600ms.
- Accessory removed: no per-card colour inversion on hover — the pull-in of the hard shadow is the only hover statement.

## Direction
- Experience strategy: efficiency-first with a brand-first skin (zine).
- Layout pattern: cover + sticky toolbar + sectioned single-column directory.
- Density: controlled dense; typography does the work.
- Motion level: subtle (one orchestrated load moment; shadow pull-in hovers; press states).

## Visual system
- All color/spacing through CSS variables; zero radius; hard offset shadows (`box-shadow: 4px 4px 0`) instead of soft ones — this is the zine's signature.
- Tables: monospace, dotted row rules, uppercase tracked headers, horizontally scrollable wrapper on mobile.
- Collapsible sections use native `<details>`; summary rows show: seq badge, provider name (verbatim), flag, base-URL preview chip, `+` marker.

## Components and states
- Provider card: collapsed by default; open state adds a filled header rule. Copy box: bordered mono box + `copy` button; success flash label on the button (`copied`); fallback `execCommand` path for non-HTTPS contexts.
- Empty search / no-match: `0 of 16 shown` counter state in the toolbar; groups hide when all members hidden.
- Toolbar states: active filter is filled (ink-on-paper inverse); buttons have hover, focus, press states.

## Interaction rules
- Filter (all / Provider APIs / Inference providers), text search across provider names, open all / collapse all; `/` focuses search.
- Every provider's key-page link and every footnote citation link preserved as real `<a href>`; relative links resolved against the source repo.
- Motion respects `prefers-reduced-motion`.

## Accessibility and responsiveness
- Flush-left layout, `focus-visible` 2px pink outlines, 4.5:1 body contrast (ink on paper), 40px+ touch targets on summary rows and copy boxes, skip link, semantic `header/nav/main/section/footer`, native `<details>` semantics.
- Mobile-first: toolbar wraps to rows, chips drop out at narrow widths, tables scroll horizontally.
- Known risk: two-accent palette must never both sit under one element (contrast/legibility) — enforced by construction (name/link ink, accent only on stamps/borders).

## Update pipeline
- `template.html` (shell + tokens) + `build.py` (parse README → render full static HTML). Local build may read `source-README.md` (one-off); the scheduled path always fetches remote.
- `.github/workflows/refresh.yml`: Saturdays→Mondays? No — **Mondays 09:00 UTC** (`0 9 * * 1`) with `workflow_dispatch`; fetch raw README from source repo HEAD, rebuild, commit only when `index.html` changed; Pages redeploys from branch main.

## Open decisions / Next review
- Exact repo name + Pages enablement — confirmed with user at push time (blocker: ask before push).
- Local copy to be archived after one-off use per user instruction.
- v2 revisions after browser verification (1440/390): group intro parser bug fixed (raw markdown never rendered as text), desc double-wrap fixed, glossary bold markdown rendered, URL chips ellipsis + tooltip, chevron becomes a pink-stamped rotated toggle when open, +2 tone steps between desk and sheet, grain moved to screen blend, license folded into the spec strip. Interactions verified: filter/search counts, open/close all, copy handler; no console errors at either width.
