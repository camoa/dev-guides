---
description: Shape, reveal, and animate elements with clip-path — wipe reveals, diagonal sections, iris animations, mask-image soft edges, comparison sliders
tldr: "Use `clip-path` for shaped containers, animated reveals (wipes, sweeps, iris), comparison sliders, and creative transitions. It is compositor-accelerated and produces no layout shifts."
---

# Clip-Path and Masks

## When to Use
`clip-path` hides portions of elements without affecting layout — the clipped area is invisible but still occupies space. Use it for shaped containers, animated reveals, comparison sliders, and creative transitions. Unlike `overflow: hidden`, clip-path is compositor-accelerated and produces no layout shifts during animation.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Animate a reveal (wipe, sweep, iris) | `clip-path` from hidden to visible state | Compositor-only, smooth 60fps |
| Reveal content on scroll | `clip-path` + IntersectionObserver class toggle | Cleaner than opacity-fade for directional reveals |
| Diagonal or angled section break | `clip-path: polygon()` on the section | No extra pseudo-elements needed |
| Complex SVG shape mask | `clip-path: url(#svg-clippath)` | Arbitrary shapes, curves, text masks |
| Shadow on a clipped shape | `filter: drop-shadow()` on the parent | `box-shadow` is clipped; `drop-shadow` follows the shape |
| Fade content at an edge | `mask-image` with gradient | Clip-path creates hard edges; mask creates soft ones |

## Animation Rules for clip-path
- You can animate between `polygon()` values — but they must have the **same number of points**. A triangle cannot animate to a rectangle without adding a co-located extra point.
- You can animate `inset()` to `inset()` freely (different values, same type).
- You cannot animate between shape types (e.g., `circle()` to `polygon()`).
- CSS 2025: the `shape()` function enables curves with fewer workarounds, but animating to/from `shape()` still requires matching point counts.

## Pattern

**Wipe reveal on scroll:**

```css
.reveal-wipe {
  clip-path: inset(0 100% 0 0); /* Fully hidden — right edge covers all */
  transition: clip-path var(--duration-slow) var(--ease-emphasized-decel);
}

.reveal-wipe.is-visible {
  clip-path: inset(0 0% 0 0); /* Fully revealed */
}
```

**Diagonal section break:**

```css
.diagonal-section {
  clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
  /* Top: flat. Bottom: angled down-right */
}
```

**Animated iris reveal (circle expand):**

```css
@keyframes iris-open {
  from { clip-path: circle(0% at 50% 50%); }
  to   { clip-path: circle(150% at 50% 50%); }
}

.iris-reveal {
  animation: iris-open var(--duration-slow) var(--ease-emphasized-decel) both;
}
```

**Mask-image for soft edge fade:**

```css
.fade-bottom {
  mask-image: linear-gradient(
    to bottom,
    black 0%,
    black 70%,
    transparent 100%
  );
}

/* Horizontal fade — useful for scrolling carousels */
.fade-sides {
  mask-image: linear-gradient(
    to right,
    transparent 0%,
    black 10%,
    black 90%,
    transparent 100%
  );
}
```

**Clip-path comparison slider:**

```css
.comparison {
  position: relative;
  --divider: 50%; /* Controlled by JS */
}

.comparison .before {
  position: absolute;
  inset: 0;
  clip-path: inset(0 calc(100% - var(--divider)) 0 0);
}
```

```javascript
slider.addEventListener('input', (e) => {
  comparison.style.setProperty('--divider', `${e.target.value}%`);
});
```

## Common Mistakes
- Animating between different point-count polygons — browser cannot interpolate; the shape snaps
- Expecting `box-shadow` to appear on clipped elements — use `filter: drop-shadow()` on a wrapper instead
- Using `clip-path` for layout-affecting shapes — clip-path hides content but it still occupies its original space; use `shape-outside` for text wrapping
- Forgetting the overflow behavior — elements outside the clip region are hidden but still receive pointer events unless you also set `pointer-events: none`

## See Also
- [Entrance Animations](entrance-animations.md) — clip-path reveals as alternatives to opacity fades
- [Animation Performance](animation-performance.md) — `clip-path` is compositor-only
- [Blend Modes and Visual Effects](blend-modes-and-visual-effects.md) — combining clip with blend for creative effects
- Reference: [Emil Kowalski: The Magic of Clip-Path](https://emilkowal.ski/ui/the-magic-of-clip-path)
- Reference: [CSS-Tricks: Animating with Clip-Path](https://css-tricks.com/animating-with-clip-path/)
- Reference: [Sara Soueidan: CSS and SVG Clipping](https://www.sarasoueidan.com/blog/css-svg-clipping/)
