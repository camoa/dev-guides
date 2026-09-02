---
description: SVG line draw animations — stroke-dashoffset technique, staggered multi-path draw, draw-then-fill, and scroll-triggered drawing
tldr: "Use `stroke-dasharray` + `stroke-dashoffset` animation when a client wants icons, logos, or illustrations that draw themselves. Pure CSS on SVG strokes — no JavaScript needed."
---

# SVG Line Draw

## When to Use
When a client wants an icon, logo, or illustration that draws itself — lines appearing progressively as if being drawn by hand. Pure CSS animation on SVG `stroke` properties.

## Decision
| Client asks for... | Use... | Why |
|---|---|---|
| Icon that draws itself on load | `stroke-dasharray` + `stroke-dashoffset` animation | Pure CSS, no JS |
| Logo that draws on scroll | Same + `animation-timeline: view()` | Scroll-triggered draw |
| Complex illustration drawing | Same technique per `<path>` with staggered delays | Each path draws independently |
| Handwriting effect | SVG text converted to paths + stroke animation | Text "writes" itself |
| Draw then fill | Two-stage animation: stroke draw → fill opacity | Draw outlines first, color in |

## Pattern: Basic Line Draw
```css
.draw-icon path {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  /* Total path length — measure with JS: path.getTotalLength() */
  stroke-dasharray: 200;
  stroke-dashoffset: 200;
  animation: draw 1.5s var(--ease-emphasized-decel) forwards;
}

@keyframes draw {
  to { stroke-dashoffset: 0; }
}
```

## Pattern: Staggered Multi-Path Draw
```css
.draw-logo path:nth-child(1) { stroke-dasharray: 150; stroke-dashoffset: 150; animation-delay: 0s; }
.draw-logo path:nth-child(2) { stroke-dasharray: 200; stroke-dashoffset: 200; animation-delay: 0.3s; }
.draw-logo path:nth-child(3) { stroke-dasharray: 180; stroke-dashoffset: 180; animation-delay: 0.6s; }

.draw-logo path {
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  animation: draw 1s var(--ease-emphasized-decel) forwards;
}
```

## Pattern: Draw Then Fill
```css
.draw-fill path {
  fill: transparent;
  stroke: var(--color-primary);
  stroke-width: 2;
  stroke-dasharray: 200;
  stroke-dashoffset: 200;
  animation:
    draw-stroke 1s var(--ease-emphasized-decel) forwards,
    fill-in 0.5s var(--ease-standard) 1s forwards;
}

@keyframes draw-stroke {
  to { stroke-dashoffset: 0; }
}

@keyframes fill-in {
  to { fill: var(--color-primary); stroke-width: 0; }
}
```

## Pattern: Scroll-Triggered Draw
```css
.draw-on-scroll path {
  stroke-dasharray: 200;
  stroke-dashoffset: 200;
  animation: draw 1s linear forwards;
  animation-timeline: view();
  animation-range: entry 20% entry 80%;
}
```

## Measuring Path Length
```js
// Run once to get dasharray value
document.querySelectorAll('svg path').forEach(path => {
  console.log(path.getTotalLength()); // Use this value for stroke-dasharray
});
```

**Browser support:** SVG stroke animation: all browsers. Production-ready since ~2016.

## Common Mistakes
- **Wrong `stroke-dasharray` value** — must match or exceed the path's total length; too short = partial draw
- **Forgetting `fill: none`** — SVG paths often have a fill; set to `none` during draw, then animate fill in
- **Using on complex filled SVGs** — line draw works best on outlined/stroked SVGs; filled SVGs need the two-stage draw-then-fill pattern
- **Not setting `stroke-linecap: round`** — round line caps look much more natural than default `butt`

## See Also
- [Entrance Animations](entrance-animations.md) → combine line draw with scroll triggers
- [Cinematic Effects](cinematic-effects.md) → dramatic reveal effects
- [CSS Shapes](css-shapes.md) → decorative SVG/CSS shape techniques
