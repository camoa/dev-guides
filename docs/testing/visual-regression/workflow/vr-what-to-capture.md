---
description: Deciding scope, state, breakpoint, browser, and theme combinations for a visual regression test.
tldr: Use the 5-axis cube (scope × state × breakpoint × browser × theme) and pick the smallest cross-section per test. Default to component-level scope, Chromium-only, 3 breakpoints for responsive components, and only capture states with distinct CSS.
---

# What to Capture

## When to Use

> Use this guide when deciding scope, state, breakpoint, browser, and theme combinations for a given VR test. Multiplying all axes is how teams end up with 2,000 baselines and a burning suite.

## Decision

### Scope

| Approach | When | Notes |
|----------|------|-------|
| Component-level (`locator.screenshot()` or `clip`) | Default for shared atoms/molecules | Smaller PNG, less surface for false positives |
| Above-the-fold full-page (`fullPage: false`) | Hero / landing-page header treatments | Captures one viewport-height of the page |
| Full-page (`fullPage: true`) | Templates whose entire vertical rhythm matters | 5–15 MB PNGs; *will* find diffs you don't care about |

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

- **Wrong**: `fullPage: true` everywhere → **Right**: produces huge PNGs, captures editorial content, fails on every navigation tweak
- **Wrong**: one viewport baseline for responsive components → **Right**: "it looked fine in the screenshot. The desktop one. Mobile shipped broken"
- **Wrong**: capturing all 7 button states → **Right**: only 3 of them have distinct CSS

## See Also

- [Matrix Design](vr-matrix-design.md)
- [Stability Checklist](vr-stability-checklist.md)
- [Authoring Patterns](vr-authoring-patterns.md)
