---
description: Guide the browser's network scheduler with preconnect, preload, prefetch, and fetchpriority to accelerate LCP and asset delivery.
tldr: Preconnect for known third-party origins (DNS+TCP+TLS), preload for late-discovered same-origin assets like @font-face fonts, prefetch for next-page bundles; only apply fetchpriority="high" to 1-2 resources or it creates bandwidth contention.
---

# Resource Hints and Fetch Priority

## When to Use

> Resource hints and `fetchpriority` let you guide the browser's network scheduler. Use them when the browser's default discovery order leaves critical resources fetching too late, or when non-critical resources are competing for bandwidth with the LCP element.

**Mental model:** "Preconnect for domains, Preload for viewport, Prefetch for futures."

## Decision: Which Hint to Use

| If you need to... | Use | Notes |
|-------------------|-----|-------|
| Start TLS handshake early for a known third-party origin | `<link rel="preconnect">` | Resolves DNS + TCP + TLS. Limit to 2-3 origins; each is an open socket |
| Hint at an origin without keeping a socket open | `<link rel="dns-prefetch">` | DNS only. Fallback for origins where preconnect overhead isn't justified |
| Fetch a same-origin asset the browser won't discover until CSS/JS executes | `<link rel="preload">` | Must include correct `as` attribute. For fonts, always add `crossorigin` |
| Fetch assets for likely next-page navigation | `<link rel="prefetch">` | Low-priority background fetch. Browser may ignore under memory pressure |
| Prefetch + fully prerender next page | Speculation Rules API | See [Code Splitting](code-splitting.md) |

## Decision: `fetchpriority` on Resources

**Baseline Newly Available** since 2024-10-29. Supported: Chrome 103+, Edge 103+, Firefox 132+, Safari 17.2+.

| Resource | Default browser priority | When to override |
|----------|--------------------------|-----------------|
| LCP `<img>` | Medium (in viewport) | `fetchpriority="high"` |
| CSS background-image used as LCP | Not discovered until CSSOM | `<link rel="preload" as="image" fetchpriority="high">` |
| Above-fold carousel image (not LCP) | Medium | `fetchpriority="low"` — it competes with the real LCP |
| `<script async>` for critical interaction | Medium-low | `fetchpriority="high"` |
| Analytics / tracking scripts | Medium-low | `fetchpriority="low"` — prevent bandwidth competition |
| Non-critical font preload | High (fonts are high by default) | `fetchpriority="low"` to free bandwidth for LCP image |

**MANDATORY:** Only use `fetchpriority="high"` on at most 1-2 resources. Priority is zero-sum — elevating more dilutes the benefit.

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

- **Wrong**: Preloading everything → **Right**: Limit to 2 image preloads and 2-3 essential fonts; preloads compete with each other
- **Wrong**: `<link rel="preload" as="font">` without `crossorigin` → **Right**: Font preload is ignored without it, even on same-origin
- **Wrong**: `fetchpriority="high"` on every above-fold image → **Right**: Only the LCP candidate benefits from high priority
- **Wrong**: Using `importance` attribute → **Right**: Deprecated and never implemented consistently; use `fetchpriority`
- **Wrong**: Preloading resources already in the HTML `<img src>` tag → **Right**: The preload scanner already discovers them; adding a preload wastes a request slot

## See Also

- [LCP Image Optimization](lcp-image-optimization.md) — `fetchpriority` applied specifically to LCP images
- [Web Font Performance](web-font-performance.md) — coordinating font preloads
- Reference: [web.dev: Resource hints](https://web.dev/articles/resource-hints)
- Reference: [web.dev: Fetch Priority](https://web.dev/articles/fetch-priority)
