---
description: "How to use the VR diff panel in the Playwright HTML report to triage toHaveScreenshot() failures."
tldr: "When toHaveScreenshot() fails, the per-test detail shows a diff panel with Expected, Actual, and Diff images in four interactive modes — Slider is the most useful for catching pixel shifts. Red diff pixels exceed threshold; yellow are anti-aliasing skips."
---

# VR Diff Panel

## When to Use

> Triaging an `expect(page).toHaveScreenshot()` failure.

## What You See

When a screenshot assertion fails, the per-test detail page renders a dedicated **Image diff** panel above the rest of the test output. Three images are attached:

1. **Expected** — the committed baseline PNG (`<test>-snapshots/<name>-<project>-<platform>.png`)
2. **Actual** — the screenshot captured this run (`<name>-actual.png`)
3. **Diff** — pixelmatch-style overlay highlighting changed pixels (`<name>-diff.png`)

## Four Interactive Modes (tabs above the image)

| Mode | What it does | Use when |
|---|---|---|
| **Side-by-side** | Expected and Actual rendered next to each other | Spotting layout shifts at a glance |
| **Slider** | Single image area with a draggable vertical handle that wipes between Expected (left) and Actual (right) | Catching small element shifts; the most useful mode |
| **Onion-skin / Overlay** | Expected and Actual stacked with adjustable opacity slider | Spotting sub-pixel positional drift |
| **Diff** | Highlight overlay; **red** = exceeds tolerance, **yellow** = within tolerance | Confirming where the diff actually is |

## Pattern: Triage with the Slider

1. Open the failing test
2. Switch to **Slider** mode
3. Drag the handle slowly across the image
4. Cross-check with **Diff** mode to confirm red regions match what your eye saw
5. Decide: intentional vs regression

## Reading the Diff PNG Colors

| Color | Meaning |
|---|---|
| Red | Pixel exceeds `threshold` and counts toward `maxDiffPixels` / `maxDiffPixelRatio` |
| Yellow | Pixel differs but was detected as anti-aliasing — skipped |
| Faded original colors | The original image's content rendered behind the overlay (controlled by pixelmatch's `alpha` option) |

If multiple `toHaveScreenshot()` calls fail in one test, each gets its own labeled diff block.

## Click-Through

Each image is clickable to open at full resolution in a new tab. The report also surfaces the comparison parameters Playwright used (threshold, `maxDiffPixelRatio`, animation handling) when the assertion failed.

## Common Mistakes

- **Trusting "looks the same" in Side-by-side without Slider** — the eye misses 1px shifts at thumbnail size
- **Dismissing yellow regions** — they're within tolerance now; if your tolerance is wrong, they should have been red
- **Not zooming** — full-resolution view is one click; use it for fine details

## See Also

- [Navigation](pw-report-navigation.md)
- [Per-Test Detail](pw-report-per-test-detail.md)
- [Baseline Updates](pw-report-baseline-updates.md)
- Reference: [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)
