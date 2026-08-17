---
description: Drupal caching decision guides — cache metadata, backends, invalidation, and performance
tracks:
  - project: drupal
    channel: stable
    verified: 2026-02-14
guide-meta:
  concepts:
    - cache tags
    - cache contexts
    - cache max-age
    - cache metadata trinity
    - cache backends
    - Redis
    - Memcache
    - render caching
    - lazy builders
    - BigPipe
    - Dynamic Page Cache
    - cache invalidation
  not:
    - HTTP caching headers (see drupal/security)
    - CDN configuration
  requires: []
  complements:
    - drupal/render-api
    - drupal/blocks
    - drupal/views
  specializes: ""
  category: drupal
---

# Drupal Caching

**Philosophy**: Configuration first. Prioritize declarative caching (cache metadata in render arrays, config schema for cache backends) over programmatic approaches.

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand Drupal's caching layers and when to use each | [Cache System Overview](cache-system-overview.md) | When you need to understand which caching layer to use for different scenarios — page cache for anonymous users, dynamic page cache for authenticated users, render cache for reusable components, or programmatic cache bins for custom data. |
| Learn the three pillars of cache metadata | [Cache Metadata Trinity](cache-metadata-trinity.md) | Every time you cache a render array or create a cacheable dependency. All three metadata properties — cache tags, cache contexts, and max-age — must be considered together. |
| Add cache tags to invalidate on entity/config changes | [Cache Tags](cache-tags.md) | When you need to invalidate cached content when specific data changes. Cache tags declare "this cached item depends on X" — when X changes, Drupal automatically invalidates all cache entries with that tag. |
| Vary cached content by URL, user, language, etc. | [Cache Contexts](cache-contexts.md) | When cached content varies based on request context. Cache contexts create separate cache entries for different variations — e.g., one cached version per language, per user role, per URL path. |
| Set how long content can be cached | [Cache Max-Age](cache-max-age.md) | When you need to set expiration on cached content. Max-age is the third pillar of cache metadata (alongside tags and contexts) and controls how long cached data remains valid. |
| Choose and configure a cache backend (Redis, Memcache, APCu) | [Cache Backends](cache-backends.md) | When you need to choose where cached data is stored. Cache backends determine storage mechanism — database (default), memory (APCu, Redis, Memcache), or specialized backends (chained, null). |
| Understand cache bins and their purposes | [Cache Bins](cache-bins.md) | When you need to understand where different types of cached data are stored. Cache bins are logical containers for cache data — each bin can use a different backend, have different expiration policies, and serve different purposes. |
| Cache render arrays and understand render caching | [Render Caching](render-caching.md) | When you need to cache rendered output of render arrays. Render caching stores the final rendered HTML along with cache metadata, avoiding expensive re-rendering on subsequent requests. |
| Handle cache metadata bubbling in nested render arrays | [BubbleableMetadata & Cache Bubbling](bubbleable-metadata-cache-bubbling.md) | When you need to propagate cache metadata from child render arrays to parent. Cache bubbling ensures that when a parent element is cached, it includes all cacheability requirements from its children. |
| Defer expensive rendering with placeholders | [Lazy Builders](lazy-builders.md) | When you need to defer expensive or user-specific rendering until after the main page is cached. Lazy builders create placeholders in cached content that are replaced with personalized or dynamic content during rendering. |
| Understand anonymous page caching | [Page Cache](page-cache.md) | When you need to cache full HTML pages for anonymous users. Page Cache (Internal Page Cache module) stores complete rendered pages, serving them without bootstrapping Drupal. |
| Cache pages for authenticated users | [Dynamic Page Cache](dynamic-page-cache.md) | When you need to cache pages for authenticated users or pages with personalized content. Dynamic Page Cache caches page structure while excluding personalized parts (converted to placeholders). |
| Progressively render expensive content | [BigPipe](bigpipe.md) | When you need to progressively render expensive content. BigPipe sends page skeleton immediately, then streams placeholder replacements as they become ready, improving perceived performance. |
| Invalidate caches when data changes | [Cache Invalidation Patterns](cache-invalidation-patterns.md) | When you need to clear cached data when source data changes. Cache invalidation removes stale cache entries using cache tags, programmatic deletion, or time-based expiration. |
| Create and invalidate custom cache tags | [Custom Cache Tags](custom-cache-tags.md) | When you need to invalidate cached content based on non-entity data. Custom cache tags let you create invalidation triggers for API data, computed values, or external resources. |
| Configure Redis or Memcache backends in settings.php | [Cache Backend Configuration](cache-backend-configuration.md) | When you need to configure cache backends (Redis, Memcache, APCu) in settings.php. Backend configuration determines where cached data is stored and how it's accessed. |
| Follow caching best practices | [Best Practices & Patterns](best-practices-patterns.md) | When you need proven patterns for effective caching. These practices maximize cache hit rates, minimize stale content, and maintain performance. |
| Avoid common caching mistakes | [Anti-Patterns & Common Mistakes](anti-patterns-common-mistakes.md) | When you need to avoid common caching mistakes that cause bugs, performance issues, or stale content. |
| Ensure cache security and performance | [Security & Performance](security-performance.md) | When you need to ensure cache security and optimal performance. Caching affects both security (sensitive data leakage) and performance (cache hit rates, memory usage). |
| Find core cache files and APIs | [Code Reference Map](code-reference-map.md) |  |
