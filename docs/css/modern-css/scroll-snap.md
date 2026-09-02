---
description: "Paged scrolling and carousels with CSS Scroll Snap — mandatory vs proximity, native controls in Chrome 135+"
tldr: "Use CSS Scroll Snap when you need paged scrolling, carousel behavior, or snap-to-item navigation without JavaScript. Use `scroll-snap-type: mandatory` for full-slide carousels; use `proximity` for galleries where stopping between items is…"
---

# CSS Scroll Snap

## When to Use

> When you need paged scrolling, carousel-like behavior, or snap-to-item navigation — without JavaScript. CSS Scroll Snap provides the scroll physics; Chrome 135+ adds native carousel controls with `::scroll-button` and `::scroll-marker`.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Carousel/slider with snap behavior | `scroll-snap-type: x mandatory` | Full-slide snapping, no JS |
| Gallery where user can stop between items | `scroll-snap-type: x proximity` | Snaps only when close to a snap point |
| Full-page vertical sections | `scroll-snap-type: y mandatory` | Each section fills the viewport |
| Prev/next buttons without JS | `::scroll-button(left/right)` | Chrome 135+ native controls |
| Dot indicators without JS | `::scroll-marker` | Chrome 135+ native markers |
| Active slide detection | `::scroll-marker:target-current` | Chrome 135+ active state |
| Cross-browser carousel with controls | JS for buttons, CSS for snapping | `::scroll-button` is Chromium-only |

## Pattern

```css
/* Basic horizontal carousel */
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  gap: 1rem;
  /* Hide scrollbar but keep functionality */
  scrollbar-width: none;
}
.carousel::-webkit-scrollbar { display: none; }

.carousel > .slide {
  flex: 0 0 100%;
  scroll-snap-align: center;
}

/* Multi-item carousel */
.carousel--multi > .slide {
  flex: 0 0 calc(33.333% - 0.67rem);
  scroll-snap-align: start;
}

/* Vertical full-page snap */
.fullpage {
  overflow-y: auto;
  scroll-snap-type: y mandatory;
  height: 100dvh;
}
.fullpage > section {
  height: 100dvh;
  scroll-snap-align: start;
}

/* scroll-snap-stop: always — prevent skipping slides */
.carousel > .slide {
  scroll-snap-stop: always; /* User cannot fast-scroll past */
}
```

#### Native Carousel Controls (Chrome 135+)
```css
/* Prev/next buttons */
.carousel {
  /* Enable marker group positioning */
  scroll-marker-group: after;
}

.carousel::scroll-button(left) {
  content: "‹" / "Previous slide";
}
.carousel::scroll-button(right) {
  content: "›" / "Next slide";
}

/* Dot indicators */
.carousel > .slide::scroll-marker {
  content: '';
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: oklch(70% 0 0);
  border: 2px solid transparent;
}

/* Active dot */
.carousel > .slide::scroll-marker:target-current {
  background: oklch(50% 0.2 260);
  border-color: oklch(50% 0.2 260);
}
```

#### Scroll Padding (for fixed headers)
```css
/* Account for sticky header height */
.scroll-container {
  scroll-padding-top: 80px;   /* Height of sticky header */
  scroll-padding-inline: 1rem; /* Horizontal padding */
}
```

**`mandatory` vs `proximity`:**
- `mandatory` — always snaps to nearest snap point, even mid-scroll. Use for carousels, full-page sections.
- `proximity` — only snaps when close to a snap point. Use for galleries where stopping between items is OK.

**Browser support:** Core scroll-snap: all browsers (Baseline 2021). `::scroll-button`, `::scroll-marker`, `scroll-marker-group`: Chrome 135+ only. Use scroll-snap for the snapping behavior (universal) and progressive-enhance with native controls on Chromium.

## Common Mistakes

- Forgetting `scroll-behavior: smooth` — without it, snapping is instantaneous (jarring)
- Using `scroll-snap-type: both mandatory` without careful planning — locks scroll in both axes, can trap users
- Not setting `scroll-snap-stop: always` on single-item carousels — fast swipes can skip multiple slides
- Expecting `::scroll-button` to work in Firefox/Safari — Chromium-only; provide fallback JS buttons
- Missing `scroll-padding` when page has sticky headers — snap position hides content under the header

## See Also

- [Scroll-Driven Animations](scroll-driven-animations.md) → for animating elements based on scroll position
- [Container Scroll-State Queries](container-scroll-state.md) → style the active slide via the `snapped` state
- Reference: [MDN: CSS Scroll Snap](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll_snap)
- Reference: [Chrome: Carousels with CSS](https://developer.chrome.com/blog/carousels-with-css)
