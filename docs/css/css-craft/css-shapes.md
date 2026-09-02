---
description: CSS shapes and decorative geometry — wave dividers, blobs, diagonal sections, clip-path polygons, and the shape() function
tldr: "Use `clip-path` when you need precise geometric cuts or responsive curves. Use `border-radius` with uneven values when you need animatable organic blob shapes."
---

# CSS Shapes & Decorative Geometry

## When to Use
When a client asks for blob shapes, wave dividers, organic forms, rounded section breaks, or any non-rectangular decorative element — all achievable without JavaScript or SVG imports.

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

## Pattern: Wave Section Divider
```css
/* Using clip-path with path() */
.section--wave {
  clip-path: path('M0,0 L1440,0 L1440,280 Q720,360 0,280 Z');
  /* Scale with vw for responsive */
}

/* Better: SVG approach with CSS */
.section--wave-bottom {
  position: relative;
  padding-bottom: 80px;
}
.section--wave-bottom::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 80px;
  background: var(--color-next-section);
  clip-path: ellipse(60% 100% at 50% 100%);
}
```

## Pattern: Blob Shape (Animated)
```css
.blob {
  width: 300px;
  height: 300px;
  background: var(--color-primary);
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  animation: morph 8s ease-in-out infinite;
}

@keyframes morph {
  0%   { border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }
  25%  { border-radius: 58% 42% 75% 25% / 76% 46% 54% 24%; }
  50%  { border-radius: 50% 50% 33% 67% / 55% 27% 73% 45%; }
  75%  { border-radius: 33% 67% 58% 42% / 63% 68% 32% 37%; }
  100% { border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }
}
```

## Pattern: Diagonal Section Break
```css
.section--diagonal {
  clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
  padding-bottom: 6rem; /* Extra space for the angle */
}

/* Reverse angle for alternating sections */
.section--diagonal-reverse {
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 85%);
  padding-top: 6rem;
}
```

## Pattern: shape() Function (Chrome 2025+)
```css
/* Responsive curves with percentage-based coords */
.hero-mask {
  clip-path: shape(from 0% 0%,
    line to 100% 0%,
    line to 100% 80%,
    curve to 50% 100% with 75% 90%,
    curve to 0% 80% with 25% 90%,
    close
  );
}
```

## Pattern: Animated Shape Morph on Hover
```css
.morph-card {
  clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
  transition: clip-path 0.6s var(--ease-emphasized-decel);
}

.morph-card:hover {
  clip-path: polygon(5% 5%, 95% 0, 100% 95%, 0 100%);
}
```

## Tools
- [Blobmaker.app](https://www.blobmaker.app/) — generate blob border-radius values
- [Fancy Border Radius](https://9elements.github.io/fancy-border-radius/) — 8-value border-radius generator
- [Clippy](https://bennettfeely.com/clippy/) — visual clip-path polygon editor
- [CSS shape() editor](https://css-shape.com/) — the new shape() function builder

## Common Mistakes
- **Using SVG when clip-path suffices** — clip-path is more performant and CSS-native
- **Forgetting padding** on diagonally clipped sections — clipped content is invisible but still occupies space
- **Animating between different point counts** — clip-path polygon transitions require the same number of points
- **Fixed pixel values in clip-path** — use percentages for responsive shapes

## See Also
- [Clip-Path and Masks](clip-path-and-masks.md) → reveals, iris animations, comparison sliders
- [Glassmorphism](glassmorphism-and-frosted-glass.md) → frosted glass on shaped elements
- [Gradient Craft](gradient-craft.md) → gradient fills inside shaped elements
