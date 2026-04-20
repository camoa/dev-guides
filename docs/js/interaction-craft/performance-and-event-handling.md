---
description: Passive event listeners, layout thrashing prevention, event delegation, breaking up long tasks, and memory leak patterns
tldr: "Apply these patterns to every JS interaction. Passive listeners, read/write batching, event delegation, and AbortController cleanup are baselines — not optimizations."
---

# Performance and Event Handling

## When to Use

> Apply these patterns to every JS interaction. Passive listeners, read/write batching, event delegation, and AbortController cleanup are baselines — not optimizations.

## Decision

| Practice | Amateur | Professional |
|---|---|---|
| Scroll listener | Raw listener, reads DOM | Passive + rAF throttle + batched reads |
| Dynamic list events | Listener per item | Event delegation on container |
| Long data processing | Single synchronous loop | Chunked with `scheduler.yield()` |
| Cleanup | Never cleaned up | AbortController `destroy()` method |
| Layout reads during animation | `getBoundingClientRect()` in rAF | Read before rAF, write inside rAF |

**scheduler.yield() vs alternatives:**

| Method | Priority | When to Use |
|---|---|---|
| `scheduler.yield()` | High (resumes before other tasks) | Mid-task yields that must continue quickly |
| `setTimeout(fn, 0)` | Low (goes to end of queue) | Simple yields; cross-browser compatible |
| `requestIdleCallback` | Idle only | Background work that can wait indefinitely |
| `requestAnimationFrame` | Before next paint | Visual updates only |

## Pattern

```javascript
// Passive listeners — always for scroll/touch/wheel
window.addEventListener('scroll', handler, { passive: true });
element.addEventListener('touchstart', handler, { passive: true });
// Only omit passive when you actually call preventDefault()
element.addEventListener('touchmove', preventScroll, { passive: false });

// Read/write batching — prevent layout thrashing
// BAD: read, write, read forces 2 layout recalculations
// GOOD: batch reads first, then writes
const heights = elements.map(el => el.offsetHeight);           // Batch reads
elements.forEach((el, i) => { el.style.height = `${heights[i] + 10}px`; }); // Batch writes

// rAF pattern: read in handler, write in rAF
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;                              // Read immediately
  requestAnimationFrame(() => { header.style.transform = `translateY(${scrollY * 0.1}px)`; }); // Write in rAF
}, { passive: true });

// Event delegation — one listener for dynamic collections
document.querySelector('#list').addEventListener('click', (e) => {
  const item = e.target.closest('[data-item-id]');
  if (!item) return;
  handleItemClick(item.dataset.itemId);
});

// Break up long tasks — yield to main thread every ~50 items
async function processLargeArray(items) {
  const yieldToMain = () => typeof scheduler !== 'undefined'
    ? scheduler.yield() : new Promise(resolve => setTimeout(resolve, 0));
  for (let i = 0; i < items.length; i++) {
    processItem(items[i]);
    if (i % 50 === 0) await yieldToMain();
  }
}

// AbortController — bulk listener cleanup
class Component {
  #controller = new AbortController();
  init() {
    const { signal } = this.#controller;
    window.addEventListener('resize', this.#onResize, { signal });
    document.addEventListener('keydown', this.#onKeydown, { signal });
  }
  destroy() { this.#controller.abort(); } // Removes all listeners registered with this signal
}

// Memory leak table sources and fixes:
// Event listeners on removed elements → AbortController cleanup
// IntersectionObserver not disconnected → observer.disconnect() on component remove
// setInterval not cleared → clearInterval(id) in cleanup
// { once: true } for one-shot listeners — auto-removes after firing
element.addEventListener('transitionend', cleanup, { once: true });
```

## Common Mistakes

- **Wrong**: `{ passive: true }` on a handler that calls `preventDefault()` → **Right**: preventDefault is silently ignored; set `{ passive: false }` explicitly
- **Wrong**: Reading `offsetHeight` inside rAF after writes → **Right**: Read before rAF, write inside rAF to avoid forcing layout
- **Wrong**: Event delegation without `closest()` → **Right**: Direct `target` matching breaks when click lands on a child element (e.g., icon inside button)
- **Wrong**: `setInterval` for animation → **Right**: Interval timing drifts; use rAF
- **Wrong**: Never calling `observer.disconnect()` → **Right**: Long-lived pages accumulate dead observers

## See Also

- [Debounce and Throttle](./debounce-and-throttle.md) — rate limiting for specific event types
- [Scroll Interaction Patterns](./scroll-interaction-patterns.md) — IntersectionObserver as alternative to scroll listeners
- [Touch and Gesture Craft](./touch-and-gesture-craft.md) — passive listeners for touch events
- Reference: [web.dev: Optimize Long Tasks](https://web.dev/articles/optimize-long-tasks)
- Reference: [Chrome Developers: scheduler.yield](https://developer.chrome.com/blog/use-scheduler-yield)
- Reference: [MDN: Scheduler.yield()](https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield)
