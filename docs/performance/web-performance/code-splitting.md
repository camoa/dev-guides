---
description: Reduce initial JS parse budget by splitting bundles at route and interaction boundaries with dynamic import().
tldr: Use dynamic `import()` on first interaction for features never needed on initial load; use Speculation Rules API (Chrome/Edge only) for near-instant next-page prerender; never speculatively prerender state-changing URLs like /logout or /checkout.
---

# Code Splitting

## When to Use

> A monolithic `app.js` bundle makes every page download and parse code it may never execute. Split at route or interaction boundaries so the initial parse budget covers only what the current view needs. Particularly impactful on mobile where JS parse times are 3–5x slower than desktop.

## Decision

| Pattern | When to use | How |
|---------|-------------|-----|
| **Route splitting** | Multi-page or SPA with distinct routes | Dynamic `import()` triggered by router navigation |
| **Interaction splitting** | Heavy feature only needed after a user action (modal, chart, rich editor) | Dynamic `import()` on first click/focus/hover |
| **Conditional polyfill loading** | Browser support gap; only some users need it | Top-level `await` + `import()` inside a detection module |
| **Vendor chunking** | Large stable third-party libraries (React, D3) | Bundler config: `splitChunks` (webpack) or `manualChunks` (Vite/Rollup) |
| **Speculative next-page prefetch** | Static site, known navigation path | Speculation Rules API |

## Pattern: Interaction-Triggered Dynamic Import

```javascript
const btn = document.getElementById('open-chart');
btn.addEventListener('click', async () => {
  const { renderChart } = await import('./chart-heavy.js');
  renderChart(document.getElementById('chart-container'));
}, { once: true });
```

## Pattern: Conditional Polyfill via Top-Level Await

**MANDATORY Safari bug:** Multiple sibling modules importing the same top-level-await module simultaneously crash in WebKit. Import it exactly once at the application entry point.

```javascript
// conditionally-load-polyfill.js
if (!('popover' in HTMLElement.prototype)) {
  await import('/vendor/popover-polyfill.js');
}
export const polyfillReady = true;

// main.js — import ONCE at the top, before any other modules
import './conditionally-load-polyfill.js';
import './app.js';
// DO NOT also import conditionally-load-polyfill.js from inside app.js
```

## Pattern: Speculation Rules API

> **LIMITED AVAILABILITY:** Chrome and Edge only as of June 2026; not supported in Firefox or Safari.

```html
<script type="speculationrules">
{
  "prefetch": [{ "where": { "href_matches": "/*" }, "eagerness": "eager" }],
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

**Eagerness levels:** `immediate` → `eager` → `moderate` → `conservative`. Use `immediate` only for 1–2 links.

## Common Mistakes

- **Wrong**: Shipping a single `app.js` without splitting → **Right**: Initial parse time scales with bundle size; low-end devices parse JS 3–5x slower than desktop
- **Wrong**: Dynamic importing on every render → **Right**: Split at genuine branch points only; always-needed modules should be in the main bundle
- **Wrong**: Speculation Rules on SPAs → **Right**: Rules prerender a new document; SPAs do client-side navigation so rules have no effect
- **Wrong**: Speculatively prerendering `/logout` or `/checkout/confirm` → **Right**: Prerendering these triggers server-side side effects before the user clicked
- **Wrong**: No vendor chunking → **Right**: Without `manualChunks`, bundlers may re-bundle the same React/lodash code into every route chunk

## See Also

- [Resource Hints](resource-hints.md) — `<link rel="prefetch">` as a lightweight alternative to Speculation Rules
- [Service Worker Caching](service-worker-caching.md) — cached split chunks serve from disk on repeat loads
- Reference: [web.dev: Code splitting](https://web.dev/articles/code-splitting-suspense)
- Reference: [Speculation Rules API](https://developer.chrome.com/docs/web-platform/prerender-pages)
