---
description: "Deciding scope, state, breakpoint, browser, and theme combinations for a visual regression test."
tldr: "Use the 5-axis cube (scope × state × breakpoint × browser × theme); pick the smallest cross-section per test. Full-page baselines cost ~150 KB each — the real trade-off is coverage, not bytes: viewport-only can miss most of the page."
---

# What to Capture

## When to Use

> Use this guide when deciding scope, state, breakpoint, browser, and theme combinations for a given VR test. Multiplying all axes is how teams end up with 2,000 baselines and a burning suite.

## Decision

### Scope

| Approach | When | Notes |
|----------|------|-------|
| Component-level (`locator.screenshot()` or `clip`) | Default for shared atoms/molecules | Smaller PNG, less surface for false positives |
| Above-the-fold full-page (`fullPage: false` — Playwright default) | Hero / landing-page header treatments | Captures one viewport-height of the page |
| Full-page (`fullPage: true`) | Templates whose entire vertical rhythm matters (home, key landing) | ~150 KB per masked baseline; *will* find diffs you don't care about |

**Full-page cost, measured, not assumed.** Full-page capture is routinely described as expensive; measured on a real Drupal site it isn't — fifteen masked full-page baselines across five surfaces and three viewports totalled 2.3 MB, about 150 KB each. PNG size tracks *photographic* content, not page height: flat type and background compress to almost nothing, so a photo-heavy landing page costs more, but megabytes per shot is not the default case.

The real trade is coverage, not bytes. A viewport-only shot of one article on the same site covered **14% of the page**: the byline fell inside the baseline; an evidence callout, the closing question, and the footer fell outside it entirely. A refactor could rewrite all three and the gate would stay green. Decide which failure you'd rather have — a full-page baseline that goes red when editorial content moves, or a viewport baseline that stays green when the template below the fold breaks.

### Browser

| Situation | Choose |
|-----------|--------|
| Default | Chromium-only |
| CSS known to differ across engines (`backdrop-filter`, `mask-image`, complex `filter`) | Add Firefox or WebKit for that component |
| Audience is measurably Safari-skewed (verify with analytics) | Add WebKit |

### State

Capture each state with **distinct CSS** only: `default`, `hover`, `focus-visible`, `active`, `disabled`, `error`, `loading`, `empty`. Don't capture states that look identical.

## Pattern

The 5-axis cube: `scope × state × breakpoint × browser × theme`

Recommended breakpoint starter set:
- **375 × 812** — mobile (iPhone-class)
- **768 × 1024** — tablet
- **1440 × 900** — desktop

For themes/dark-mode: capture each variant **only** for components whose tokens actually change.

## Common Mistakes

- **Wrong**: retreating to viewport-only capture because full-page PNGs seem expensive → **Right**: masked full-page baselines run ~150 KB each; the actual problem with unmasked `fullPage: true` is capturing editorial content, so fix it with masking and surface selection, not by dropping coverage
- **Wrong**: one viewport baseline for responsive components → **Right**: "it looked fine in the screenshot. The desktop one. Mobile shipped broken"
- **Wrong**: capturing all 7 button states → **Right**: only 3 of them have distinct CSS

## See Also

- [Matrix Design](vr-matrix-design.md)
- [Stability Checklist](vr-stability-checklist.md)
- [Authoring Patterns](vr-authoring-patterns.md)
