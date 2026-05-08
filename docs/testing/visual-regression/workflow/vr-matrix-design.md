---
description: Designing the browser × viewport × project topology of a VR suite using a tiered matrix.
tldr: Use a tiered matrix instead of a uniform N×M cube — component-shared tests use 1 viewport, layout-aware and page tests use 3 viewports, cross-browser tests use 1 viewport with 3 browsers. Name projects so the name flows into the baseline filename.
---

# Matrix Design

## When to Use

> Use this guide when designing the browser × viewport × project topology of a VR suite. A uniform N×M cube collapses under maintenance; a tiered matrix scales.

## Decision

| Question | Answer |
|----------|--------|
| Will Chromium-only catch the regression? | Default to yes |
| Does this component have responsive behavior? | If no → 1 viewport. If yes → 3 |
| Do you ship CSS that's known to differ across engines? | If yes → cross-browser tier matters |
| Is your traffic measurably Safari-skewed? | If yes → cross-browser tier matters |
| Can you maintain N tests × M viewports × B browsers PNGs? | If no → cut B first, then M |

## Pattern

Tiered matrix:

| Tier | Browsers | Viewports | Per-test multiplier |
|------|----------|-----------|---------------------|
| Component shared | Chromium | 1 (desktop) | 1× |
| Component layout-aware | Chromium | 3 (mobile/tablet/desktop) | 3× |
| Page critical | Chromium | 3 | 3× |
| Page cross-browser | Chromium + Firefox + WebKit | 1 (desktop) | 3× |

Project naming — name projects so the project name flows into the baseline filename. Playwright generates `{test}-{project}-{platform}.png`:

```ts
projects: [
  { name: 'chromium-1440', use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } } },
  { name: 'chromium-768',  use: { ...devices['Desktop Chrome'], viewport: { width: 768,  height: 1024 } } },
  { name: 'chromium-375',  use: { ...devices['Desktop Chrome'], viewport: { width: 375,  height: 667 } } },
]
```

This produces `homepage-1-chromium-1440-linux.png` — the project name is self-documenting.

## Common Mistakes

- **Wrong**: starting with all 9 cells of the cube filled → **Right**: never recover; team disables flaky tests until none remain
- **Wrong**: single project, multiple viewports per test (`page.setViewportSize` mid-test) → **Right**: baselines collide; project per viewport is the only sane pattern

## See Also

- [What to Capture](vr-what-to-capture.md)
- [Baseline Management](vr-baseline-management.md)
- [Reference Program](vr-reference-program.md)
