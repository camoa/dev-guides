---
description: SVG line draw animations — stroke-dashoffset technique, staggered multi-path draw, draw-then-fill, and scroll-triggered drawing
---

# SVG Line Draw

## When to Use

> Use `stroke-dasharray` + `stroke-dashoffset` animation when a client wants icons, logos, or illustrations that draw themselves. Pure CSS on SVG strokes — no JavaScript needed.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| Icon that draws itself on load | `stroke-dasharray` + `stroke-dashoffset` animation | Pure CSS, no JS |
| Logo that draws on scroll | Same + `animation-timeline: view()` | Scroll-triggered draw |
| Complex illustration drawing | Same per `<path>` with staggered delays | Each path draws independently |
| Handwriting effect | SVG text converted to paths + stroke animation | Text "writes" itself |
| Draw then fill | Two-stage animation: stroke draw → fill opacity | Draw outlines first, color in |

## Pattern

```css
/* Basic line draw */
.draw-icon path {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  /* Measure with: path.getTotalLength() */
  stroke-dasharray: 200;
  stroke-dashoffset: 200;
  animation: draw 1.5s var(--ease-emphasized-decel) forwards;
}
@keyframes draw { to { stroke-dashoffset: 0; } }

/* Staggered multi-path */
.draw-logo path { fill: none; stroke: currentColor; stroke-width: 2; animation: draw 1s var(--ease-emphasized-decel) forwards; }
.draw-logo path:nth-child(1) { stroke-dasharray: 150; stroke-dashoffset: 150; }
.draw-logo path:nth-child(2) { stroke-dasharray: 200; stroke-dashoffset: 200; animation-delay: 0.3s; }

/* Draw then fill */
.draw-fill path {
  fill: transparent; stroke: var(--color-primary); stroke-width: 2;
  stroke-dasharray: 200; stroke-dashoffset: 200;
  animation:
    draw-stroke 1s var(--ease-emphasized-decel) forwards,
    fill-in 0.5s var(--ease-standard) 1s forwards;
}
@keyframes draw-stroke { to { stroke-dashoffset: 0; } }
@keyframes fill-in { to { fill: var(--color-primary); stroke-width: 0; } }

/* Scroll-triggered */
.draw-on-scroll path {
  stroke-dasharray: 200; stroke-dashoffset: 200;
  animation: draw 1s linear forwards;
  animation-timeline: view();
  animation-range: entry 20% entry 80%;
}
```

**Measuring path length:**
```js
// Run once to get dasharray value
document.querySelectorAll('svg path').forEach(p =>
  console.log(p.getTotalLength())
);
```

## Common Mistakes

- **Wrong `stroke-dasharray` value** — must match or exceed the path's total length; too short = partial draw
- **Forgetting `fill: none`** — SVG paths often have a fill; set to `none` during draw, then animate it in
- **Not setting `stroke-linecap: round`** — round line caps look far more natural than default `butt`
- **Using on complex filled SVGs** — line draw works best on stroked/outlined SVGs

## See Also

- [Entrance Animations](entrance-animations.md) → combine line draw with scroll triggers
- [Cinematic Effects](cinematic-effects.md) → dramatic reveal effects
- [CSS Shapes & Decorative Geometry](css-shapes.md) → decorative SVG/CSS shape techniques
