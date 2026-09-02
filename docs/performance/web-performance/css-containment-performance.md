---
description: "Use CSS containment and content-visibility to skip rendering work for off-screen sections and isolate component reflows."
tldr: "Apply `content-visibility: auto` + `contain-intrinsic-size` to confirmed-off-screen sections to skip layout/paint; never apply to above-fold content; use `content-visibility: hidden` for SPA view caching but beware it removes content from the a11y tree."
---

# CSS Containment Performance

## When to Use

> CSS containment tells the browser that a subtree is independent from the rest of the page — changes inside it cannot affect geometry or styles outside it. This eliminates page-wide reflows for isolated mutations, and allows entire off-screen sections to skip layout/paint entirely until they approach the viewport.
>
> Use `content-visibility: auto` on large, complex pages with many off-screen sections (articles, feeds, dashboards). Use `contain: layout style paint` directly on components that need isolation regardless of viewport position.

**Newly Available — `content-visibility`:** Baseline since 2025-09-15. Chrome 108+, Edge 108+, Firefox 130+, Safari 26+.

## Decision: Which Containment Approach

| Scenario | Approach | Notes |
|----------|----------|-------|
| Long page, heavy off-screen sections (infinite feed, long article) | `content-visibility: auto` + `contain-intrinsic-size` | Browser skips layout/paint until within the viewport margin |
| SPA with multiple view tabs you want to switch instantly | `content-visibility: hidden` | Preserves rendering cache; faster than `display:none`; but removes from a11y tree |
| Complex isolated widget (modal, dashboard card) — avoid page-wide reflow | `contain: layout style paint` | Manual containment; always-on, not viewport-dependent |
| Complex layout (Kanban, grid) with drag-and-drop | `content-visibility: auto` on columns | Containment boundary prevents inter-column reflow during mutations |
| Canvas/WebGL component that should pause when off-screen | `content-visibility: auto` + `contentvisibilityautostatechange` event | Event fires when browser skips/resumes rendering the element |

## Pattern: content-visibility: auto for Off-Screen Sections

**MANDATORY:** Always pair with `contain-intrinsic-size`. Without it the element collapses to 0px height when off-screen, causing layout jumps and scrollbar position errors as the user scrolls.

```css
/* Only apply to elements confirmed off-screen on initial load */
.article-card {
  content-visibility: auto;

  /* 'auto' keyword: browser remembers real size after first render */
  /* Fallback value (150px here): used until element is first rendered */
  contain-intrinsic-size: auto none auto 150px;
}

/* Manual containment: always-on isolation for complex widgets */
.isolated-widget {
  contain: layout style paint;
}
```

Do NOT apply `content-visibility: auto` to above-fold elements — it forces the browser to evaluate visibility boundaries before rendering, paradoxically slowing the initial paint.

## Pattern: SPA View Caching with content-visibility: hidden

```css
/* hidden: removes from layout flow + paint but RETAINS rendering cache */
.spa-view.inactive {
  content-visibility: hidden;
  position: absolute;  /* prevent it from occupying layout space */
}

/* Fallback: display:none for browsers without content-visibility support */
@supports not (content-visibility: hidden) {
  .spa-view.inactive { display: none; }
}
```

```javascript
function switchToView(viewId) {
  document.querySelectorAll('.spa-view').forEach(v => {
    v.classList.add('inactive');
    v.setAttribute('aria-hidden', 'true');
  });
  const active = document.getElementById(viewId);
  active.classList.remove('inactive');
  active.setAttribute('aria-hidden', 'false');
  active.focus();  // MANDATORY: restore keyboard focus
}
```

**Warning:** `content-visibility: hidden` removes children from the accessibility tree and find-in-page search. If those features are needed while hidden, use `hidden="until-found"` instead.

**Trade-off:** Each cached view retains its DOM nodes, event listeners, and JS state in memory. Safe for 3-5 views; implement a Least-Recently-Used eviction strategy for highly dynamic applications.

## Pattern: Pause Canvas/WebGL When Off-Screen

```javascript
const component = document.querySelector('.heavy-canvas');

// Direct listener — event does NOT bubble in all browsers
component.addEventListener('contentvisibilityautostatechange', (e) => {
  if (e.skipped) {
    stopAnimation();         // browser skipping = off-screen
    pauseWebSocketPolling();
  } else {
    startAnimation();        // browser resuming = approaching viewport
    resumeWebSocketPolling();
  }
});

// Fallback for browsers without content-visibility
if (!('contentVisibility' in document.documentElement.style)) {
  const obs = new IntersectionObserver(
    ([entry]) => entry.isIntersecting ? startAnimation() : stopAnimation(),
    { rootMargin: '200px' }
  );
  obs.observe(component);
}
```

## Common Mistakes

- Applying `content-visibility: auto` to above-fold content — triggers visibility evaluation overhead on critical paint path; only apply to confirmed-off-screen sections
- Missing `contain-intrinsic-size` — element collapses to 0px height off-screen, causing scroll jumps
- Applying `content-visibility: hidden` when content must remain accessible to screen readers — use `hidden="until-found"` for searchable/accessible hidden content
- Over-caching SPA views without eviction — unbounded view caching crashes low-memory devices
- Not attaching `contentvisibilityautostatechange` directly to the element — the event does not bubble reliably; attach to the element or use `{ capture: true }` on a parent

## See Also

- [css/css-craft/animation-performance](../../css/css-craft/animation-performance.md) — `will-change`, compositor layers, property tiers; use with CSS containment for compound isolation
- [css/modern-css/scroll-driven-animations](../../css/modern-css/scroll-driven-animations.md) — scroll-linked animations; `content-visibility` and scroll animations interact on the same rendering pipeline
- Reference: [web.dev: content-visibility](https://web.dev/articles/content-visibility)
