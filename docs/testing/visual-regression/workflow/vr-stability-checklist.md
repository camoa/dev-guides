---
description: The pre-baseline capture checklist that prevents flaky VR tests before they happen.
tldr: "Run the 10-point checklist before any baseline capture: disable animations, hide carets, wait for fonts and images, wait for network idle, mask dynamic regions, normalize scroll and focus, dismiss cookie banners, and pin the Chromium version via the official Playwright Docker image."
---

# Stability Checklist

## When to Use

> Use this checklist before *any* baseline is captured. Skip a step here, get a flake later.

## Decision

| Symptom | Most likely missing checklist item |
|---------|-----------------------------------|
| First baseline capture differs slightly each time | Fonts (3) or network (5) |
| Hover state shows briefly | Mouse position not normalized — move it to (0,0) before capture |
| Image regions vary | Lazy-loading (4) |
| Time/counter regions vary | Masking (6) |
| Cross-OS diffs | Pinning (10) |

## Pattern

The 10-point checklist:

1. **Disable animations** — `animations: 'disabled'` (Playwright default for `toHaveScreenshot`)
2. **Hide carets / blinking cursors** — `caret: 'hide'` (Playwright default)
3. **Wait for fonts loaded** — `await page.evaluate(() => document.fonts.ready)`
4. **Wait for images loaded (including lazy)** — scroll-to-bottom-then-top, or eager-load
5. **Wait for network idle** — `await page.waitForLoadState('networkidle')`
6. **Mask dynamic regions** — `mask: [page.locator('[data-vrt-mask]')]`
7. **Normalize scroll position** — `await page.evaluate(() => window.scrollTo(0, 0))`
8. **Hide cookie banners / GDPR overlays** — set the consent cookie before navigation
9. **Clear focus indicators that shift across OSes** — `(document.activeElement as HTMLElement)?.blur()`
10. **Pin the Chromium version** — use the official Playwright Docker image (`mcr.microsoft.com/playwright:v1.X.Y-noble`) for both local capture and CI

Global stability stylesheet via `expect.toHaveScreenshot.stylePath`:

```css
/* tests/playwright/screenshot.css */
*, *::before, *::after {
  animation: none !important;
  transition: none !important;
  caret-color: transparent !important;
}
iframe { visibility: hidden; }
[data-vrt-mask] { visibility: hidden; }
```

```ts
// playwright.config.ts
expect: {
  toHaveScreenshot: { stylePath: './screenshot.css' },
}
```

## Common Mistakes

- **Wrong**: adding VR tests without disabling animations → **Right**: universal first-month flakiness cause
- **Wrong**: `waitForLoadState('networkidle')` on a page with long-poll/SSE → **Right**: hangs forever; switch to `'domcontentloaded'` plus explicit waits
- **Wrong**: dismissing cookie banner via UI click each test → **Right**: slow and flaky; set the cookie before navigation instead

## See Also

- [Authoring Patterns](vr-authoring-patterns.md)
- [Threshold Tuning](vr-threshold-tuning.md)
- [Triaging False Positives](vr-triaging-false-positives.md)
- [Drupal & DDEV Procedure](vr-drupal-ddev-procedure.md)
