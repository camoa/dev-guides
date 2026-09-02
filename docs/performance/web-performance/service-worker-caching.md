---
description: "Implement CacheFirst, NetworkFirst, and StaleWhileRevalidate strategies with Workbox for offline support and instant repeat-visit performance."
tldr: "Use NetworkFirst for HTML navigation, CacheFirst for versioned static assets, StaleWhileRevalidate for non-critical API feeds; always add ExpirationPlugin to prevent unbounded cache growth; opaque responses can consume ~7MB of quota each."
---

# Service Worker Caching

## When to Use

> Service workers intercept network requests and serve from a local cache, enabling repeat visits to be nearly instant and sites to work offline. Use Workbox to implement strategies without low-level cache API boilerplate. Choose the strategy per resource type — there is no single correct strategy for an entire site.

## Decision: Caching Strategy by Resource Type

| Resource type | Strategy | Rationale |
|---------------|----------|-----------|
| HTML documents (navigation requests) | **NetworkFirst** | Always serve fresh HTML; fall back to cached version only if offline |
| Versioned static assets — JS/CSS bundles with content hash, fonts | **CacheFirst** | Immutable files: once cached, serve from disk forever (until cache is purged) |
| API responses where slight staleness is acceptable | **StaleWhileRevalidate** | Serve immediately from cache; silently refresh cache in the background |
| User-specific or authentication-gated content | **NetworkOnly** | Never cache private data in a service worker |
| Third-party resources without CORS headers (opaque responses) | **NetworkFirst** or **StaleWhileRevalidate** with size limits | Opaque responses consume significant quota; `CacheFirst` risks storing errors |

## Pattern

```javascript
import { registerRoute } from 'workbox-routing';
import { CacheFirst, StaleWhileRevalidate, NetworkFirst } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

// HTML: always attempt network first
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst({ cacheName: 'pages-cache' })
);

// Versioned static assets: cache first with expiry safety net
registerRoute(
  ({ request }) => ['style', 'script', 'font'].includes(request.destination),
  new CacheFirst({
    cacheName: 'static-resources',
    plugins: [
      new CacheableResponsePlugin({ statuses: [0, 200] }),
      new ExpirationPlugin({ maxEntries: 60, maxAgeSeconds: 30 * 24 * 60 * 60 }),
    ],
  })
);

// API: stale-while-revalidate for non-critical content feeds
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/v1/content'),
  new StaleWhileRevalidate({
    cacheName: 'api-cache',
    plugins: [new CacheableResponsePlugin({ statuses: [0, 200] })],
  })
);
```

## Common Mistakes

- Caching opaque responses with `CacheFirst` — opaque responses (from cross-origin, non-CORS resources) each consume roughly 7MB of quota on some browsers regardless of actual size; stale cached errors serve silently
- Caching POST requests — service workers cannot cache non-GET requests natively; use Background Sync for offline POST queuing
- No `ExpirationPlugin` on any cache — without expiry limits, the service worker grows unbounded until the browser's storage quota is exhausted and the cache is evicted entirely
- Forgetting to update asset hashes when redeploying with CacheFirst — users get cached old files indefinitely; always use content-hash filenames for immutable assets
- Using `CacheFirst` for HTML — users see stale application shells; always use `NetworkFirst` for navigation requests

## See Also

- [Code Splitting](code-splitting.md) — versioned chunk files are ideal candidates for CacheFirst
- Reference: [Workbox documentation](https://developer.chrome.com/docs/workbox/)
