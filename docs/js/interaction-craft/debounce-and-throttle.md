---
description: Choose between debounce, throttle, and requestAnimationFrame for rate-limiting events — scroll, resize, search input, and button submission
tldr: "Use `throttle` or `requestAnimationFrame` when you want continuous updates (scroll, mousemove, progress). Use `debounce` when you want to react once after the user stops (resize, search input, async validation)."
---

# Debounce and Throttle

## When to Use

> Use `throttle` or `requestAnimationFrame` when you want continuous updates (scroll, mousemove, progress). Use `debounce` when you want to react once after the user stops (resize, search input, async validation).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| React to scroll for visual updates | `throttle` (16ms) or `requestAnimationFrame` | Regular updates, not waiting for scroll to stop |
| React to resize for layout recalculation | `debounce` (150ms) | React once after the user finishes resizing |
| Search-as-you-type API calls | `debounce` (300ms) | Wait for typing pause, then fire once |
| Button that must not fire twice | `debounce` (leading edge) | Fire immediately, block subsequent calls |
| Progress bar tied to scroll position | `requestAnimationFrame` | rAF syncs to display refresh — more accurate than 16ms throttle |
| Pointer `mousemove` for hover effects | `throttle` (60fps) or rAF | Continuous updates wanted, just rate-limited |

**Leading vs trailing edge:**

| Edge | Behavior | Use Case |
|---|---|---|
| Trailing (default) | Fires at end of quiet period | Search input — fire after typing stops |
| Leading | Fires immediately, then blocks | Button submit — instant response, prevent double-submit |
| Both | Fires immediately AND at end | Rare; drag start + drag end |

## Pattern

```javascript
function throttle(fn, ms) {
  let lastCall = 0;
  return (...args) => {
    const now = Date.now();
    if (now - lastCall >= ms) { lastCall = now; fn(...args); }
  };
}

function debounce(fn, ms) {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
}

// rAF as throttle — syncs to display refresh (best for visual work)
function rafThrottle(fn) {
  let rafId = null;
  return (...args) => {
    if (rafId) return;
    rafId = requestAnimationFrame(() => { fn(...args); rafId = null; });
  };
}

// Usage
window.addEventListener('scroll', rafThrottle(updateStickyHeader), { passive: true });
window.addEventListener('resize', debounce(recalculateLayout, 150));
searchInput.addEventListener('input', debounce(fetchResults, 300));
```

## Common Mistakes

- **Wrong**: Debouncing `scroll` for visual updates → **Right**: Use throttle or rAF; debounce only shows updates after scroll stops
- **Wrong**: Throttling `resize` → **Right**: Use debounce; throttle gives intermediate calculations with wrong dimensions
- **Wrong**: `Date.now()` throttle for visual updates → **Right**: Use rAF; it syncs to display frame, Date.now() does not
- **Wrong**: Creating debounce/throttle inline inside event callbacks → **Right**: Create once and assign; inline defeats the purpose
- **Wrong**: Omitting `{ passive: true }` on scroll/touch listeners → **Right**: Always add it; browser cannot optimize scrolling without it

## See Also

- [Scroll Interaction Patterns](./scroll-interaction-patterns.md) — IntersectionObserver as rAF alternative for entry detection
- [Performance and Event Handling](./performance-and-event-handling.md) — passive listeners, read/write batching
- Reference: [CSS-Tricks: Debouncing and Throttling Explained](https://css-tricks.com/debouncing-throttling-explained-examples/)
- Reference: [MDN: requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame)
