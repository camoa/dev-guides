---
description: "Passive event listeners, layout thrashing prevention, event delegation, breaking up long tasks, and memory leak patterns"
tldr: "Apply these patterns to every JS interaction. Passive listeners, read/write batching, event delegation, and AbortController cleanup are baselines — not optimizations."
---

# Performance and Event Handling

## When to Use

> Every section of this guide. These are the underlying performance rules that apply to all JS interactions — event handling, DOM manipulation, long tasks, and memory management.

## Passive Event Listeners

Adding `{ passive: true }` to scroll, touch, and wheel listeners tells the browser "I will not call `preventDefault()`." The browser can then optimize scrolling without waiting for your JS to complete — eliminating a major source of scroll jank.

```javascript
// ALWAYS passive for scroll/touch/wheel unless you need to prevent default
window.addEventListener('scroll', handler, { passive: true });
element.addEventListener('touchstart', handler, { passive: true });
element.addEventListener('wheel', handler, { passive: true });

// Only omit passive when you actually call preventDefault()
element.addEventListener('touchmove', preventScroll, { passive: false });
```

Browsers default `touchstart` and `touchmove` to passive on the document, but not on arbitrary elements. Explicit `{ passive: true }` on scroll handlers eliminates the "non-passive event listener" DevTools warning and measurably improves scroll performance on low-end devices.

## Layout Thrashing: Read-Write Batching

Layout thrashing occurs when JS reads a layout property (`offsetHeight`, `getBoundingClientRect()`, `clientWidth`), then writes a style, then reads again in the same synchronous block. Each read after a write forces the browser to flush pending style changes and recalculate layout synchronously — potentially taking 5-20ms per flush on complex pages.

**Recognize the pattern:**
```javascript
// BAD — read, write, read (forces 2 layout recalculations)
const height = el.offsetHeight;          // Read — forces layout
el.style.height = `${height + 10}px`;   // Write
const newHeight = el.offsetHeight;       // Read again — forces layout again
```

**Fix — batch reads first, then writes:**
```javascript
// GOOD — all reads first, then all writes
const heights = elements.map(el => el.offsetHeight);  // Batch reads
elements.forEach((el, i) => { el.style.height = `${heights[i] + 10}px`; }); // Batch writes
```

**rAF batching (for animation loops):**
```javascript
// Read in handler, write in rAF (deferred to next paint)
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;  // Read immediately
  requestAnimationFrame(() => {
    header.style.transform = `translateY(${scrollY * 0.1}px)`;  // Write in rAF
  });
}, { passive: true });
```

## Event Delegation

Attach one listener to a parent instead of many listeners to children. Essential for dynamic lists, tables, or any collection that grows/changes.

```javascript
// Instead of: items.forEach(item => item.addEventListener('click', handler))
// Do this:
document.querySelector('#list').addEventListener('click', (e) => {
  const item = e.target.closest('[data-item-id]');
  if (!item) return;
  handleItemClick(item.dataset.itemId);
});
```

Delegation works because events bubble. `closest()` is the correct selector — it finds the matching ancestor even when the click target is a child element (e.g., an icon inside a button).

## Breaking Up Long Tasks

A "long task" is any JS that runs for > 50ms without yielding. Long tasks block the main thread, preventing user input responses and causing INP (Interaction to Next Paint) failures.

```javascript
// scheduler.yield() — preferred (Chromium only, 2024+)
async function processLargeArray(items) {
  for (let i = 0; i < items.length; i++) {
    processItem(items[i]);
    if (i % 50 === 0) await scheduler.yield(); // Yield every 50 items
  }
}

// Fallback for non-Chromium browsers
const yieldToMain = () =>
  typeof scheduler !== 'undefined'
    ? scheduler.yield()
    : new Promise(resolve => setTimeout(resolve, 0));

// requestIdleCallback — for non-urgent background work
requestIdleCallback((deadline) => {
  while (deadline.timeRemaining() > 0 && workQueue.length) {
    processItem(workQueue.shift());
  }
});
```

**scheduler.yield() vs alternatives:**

| Method | Priority | When to Use |
|---|---|---|
| `scheduler.yield()` | High (resumes before other tasks) | Mid-task yields that must continue quickly |
| `setTimeout(fn, 0)` | Low (goes to end of queue) | Simple yields; cross-browser compatible |
| `requestIdleCallback` | Idle only | Background work that can wait indefinitely |
| `requestAnimationFrame` | Before next paint | Visual updates only |

## Memory Leak Prevention

**Pattern 1: AbortController for bulk listener cleanup**

```javascript
class Component {
  #controller = new AbortController();

  init() {
    const signal = this.#controller.signal;
    window.addEventListener('resize', this.#onResize, { signal });
    document.addEventListener('keydown', this.#onKeydown, { signal });
    // All listeners removed with one call — no need to store references
  }

  destroy() {
    this.#controller.abort(); // Removes ALL listeners registered with this signal
  }
}
```

**Pattern 2: { once: true } for one-shot listeners**

```javascript
// Automatically removes itself after firing once
element.addEventListener('transitionend', cleanup, { once: true });
```

**Pattern 3: Disconnect observers when done**

```javascript
const observer = new IntersectionObserver(callback);
observer.observe(target);
// When component is removed:
observer.disconnect(); // Stop observing all targets
```

**Common memory leak sources:**

| Source | Symptom | Fix |
|---|---|---|
| Event listeners on removed elements | Memory grows over time | Use AbortController; remove on cleanup |
| IntersectionObserver not disconnected | Observer fires on detached elements | Call `observer.disconnect()` or `unobserve()` |
| Closures holding DOM references | Elements cannot be GC'd | Nullify references in cleanup; use WeakRef for optional holds |
| Timers not cleared | `setInterval` fires after component removed | Store ID; call `clearInterval` in cleanup |
| Promises awaiting removed elements | Resolve/reject handler holds element ref | Use AbortController signal to cancel async operations |

## Professional vs Amateur Performance Table

| Practice | Amateur | Professional |
|---|---|---|
| Scroll listener | Raw listener, reads DOM | Passive + rAF throttle + batched reads |
| Dynamic list events | Listener per item | Event delegation on container |
| Long data processing | Single synchronous loop | Chunked with `scheduler.yield()` |
| Cleanup | Never cleaned up | AbortController `destroy()` method |
| Layout reads during animation | `getBoundingClientRect()` in rAF | Read before rAF, write inside rAF |

## Common Mistakes

- **`{ passive: true }` on a handler that calls `preventDefault()`** — preventDefault is silently ignored; scroll proceeds anyway
- **Reading `offsetHeight` inside a `requestAnimationFrame` callback** — rAF runs before paint but after layout; reads here are fine but writes after reads force another layout
- **Event delegation without `closest()`** — direct `target` matching breaks when click lands on a child element
- **Using `setInterval` for animation** — interval timing drifts, not tied to display refresh; use rAF
- **Never calling `observer.disconnect()`** — long-lived pages accumulate dead observers

## See Also

- [Debounce and Throttle](./debounce-and-throttle.md) — rate limiting for specific event types
- [Scroll Interaction Patterns](./scroll-interaction-patterns.md) — IntersectionObserver as alternative to scroll listeners
- [Touch and Gesture Craft](./touch-and-gesture-craft.md) — passive listeners for touch events
- Reference: [web.dev: Optimize Long Tasks](https://web.dev/articles/optimize-long-tasks)
- Reference: [Chrome Developers: scheduler.yield](https://developer.chrome.com/blog/use-scheduler-yield)
- Reference: [MDN: Scheduler.yield()](https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield)
