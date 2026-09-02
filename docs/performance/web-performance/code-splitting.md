---
description: "Reduce initial JS parse budget by splitting bundles at route and interaction boundaries with dynamic import()."
tldr: "Use dynamic `import()` on first interaction for features never needed on initial load; use Speculation Rules API (Chrome/Edge only) for near-instant next-page prerender; never speculatively prerender state-changing URLs like /logout or /checkout."
---

# Code Splitting

## When to Use

> A monolithic `app.js` bundle makes every page download and parse code it may never execute. Split at route or interaction boundaries so the initial parse budget covers only what the current view needs. Particularly impactful on mobile where parse times are 3-5x slower than desktop.

## Decision: Split Point Strategy

| Pattern | When to use | How |
|---------|-------------|-----|
| **Route splitting** | Multi-page or SPA with distinct routes | Dynamic `import()` triggered by router navigation |
| **Interaction splitting** | Heavy feature only needed after a user action (modal, chart, rich editor) | Dynamic `import()` on first click/focus/hover |
| **Conditional polyfill loading** | Browser support gap; only some users need the polyfill | Top-level `await` + `import()` inside a detection module |
| **Vendor chunking** | Large stable third-party libraries (React, D3, Lodash) | Bundler config: `splitChunks` (webpack) or `manualChunks` (Vite/Rollup) |
| **Speculative next-page prefetch** | Static site, known navigation path | Speculation Rules API |

## Pattern: Interaction-Triggered Dynamic Import

```javascript
// Heavy module only downloaded + parsed when user requests it
const btn = document.getElementById('open-chart');
btn.addEventListener('click', async () => {
  const { renderChart } = await import('./chart-heavy.js');
  renderChart(document.getElementById('chart-container'));
}, { once: true });
```

## Pattern: Conditional Polyfill via Top-Level Await

Top-level `await` blocks the importing module until the polyfill is ready, ensuring safe use without callback nesting.

**Broadly supported since 2021** (Chrome 89, Firefox 89, Safari 15). No fallback needed for modern apps. Avoid pre-2021 legacy targets.

**MANDATORY Safari bug:** Multiple sibling modules importing the same top-level-await module simultaneously crash in WebKit. Import it exactly once at the application entry point:

```javascript
// conditionally-load-polyfill.js
if (!('popover' in HTMLElement.prototype)) {
  await import('/vendor/popover-polyfill.js');
}
export const polyfillReady = true;

// main.js — import ONCE at the top, before any other modules
import './conditionally-load-polyfill.js';  // blocks until polyfill resolves
import './app.js';
// DO NOT also import conditionally-load-polyfill.js from inside app.js or any sibling
```

## Pattern: Speculative Next-Page Loading

The Speculation Rules API tells the browser to prefetch or prerender pages the user is likely to visit, providing near-instant navigation.

> **LIMITED AVAILABILITY — Speculation Rules API:** Chrome and Edge only as of June 2026; not supported in Firefox or Safari. Progressive enhancement — ignored in unsupported browsers. Verify current support at [web.dev/baseline](https://web.dev/baseline) before production reliance.

```html
<!-- Conservative: prefetch eagerly, prerender only when user hovers -->
<script type="speculationrules">
{
  "prefetch": [{
    "where": { "href_matches": "/*" },
    "eagerness": "eager"
  }],
  "prerender": [{
    "where": {
      "and": [
        { "href_matches": "/*" },
        { "not": { "href_matches": "/logout" } },
        { "not": { "href_matches": "/*?*add-to-cart=*" } },
        { "not": { "selector_matches": ".no-prerender" } }
      ]
    },
    "eagerness": "moderate"
  }]
}
</script>
```

**Eagerness levels:** `immediate` (speculate now) → `eager` (short hover) → `moderate` (longer hover) → `conservative` (starting to click). Use `immediate` only for 1-2 links.

## Common Mistakes

- Shipping a single `app.js` without splitting — increases initial parse time proportionally to bundle size; low-end devices parse JS at 3-5x slower than desktop
- Dynamic importing on every render — adds waterfall latency if the module is always needed; split at genuine branch points only
- Using Speculation Rules on SPAs — speculation rules prerender a new document; SPAs do client-side navigation without document navigation, so rules have no effect
- Speculatively prerendering state-changing URLs (`/logout`, `/checkout/confirm`) — prerendering these triggers server-side side effects before the user clicked
- Neglecting vendor chunking — without explicit `manualChunks`, bundlers may re-bundle the same React/lodash code into every route chunk

## See Also

- [Resource Hints](resource-hints.md) — `<link rel="prefetch">` as a lightweight alternative to Speculation Rules for asset prefetch
- [Service Worker Caching](service-worker-caching.md) — cached split chunks serve from disk on repeat loads
- Reference: [web.dev: Code splitting](https://web.dev/articles/code-splitting-suspense)
- Reference: [web.dev: Speculation Rules API](https://developer.chrome.com/docs/web-platform/prerender-pages)
