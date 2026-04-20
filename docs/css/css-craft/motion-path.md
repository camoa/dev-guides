---
description: Motion path animations — orbit, curve-following, scroll-driven path, and staggered multi-element paths with offset-path
tldr: "Use `offset-path` when a client wants an element to animate along a curve, orbit, or custom path — loading animations, decorative elements, flight paths. No JavaScript needed."
---

# Motion Path

## When to Use

> Use `offset-path` when a client wants an element to animate along a curve, orbit, or custom path — loading animations, decorative elements, flight paths. No JavaScript needed.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| Element orbiting in a circle | `offset-path: circle()` | Perfect circular motion |
| Element following a curved line | `offset-path: path('M...')` | SVG path syntax, arbitrary curves |
| Element moving along a ray | `offset-path: ray(45deg)` | Directional movement |
| Scroll-triggered path animation | `offset-path` + `animation-timeline: scroll()` | Path progress tied to scroll |
| Logo/icon along a decorative curve | `offset-path` + `offset-rotate` | Element rotates to follow path tangent |

## Pattern

```css
/* Circular orbit */
.orbiting-dot {
  offset-path: circle(120px at center);
  offset-rotate: 0deg; /* Stay upright */
  animation: orbit 4s linear infinite;
}
@keyframes orbit {
  to { offset-distance: 100%; }
}

/* Custom curve path */
.along-curve {
  offset-path: path('M 0,300 Q 150,0 300,300 Q 450,600 600,300');
  offset-rotate: auto; /* Rotate to follow tangent */
  animation: follow-path 3s ease-in-out infinite alternate;
}
@keyframes follow-path {
  from { offset-distance: 0%; }
  to   { offset-distance: 100%; }
}

/* Scroll-driven path */
.scroll-along-path {
  offset-path: path('M 10,80 Q 200,10 390,80 T 770,80');
  animation: trace-path linear;
  animation-timeline: scroll();
}
@keyframes trace-path {
  from { offset-distance: 0%; }
  to   { offset-distance: 100%; }
}

/* Staggered orbit group */
.path-group > * {
  offset-path: circle(100px at center);
  animation: orbit 6s linear infinite;
}
.path-group > :nth-child(2) { animation-delay: -2s; }
.path-group > :nth-child(3) { animation-delay: -4s; }
```

## Common Mistakes

- **Forgetting `offset-rotate`** — default is `auto` which rotates the element; set `0deg` for upright elements
- **Using pixel-based paths that don't scale** — use percentage-based shapes or viewBox-relative SVG paths
- **Not using `will-change: offset-distance`** for heavy animations — hints the browser for compositor optimization

## See Also

- [Parallax Effects](parallax-effects.md) → scroll-driven motion without paths
- [Entrance Animations](entrance-animations.md) → simpler scroll-triggered reveals
- [Animation Performance](animation-performance.md) → offset-distance is compositor-safe
- Reference: [MDN: offset-path](https://developer.mozilla.org/en-US/docs/Web/CSS/offset-path)
