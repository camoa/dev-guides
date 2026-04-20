---
description: Style elements based on scroll container state — stuck, snapped, or scrollable — without JavaScript
tldr: "Use `@container scroll-state()` when you need to style elements based on whether their scroll container is stuck, snapped, or scrollable. Use `IntersectionObserver` when cross-browser support is required — scroll-state queries are Chrome…"
drupal_version: "11.x"
---

# Container Scroll-State Queries

## When to Use

> Use `@container scroll-state()` when you need to style elements based on whether their scroll container is stuck, snapped, or scrollable. Use `IntersectionObserver` when cross-browser support is required — scroll-state queries are Chrome 133+ only.

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

.slide {
  opacity: 0.6;
  transform: scale(0.95);
  transition: opacity 0.3s, transform 0.3s;
}

@container scroll-state(snapped: x) {
  .slide {
    opacity: 1;
    transform: scale(1);
  }
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

**Browser support:** Chrome 133+, Edge 133+. Not supported in Firefox or Safari. Use as progressive enhancement with sensible defaults.

## Common Mistakes

- **Wrong**: Omitting `container-type: scroll-state` → **Right**: Without declaring the container type, queries won't match
- **Wrong**: Confusing with size container queries → **Right**: `container-type: scroll-state` is separate from `container-type: inline-size`; you can combine: `container-type: inline-size scroll-state`
- **Wrong**: Expecting scroll position percentage detection → **Right**: Scroll-state only detects binary states (stuck/not stuck, snapped/not snapped, scrollable/not scrollable)

## See Also

- [Container Queries (@container)](container-queries.md) — for size-based container queries
- [CSS Scroll Snap](scroll-snap.md) — works with `snapped` state queries
- Reference: [Chrome: Scroll-State Container Queries](https://developer.chrome.com/docs/css-ui/scroll-state-queries)
