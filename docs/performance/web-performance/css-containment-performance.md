---
description: Use CSS containment and content-visibility to skip rendering work for off-screen sections and isolate component reflows.
tldr: "Apply `content-visibility: auto` + `contain-intrinsic-size` to confirmed-off-screen sections to skip layout/paint; never apply to above-fold content; use `content-visibility: hidden` for SPA view caching but beware it removes content from the a11y tree."
---

# CSS Containment Performance

## When to Use

> CSS containment tells the browser that a subtree is independent from the rest of the page — changes inside cannot affect geometry outside. Use `content-visibility: auto` on large pages with many off-screen sections (feeds, dashboards). Use `contain: layout style paint` on components that need isolation regardless of viewport position.

**Newly Available — `content-visibility`:** Baseline since 2025-09-15. Chrome 108+, Edge 108+, Firefox 130+, Safari 26+.

## Decision

| Scenario | Approach | Notes |
|----------|----------|-------|
| Long page, heavy off-screen sections | `content-visibility: auto` + `contain-intrinsic-size` | Browser skips layout/paint until within viewport margin |
| SPA with multiple view tabs | `content-visibility: hidden` | Preserves rendering cache; faster than `display:none`; but removes from a11y tree |
| Complex isolated widget — avoid page-wide reflow | `contain: layout style paint` | Always-on, not viewport-dependent |
| Canvas/WebGL component that should pause off-screen | `content-visibility: auto` + `contentvisibilityautostatechange` event | Event fires when browser skips/resumes rendering |

## Pattern

```css
/* MANDATORY: always pair with contain-intrinsic-size */
/* Without it, element collapses to 0px height off-screen → scroll jumps */
.article-card {
  content-visibility: auto;
  contain-intrinsic-size: auto none auto 150px;
}

/* Manual containment: always-on isolation for complex widgets */
.isolated-widget {
  contain: layout style paint;
}
```

```css
/* SPA view caching — retains rendering cache between view switches */
.spa-view.inactive {
  content-visibility: hidden;
  position: absolute;
}
@supports not (content-visibility: hidden) {
  .spa-view.inactive { display: none; }
}
```

```javascript
// Pause Canvas/WebGL when off-screen
const component = document.querySelector('.heavy-canvas');
component.addEventListener('contentvisibilityautostatechange', (e) => {
  if (e.skipped) { stopAnimation(); pauseWebSocketPolling(); }
  else           { startAnimation(); resumeWebSocketPolling(); }
});
```

## Common Mistakes

- **Wrong**: `content-visibility: auto` on above-fold content → **Right**: Only apply to confirmed-off-screen sections; applying to above-fold triggers visibility evaluation overhead on the critical paint path
- **Wrong**: Missing `contain-intrinsic-size` → **Right**: Element collapses to 0px height off-screen, causing scroll position jumps
- **Wrong**: `content-visibility: hidden` when content must remain accessible to screen readers → **Right**: Use `hidden="until-found"` for searchable/accessible hidden content
- **Wrong**: Over-caching SPA views without eviction → **Right**: Each cached view retains DOM nodes, event listeners, and JS state; implement LRU eviction for highly dynamic apps
- **Wrong**: Attaching `contentvisibilityautostatechange` to a parent → **Right**: The event does not bubble reliably; attach directly to the element

## See Also

- [css/css-craft/animation-performance](../../css/css-craft/animation-performance.md) — `will-change`, compositor layers; use with CSS containment for compound isolation
- Reference: [web.dev: content-visibility](https://web.dev/articles/content-visibility)
