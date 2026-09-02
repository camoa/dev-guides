---
description: "IntersectionObserver for entry detection, scroll-linked state, lazy load, infinite scroll, and scroll position restoration"
tldr: "Use `IntersectionObserver` for threshold-based events (entering viewport, lazy load, infinite scroll). Use `scroll` + rAF for continuous position-linked updates (parallax, progress bars)."
---

# Scroll Interaction Patterns

## When to Use

> When scroll position must trigger state changes, reveal animations, or load more content. IntersectionObserver is almost always the right tool — it runs off the main thread and fires only when visibility changes rather than on every scroll event.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Detect when element enters viewport | `IntersectionObserver` | Async, off-main-thread, exact threshold control |
| Scroll-linked progress bar | `scroll` event + rAF throttle | Progress must update continuously, not just on entry |
| Sticky header that shrinks on scroll | `IntersectionObserver` on sentinel element | More reliable than scroll position comparison |
| Lazy-load images | `IntersectionObserver` with `rootMargin` | Pre-load before visible with positive rootMargin |
| Infinite scroll / load-more trigger | `IntersectionObserver` on final list item | Cleaner than scroll position math |
| Scroll snap active slide tracking | `IntersectionObserver` on each slide | `snapchanged` event has limited support; observer is universal |
| Parallax effect coordinates | `scroll` event + rAF (or CSS scroll-driven) | Parallax is continuous, not threshold-based |
| Restore scroll after back navigation | `history.scrollRestoration = 'manual'` + `sessionStorage` | Browser auto-restore conflicts with SPA rendering |

## Pattern: IntersectionObserver Orchestration

```javascript
// Multi-purpose observer factory
function createObserver({ threshold = 0.1, rootMargin = '0px', once = true } = {}) {
  return new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.dispatchEvent(new CustomEvent('visible', { bubbles: true }));
      if (once) entry.target.dataset.observerKey &&
        observers.get(entry.target.dataset.observerKey)?.unobserve(entry.target);
    });
  }, { threshold, rootMargin });
}

// Entrance animations — fire once, unobserve after
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('is-visible');
    revealObserver.unobserve(entry.target);   // Critical: prevents re-animation
  });
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));
```

## Pattern: Scroll-Linked State (Sticky Header)

```javascript
// Sentinel approach — more reliable than scroll Y comparison
const sentinel = document.querySelector('#scroll-sentinel'); // 1px element at top of page

const headerObserver = new IntersectionObserver(([entry]) => {
  document.querySelector('header').classList.toggle('is-compact', !entry.isIntersecting);
}, { threshold: 0, rootMargin: '0px' });

headerObserver.observe(sentinel);
```

## Pattern: Scroll Position Restoration

```javascript
// Disable browser's auto-restore (conflicts with async content rendering in SPAs)
history.scrollRestoration = 'manual';

// Save before navigation
window.addEventListener('beforeunload', () => {
  sessionStorage.setItem(`scroll:${location.pathname}`, window.scrollY);
});

// Restore after content renders
function restoreScroll() {
  const saved = sessionStorage.getItem(`scroll:${location.pathname}`);
  if (saved) {
    window.scrollTo({ top: parseInt(saved, 10), behavior: 'instant' });
    sessionStorage.removeItem(`scroll:${location.pathname}`);
  }
}
```

## Pattern: Infinite Scroll Trigger

```javascript
const loadMoreTrigger = document.querySelector('#load-more-sentinel');
let loading = false;

const infiniteObserver = new IntersectionObserver(async ([entry]) => {
  if (!entry.isIntersecting || loading) return;
  loading = true;
  await fetchAndAppendItems();
  loading = false;
}, { rootMargin: '0px 0px 200px 0px' }); // Load 200px before user reaches bottom

infiniteObserver.observe(loadMoreTrigger);
```

## Threshold and rootMargin Values Reference

| Use Case | threshold | rootMargin |
|---|---|---|
| Entrance animations | `0.15` | `'0px 0px -50px 0px'` (slightly inside viewport) |
| Lazy load images | `0` | `'0px 0px 200px 0px'` (preload 200px ahead) |
| Infinite scroll trigger | `0` | `'0px 0px 300px 0px'` (generous buffer) |
| Progress tracking (counted as seen) | `0.5` | `'0px'` |
| Sticky header sentinel | `0` | `'0px'` |

## Common Mistakes

- **Using a scroll listener for intersection detection** — 10-50x more work than IntersectionObserver
- **Forgetting `unobserve()` on one-shot animations** — elements re-animate on scroll out then in
- **Setting `rootMargin` without understanding its sign convention** — positive values grow the intersection root, so a target counts as intersecting before it is visible; negative values shrink it
- **Not checking `entry.isIntersecting`** — the callback fires on both enter and exit; always check the flag
- **Scroll restoration fighting with async rendering** — always `'manual'` + wait for content before restoring

## See Also

- [Debounce and Throttle](./debounce-and-throttle.md) — throttle/rAF for continuous scroll handlers
- [Performance and Event Handling](./performance-and-event-handling.md) — passive scroll listeners
- [Entrance Animations](../../css/css-craft/entrance-animations.md) — the CSS side of IntersectionObserver reveals
- [Parallax Effects](../../css/css-craft/parallax-effects.md) — scroll-driven CSS alternative
- Reference: [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- Reference: [MDN: History.scrollRestoration](https://developer.mozilla.org/en-US/docs/Web/API/History/scrollRestoration)
