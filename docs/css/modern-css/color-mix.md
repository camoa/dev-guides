---
description: "Mix colors natively with color-mix() — replace Sass lighten(), darken(), mix()"
tldr: "Use `color-mix()` to mix two colors natively — the direct replacement for Sass `lighten()`, `darken()`, and `mix()`. Always specify `in oklch` for perceptually uniform results; use `in srgb` only when mixing with `transparent`."
---

# color-mix()

## When to Use

> To mix two colors natively — the direct replacement for Sass `lighten()`, `darken()`, and `mix()`. Works with any two colors in any color space.

## Decision

| If you need... | Use... | Example |
|---|---|---|
| Lighter tint of a brand color | Mix with white in `oklch` | `color-mix(in oklch, var(--brand) 70%, white)` |
| Semi-transparent overlay | Mix with transparent | `color-mix(in srgb, var(--brand) 20%, transparent)` |
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

**Color space matters:** Always use `in oklch` for perceptually uniform mixing. `in srgb` produces muddy mid-tones because it interpolates through grays. `in hsl` has similar perceptual uniformity problems as HSL generally.

The percentage in `color-mix(in oklch, colorA X%, colorB)` is the proportion of color A. Omitting it defaults to 50%.

**Browser support:** Chrome 111, Firefox 113, Safari 16.2. Widely available since May 2023. Safe to use.

## Common Mistakes

- Using `in srgb` for tints/shades — produces visually muddy results; use `in oklch`
- Expecting `color-mix` to work as a fallback for older browsers — it's not supported in any version before the ones listed; test your fallback
- Mixing with `transparent` using `in oklch` for overlays — oklch transparent has hue artifacts; use `in srgb` specifically for transparent mixing

## See Also

- ← [oklch() Color Space](oklch-color.md) | [Relative Color Syntax](relative-color.md) →
- Reference: [MDN color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix)
