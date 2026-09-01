---
description: How to use the VR diff panel in the Playwright HTML report to triage toHaveScreenshot() failures.
tldr: When toHaveScreenshot() fails, the per-test detail shows a diff panel with Expected, Actual, and Diff images in four interactive modes — Slider is the most useful for catching pixel shifts. Red diff pixels exceed threshold; yellow are anti-aliasing skips.
---

# VR Diff Panel

## When to Use

> Use this when triaging an `expect(page).toHaveScreenshot()` failure — the diff panel is the primary tool for deciding intentional change vs regression.

## What You See

When a screenshot assertion fails, the per-test detail page renders a dedicated **Image diff** panel above the rest of the test output. Three images are attached:

1. **Expected** — the committed baseline PNG (`<test>-snapshots/<name>-<project>-<platform>.png`)
2. **Actual** — the screenshot captured this run (`<name>-actual.png`)
3. **Diff** — pixelmatch-style overlay highlighting changed pixels (`<name>-diff.png`)

## Decision

| Mode | Use when |
|---|---|
| **Side-by-side** | Spotting layout shifts at a glance |
| **Slider** | Catching small element shifts — the most useful mode |
| **Onion-skin / Overlay** | Spotting sub-pixel positional drift |
| **Diff** | Confirming where the diff is; interpreting red vs yellow regions |

## Pattern

Standard triage flow with the slider:

```
1. Open the failing test
2. Switch to Slider mode
3. Drag handle slowly across the image
4. Cross-check with Diff mode to confirm red regions match what you saw
5. Decide: intentional change vs regression
```

## Reading Diff PNG Colors

| Color | Meaning |
|---|---|
| Red | Pixel exceeds `threshold` — counts toward `maxDiffPixels` / `maxDiffPixelRatio` |
| Yellow | Pixel differs but detected as anti-aliasing — skipped by pixelmatch |
| Faded original | Background content behind the overlay |

If multiple `toHaveScreenshot()` calls fail in one test, each gets its own labeled diff block.

Each image is clickable to open at full resolution in a new tab.

## Common Mistakes

- **Wrong**: trusting "looks the same" in Side-by-side without using Slider → **Right**: the eye misses 1px shifts at thumbnail size
- **Wrong**: dismissing yellow regions as safe → **Right**: they're within tolerance now; if tolerance is misconfigured they should have been red
- **Wrong**: not clicking to full resolution → **Right**: fine details require the full-resolution view; one click away

## See Also

- [Navigation](pw-report-navigation.md)
- [Per-Test Detail](pw-report-per-test-detail.md)
- [Baseline Updates](pw-report-baseline-updates.md)
- Reference: [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)
