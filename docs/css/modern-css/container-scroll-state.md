---
description: "Style elements based on scroll container state — stuck, snapped, or scrollable — without JavaScript"
tldr: "Use `@container scroll-state()` when you need to style elements based on whether their scroll container is stuck, snapped, or scrollable. Use `IntersectionObserver` when cross-browser support is required — scroll-state queries are Chrome…"
---

# Container Scroll-State Queries

## When to Use

> When you need to style elements based on their scroll container's state — whether an element is stuck (via `position: sticky`), snapped (via `scroll-snap`), or scrollable.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Add shadow to sticky header when stuck | `@container scroll-state(stuck: top)` | Pure CSS stuck detection |
| Style active carousel slide | `@container scroll-state(snapped: x)` | No IntersectionObserver needed |
| Show scroll indicators when content overflows | `@container scroll-state(scrollable: top)` | Detect scroll position |
| Cross-browser stuck detection | IntersectionObserver with threshold | Scroll-state queries are Chromium-only |

## Pattern

```css
/* Sticky header with shadow when stuck */
.header-wrapper {
  container-type: scroll-state;
  position: sticky;
  top: 0;
}

@container scroll-state(stuck: top) {
  .header {
    box-shadow: 0 2px 8px oklch(0% 0 0 / 0.15);
    border-bottom: 1px solid oklch(90% 0 0);
  }
}

/* Active carousel slide styling */
.carousel {
  container-type: scroll-state;
  scroll-snap-type: x mandatory;
}

@container scroll-state(snapped: x) {
  .slide {
    opacity: 1;
    transform: scale(1);
  }
}

/* Non-snapped slides dimmed */
.slide {
  opacity: 0.6;
  transform: scale(0.95);
  transition: opacity 0.3s, transform 0.3s;
}

/* Scroll shadow indicators */
.scrollable-container {
  container-type: scroll-state;
}

@container scroll-state(scrollable: bottom) {
  .scroll-indicator-bottom { opacity: 1; }
}

@container not scroll-state(scrollable: bottom) {
  .scroll-indicator-bottom { opacity: 0; }
}
```

**Browser support:** Chrome 133+, Edge 133+. **Not supported** in Firefox or Safari. Very new — use as progressive enhancement with sensible defaults.

## Common Mistakes

- Forgetting `container-type: scroll-state` — without declaring the container type, queries won't match
- Confusing with regular container size queries — `container-type: scroll-state` is separate from `container-type: inline-size`; you can combine them: `container-type: inline-size scroll-state`
- Expecting it to detect scroll position (percentage) — scroll-state only detects binary states (stuck/not stuck, snapped/not snapped, scrollable/not scrollable)

## See Also

- [Container Queries](container-queries.md) → for size-based container queries
- [CSS Scroll Snap](scroll-snap.md) → works with `snapped` state queries
- Reference: [Chrome: Scroll-State Container Queries](https://developer.chrome.com/docs/css-ui/scroll-state-queries)
