---
description: "Guide the browser's network scheduler with preconnect, preload, prefetch, and fetchpriority to accelerate LCP and asset delivery."
tldr: "Preconnect for known third-party origins, preload for late-discovered same-origin assets like @font-face fonts, prefetch for next-page bundles; only apply fetchpriority=\"high\" to 1-2 resources or it creates bandwidth contention."
---

# Resource Hints and Fetch Priority

## When to Use

> Resource hints and `fetchpriority` let you guide the browser's network scheduler. Use them when the browser's default discovery order leaves critical resources fetching too late, or when non-critical resources are competing for bandwidth with the LCP element. Applied correctly these produce measurable LCP improvements; misapplied they create contention that makes things worse.

## Decision: Which Hint to Use

| If you need to... | Use | Notes |
|-------------------|-----|-------|
| Start TLS handshake early for a known third-party origin | `<link rel="preconnect">` | Resolves DNS + TCP + TLS. Limit to 2-3 origins; each is an open socket that consumes resources |
| Hint at an origin without keeping a socket open | `<link rel="dns-prefetch">` | DNS only. Use as fallback for origins where preconnect overhead isn't justified |
| Fetch a same-origin asset the browser won't discover until CSS/JS executes (fonts in @font-face, hero background-image) | `<link rel="preload">` | Must include correct `as` attribute. For fonts, always add `crossorigin` even on same-origin |
| Fetch assets for likely next-page navigation before user clicks | `<link rel="prefetch">` | Low-priority background fetch. Browser may ignore under memory pressure |
| Prefetch + fully prerender next page | Speculation Rules API | See [Code Splitting](code-splitting.md) for Speculation Rules |

**Mental model:** "Preconnect for domains, Preload for viewport, Prefetch for futures."

## Decision: `fetchpriority` on Resources

**Baseline Newly Available** since 2024-10-29. Supported: Chrome 103+, Edge 103+, Firefox 132+, Safari 17.2+. Progressive enhancement — browsers that do not support it use default heuristics.

| Resource | Default browser priority | When to override |
|----------|--------------------------|-----------------|
| LCP `<img>` | Medium (in viewport) | `fetchpriority="high"` — browser may still not elevate it enough |
| CSS background-image used as LCP | Not discovered until CSSOM | `<link rel="preload" as="image" fetchpriority="high">` |
| Above-fold carousel image (not LCP) | Medium | `fetchpriority="low"` — it competes with the real LCP |
| `<script async>` for critical interaction | Medium-low | `fetchpriority="high"` — elevate for INP-critical scripts |
| Analytics / tracking scripts | Medium-low | `fetchpriority="low"` — prevent bandwidth competition |
| Background `fetch()` API calls | Medium | `priority: 'low'` option in fetch init |
| Non-critical font preload | High (fonts are high by default) | `fetchpriority="low"` to free bandwidth for LCP image |

**MANDATORY:** Only use `fetchpriority="high"` on at most 1-2 resources. Priority is zero-sum — elevating more than 2 items dilutes the benefit and creates network contention.

## Pattern

```html
<!-- Preconnect for critical third-party origins -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="dns-prefetch" href="https://analytics.example.com">

<!-- Preload: LCP background-image not in HTML -->
<link rel="preload" href="/images/hero-bg.webp" as="image" fetchpriority="high">

<!-- Preload: font not discoverable until @font-face parses -->
<link rel="preload" href="/fonts/brand.woff2" as="font" type="font/woff2" crossorigin>

<!-- Prefetch: next-page bundle user will likely navigate to -->
<link rel="prefetch" href="/js/detail-page.js" as="script">
```

```javascript
// Deprioritize background analytics fetch
fetch('/api/analytics', {
  method: 'POST',
  body: JSON.stringify(payload),
  priority: 'low'   // 'low' | 'auto' | 'high'
});
```

## Common Mistakes

- Preloading everything — preloads compete with each other; limit to 2 image preloads and 2-3 essential fonts per page
- `<link rel="preload" as="font">` without `crossorigin` — font preload is ignored without it, even on same-origin
- Using `fetchpriority="high"` on every above-fold image — cascades to contention; only the LCP candidate benefits
- Using `importance` attribute — deprecated, never implemented consistently; use `fetchpriority`
- Preloading resources that are already in the HTML `<img src>` tag and discoverable by the preload scanner — wastes a duplicate request slot

## See Also

- [LCP Image Optimization](lcp-image-optimization.md) — `fetchpriority` applied specifically to LCP images
- [Web Font Performance](web-font-performance.md) — coordinating font preloads
- Reference: [web.dev: Resource hints](https://web.dev/learn/performance/resource-hints)
- Reference: [web.dev: Fetch Priority](https://web.dev/articles/fetch-priority)
