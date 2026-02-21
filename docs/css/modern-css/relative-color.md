---
description: Derive color variations with relative color syntax — generate palettes from one base
---

# Relative Color Syntax

## When to Use

> Use relative color syntax to derive color variations from a base color variable — the native replacement for Sass color manipulation libraries. Use a literal color value when no derivation is needed.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Generate a full palette from one base color | Relative color syntax | Computationally derived, stays in sync |
| Hover/focus state slightly darker | `oklch(from var(--brand) calc(l - 0.1) c h)` | Reads and modifies one channel |
| Muted version of a color | `oklch(from var(--brand) l calc(c * 0.5) h)` | Reduces chroma only |
| Complementary hue | `oklch(from var(--brand) l c calc(h + 180))` | Rotates hue 180° |
| Fixed color, no derivation needed | Literal value | Relative syntax adds complexity for no benefit |
| Dark mode variants | Relative syntax inside `@media (prefers-color-scheme: dark)` | Single source of truth |

## Pattern

```css
:root {
  --brand: oklch(55% 0.18 250);
}

.button {
  background: var(--brand);

  /* Darker hover — lower lightness, same chroma and hue */
  &:hover {
    background: oklch(from var(--brand) calc(l - 0.1) c h);
  }

  /* Focus ring — higher lightness */
  &:focus-visible {
    outline: 2px solid oklch(from var(--brand) calc(l + 0.2) c h);
  }
}

/* Muted background version */
.card {
  background: oklch(from var(--brand) 95% calc(c * 0.3) h);
}

/* Complementary accent */
.accent {
  color: oklch(from var(--brand) l c calc(h + 180));
}
```

**Syntax:** `color-function(from origin-color channel1 channel2 channel3)` — channel values resolve as unitless numbers that can be used in `calc()`.

**Browser support:** Chrome 119, Firefox 128 (July 2024), Safari 16.4. Safe to use.

## Common Mistakes

- **Wrong**: Using percentage units in `calc()` on channels → **Right**: Channel values in relative syntax are unitless numbers (`l` in OKLCH is 0–1, not 0%–100%); write `calc(l - 0.1)` not `calc(l - 10%)`
- **Wrong**: Mixing color spaces in relative syntax → **Right**: The origin color must match the function; you cannot extract oklch channels inside `rgb()`
- **Wrong**: Relying on older Safari behavior with typed channel units → **Right**: The current spec resolves channels to unitless numbers; `calc()` without units is correct

## See Also

- [color-mix()](color-mix.md)
- [light-dark() — One-Line Dark Mode](light-dark.md)
- Reference: [MDN Relative colors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_colors/Relative_colors)
