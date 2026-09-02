---
description: Card flips, perspective tilt, and 3D hover effects — perspective values guide, preserve-3d setup, mouse-tracked tilt with CSS variables
tldr: "Use CSS 3D transforms for interactive components that benefit from a spatial metaphor: flip cards, showcase elements, hover-responsive cards. Do not apply to body copy, long lists, or navigation."
---

# 3D Transforms

## When to Use
CSS 3D transforms add genuine depth to interfaces — card flips reveal hidden content, perspective tilt makes elements respond to the user's mouse, layered Z-depth creates tactile product card feels. Use for interactive components that benefit from spatial metaphor: flip cards, showcase elements, hover-responsive cards. Do not apply to body copy, long lists, or navigation.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Card that flips to reveal back face | `transform-style: preserve-3d` + `rotateY(180deg)` | The classic implementation; back face hidden until rotated |
| Perspective tilt following mouse | JS writes `--rotate-x`/`--rotate-y` CSS variables | Clean separation — CSS handles all rendering, JS only does math |
| Element that appears to lean back | `perspective` on parent + `rotateX()` on child | No JS needed for static depth feel |
| Depth layering (floating layers effect) | Multiple `translateZ()` values within preserve-3d | Each layer sits at a different Z position |
| Disable 3D on reduced motion | Remove `transform-style: preserve-3d`, set transforms to `none` | Respects vestibular sensitivity |

## Perspective Values Guide

| Value | Effect | Use For |
|---|---|---|
| `400-600px` | Dramatic, close viewpoint | Emphasis, small components |
| `800-1200px` | Natural, moderate depth | Cards, standard UI elements |
| `1500-2000px` | Subtle, distant viewpoint | Full-page layout effects |
| `none` | No perspective (flat) | Default; removes all 3D |

## Pattern

**Classic card flip:**

```css
.flip-card {
  perspective: 1000px;
}

.flip-card__inner {
  position: relative;
  transform-style: preserve-3d;
  transition: transform var(--duration-slow) var(--ease-standard);
}

.flip-card:hover .flip-card__inner {
  transform: rotateY(180deg);
}

.flip-card__front,
.flip-card__back {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
}

.flip-card__back {
  transform: rotateY(180deg);
}
```

**Mouse-tracked 3D tilt** — JS writes to CSS variables, CSS handles all transforms:

```css
.tilt-card {
  --rotate-x: 0deg;
  --rotate-y: 0deg;
  --shine-x: 50%;
  --shine-y: 50%;

  transform: perspective(800px) rotateX(var(--rotate-x)) rotateY(var(--rotate-y)) scale3d(1.02, 1.02, 1.02);
  transition: transform var(--duration-fast) var(--ease-standard);
}

/* Shine layer follows mouse position */
.tilt-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    circle at var(--shine-x) var(--shine-y),
    hsl(0 0% 100% / 0.15) 0%,
    transparent 60%
  );
  border-radius: inherit;
  pointer-events: none;
}
```

```javascript
document.querySelectorAll('.tilt-card').forEach((card) => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;  // 0-1
    const y = (e.clientY - rect.top) / rect.height;  // 0-1
    const maxTilt = 10; // degrees

    card.style.setProperty('--rotate-x', `${(y - 0.5) * -maxTilt}deg`);
    card.style.setProperty('--rotate-y', `${(x - 0.5) * maxTilt}deg`);
    card.style.setProperty('--shine-x', `${x * 100}%`);
    card.style.setProperty('--shine-y', `${y * 100}%`);
  });

  card.addEventListener('mouseleave', () => {
    card.style.setProperty('--rotate-x', '0deg');
    card.style.setProperty('--rotate-y', '0deg');
  });
});
```

**Accessibility:**

```css
@media (prefers-reduced-motion: reduce) {
  .flip-card__inner {
    transform: none !important;
    transition: none;
  }

  .flip-card__back {
    display: none;
  }

  .flip-card:hover .flip-card__back {
    display: block;
    transform: none;
    backface-visibility: visible;
  }
}
```

## Common Mistakes
- Not setting `backface-visibility: hidden` on both faces — the back card face shows through the front during the flip
- Applying `perspective` to the card itself instead of its parent — perspective must be on an ancestor; placing it on the transforming element produces a different (less realistic) effect
- Missing `transform-style: preserve-3d` on the inner wrapper — without it, child elements are flattened into 2D
- Setting max tilt above 15-20 degrees for mouse tracking — goes from "cool tilt" to "broken UI" quickly; 8-12 degrees is the sweet spot
- No mouse-leave reset — card stays tilted after the cursor leaves, looks broken

## See Also
- [Micro-Interactions](micro-interactions.md) — 2D hover effects for elements that don't need full 3D
- [Parallax Effects](parallax-effects.md) — perspective-based scroll depth vs interactive 3D
- [Accessibility and Motion](accessibility-and-motion.md) — `prefers-reduced-motion` for 3D effects
- Reference: [Polypane: CSS 3D Transform Examples](https://polypane.app/css-3d-transform-examples/)
- Reference: [David DeSandro: Intro to CSS 3D Transforms](https://3dtransforms.desandro.com/card-flip)
