---
description: Fluid typography — clamp() type scales, fluid spacing systems, and container-relative sizing with cqi units
tldr: "Use `clamp()` for font sizes and spacing that scale smoothly between viewport sizes with no jarring breakpoint jumps. Use `cqi` units for component-relative scaling inside container queries."
---

# Fluid Typography

## When to Use

> Use `clamp()` for font sizes and spacing that scale smoothly between viewport sizes with no jarring breakpoint jumps. Use `cqi` units for component-relative scaling inside container queries.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| Font size scales with viewport | `clamp()` | One line, min/max/preferred |
| Spacing scales with viewport | `clamp()` on `gap`, `padding`, `margin` | Same technique |
| Type scale system (h1–h6) | `clamp()` per heading level | Consistent hierarchy at all sizes |
| Container-relative sizing | `cqi` units | Scales with container, not viewport |

## Pattern

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
p  { font-size: var(--text-base); }

/* Fluid spacing */
:root {
  --space-sm: clamp(0.5rem,  0.4rem + 0.5vw, 1rem);
  --space-md: clamp(1rem,    0.8rem + 1vw,   2rem);
  --space-lg: clamp(1.5rem,  1rem   + 2vw,   4rem);
}

/* Container-relative typography */
.card-container { container-type: inline-size; }
.card__title    { font-size: clamp(1rem, 3cqi, 2rem); }
```

**`clamp()` formula:** `clamp(MIN, calcRem + Xvw, MAX)` where `X = (max - min) / (maxVp - minVp) * 100`. Tool: [Utopia.fyi](https://utopia.fyi/).

## Common Mistakes

- **Body text min below 1rem** — accessibility minimum; `clamp()` min must be ≥ 1rem for body text
- **Too aggressive vw component** — text changing too drastically feels unstable; keep ≤ 3vw for most uses
- **Not combining with `text-wrap: balance`** — fluid headings benefit from balanced line breaks
- **Using only vw units** without `clamp` — `font-size: 3vw` has no floor/ceiling, becomes illegible at extremes

## See Also

- [Container Query Craft](container-queries-craft.md) → `cqi`/`cqw` for component-level sizing
- [Motion Design Tokens](motion-design-tokens.md) → consistent spacing system
- Reference: [Utopia.fyi](https://utopia.fyi/) — fluid type/space calculator
