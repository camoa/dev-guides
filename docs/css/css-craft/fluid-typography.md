---
description: Fluid typography — clamp() type scales, fluid spacing systems, and container-relative sizing with cqi units
tldr: "Use `clamp()` for font sizes and spacing that scale smoothly between viewport sizes with no jarring breakpoint jumps. Use `cqi` units for component-relative scaling inside container queries."
---

# Fluid Typography

## When to Use
When a client wants text that scales smoothly between viewport sizes with no jarring breakpoint jumps — the standard approach for modern responsive typography.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| Font size scales with viewport | `clamp()` | One line, min/max/preferred |
| Spacing scales with viewport | `clamp()` on `gap`, `padding`, `margin` | Same technique |
| Type scale system (h1-h6) | `clamp()` per heading level | Consistent hierarchy at all sizes |
| Container-relative sizing | `cqi` units | Scales with container, not viewport |

## Pattern: Fluid Type Scale
```css
:root {
  --text-xs:   clamp(0.75rem,  0.7rem  + 0.25vw, 0.875rem);
  --text-sm:   clamp(0.875rem, 0.8rem  + 0.35vw, 1rem);
  --text-base: clamp(1rem,     0.9rem  + 0.5vw,  1.125rem);
  --text-lg:   clamp(1.125rem, 0.95rem + 0.75vw, 1.5rem);
  --text-xl:   clamp(1.5rem,   1rem    + 1.5vw,  2.5rem);
  --text-2xl:  clamp(2rem,     1.2rem  + 2.5vw,  3.5rem);
  --text-3xl:  clamp(2.5rem,   1.5rem  + 3vw,    5rem);
}

h1 { font-size: var(--text-3xl); }
h2 { font-size: var(--text-2xl); }
h3 { font-size: var(--text-xl); }
p  { font-size: var(--text-base); }
```

## Pattern: Fluid Spacing
```css
:root {
  --space-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --space-sm: clamp(0.5rem,  0.4rem + 0.5vw,  1rem);
  --space-md: clamp(1rem,    0.8rem + 1vw,     2rem);
  --space-lg: clamp(1.5rem,  1rem   + 2vw,     4rem);
  --space-xl: clamp(2rem,    1.5rem + 3vw,     6rem);
}

.section { padding-block: var(--space-xl); }
.card { padding: var(--space-md); gap: var(--space-sm); }
```

## Pattern: Container-Relative Typography
```css
.card-container {
  container-type: inline-size;
}

.card__title {
  font-size: clamp(1rem, 3cqi, 2rem);
}

.card__body {
  font-size: clamp(0.875rem, 2cqi, 1.125rem);
}
```

## The clamp() Formula
```
clamp(MIN, PREFERRED, MAX)
```
- **MIN**: smallest the text will ever be (accessibility floor — usually ≥1rem for body)
- **PREFERRED**: scales with viewport (e.g., `0.9rem + 1vw`)
- **MAX**: largest the text will ever be (design ceiling)

**Quick formula**: `clamp(minRem, calcRem + Xvw, maxRem)` where `X` = `(max - min) / (maxViewport - minViewport) * 100`.

**Tools**: [Utopia.fyi](https://utopia.fyi/) generates fluid type/space scales with custom min/max viewports.

**Browser support:** `clamp()`: all browsers (Baseline 2020). `cqi`: all browsers (Baseline 2023). Fully production-ready.

## Common Mistakes
- **Body text below 1rem** — accessibility minimum; ensure `clamp()` min is ≥ 1rem for body text
- **Too aggressive vw component** — text that changes too drastically feels unstable; keep vw multiplier ≤ 3vw for most uses
- **Not combining with `text-wrap: balance`** — fluid headings benefit from balanced line breaks
- **Using only vw units** (no clamp) — pure `font-size: 3vw` has no min/max, becomes illegible on small/huge screens

## See Also
- [Modern CSS: Container Units](../modern-css/container-units.md) → cqi/cqw for component-level sizing
- [Modern CSS: text-wrap](../modern-css/text-wrap.md) → balanced headings
- [Motion Design Tokens](motion-design-tokens.md) → consistent spacing system
- Reference: [Utopia.fyi](https://utopia.fyi/) — fluid type/space calculator
