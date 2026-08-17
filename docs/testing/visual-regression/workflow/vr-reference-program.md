---
description: A tiered VR program plan for a mid-size Drupal site — ~95 baselines, ~5 minutes locally, manageable maintenance.
tldr: "Build a 4-tier program: Tier 1 smoke set (~15 baselines, 3–6 critical pages, 3 viewports); Tier 2 component set (~50 baselines, SDC atoms against fixture routes); Tier 3 theme variants (~20 baselines, conditional); Tier 4 cross-browser (~10 baselines, nightly). Ramp up over weeks, not days — stability must be proven before scale."
---

# Reference Program

## When to Use

> Use this guide when planning a VR program from scratch for a mid-size Drupal site.

## Decision

Ramp-up order:

| Week | Action |
|------|--------|
| 1 | Tier 1 smoke set + stability checklist + global stylesheet. Confirm suite runs green twice in a row |
| 2–4 | Tier 2 component set, one component family at a time. After each, confirm stable; commit baselines |
| Month 2+ | Tier 3 + Tier 4 only when there's a measurable need |

Don't build the whole suite at once — most failed VR programs over-invest before stability is proven.

## Pattern

**Tier 1 — Smoke set (~15 baselines)**
- 3–6 critical pages: home, primary landing, login, primary content type render
- Chromium-only, 3 viewports (mobile / tablet / desktop)
- ~5 minutes locally to update

**Tier 2 — Component set (~50 baselines)**
- Every shared SDC / paragraph / block plugin
- Chromium-only, 1 viewport (desktop) by default; 3 viewports for responsive components
- Captured against `/vrt-fixtures/<component>` routes, not real content pages

**Tier 3 — Theme variant set (~20 baselines)**
- Only when light/dark or UI Skins variants are in scope
- 1 viewport, 1 browser
- Conditional: `test.skip(!process.env.RUN_THEME_VR, ...)`

**Tier 4 — Cross-browser set (~10 baselines)**
- 5 critical pages × {Firefox, WebKit}
- Desktop viewport only
- Slower cadence (nightly, not per-PR)

**Total: ~95 baselines, ~5 minutes locally, manageable maintenance.**

## See Also

- [Matrix Design](vr-matrix-design.md)
- [When to Add a VR Test](vr-when-to-add.md)
- [VR Debt & Hygiene](vr-debt-and-hygiene.md)
- Reference: `drupal-playwright-vr.md`, `pixelmatch.md`, `playwright-html-report.md`
