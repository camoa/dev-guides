---
description: "Break up long JS tasks with scheduler.yield() and scheduler.postTask() to keep INP under 200ms."
tldr: "Yield mid-loop every 50ms budget using `scheduler.yield()` (Chrome 129+/Edge 129+/Firefox 142+; no Safari) with a `setTimeout(0)` fallback; use the `scrollend` event instead of `scroll` for expensive post-scroll work."
---

# INP: Scheduler API and Task Splitting

## When to Use

> Apply when interactions feel sluggish (INP >200ms), a processing loop blocks user input, or DevTools shows long tasks (red bar at top of main thread). The browser can only process user input between tasks — a task >50ms is a "long task" that delays any interaction that occurs during it.

**The 50ms Rule:**
- Under 50ms → safe to run synchronously
- 50–250ms → split the work and yield periodically with the patterns below
- Over 250ms of computation → offload to a Web Worker

## Decision: Yield Strategy

| Method | Queue position | Browser support | Use when |
|--------|---------------|-----------------|----------|
| `scheduler.yield()` | Front of task queue — resumes before other pending tasks | Chrome 129+, Edge 129+, Firefox 142+; **no Safari** | Mid-task yield that must resume quickly; best for INP-critical paths |
| `setTimeout(fn, 0)` | Back of task queue | All browsers | Cross-browser fallback; may delay resume if other tasks are queued |
| `requestIdleCallback` | Only when browser is idle | Chrome, Firefox; no Safari | Background work that can wait indefinitely |
| `requestAnimationFrame` | Before next paint | All browsers | Visual updates only; not a general task yield |

> **LIMITED AVAILABILITY — scheduler API:** Chrome 129+, Edge 129+, Firefox 142+; **not supported in Safari** as of June 2026. Always feature-detect and provide the `setTimeout` fallback shown below. Verify current support at [web.dev/baseline](https://web.dev/baseline) before production reliance.

## Decision: scheduler.postTask() Priorities

Use `scheduler.postTask()` to schedule discrete background tasks with explicit priorities rather than mid-loop yields.

| Priority | Use for |
|----------|---------|
| `user-blocking` | Input handling, critical rendering updates that block the user |
| `user-visible` | Non-blocking UI updates visible to the user (default) |
| `background` | Analytics, prefetching, telemetry — anything not time-critical |

> **LIMITED AVAILABILITY — scheduler.postTask():** same support as `scheduler.yield()` above. Use the polyfill shown in the Pattern section.

## Pattern: Time-Budget Yield Loop

```javascript
// Feature-detect once; reuse everywhere
async function yieldToMain() {
  if ('scheduler' in window && 'yield' in scheduler) {
    return scheduler.yield();
  }
  return new Promise(resolve => setTimeout(resolve, 0));
}

// Process a large array without blocking user input
async function processLargeArray(items) {
  let deadline = performance.now() + 50; // 50ms budget

  for (const item of items) {
    processItem(item);

    if (performance.now() >= deadline) {
      await yieldToMain();          // surrender main thread
      deadline = performance.now() + 50; // reset budget
    }
  }
}
```

## Pattern: scheduler.postTask() with Polyfill

```javascript
// Feature-detect and load polyfill (scheduler-polyfill on npm)
if (!('scheduler' in window && 'postTask' in window.scheduler)) {
  const s = document.createElement('script');
  s.src = 'https://unpkg.com/scheduler-polyfill';
  s.onload = runTasks;
  document.head.appendChild(s);
} else {
  runTasks();
}

function runTasks() {
  scheduler.postTask(handleCriticalUpdate, { priority: 'user-blocking' });
  scheduler.postTask(renderSecondaryContent);  // default: 'user-visible'
  scheduler.postTask(sendAnalytics, { priority: 'background' });
}
```

## Pattern: Defer Work Until Scroll Ends

The `scrollend` event fires exactly when a scroll has come to rest (all transitions finished, touch gesture released). Use it instead of debounced `scroll` to avoid firing layout-heavy work mid-scroll.

**Newly Available** (Baseline since 2025-12-12): Chrome 114+, Edge 114+, Firefox 109+, Safari 26.2+.

```javascript
const scroller = document.querySelector('.scroll-container');

// Light informational updates during scroll
scroller.addEventListener('scroll', () => {
  updateProgressIndicator();  // keep this cheap
}, { passive: true });

// Expensive work only after scroll rests
scroller.addEventListener('scrollend', () => {
  const section = findMostVisibleSection(scroller);
  fetchAdditionalData(section);  // safe to do layout reads + fetches here
});
```

Fallback for browsers without `scrollend`:
```javascript
if (!('onscrollend' in window)) {
  scroller.addEventListener('scroll', () => {
    clearTimeout(window._scrollendTimer);
    window._scrollendTimer = setTimeout(() =>
      scroller.dispatchEvent(new CustomEvent('scrollend')), 100);
  });
}
```

## Common Mistakes

- Relying solely on `setTimeout(fn, 0)` as a yield — it places continuations at the back of the task queue; if other tasks are pending, the resume can be delayed hundreds of ms. Use `scheduler.yield()` for INP-critical paths
- Heavy polling with `setInterval` — starves the main thread; restructure as event-driven or use `requestIdleCallback`
- Yielding inside synchronous callbacks (`addEventListener` handlers without `async`) — you must mark the handler `async` to `await` `yieldToMain()`
- Firing analytics, DOM updates, or content fetches on every `scroll` event — use `scrollend` or throttle with rAF

## See Also

- [INP: Field Measurement](inp-field-measurement.md) — measure which tasks are causing poor INP before optimizing
- [js/interaction-craft/performance-and-event-handling](../../js/interaction-craft/performance-and-event-handling.md) — layout thrashing prevention, passive listeners, AbortController cleanup; this section supplements with `scheduler.postTask()` priorities and field measurement
- Reference: [web.dev: Optimize Long Tasks](https://web.dev/articles/optimize-long-tasks)
