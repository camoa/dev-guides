---
description: Know which CSS properties animate at 60fps — compositor-only vs paint vs layout tiers, practical property mapping
tldr: "Before animating any CSS property, know its rendering cost. The difference between animating `transform` and `width` is the difference between 60fps and dropped frames."
---

# Animation Performance

## When to Use
Before animating any CSS property, know its rendering cost. The difference between animating `transform` and `width` is the difference between 60fps and dropped frames.

## Decision: The Performance Tier List

| Tier | Properties | Rendering Cost | When to Use |
|---|---|---|---|
| **Compositor-only** (best) | `transform`, `opacity`, `filter`, `clip-path` | GPU thread, no layout/paint | Always prefer these for animation |
| **Paint-only** (moderate) | `background-color`, `border-color`, `color`, `box-shadow`, `outline` | Repaint, no layout | Acceptable for small/few elements |
| **Layout-triggering** (avoid) | `width`, `height`, `padding`, `margin`, `top`, `left`, `font-size`, `border-width` | Full layout recalc + paint | Never animate these; use `transform` equivalents |

## Frame Budget Numbers

| Metric | Value |
|---|---|
| Target frame rate | 60fps = 16.6ms per frame |
| Compositor-only animation | Well within budget |
| Single `box-shadow` repaint | 0.5-2ms (acceptable) |
| 5-layer `box-shadow` repaint | 2-5ms (careful on mobile) |
| Layout-triggering property | 5-20ms+ depending on DOM size |
| `top/left` animation vs `transform` | 50% frame drops vs 1% (web.dev benchmark) |

## Pattern

```css
/* BAD: layout-triggering animation */
.animate-bad {
  transition: top 300ms, left 300ms, width 300ms;
}

/* GOOD: compositor-only equivalents */
.animate-good {
  transition: transform 300ms;
  /* Use translate instead of top/left */
  /* Use scale instead of width/height */
}

/* will-change — use sparingly, only before animation starts */
.about-to-animate {
  will-change: transform, opacity;
}

/* contain — help browser isolate rendering boundaries */
.isolated-component {
  contain: layout style paint;
}
```

**Practical mapping of layout properties to compositor equivalents:**

| Instead of animating... | Animate... | How |
|---|---|---|
| `top` / `left` | `transform: translate()` | Same visual result, GPU-composited |
| `width` / `height` | `transform: scale()` | Or use `clip-path` for reveal effects |
| `margin` | `transform: translate()` | Shift visual position without layout |
| `border-width` | `outline` or `box-shadow` | Outline does not trigger layout |

## Common Mistakes
- Using `will-change` as a global performance fix — it reserves GPU memory; only apply it right before animation and remove after
- Animating `box-shadow` on 50+ cards simultaneously — each triggers repaint; use a `::after` pseudo-element with `opacity` transition instead
- Animating `height: auto` directly — use `max-height` with a generous upper bound, or `grid-template-rows: 0fr` to `1fr` for modern collapse
- Using `transition: all` — transitions every property including layout-triggering ones; always list specific properties
- Forgetting mobile — mobile GPUs have less headroom; test animations on real devices, not just desktop DevTools

## See Also
- [Micro-Interactions](micro-interactions.md) — applying compositor-safe properties in practice
- [Entrance Animations](entrance-animations.md) — `transform` + `opacity` reveal patterns
- Reference: [web.dev: High-Performance CSS Animations](https://web.dev/articles/animations-guide)
- Reference: [Motion.dev: Animation Performance Tier List](https://motion.dev/magazine/web-animation-performance-tier-list)
