---
description: "Visual regression testing — baseline-comparison screenshot testing for design systems, and when it earns its keep vs. adds noise."
tldr: "Visual regression testing captures screenshots and diffs pixels against a baseline. It earns its keep for stable component libraries and design systems; it adds friction when UI is still changing. Requires deterministic rendering — disable animations, pin browser versions, set a 1–3% diff threshold."
---

# Visual Regression Concepts

## When to Use

> When you have a stable UI component library, design system, or page layout that must not change unexpectedly. Visual regression (VR) testing captures screenshots of rendered UI and alerts when pixels change. It earns its keep for design systems and component libraries; it adds noise and cost when applied indiscriminately.

## What Visual Regression Testing Is

VR testing works on a baseline-comparison model:

1. **Capture baseline** — screenshot the component or page in a known-good state
2. **Run tests** — screenshot the same component/page after each change
3. **Diff** — compare pixel-by-pixel; report if difference exceeds a threshold
4. **Triage** — developer reviews diff: is it an intentional change (update baseline) or a regression (fix the code)?

VR testing catches regressions that functional tests miss:
- CSS layout shifts caused by a selector specificity change
- Font rendering differences from a dependency upgrade
- Subtle color or spacing drift from a token change
- Third-party widget layout changes

VR testing does **not** replace functional tests:
- It cannot verify that a button click does the right thing
- It cannot verify accessibility of the rendered output
- Pixel diffs tell you *something changed*, not *why* or *whether it matters*

## When VR Earns Its Keep

Use VR testing when:
- You maintain a component library or design system with many consumers
- Visual consistency across breakpoints and browsers is a hard requirement
- You make frequent CSS/SCSS changes and need an automated regression net
- You have a style-guide or Storybook-equivalent and want to prevent silent drift

Skip or defer VR testing when:
- The UI is still rapidly changing (VR tests require constant baseline updates, creating friction)
- You have no stable component boundary to test against
- You cannot allocate time to triage false positives (VR noise degrades into ignored alerts)

## Baseline Management

Baselines are image files committed alongside tests. Core discipline:

- **Update baselines deliberately** — only when the visual change is intentional and reviewed
- **Threshold tuning** — set a pixel-difference threshold low enough to catch real regressions, high enough to not fail on subpixel antialiasing differences (1–3% is typical)
- **Deterministic rendering** — disable animations, use consistent fonts, pin browser versions; non-deterministic rendering = false positives on every run
- **Responsive coverage** — capture baselines at each breakpoint you guarantee (mobile, tablet, desktop)

## Pattern

```javascript
// Playwright visual regression (built-in toHaveScreenshot)
// One screenshot per meaningful visual state

test('hero banner renders correctly at desktop', async ({ page }) => {
  await page.goto('/');
  await page.setViewportSize({ width: 1280, height: 800 });
  // Stabilize: wait for fonts, images, animations
  await page.waitForLoadState('networkidle');
  await expect(page).toHaveScreenshot('hero-desktop.png', {
    maxDiffPixelRatio: 0.02, // 2% threshold
  });
});
```

## Common Mistakes

- Running VR on non-deterministic pages → Animation, dynamic dates, random content cause constant false positives; stabilize before shooting
- No triage process → VR failures get ignored because no one knows if they matter; define a triage workflow before enabling VR
- VR for every page instead of components → Leads to thousands of screenshots and unmanageable maintenance; test components in isolation first
- Not pinning browser and font versions → The same CSS renders differently in Chrome 120 vs 121; CI must match local baseline capture conditions

## See Also

- ← Previous: [E2E Testing Concepts](e2e-testing-concepts.md) | Next: [Contract & API Testing Concepts](contract-api-testing-concepts.md) →
- Related: [testing/visual-regression](https://camoa.github.io/dev-guides/testing/visual-regression/) — full VR how-to (workflow, Playwright VR, pixelmatch, HTML report)
