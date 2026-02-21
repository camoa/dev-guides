---
description: Mix colors natively with color-mix() — replace Sass lighten(), darken(), mix()
---

# color-mix()

## When to Use

> Use `color-mix()` to mix two colors natively — the direct replacement for Sass `lighten()`, `darken()`, and `mix()`. Always specify `in oklch` for perceptually uniform results; use `in srgb` only when mixing with `transparent`.

## Decision

| If you need... | Use... | Example |
|---|---|---|
| Lighter tint of a brand color | Mix with white in `oklch` | `color-mix(in oklch, var(--brand) 70%, white)` |
| Semi-transparent overlay | Mix with transparent in `srgb` | `color-mix(in srgb, var(--brand) 20%, transparent)` |
| Mid-point between two colors | 50% mix | `color-mix(in oklch, red 50%, blue)` |
| Darkened shade | Mix with black | `color-mix(in oklch, var(--brand) 70%, black)` |

## Pattern

```css
:root {
  --brand: oklch(55% 0.18 250);

  /* Tint — like Sass lighten() */
  --brand-light: color-mix(in oklch, var(--brand) 60%, white);

  /* Shade — like Sass darken() */
  --brand-dark: color-mix(in oklch, var(--brand) 70%, black);

  /* Semi-transparent — like rgba() but from a token */
  --brand-overlay: color-mix(in srgb, var(--brand) 15%, transparent);

  /* Mix two brand colors */
  --brand-mixed: color-mix(in oklch, var(--primary) 60%, var(--secondary));
}
```

The percentage is the proportion of the first color. Omitting it defaults to 50%.

**Color space matters:** `in oklch` produces perceptually uniform mixing. `in srgb` produces muddy mid-tones. `in hsl` has similar perceptual uniformity problems as HSL generally.

**Browser support:** Chrome 111, Firefox 113, Safari 16.2. Widely available since May 2023. Safe to use.

## Common Mistakes

- **Wrong**: Using `in srgb` for tints and shades → **Right**: `in srgb` produces visually muddy results; use `in oklch`
- **Wrong**: Expecting `color-mix` as a fallback for older browsers → **Right**: There is no graceful degradation; older browsers get no color; test your fallbacks
- **Wrong**: Mixing with `transparent` using `in oklch` → **Right**: OKLCH transparent has hue artifacts; use `in srgb` specifically for transparent mixing

## See Also

- [oklch() / oklab() — Modern Color Spaces](oklch-color.md)
- [Relative Color Syntax](relative-color.md)
- Reference: [MDN color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix)
