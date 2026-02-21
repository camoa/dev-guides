---
description: Perceptually uniform color with oklch() and oklab() — better than HSL for design tokens
---

# oklch() and oklab() — Modern Color Spaces

## When to Use

> Use `oklch` for design token systems and color palettes — its perceptually uniform lightness means adjusting `L` gives predictable brightness changes across all hues. Use `hex` or `rgb` for exact brand color matching.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Design token system with consistent lightness | `oklch` | Perceptually uniform — same `L` looks equally bright across hues |
| Accessible dark/light variants from one base | `oklch` + adjust `L` | Predictable contrast relationship |
| Wide gamut (P3) colors | `oklch` | Naturally expresses values beyond sRGB |
| An exact hex/brand color | `hex` or `rgb` | OKLCH is for token-driven palettes, not color matching |
| Smooth color interpolation in gradients | `oklab` or `oklch` | More perceptually even gradients than RGB or HSL |

## Pattern

Token system using OKLCH — one base color generates a full scale:

```css
:root {
  /* Brand blue — l=lightness(0-1), c=chroma(0-0.4), h=hue(0-360) */
  --brand-50:  oklch(95% 0.05 250);
  --brand-100: oklch(88% 0.09 250);
  --brand-400: oklch(65% 0.18 250);
  --brand-500: oklch(55% 0.18 250); /* base */
  --brand-600: oklch(45% 0.18 250);
  --brand-900: oklch(25% 0.12 250);
}
```

The same `c` (chroma) and `h` (hue) values held constant while adjusting `L` guarantees a perceptually uniform scale. In HSL, this produces wildly inconsistent apparent brightness.

**Parameter reference:**

| Parameter | Range | What it controls |
|---|---|---|
| `L` | 0%–100% (or 0–1) | Perceived lightness — 0=black, 100=white |
| `C` | 0–0.4 (practical max) | Chroma / color intensity — 0=gray |
| `H` | 0–360deg | Hue angle (0°≈pink/red, 120°≈green, 250°≈blue) |

**`oklab` vs `oklch`:** `oklab` uses Cartesian coordinates (`a`, `b` axes); `oklch` uses polar coordinates (`C`, `H`). Prefer `oklch` for token definition. Prefer `oklab` for gradient interpolation.

**Browser support:** Chrome 111, Firefox 113, Safari 15.4. Widely available since May 2023. Safe to use.

## Common Mistakes

- **Wrong**: Assuming OKLCH hue 0° is red → **Right**: OKLCH hue 0° is closer to magenta/pink; ~41° is red, ~250° is blue (different from HSL where 0°=red, 240°=blue)
- **Wrong**: Setting `C` above ~0.37 expecting full color → **Right**: Values above ~0.37 may be clamped on sRGB screens; wide gamut is only fully visible on P3 displays
- **Wrong**: Using `oklch` for exact brand color matching → **Right**: If a brand color is `#1d6efa`, convert it once; the resulting decimal values are fragile to hand-edit

## See Also

- [color-mix()](color-mix.md)
- [Relative Color Syntax](relative-color.md)
- Reference: [MDN oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch)
