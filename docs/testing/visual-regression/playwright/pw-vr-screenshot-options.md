---
description: Reference for every option available to toHaveScreenshot() and page.screenshot().
tldr: "Set `animations: 'disabled'`, `caret: 'hide'`, `threshold: 0.15`, and `maxDiffPixelRatio: 0.005` globally in `expect.toHaveScreenshot`. Never override `animations: 'allow'` — it reintroduces flake."
---

# Screenshot Options

## When to Use

> Use this as a reference when configuring screenshot capture and diff thresholds globally or per-assertion.

## Capture Options

Applies to both `toHaveScreenshot()` and `page.screenshot()`:

| Option | Type | Default | Purpose |
|---|---|---|---|
| `animations` | `"disabled" \| "allow"` | `"disabled"` | Stops CSS animations/transitions; finite animations fast-forwarded, infinite canceled |
| `caret` | `"hide" \| "initial"` | `"hide"` | Hides the text caret |
| `clip` | `{ x, y, width, height }` | unset | Crop to a rect |
| `fullPage` | `boolean` | `false` | Full scrollable page capture |
| `mask` | `Array<Locator>` | `[]` | Overlays matched elements with `#FF00FF` |
| `maskColor` | CSS color | `#FF00FF` | Mask overlay color |
| `omitBackground` | `boolean` | `false` | Transparent background; not for JPEG |
| `scale` | `"css" \| "device"` | `"css"` | `"css"` = 1px per CSS px |
| `stylePath` | `string \| string[]` | unset | Inject CSS during capture; pierces Shadow DOM |
| `timeout` | number (ms) | `5000` | Total auto-retry budget |

## Diff Options

Only on `toHaveScreenshot()`:

| Option | Type | Default | Purpose |
|---|---|---|---|
| `threshold` | number 0–1 | `0.2` | YIQ color tolerance per pixel |
| `maxDiffPixels` | number | unset | Hard cap on differing pixels |
| `maxDiffPixelRatio` | number 0–1 | unset | Cap as ratio of total pixels |

## Pattern

### Global defaults

```ts
expect: {
  timeout: 5000,
  toHaveScreenshot: {
    threshold: 0.15,
    maxDiffPixelRatio: 0.005,
    stylePath: './screenshot.css',
    animations: 'disabled',
    caret: 'hide',
  },
  toMatchSnapshot: { maxDiffPixelRatio: 0.1 },
}
```

`toMatchSnapshot()` only supports `name`, `threshold`, `maxDiffPixels`, `maxDiffPixelRatio` — no `mask`, `animations`, etc.

## Common Mistakes

- **Wrong**: `animations: 'allow'` → **Right**: never override the default; it reintroduces flake
- **Wrong**: `fullPage: true` on every test → **Right**: use selectively; full-page PNGs are 5–15 MB
- **Wrong**: `threshold: 0` chasing pixel-perfect → **Right**: trust `0.2`; tighten only with a documented reason

## See Also

- [Stability Controls](pw-vr-stability-controls.md)
- [Screenshot APIs](pw-vr-screenshot-apis.md)
- Reference: [Playwright toHaveScreenshot](https://playwright.dev/docs/api/class-pageassertions#page-assertions-to-have-screenshot-1)
