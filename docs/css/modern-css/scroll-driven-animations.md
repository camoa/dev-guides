---
description: Scroll-linked animations without JS — progress bars, reveal on scroll, parallax
---

# Scroll-Driven Animations

## When to Use

> Use scroll-driven animations for scroll-linked effects — progress bars, reveal-on-scroll, parallax — without JavaScript. Use `@supports` for progressive enhancement and always treat effects as decorative.

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

Always wrap in `@supports` — Firefox does not have production support as of early 2026:

```css
@supports (animation-timeline: scroll()) {
  .progress-bar { animation: grow linear; animation-timeline: scroll(root); }
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

**Browser support:** Chrome 115. Firefox behind flag (not production-ready as of early 2026). Safari 26 (2025). Use `@supports` progressive enhancement.

## Common Mistakes

- **Wrong**: Relying on scroll-driven animations in Firefox without a flag → **Right**: The feature is not enabled by default; always provide a non-animated fallback
- **Wrong**: Setting `animation-duration` → **Right**: Duration is ignored when `animation-timeline` is a scroll or view timeline; remove it or set it to `auto`
- **Wrong**: Using scroll animation for content that must be read → **Right**: Always respect `prefers-reduced-motion`; the effect should be decorative, not essential
- **Wrong**: Treating `animation-range` percentages as scroll-position-relative → **Right**: They are container-relative, not viewport-scroll-position-relative

## See Also

- [@starting-style & Discrete Transitions](starting-style-transitions.md)
- [View Transitions](view-transitions.md)
- Reference: [MDN Scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations)
