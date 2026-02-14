---
description: Understand cache bins and their purposes for different types of cached data
---

# Cache Bins

## When to Use

When you need to understand where different types of cached data are stored. Cache bins are logical containers for cache data — each bin can use a different backend, have different expiration policies, and serve different purposes.

## Core Cache Bins

### cache.default

Default cache bin for miscellaneous cached data.

**Typical contents:** Custom module cache data, temporary calculations, fallback for bins without specific configuration.

**Backend recommendation:** Redis/Memcache (high-churn data)

**Gotchas:** Default for new cache data unless specified otherwise. Can grow large on active sites — monitor size.

### cache.bootstrap

Cached data needed during early bootstrap.

**Typical contents:** Module list, system list, hook implementations, container definitions.

**Backend recommendation:** ChainedFastBackend (small, frequently accessed)

**Gotchas:** Cleared very rarely (mostly on module enable/disable). Good candidate for APCu as fast backend. Critical for performance — keep fast.

### cache.config

Configuration object cache.

**Typical contents:** Config entity data, simple configuration, schema data.

**Backend recommendation:** Redis/Memcache (moderate-churn)

**Gotchas:** Invalidated when configuration changes. Not same as config storage (config is stored separately, this caches processed config objects).

### cache.data

General application data cache.

**Typical contents:** Form structures, system information, locale data.

**Backend recommendation:** Redis/Memcache (moderate-churn)

**Gotchas:** Mixed-use bin — can contain both long-lived and short-lived data.

### cache.discovery

Plugin discovery cache.

**Typical contents:** Plugin definitions, annotation discovery results, derivative plugin information.

**Backend recommendation:** ChainedFastBackend (small, stable)

**Gotchas:** Cleared on cache rebuild or plugin changes. Very stable data — excellent ChainedFast candidate.

### cache.dynamic_page_cache

Dynamic Page Cache storage.

**Typical contents:** Page render arrays with placeholders, partial page content for authenticated users.

**Backend recommendation:** Redis/Memcache (high-churn, large items)

**Gotchas:** Large entries (entire page render arrays). High churn on busy sites. Critical for authenticated user performance.

### cache.entity

Entity cache.

**Typical contents:** Loaded entity objects, entity field values, computed entity properties.

**Backend recommendation:** Redis/Memcache (high-access, moderate-churn)

**Gotchas:** Stores entire entity objects (can be large). Automatically managed by entity system. Invalidated by entity cache tags.

### cache.menu

Menu system cache.

**Typical contents:** Menu link trees, menu active trails, breadcrumbs.

**Backend recommendation:** Redis/Memcache (moderate-churn)

**Gotchas:** Varies by menu, language, and active trail contexts. Cleared when menu links change.

### cache.page

Page Cache for anonymous users.

**Typical contents:** Full HTML pages for anonymous users, HTTP response headers.

**Backend recommendation:** Redis/Memcache (large items, high-access)

**Gotchas:** Only for anonymous users. Very large entries (full HTML). External reverse proxy (Varnish) often better than internal page cache.

### cache.render

Render cache.

**Typical contents:** Rendered render arrays, cached components, block output.

**Backend recommendation:** Redis/Memcache (high-churn, varied sizes)

**Gotchas:** Can contain very large entries (complex render arrays). High churn due to fine-grained cache tags. Most-used bin on many sites — monitor size.

### cache.toolbar

Toolbar cache.

**Typical contents:** Toolbar menu structure, admin menu items.

**Backend recommendation:** Database/Redis (low-churn)

**Gotchas:** Only used when toolbar module enabled. Varies by user permissions.

## Custom Cache Bins

Module-defined cache bins for custom data.

**Creation:**
```yaml
# my_module.services.yml
services:
  cache.my_module:
    class: Drupal\Core\Cache\CacheBackendInterface
    tags:
      - { name: cache.bin }
    factory: cache_factory:get
    arguments: [my_module]
```

**Usage:**
```php
$cache = \Drupal::cache('my_module');
$cache->set('my_key', $data);
```

**Gotchas:**
- Define in services.yml to register bin
- Use module name as bin ID by convention
- Configure backend separately if needed

## Common Mistakes

- Storing everything in cache.default — Use specific bins or create custom bin
- Using same backend for all bins — Different bins have different access patterns; optimize per-bin
- Clearing entire bins frequently — Use cache tags for targeted invalidation
- Creating too many custom bins — More bins = more overhead; use tags for logical separation within bin
- Not monitoring bin sizes — Large bins (especially render, page) can cause performance issues

## See Also

- [Cache Backends](cache-backends.md) — Backend types and selection
- [Cache Backend Configuration](cache-backend-configuration.md) — Per-bin configuration
- Reference: `/core/core.services.yml` for core cache bins
