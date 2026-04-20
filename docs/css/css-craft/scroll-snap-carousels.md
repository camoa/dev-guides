---
description: CSS scroll-snap carousel patterns — full-width, multi-item, fade effect, CSS-only controls (Chrome 135+), and cross-browser fallbacks
tldr: "Use CSS scroll-snap when you need a carousel, image gallery, slider, or paginated scrolling experience with native browser physics. Use JavaScript carousel libraries when you need infinite looping — CSS scroll-snap does not support it…"
drupal_version: "11.x"
---

# Scroll-Snap Carousels

## When to Use

> Use CSS scroll-snap when you need a carousel, image gallery, slider, or paginated scrolling experience with native browser physics. Use JavaScript carousel libraries when you need infinite looping — CSS scroll-snap does not support it natively.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Full-width hero carousel | Horizontal snap + `flex: 0 0 100%` | Each slide fills the container |
| Multi-item card carousel | Horizontal snap + `flex: 0 0 calc(33.333% - gap)` | Shows 3 items, snaps to first |
| Image gallery with thumbnails | Two synced snap containers | Thumbnail carousel drives main |
| Vertical section scroller | `scroll-snap-type: y mandatory` + `height: 100dvh` | Full-page vertical sections |
| Comparison slider (before/after) | `clip-path` + CSS variable + input range | See [Clip-Path and Masks](clip-path-and-masks.md) |
| Infinite loop carousel | JavaScript | CSS scroll-snap doesn't loop |

## Pattern

### Full-Width Carousel
```css
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  scrollbar-width: none;
}
.carousel::-webkit-scrollbar { display: none; }

.carousel__slide {
  flex: 0 0 100%;
  scroll-snap-align: center;
  scroll-snap-stop: always; /* Prevent skipping */
}
```

### Multi-Item Carousel with Responsive Peek
```css
.carousel--multi {
  display: flex;
  gap: var(--space-4, 1rem);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  scroll-padding-inline: var(--space-4, 1rem);
  padding-inline: var(--space-4, 1rem);
  scrollbar-width: none;
}

.carousel--multi__item {
  flex: 0 0 calc(33.333% - 0.67rem);
  scroll-snap-align: start;
}

@media (width < 640px) {
  .carousel--multi__item { flex: 0 0 85%; }
}
@media (640px <= width < 1024px) {
  .carousel--multi__item { flex: 0 0 calc(50% - 0.5rem); }
}
```

### Fade Effect on Non-Active Slides (scroll-driven)
```css
.carousel__slide {
  animation: snap-fade linear;
  animation-timeline: view(inline);
  animation-range: entry 0% entry 100%;
}

@keyframes snap-fade {
  0% { opacity: 0.4; transform: scale(0.92); }
  50% { opacity: 1; transform: scale(1); }
  100% { opacity: 0.4; transform: scale(0.92); }
}
```

### CSS-Only Prev/Next Controls (Chrome 135+)
```css
.carousel { scroll-marker-group: after; }

.carousel::scroll-button(left),
.carousel::scroll-button(right) {
  position: absolute;
  top: 50%;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: oklch(100% 0 0 / 0.9);
  box-shadow: 0 2px 8px oklch(0% 0 0 / 0.15);
  cursor: pointer;
  transition: opacity var(--duration-fast) var(--ease-standard);
}

.carousel::scroll-button(left) { content: "‹" / "Previous"; left: var(--space-2); }
.carousel::scroll-button(right) { content: "›" / "Next"; right: var(--space-2); }

.carousel::scroll-button(left):disabled,
.carousel::scroll-button(right):disabled { opacity: 0; pointer-events: none; }

.carousel__slide::scroll-marker {
  content: '';
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: oklch(80% 0 0);
}

.carousel__slide::scroll-marker:target-current {
  background: oklch(50% 0.2 260);
  width: 24px;
  border-radius: 5px;
}
```

### Cross-Browser Fallback Controls
```html
<div class="carousel-wrapper">
  <button class="carousel-btn carousel-btn--prev" aria-label="Previous">‹</button>
  <div class="carousel" role="region" aria-label="Featured content" tabindex="0">
    <div class="carousel__slide" role="group" aria-label="1 of 5">...</div>
    <div class="carousel__slide" role="group" aria-label="2 of 5">...</div>
  </div>
  <button class="carousel-btn carousel-btn--next" aria-label="Next">›</button>
</div>
```
```js
const carousel = document.querySelector('.carousel');
const slideWidth = carousel.querySelector('.carousel__slide').offsetWidth;

document.querySelector('.carousel-btn--next')
  .addEventListener('click', () => carousel.scrollBy({ left: slideWidth, behavior: 'smooth' }));
document.querySelector('.carousel-btn--prev')
  .addEventListener('click', () => carousel.scrollBy({ left: -slideWidth, behavior: 'smooth' }));
```

## Accessibility Checklist

- `role="region"` + `aria-label` on carousel container
- `role="group"` + `aria-label="N of M"` on each slide
- `tabindex="0"` on carousel for keyboard scrolling
- `aria-label` on prev/next buttons
- `prefers-reduced-motion`: disable scroll-driven fade animations
- Ensure content is accessible without JavaScript

## Common Mistakes

- **Missing `scroll-snap-stop: always`** on full-width carousels → fast swipes skip multiple slides
- **No `scroll-padding`** when there's a sticky header → slides snap under the header
- **Using `scroll-snap-type: both mandatory`** → locks both axes, can trap keyboard users
- **Not hiding the scrollbar** → always use `scrollbar-width: none` + `::-webkit-scrollbar { display: none }`
- **No reduced motion fallback** → disable scroll-driven fade animations with `prefers-reduced-motion: reduce`

## See Also

- [Entrance Animations](entrance-animations.md) — scroll-triggered reveals complement carousel scroll
- [Micro-Interactions](micro-interactions.md) — hover effects for carousel items
- [Accessibility and Motion](accessibility-and-motion.md) — motion preferences
- Reference: [CSS Scroll Snap — Modern CSS](../modern-css/scroll-snap.md)
