---
description: "Scroll-linked animations without JS — progress bars, reveal on scroll, parallax"
tldr: "Use scroll-driven animations for scroll-linked effects — progress bars, reveal-on-scroll, parallax — without JavaScript. Use `@supports` for progressive enhancement and always treat effects as decorative."
---

# Scroll-Driven Animations

## When to Use

> For scroll-linked effects — progress bars, reveal-on-scroll, parallax — without JavaScript IntersectionObserver or scroll event listeners. Runs on the compositor thread; no main thread JS cost.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Progress bar that fills as user scrolls the page | `animation-timeline: scroll(root)` | Tracks root scrollbar position |
| Element reveals as it enters the viewport | `animation-timeline: view()` with `animation-range` | Tracks element's intersection with scroller |
| Named scroll container (not root) | `scroll-timeline-name: --my-scroll` | Attach to a specific scrollable ancestor |
| Complex scroll behavior with branching logic | JavaScript + IntersectionObserver | Scroll-driven animations handle linear mappings only |
| Replace IntersectionObserver for simple fade-in | `animation-timeline: view()` | No JS, composited, accessible |

## Pattern

Reading progress bar:
```css
@keyframes grow { from { width: 0% } to { width: 100% } }

.progress-bar {
  animation: grow linear;
  animation-timeline: scroll(root);
  /* No animation-duration needed — scroll position drives it */
}
```

Reveal on scroll — element fades in as it enters the viewport:
```css
@keyframes reveal {
  from { opacity: 0; translate: 0 2rem; }
  to   { opacity: 1; translate: none; }
}

.card {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 40%; /* animate while entering */
}
```

Named scroll container (for non-root scrollers):
```css
.scroll-container {
  overflow-y: auto;
  scroll-timeline: --my-scroll block;
}

.sticky-header {
  animation: shrink linear;
  animation-timeline: --my-timeline;
}
```

**`animation-timeline` values:**
| Value | Tracks |
|---|---|
| `scroll()` | Nearest scrollable ancestor |
| `scroll(root)` | Document scroll position |
| `scroll(self)` | The element's own scroll |
| `view()` | Element's visibility in its scroll container |

**`animation-range` with `view()`:** `entry` = entering scroller edge, `exit` = leaving, `contain` = fully inside, `cover` = any overlap.

**Browser support:** Chrome 115. Firefox behind flag (not production-ready as of early 2026). Safari 26 (2025). **Use with `@supports` progressive enhancement** — the effect should be decorative, not essential.

```css
@supports (animation-timeline: scroll()) {
  .progress-bar { animation: grow linear; animation-timeline: scroll(root); }
}
```

## Common Mistakes

- Relying on scroll-driven animations in Firefox without a flag — the feature is not enabled by default; always provide a non-animated fallback
- Setting `animation-duration` — it is ignored when `animation-timeline` is set to a scroll or view timeline; remove it or set it to `auto`
- Overusing scroll animation for content that must be read — assistive technologies and users with `prefers-reduced-motion` need accessible fallbacks; always respect this preference
- Using `animation-range` percentages without understanding they are container-relative, not scroll-position-relative

## See Also

- [@starting-style Transitions](starting-style-transitions.md) → for animating elements entering the DOM
- [View Transitions](view-transitions.md) → for animating between page states
- Reference: [MDN Scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations)
