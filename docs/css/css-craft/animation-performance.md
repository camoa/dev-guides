---
description: Know which CSS properties animate at 60fps — compositor-only vs paint vs layout tiers, practical property mapping
tldr: "Before animating any CSS property, know its rendering cost. The difference between animating `transform` and `width` is the difference between 60fps and dropped frames."
---

# Animation Performance

## When to Use

> Before animating any CSS property, know its rendering cost. The difference between animating `transform` and `width` is the difference between 60fps and dropped frames.

## Decision

| Tier | Properties | Rendering Cost | When to Use |
|------|-----------|----------------|-------------|
| **Compositor-only** (best) | `transform`, `opacity`, `filter`, `clip-path` | GPU thread, no layout/paint | Always prefer for animation |
| **Paint-only** (moderate) | `background-color`, `border-color`, `color`, `box-shadow`, `outline` | Repaint, no layout | Acceptable for small/few elements |
| **Layout-triggering** (avoid) | `width`, `height`, `padding`, `margin`, `top`, `left`, `font-size` | Full layout recalc + paint | Never animate these |

### Property Equivalents

| Instead of animating | Animate | How |
|----------------------|---------|-----|
| `top` / `left` | `transform: translate()` | Same visual result, GPU-composited |
| `width` / `height` | `transform: scale()` | Or use `clip-path` for reveal effects |
| `margin` | `transform: translate()` | Shift visual position without layout |
| `border-width` | `outline` or `box-shadow` | Outline does not trigger layout |

## Pattern

```css
/* BAD: layout-triggering */
.animate-bad { transition: top 300ms, width 300ms; }

/* GOOD: compositor-only equivalents */
.animate-good { transition: transform 300ms; }

/* will-change — use sparingly, only before animation starts */
.about-to-animate { will-change: transform, opacity; }

/* contain — isolate rendering boundaries */
.isolated-component { contain: layout style paint; }
```

### Frame Budget

| Metric | Value |
|--------|-------|
| Target | 60fps = 16.6ms per frame |
| `box-shadow` repaint | 0.5-2ms (acceptable) |
| 5-layer `box-shadow` | 2-5ms (careful on mobile) |
| Layout-triggering | 5-20ms+ depending on DOM size |

## Common Mistakes

- **Wrong**: `will-change` as a global fix — **Right**: Only apply before animation; remove after. It reserves GPU memory.
- **Wrong**: Animating `box-shadow` on 50+ cards — **Right**: Use a `::after` pseudo-element with `opacity` transition instead
- **Wrong**: Animating `height: auto` — **Right**: Use `max-height` with a generous bound, or `grid-template-rows: 0fr` to `1fr`
- **Wrong**: `transition: all` — **Right**: Always list specific properties; `all` transitions layout-triggering ones too
- **Wrong**: Testing only on desktop — **Right**: Mobile GPUs have less headroom; test on real devices

## See Also

- [Micro-Interactions](micro-interactions.md) — compositor-safe properties in practice
- [Entrance Animations](entrance-animations.md) — `transform` + `opacity` reveal patterns
- Reference: [web.dev: High-Performance CSS Animations](https://web.dev/articles/animations-guide)
- Reference: [Motion.dev: Animation Performance Tier List](https://motion.dev/magazine/web-animation-performance-tier-list)
