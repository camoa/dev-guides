---
description: IntersectionObserver for entry detection, scroll-linked state, lazy load, infinite scroll, and scroll position restoration
---

# Scroll Interaction Patterns

## When to Use

> Use `IntersectionObserver` for threshold-based events (entering viewport, lazy load, infinite scroll). Use `scroll` + rAF for continuous position-linked updates (parallax, progress bars).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Detect when element enters viewport | `IntersectionObserver` | Async, off-main-thread, exact threshold control |
| Scroll-linked progress bar | `scroll` event + rAF throttle | Progress must update continuously, not just on entry |
| Sticky header that shrinks on scroll | `IntersectionObserver` on sentinel element | More reliable than scroll position comparison |
| Lazy-load images | `IntersectionObserver` with `rootMargin` | Pre-load before visible with positive rootMargin |
| Infinite scroll / load-more trigger | `IntersectionObserver` on final list item | Cleaner than scroll position math |
| Parallax effect coordinates | `scroll` event + rAF (or CSS scroll-driven) | Parallax is continuous, not threshold-based |
| Restore scroll after back navigation | `history.scrollRestoration = 'manual'` + `sessionStorage` | Browser auto-restore conflicts with SPA rendering |

**Threshold and rootMargin reference:**

| Use Case | threshold | rootMargin |
|---|---|---|
| Entrance animations | `0.15` | `'0px 0px -50px 0px'` (slightly inside viewport) |
| Lazy load images | `0` | `'0px 0px 200px 0px'` (preload 200px ahead) |
| Infinite scroll trigger | `0` | `'0px 0px 300px 0px'` (generous buffer) |
| Sticky header sentinel | `0` | `'0px'` |

## Pattern

```javascript
// Entrance animations — unobserve after first trigger
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('is-visible');
    revealObserver.unobserve(entry.target); // Critical: prevents re-animation
  });
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// Sticky header via sentinel element
const sentinel = document.querySelector('#scroll-sentinel'); // 1px element at top of page
new IntersectionObserver(([entry]) => {
  document.querySelector('header').classList.toggle('is-compact', !entry.isIntersecting);
}, { threshold: 0 }).observe(sentinel);

// Infinite scroll
let loading = false;
new IntersectionObserver(async ([entry]) => {
  if (!entry.isIntersecting || loading) return;
  loading = true;
  await fetchAndAppendItems();
  loading = false;
}, { rootMargin: '0px 0px 200px 0px' }).observe(document.querySelector('#load-more-sentinel'));

// Scroll position restoration (SPA)
history.scrollRestoration = 'manual';
window.addEventListener('beforeunload', () => {
  sessionStorage.setItem(`scroll:${location.pathname}`, window.scrollY);
});
function restoreScroll() {
  const saved = sessionStorage.getItem(`scroll:${location.pathname}`);
  if (saved) { window.scrollTo({ top: parseInt(saved, 10), behavior: 'instant' }); sessionStorage.removeItem(`scroll:${location.pathname}`); }
}
```

## Common Mistakes

- **Wrong**: Using a scroll listener for intersection detection → **Right**: IntersectionObserver does 10-50x less work
- **Wrong**: Forgetting `unobserve()` on one-shot animations → **Right**: Unobserve immediately after first trigger; elements re-animate otherwise
- **Wrong**: Not checking `entry.isIntersecting` → **Right**: Always check the flag; callback fires on both enter and exit
- **Wrong**: Scroll restoration with SPA async rendering → **Right**: Set `'manual'` and restore only after content has rendered
- **Wrong**: Positive `rootMargin` to expand root — actually shrinks it → **Right**: Negative values shrink, positive values expand

## See Also

- [Debounce and Throttle](./debounce-and-throttle.md) — rAF throttle for continuous scroll handlers
- [Performance and Event Handling](./performance-and-event-handling.md) — passive scroll listeners
- Reference: [MDN: Intersection Observer API](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API)
- Reference: [MDN: History.scrollRestoration](https://developer.mozilla.org/en-US/docs/Web/API/History/scrollRestoration)
