---
description: Paged scrolling and carousels with CSS Scroll Snap — mandatory vs proximity, native controls in Chrome 135+
drupal_version: "11.x"
---

# CSS Scroll Snap

## When to Use

> Use CSS Scroll Snap when you need paged scrolling, carousel behavior, or snap-to-item navigation without JavaScript. Use `scroll-snap-type: mandatory` for full-slide carousels; use `proximity` for galleries where stopping between items is acceptable. Use JavaScript buttons for prev/next controls — `::scroll-button` is Chromium 135+ only.

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

/* Prevent skipping slides on fast swipe */
.carousel > .slide {
  scroll-snap-stop: always;
}
```

#### Native Carousel Controls (Chrome 135+)

```css
.carousel {
  scroll-marker-group: after;
}

.carousel::scroll-button(left) { content: "‹" / "Previous slide"; }
.carousel::scroll-button(right) { content: "›" / "Next slide"; }

.carousel > .slide::scroll-marker {
  content: '';
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: oklch(70% 0 0);
}

.carousel > .slide::scroll-marker:target-current {
  background: oklch(50% 0.2 260);
}
```

#### Scroll Padding (for fixed headers)

```css
.scroll-container {
  scroll-padding-top: 80px;
  scroll-padding-inline: 1rem;
}
```

`mandatory` always snaps to the nearest snap point. `proximity` only snaps when close to one — use for galleries where stopping between items is OK.

**Browser support:** Core scroll-snap: all browsers (Baseline 2021). `::scroll-button`, `::scroll-marker`, `scroll-marker-group`: Chrome 135+ only.

## Common Mistakes

- **Wrong**: No `scroll-behavior: smooth` → **Right**: Without it, snapping is instantaneous and jarring
- **Wrong**: `scroll-snap-type: both mandatory` without care → **Right**: Locks scroll in both axes, can trap users
- **Wrong**: No `scroll-snap-stop: always` on single-item carousels → **Right**: Fast swipes can skip multiple slides
- **Wrong**: Using `::scroll-button` expecting Firefox/Safari support → **Right**: Chromium-only; provide fallback JS buttons
- **Wrong**: No `scroll-padding` with sticky headers → **Right**: Snap position hides content under the header

## See Also

- [Scroll-Driven Animations](scroll-driven-animations.md) — animate elements based on scroll position
- [Container Scroll-State Queries](container-scroll-state.md) — style active slide via `snapped` state
- Reference: [MDN: CSS Scroll Snap](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll_snap)
- Reference: [Chrome: Carousels with CSS](https://developer.chrome.com/blog/carousels-with-css)
