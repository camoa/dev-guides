---
description: Visual regression testing — baseline-comparison screenshot testing for design systems, and when it earns its keep vs. adds noise.
tldr: Visual regression testing captures screenshots and diffs pixels against a baseline. It earns its keep for stable component libraries and design systems; it adds friction when UI is still changing. Requires deterministic rendering — disable animations, pin browser versions, set a 1–3% diff threshold.
---

# Visual Regression Concepts

## When to Use

> Use VR testing for stable component libraries and design systems with many consumers. Skip it when the UI is still rapidly changing, when you have no stable component boundary, or when you cannot allocate time to triage false positives.

## Decision

| Use VR testing when... | Skip VR testing when... |
|---|---|
| You maintain a component library or design system with many consumers | UI is still rapidly changing — constant baseline updates create friction |
| Visual consistency across breakpoints is a hard requirement | You have no stable component boundary to test against |
| You make frequent CSS/SCSS changes and need an automated regression net | You cannot allocate time to triage false positives |
| You have a Storybook-equivalent and want to prevent silent drift | |

**VR does not replace functional tests:** it cannot verify that a button click does the right thing or that the output is accessible. Pixel diffs tell you *something changed*, not *why* or *whether it matters*.

## Pattern

```javascript
// Playwright visual regression (built-in toHaveScreenshot)
test('hero banner renders correctly at desktop', async ({ page }) => {
  await page.goto('/');
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.waitForLoadState('networkidle'); // stabilize: fonts, images, animations
  await expect(page).toHaveScreenshot('hero-desktop.png', {
    maxDiffPixelRatio: 0.02, // 2% threshold
  });
});
```

**Baseline discipline:** update baselines deliberately and only when the visual change is intentional. Capture baselines at each breakpoint you guarantee (mobile, tablet, desktop).

## Common Mistakes

- **Wrong**: Running VR on non-deterministic pages → **Right**: Disable animations, use consistent fonts, pin browser versions before shooting
- **Wrong**: No triage process → **Right**: Define a triage workflow before enabling VR; ignored failures degrade into noise
- **Wrong**: VR for every page instead of components → **Right**: Test components in isolation first; thousands of screenshots are unmanageable
- **Wrong**: Not pinning browser and font versions → **Right**: Same CSS renders differently across Chrome versions; CI must match local baseline conditions

## See Also

- [E2E Testing Concepts](e2e-testing-concepts.md) | Next: [Contract & API Testing Concepts](contract-api-testing-concepts.md)
- Related: [testing/visual-regression](https://camoa.github.io/dev-guides/testing/visual-regression/) — full VR how-to (workflow, Playwright VR, pixelmatch, HTML report)
