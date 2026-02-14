---
description: Understand Drupal's caching layers and when to use each one
---

# Cache System Overview

## When to Use

When you need to understand which caching layer to use for different scenarios — page cache for anonymous users, dynamic page cache for authenticated users, render cache for reusable components, or programmatic cache bins for custom data.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Cache full HTML pages for anonymous users | Page Cache module | Fastest possible delivery — serves cached HTML without bootstrapping Drupal |
| Cache pages for authenticated users | Dynamic Page Cache module | Caches page structure while excluding personalized parts (turned into placeholders) |
| Cache expensive render arrays/components | Render cache (#cache in render array) | Reuses rendered output across requests; cache metadata automatically bubbles up |
| Cache custom data (API responses, calculations) | Cache bins (cache.default, custom bins) | Store arbitrary data with expiration and tags; use DI to inject cache backend |
| Progressively load expensive content | BigPipe + lazy builders | Sends page skeleton immediately, streams expensive parts as they become ready |
| Cache computed values tied to entities | Entity cache (automatic) | Entities are automatically cached in `cache.entity` bin; use cache tags to invalidate |

**Caching layers hierarchy** (innermost to outermost):
1. **Entity cache** — automatic, stores loaded entities
2. **Render cache** — caches render arrays with cache metadata
3. **Dynamic Page Cache** — caches pages with placeholders for authenticated users
4. **Page Cache** — caches full HTML for anonymous users
5. **External CDN/reverse proxy** (Varnish, Cloudflare) — uses cache headers from Drupal

## Pattern

**Declarative render caching** (preferred):
```php
$build = [
  '#markup' => $expensive_content,
  '#cache' => [
    'keys' => ['my_module', 'expensive_component'],
    'contexts' => ['user', 'url.path'],
    'tags' => ['node:123', 'config:my_module.settings'],
    'max-age' => 3600,
  ],
];
```

**Programmatic cache bin usage** (when declarative isn't sufficient):
```php
$cache = \Drupal::cache('my_custom_bin');
$data = $cache->get('my_cache_key');
if (!$data) {
  $value = expensive_calculation();
  $cache->set('my_cache_key', $value, time() + 3600, ['custom:tag']);
}
```

Reference: `/core/lib/Drupal/Core/Cache/CacheBackendInterface.php`, `/core/modules/page_cache/`, `/core/modules/dynamic_page_cache/`

## Common Mistakes

- Using programmatic cache bins for render arrays — Use `#cache` property in render arrays instead (enables automatic bubbling)
- Forgetting cache metadata — Cache without tags/contexts becomes stale and causes incorrect content display
- Over-caching authenticated user content in Page Cache — Page Cache only works for anonymous; use Dynamic Page Cache for authenticated
- Bypassing cache metadata bubbling — Always use `CacheableMetadata::createFromObject()` when adding dependencies, never manually set cache keys
- Clearing all caches to fix cache issues — Use targeted cache tag invalidation instead; full cache clear is expensive and unnecessary

## See Also

- [Cache Metadata Trinity](cache-metadata-trinity.md) — Learn the three required cache metadata properties
- [Best Practices & Patterns](best-practices-patterns.md) — Follow proven caching patterns
- Reference: [Drupal Cache API documentation](https://www.drupal.org/docs/8/api/cache-api/cache-api)
