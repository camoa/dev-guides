---
description: CSS shapes and decorative geometry — wave dividers, blobs, diagonal sections, clip-path polygons, and the shape() function
tldr: "Use `clip-path` when you need precise geometric cuts or responsive curves. Use `border-radius` with uneven values when you need animatable organic blob shapes."
---

# CSS Shapes & Decorative Geometry

## When to Use

> Use `clip-path` when you need precise geometric cuts or responsive curves. Use `border-radius` with uneven values when you need animatable organic blob shapes.

## Decision

| Client asks for... | Use... | Why |
|---|---|---|
| Wave section divider | `clip-path: path()` or SVG in `clip-path: url()` | Smooth curves, responsive |
| Blob/organic background shape | `border-radius` with uneven values | Simpler than clip-path, animatable |
| Diagonal section break | `clip-path: polygon()` | Sharp angled cuts |
| Circle or ellipse element | `clip-path: circle()` / `ellipse()` | Perfect geometric shapes |
| Curved section overlap | `clip-path: ellipse()` on pseudo-element | Section flows into next |
| Responsive complex shape | `shape()` function (Chrome 2025+) | Percentage-based coordinates |
| Animated morphing shape | `clip-path` polygon with same point count | Transitions between shapes |
| Decorative floating blobs | `border-radius` + `animation` | Organic, animated backgrounds |

## Pattern

```css
/* Wave section divider */
.section--wave-bottom::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0;
  width: 100%; height: 80px;
  background: var(--color-next-section);
  clip-path: ellipse(60% 100% at 50% 100%);
}

/* Animated blob */
.blob {
  width: 300px; height: 300px;
  background: var(--color-primary);
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  animation: morph 8s ease-in-out infinite;
}
@keyframes morph {
  0%   { border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }
  50%  { border-radius: 50% 50% 33% 67% / 55% 27% 73% 45%; }
  100% { border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }
}

/* Diagonal section */
.section--diagonal {
  clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
  padding-bottom: 6rem;
}

/* shape() function — Chrome 2025+ */
.hero-mask {
  clip-path: shape(from 0% 0%,
    line to 100% 0%, line to 100% 80%,
    curve to 50% 100% with 75% 90%,
    curve to 0% 80% with 25% 90%, close
  );
}
```

## Common Mistakes

- **Using SVG when clip-path suffices** — clip-path is more performant and CSS-native
- **Forgetting padding** on clipped sections — clipped content is invisible but still occupies space
- **Animating between different point counts** — `clip-path` polygon transitions require the same number of points
- **Fixed pixel values in clip-path** — use percentages for responsive shapes

## See Also

- [Clip-Path and Masks](clip-path-and-masks.md) → reveals, iris animations, comparison sliders
- [Glassmorphism and Frosted Glass](glassmorphism-and-frosted-glass.md) → frosted glass on shaped elements
- [Gradient Craft](gradient-craft.md) → gradient fills inside shaped elements
- Tools: [Blobmaker.app](https://www.blobmaker.app/), [Clippy](https://bennettfeely.com/clippy/), [CSS shape() editor](https://css-shape.com/)
