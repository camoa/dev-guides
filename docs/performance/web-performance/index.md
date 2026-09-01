---
description: Web Performance — Core Web Vitals optimization, LCP/INP/CLS patterns, resource hints, JS scheduling, service workers, and font loading.
tracks: []
guide-meta:
  concepts:
    - Core Web Vitals
    - LCP
    - INP
    - CLS
    - TTFB
    - fetchpriority
    - content-visibility
    - service worker
    - Workbox
    - code splitting
    - web fonts
    - font-display
    - scheduler.yield
    - scheduler.postTask
    - Long Animation Frames
    - preconnect
    - preload
    - prefetch
    - Speculation Rules API
    - critical rendering path
    - render-blocking
  not:
    - Drupal caching (drupal/caching)
    - CSS animation performance (css/css-craft)
    - image format selection (media/image-media-craft)
  requires: []
  complements:
    - css/css-craft
    - js/interaction-craft
    - media/image-media-craft
  specializes: ""
  category: performance
---

# Web Performance

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand LCP, INP, CLS, TTFB thresholds and collect field data | [Core Web Vitals Overview](core-web-vitals-overview.md) | Use when diagnosing which Core Web Vital to investigate first; INP replaced FID in March 2024; always confirm fixes in CrUX field data, not just Lighthouse lab scores. |
| Eliminate render-blocking CSS and JS | [Critical Rendering Path](critical-rendering-path.md) | Inline only above-fold CSS (~14KB target), use `<script defer>` for app JS and `<script async>` for independent scripts; CSS `@import` inside stylesheets creates sequential request chains that block CSSOM — replace with parallel `<link>` tags. |
| Guide the browser's network scheduler with preconnect, preload, and prefetch | [Resource Hints and Fetch Priority](resource-hints.md) | Preconnect for known third-party origins (DNS+TCP+TLS), preload for late-discovered same-origin assets like @font-face fonts, prefetch for next-page bundles; only apply fetchpriority="high" to 1-2 resources or it creates bandwidth contention. |
| Optimize the LCP image with fetchpriority and correct attributes | [LCP Image Optimization](lcp-image-optimization.md) | Add `fetchpriority="high"` and remove `loading="lazy"` on the LCP image; always set `width`/`height` to prevent CLS; JS-rendered LCP elements add hundreds of ms — move them to server-rendered HTML. |
| Break up long JS tasks to keep INP under 200ms | [INP: Scheduler API and Task Splitting](inp-scheduler-api.md) | Yield mid-loop every 50ms budget using `scheduler.yield()` (Chrome 129+/Edge 129+/Firefox 142+; no Safari) with a `setTimeout(0)` fallback; use the `scrollend` event instead of `scroll` for expensive post-scroll work. |
| Collect INP subparts and slow-script data from real users | [INP: Field Measurement](inp-field-measurement.md) | Use `web-vitals/attribution` to beacon inputDelay/processingDuration/presentationDelay; Long Animation Frames API (Chrome/Edge only) profiles heavy scripts in production; use `fetchLater` (Chrome/Edge only, polyfill needed) for reliable beacon delivery on page unload. |
| Skip rendering work for off-screen sections | [CSS Containment Performance](css-containment-performance.md) | Apply `content-visibility: auto` + `contain-intrinsic-size` to confirmed-off-screen sections to skip layout/paint; never apply to above-fold content; use `content-visibility: hidden` for SPA view caching but beware it removes content from the a11y tree. |
| Implement CacheFirst / StaleWhileRevalidate / NetworkFirst service worker strategies | [Service Worker Caching](service-worker-caching.md) | Use NetworkFirst for HTML navigation, CacheFirst for versioned static assets, StaleWhileRevalidate for non-critical API feeds; always add ExpirationPlugin to prevent unbounded cache growth; opaque responses can consume ~7MB of quota each — never use CacheFirst for them. |
| Split JS bundles so initial load only parses what's needed | [Code Splitting](code-splitting.md) | Use dynamic `import()` on first interaction for features never needed on initial load; use Speculation Rules API (Chrome/Edge only) for near-instant next-page prerender; never speculatively prerender state-changing URLs like /logout or /checkout. |
| Preload fonts, choose font-display, eliminate font-swap CLS | [Web Font Performance](web-font-performance.md) | Use `font-display: swap` for body text with fallback metric overrides (`size-adjust`, `ascent-override`) to minimize CLS; preload only the primary weight of above-fold fonts; always include `crossorigin` on font preloads or the preload is silently ignored. |
