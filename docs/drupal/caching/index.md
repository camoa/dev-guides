---
description: Drupal caching decision guides — cache metadata, backends, invalidation, and performance
---

# Drupal Caching

**Philosophy**: Configuration first. Prioritize declarative caching (cache metadata in render arrays, config schema for cache backends) over programmatic approaches.

## I need to...

| I need to... | Guide |
|---|---|
| Understand Drupal's caching layers and when to use each | [Cache System Overview](cache-system-overview.md) |
| Learn the three pillars of cache metadata | [Cache Metadata Trinity](cache-metadata-trinity.md) |
| Add cache tags to invalidate on entity/config changes | [Cache Tags](cache-tags.md) |
| Vary cached content by URL, user, language, etc. | [Cache Contexts](cache-contexts.md) |
| Set how long content can be cached | [Cache Max-Age](cache-max-age.md) |
| Choose and configure a cache backend (Redis, Memcache, APCu) | [Cache Backends](cache-backends.md) |
| Understand cache bins and their purposes | [Cache Bins](cache-bins.md) |
| Cache render arrays and understand render caching | [Render Caching](render-caching.md) |
| Handle cache metadata bubbling in nested render arrays | [BubbleableMetadata & Cache Bubbling](bubbleable-metadata-cache-bubbling.md) |
| Defer expensive rendering with placeholders | [Lazy Builders](lazy-builders.md) |
| Understand anonymous page caching | [Page Cache](page-cache.md) |
| Cache pages for authenticated users | [Dynamic Page Cache](dynamic-page-cache.md) |
| Progressively render expensive content | [BigPipe](bigpipe.md) |
| Invalidate caches when data changes | [Cache Invalidation Patterns](cache-invalidation-patterns.md) |
| Create and invalidate custom cache tags | [Custom Cache Tags](custom-cache-tags.md) |
| Configure Redis or Memcache backends in settings.php | [Cache Backend Configuration](cache-backend-configuration.md) |
| Follow caching best practices | [Best Practices & Patterns](best-practices-patterns.md) |
| Avoid common caching mistakes | [Anti-Patterns & Common Mistakes](anti-patterns-common-mistakes.md) |
| Ensure cache security and performance | [Security & Performance](security-performance.md) |
| Find core cache files and APIs | [Code Reference Map](code-reference-map.md) |
