---
description: "Reference for every option available to toHaveScreenshot() and page.screenshot()."
tldr: "Set `animations: 'disabled'`, `caret: 'hide'`, and `threshold: 0.15` globally in `expect.toHaveScreenshot`. Leave `maxDiffPixels`/`maxDiffPixelRatio` unset — unset already means a zero-pixel budget, not 'no budget'; add an absolute `maxDiffPixels` only if repeat runs on an unchanged site show a residual."
---

# Screenshot Options

## When to Use

> Use this as a reference when configuring screenshot capture and diff thresholds globally or per-assertion.

## Capture Options

Applies to both `toHaveScreenshot()` and `page.screenshot()`:

| Option | Type | Default | Purpose |
|---|---|---|---|
| `animations` | `"disabled" \| "allow"` | `"disabled"` | Stops CSS animations/transitions/Web Animations; finite animations fast-forwarded, infinite canceled |
| `caret` | `"hide" \| "initial"` | `"hide"` | Hides the text caret |
| `clip` | `{ x, y, width, height }` | unset | Crop to a rect |
| `fullPage` | `boolean` | `false` | Full scrollable page capture |
| `mask` | `Array<Locator>` | `[]` | Overlays matched elements with `#FF00FF` (or `maskColor`) — applied even to invisible elements |
| `maskColor` | CSS color | `#FF00FF` | Mask overlay color (added v1.35) |
| `omitBackground` | `boolean` | `false` | Transparent background; not for JPEG |
| `scale` | `"css" \| "device"` | `"css"` | `"css"` = 1 px per CSS px; `"device"` = 1 px per device px |
| `stylePath` | `string \| string[]` | unset | Inject CSS during capture; pierces Shadow DOM and inner frames (added v1.41) |
| `timeout` | number (ms) | from `expect.timeout` (5000 default) | Total auto-retry budget |

## Diff Options

Only on `toHaveScreenshot()`:

| Option | Type | Default | Purpose |
|---|---|---|---|
| `threshold` | number 0–1 | `0.2` | YIQ color tolerance per pixel; 0 = strict, 1 = lax |
| `maxDiffPixels` | number | unset — **means 0** | Hard cap on differing pixels |
| `maxDiffPixelRatio` | number 0–1 | unset — **means 0** | Cap as ratio of total pixels; the ratio is of image *area*, so on a full-page shot the budget grows with page height — prefer `maxDiffPixels` there |

Leaving both unset is not "no budget": Playwright resolves `maxDiffPixels ?? (imageArea × maxDiffPixelRatio) ?? 0`, so an unconfigured suite runs a zero-pixel budget. Stabilise the capture, then set a budget from the residual repeat runs actually show.

## Pattern

### Global defaults

```ts
expect: {
  timeout: 5000,
  toHaveScreenshot: {
    threshold: 0.15,
    stylePath: './screenshot.css',
    animations: 'disabled',
    caret: 'hide',
    // No pixel budget: unset already means zero. Add an absolute
    // maxDiffPixels only if repeat runs on an unchanged site show a residual.
  },
  toMatchSnapshot: { maxDiffPixelRatio: 0.1 },
}
```

`toMatchSnapshot()` only supports `name`, `threshold`, `maxDiffPixels`, `maxDiffPixelRatio` — no `mask`, `animations`, etc., because the buffer was already produced.

## Common Mistakes

- **Wrong**: `animations: 'allow'` → **Right**: never override the default; it reintroduces flake
- **Wrong**: `fullPage: true` on every test → **Right**: the cost is false positives from editorial content, not file size (a masked full-page baseline measures ~150 KB); use `clip` or element shots for components, and keep full-page for whole templates while masking what churns
- **Wrong**: `threshold: 0` chasing pixel-perfect → **Right**: trust `0.2`; tighten only with a documented reason
- **Wrong**: Assuming an unset `maxDiffPixels`/`maxDiffPixelRatio` means "no diff budget" → **Right**: unset resolves to 0, the strictest possible setting; a real budget must be set explicitly

## See Also

- [Stability Controls](pw-vr-stability-controls.md)
- [Screenshot APIs](pw-vr-screenshot-apis.md)
- Reference: [Playwright toHaveScreenshot](https://playwright.dev/docs/api/class-pageassertions#page-assertions-to-have-screenshot-1)
