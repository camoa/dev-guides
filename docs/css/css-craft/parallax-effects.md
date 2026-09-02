---
description: Add depth with scroll parallax — perspective container technique, scroll-driven approach, scale compensation formula, mobile and accessibility handling
tldr: "Use parallax for marketing heroes, editorial pages, and portfolio pieces — one or two layers max. Use CSS perspective technique for compositor-safe zero-JS parallax; use scroll-driven for modern browsers with fine-grained control."
---

# Parallax Effects

## When to Use
Parallax creates the illusion of depth by moving foreground and background elements at different speeds during scroll. Use sparingly — one or two parallax layers on a hero section, not every card on the page. Most effective for marketing heroes, editorial pages, and portfolio pieces.

## Decision
| If you need... | Use... | Why |
|---|---|---|
| CSS-only parallax with no JS | `perspective` + `translateZ` technique | Compositor thread, zero JS, tied to scroll machinery |
| Per-element scroll-speed control | `animation-timeline: scroll()` with custom keyframes | Fine-grained control over each layer's travel distance |
| Background-only parallax | `background-attachment: fixed` | Simplest approach; avoid on iOS Safari (broken) |
| Mouse-driven depth effect | JS CSS variables + `rotateX/Y` | See [3D Transforms](3d-transforms.md) instead |
| Disable on mobile | Media query reducing `translateZ` to `0` | Mobile viewports too narrow; effect feels claustrophobic |

## Professional vs Cheap Parallax

| Quality | Speed Ratio | Number of Layers | Notes |
|---|---|---|---|
| **Professional** | 0.3–0.6x | 2-3 max | Subtle depth, not disorienting |
| **Acceptable** | 0.1–0.8x | 2-4 | Fine for hero sections |
| **Cheap/nauseating** | >1x (reverse parallax) | 5+ | Causes vestibular issues |
| **Invisible** | ~0.9x | Any | Not worth the performance cost |

## Pattern

**Perspective container technique** — elements pushed back in Z-space scroll slower because the browser applies perspective math to scroll matrices:

```css
.parallax-viewport {
  height: 100vh;
  overflow-x: hidden;
  overflow-y: scroll;
  perspective: 1px;
  perspective-origin: 0 0;
}

.parallax-section {
  position: relative;
  transform-style: preserve-3d;
}

/* Background layer — pushed back, scrolls at ~0.33x speed */
.parallax-bg {
  transform: translateZ(-2px) scale(3); /* scale = (perspective - distance) / perspective */
}

/* Foreground layer — stays at normal scroll speed */
.parallax-fg {
  transform: translateZ(0);
}
```

**Scale compensation formula:** `scale = (perspective - translateZ) / perspective`. With `perspective: 1px` and `translateZ(-2px)`: `scale = (1 - (-2)) / 1 = 3`. Without scale compensation, elements shrink as they move back in Z-space.

**Scroll-driven parallax (modern approach):**

```css
@keyframes parallax-bg {
  from { transform: translateY(0); }
  to   { transform: translateY(-30%); }
}

.hero-bg {
  animation: parallax-bg linear both;
  animation-timeline: scroll(root);
}

@supports not (animation-timeline: scroll()) {
  .hero-bg { transform: none; }
}
```

> **Feature reference:** See [modern-css → scroll-driven-animations](../modern-css/scroll-driven-animations.md) for `animation-timeline` syntax.

**Accessibility and mobile:**

```css
@media (prefers-reduced-motion: reduce) {
  .parallax-bg,
  .parallax-viewport {
    perspective: none;
    transform: none;
    animation: none;
  }
}

/* iOS Safari fix: background-attachment: fixed doesn't work */
@media (max-width: 768px) {
  .parallax-bg {
    transform: none;
    animation: none;
  }
}
```

## Common Mistakes
- Forgetting `transform-style: preserve-3d` on the section container — flattens the 3D space, killing the effect
- Any element between the perspective container and the parallax child — intermediate containers with their own transforms flatten the perspective
- `background-attachment: fixed` on iOS — does not work; use the `translateZ` technique or scroll-driven instead
- Too many parallax layers (5+) — creates visual noise and performance cost; 2-3 is the effective maximum
- Not applying scale compensation — background elements shrink as they're pushed back in Z-space, causing transparent edges
- No `prefers-reduced-motion` fallback — vestibular disorder users will feel sick; this is a WCAG 2.3.3 violation

## See Also
- [Entrance Animations](entrance-animations.md) — scroll-triggered reveals vs continuous parallax
- [Animation Performance](animation-performance.md) — why perspective-based parallax stays compositor-safe
- [Accessibility and Motion](accessibility-and-motion.md) — parallax is a primary vestibular trigger
- Reference: [Chrome: Performant Parallaxing](https://developer.chrome.com/blog/performant-parallaxing)
- Reference: [CSS-Tricks: Scroll-Driven Parallax](https://css-tricks.com/bringing-back-parallax-with-scroll-driven-css-animations/)
