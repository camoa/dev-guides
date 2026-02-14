---
description: Understand anonymous page caching with Drupal's Internal Page Cache
---

# Page Cache

## When to Use

When you need to cache full HTML pages for anonymous users. Page Cache (Internal Page Cache module) stores complete rendered pages, serving them without bootstrapping Drupal.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Cache pages for anonymous users | Page Cache module | Fastest delivery — serves HTML without bootstrap; only for anonymous |
| Cache pages for authenticated users | Dynamic Page Cache | Page Cache only works for anonymous; authenticated users need Dynamic Page Cache |
| Cache with external reverse proxy | Varnish/Cloudflare + Page Cache | External cache offloads traffic from PHP; Page Cache provides fallback |
| Bypass page cache for certain paths | Cache contexts or max-age 0 | Add `session` context or set `max-age = 0` to prevent page caching |

**Page Cache only works for anonymous users** — authenticated users get Dynamic Page Cache instead.

## Pattern

**Page Cache is automatic** — no configuration in code needed:
```php
// Render array at page level automatically uses Page Cache if:
// 1. User is anonymous
// 2. Request is GET or HEAD
// 3. No session cookies present
// 4. Response is cacheable (max-age > 0)
```

**Preventing page caching**:
```php
// Add session context
$build['#cache']['contexts'][] = 'session';

// Or set max-age 0
$build['#cache']['max-age'] = 0;
```

**Cache headers set automatically**:
```php
// Page Cache sets HTTP headers:
// Cache-Control: max-age=X, public
// X-Drupal-Cache: HIT or MISS
```

Reference: `/core/modules/page_cache/src/StackMiddleware/PageCache.php`

## Common Mistakes

- Expecting Page Cache for authenticated users — Page Cache skipped when session exists; use Dynamic Page Cache
- Adding session context to prevent caching — Works, but prefer explicit max-age 0 for clarity
- Storing user-specific content in Page Cache — Page Cache is anonymous-only; user content automatically uses Dynamic Page Cache
- Not testing with external cache — Page Cache headers used by external caches (Varnish); test integration
- Clearing Page Cache frequently — Use cache tags for targeted invalidation; clearing entire Page Cache expensive

## See Also

- [Dynamic Page Cache](dynamic-page-cache.md) — Caching for authenticated users
- [Cache Tags](cache-tags.md) — Invalidating cached pages
- Reference: [Internal Page Cache documentation](https://www.drupal.org/docs/administering-a-drupal-site/internal-page-cache)
