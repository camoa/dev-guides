---
description: "Choose between debounce, throttle, and requestAnimationFrame for rate-limiting events — scroll, resize, search input, and button submission"
tldr: "Use `throttle` or `requestAnimationFrame` when you want continuous updates (scroll, mousemove, progress). Use `debounce` when you want to react once after the user stops (resize, search input, async validation)."
---

# Debounce and Throttle

## When to Use

> When user events fire faster than you should react to them. The wrong choice between these two patterns is responsible for janky scroll handlers, missed search queries, and flickering UIs. Understanding the semantic difference is more important than memorizing implementations.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| React to scroll for visual updates (sticky header, parallax) | `throttle` (16ms) or `requestAnimationFrame` | You want regular updates, not to wait for scroll to stop |
| React to resize for layout recalculation | `debounce` (150ms) | You want to react once after the user finishes resizing |
| Search-as-you-type API calls | `debounce` (300ms) | Wait for the user to pause typing, then fire once |
| Button that must not fire twice | `debounce` (leading edge) | Fire immediately, block subsequent calls |
| Progress bar tied to scroll position | `requestAnimationFrame` | rAF syncs to display refresh; more accurate than 16ms throttle |
| Window `resize` with exact dimensions needed | `debounce` (200ms trailing) | Final value only, no intermediate noise |
| Pointer `mousemove` for hover effects | `throttle` (60fps) or rAF | Continuous updates wanted, just rate-limited |

**Leading vs trailing edge:**

| Edge | Behavior | Use Case |
|---|---|---|
| Trailing (default) | Fires at end of quiet period | Search input — fire after typing stops |
| Leading | Fires immediately, then blocks | Button submit — instant response, prevent double-submit |
| Both | Fires immediately AND at end | Rare; drag start + drag end |

**Professional vs Amateur scroll handling:**

| Approach | Problem |
|---|---|
| Raw `scroll` listener with DOM reads/writes | Main thread blocked, jank guaranteed |
| `debounce` on scroll | Updates only after scroll stops — feels broken |
| `throttle` at 100ms | Visible stutter at 60fps (6 frames per update) |
| `throttle` at 16ms or `requestAnimationFrame` | Smooth, synced to display refresh |
| `requestAnimationFrame` + passive listener | Best — off main thread hint + display-sync |

## Pattern

```javascript
// Throttle — rate limit continuous events
function throttle(fn, ms) {
  let lastCall = 0;
  return (...args) => {
    const now = Date.now();
    if (now - lastCall >= ms) {
      lastCall = now;
      fn(...args);
    }
  };
}

// Debounce — wait for quiet period (trailing edge)
function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

// rAF as throttle — syncs to display refresh cycle (best for visual work)
function rafThrottle(fn) {
  let rafId = null;
  return (...args) => {
    if (rafId) return;
    rafId = requestAnimationFrame(() => {
      fn(...args);
      rafId = null;
    });
  };
}
```

**Usage by event type:**

```javascript
// Scroll — visual updates use rAF; passive for scrolling performance
window.addEventListener('scroll', rafThrottle(updateStickyHeader), { passive: true });

// Resize — fire after user stops resizing
window.addEventListener('resize', debounce(recalculateLayout, 150));

// Search input — wait for typing pause
searchInput.addEventListener('input', debounce(fetchResults, 300));
```

## Common Mistakes

- **Debouncing `scroll` for visual updates** — content jumps only after scrolling stops; use throttle or rAF instead
- **Throttling `resize`** — you get intermediate layout calculations with wrong dimensions; use debounce instead
- **Using `Date.now()` throttle for visual updates** — not synced to display frame; use rAF for anything visual
- **Building debounce/throttle inline inside event callbacks** — new function created each time, defeats the purpose; create once and assign
- **Forgetting `{ passive: true }` on scroll/touch listeners** — browser cannot optimize scrolling, jank even with rAF

## See Also

- [Performance and Event Handling](./performance-and-event-handling.md) — passive listeners, read/write batching
- [Scroll Interaction Patterns](./scroll-interaction-patterns.md) — IntersectionObserver as rAF alternative for entry detection
- [Animation Performance](../../css/css-craft/animation-performance.md) — why 60fps matters for scroll-linked effects
- Reference: [CSS-Tricks: Debouncing and Throttling Explained](https://css-tricks.com/debouncing-throttling-explained-examples/)
- Reference: [MDN: requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame)
