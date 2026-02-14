---
description: Find cache-related core files, APIs, and implementation locations
---

# Code Reference Map

## When to Use

When you need to find cache-related code in Drupal core. This reference maps cache concepts to their implementation files.

## Core Cache API

| Component | File path | Description |
|---|---|---|
| CacheBackendInterface | `core/lib/Drupal/Core/Cache/CacheBackendInterface.php` | Cache backend interface (get, set, delete) |
| CacheableMetadata | `core/lib/Drupal/Core/Cache/CacheableMetadata.php` | Cache metadata value object |
| BubbleableMetadata | `core/lib/Drupal/Core/Render/BubbleableMetadata.php` | Bubbleable cache metadata (includes attachments) |
| CacheableDependencyInterface | `core/lib/Drupal/Core/Cache/CacheableDependencyInterface.php` | Interface for cacheable objects |
| RefinableCacheableDependencyInterface | `core/lib/Drupal/Core/Cache/RefinableCacheableDependencyInterface.php` | Refinable cacheable dependency |
| Cache | `core/lib/Drupal/Core/Cache/Cache.php` | Cache helper class (merge functions, constants) |
| CacheTagsInvalidatorInterface | `core/lib/Drupal/Core/Cache/CacheTagsInvalidatorInterface.php` | Cache tag invalidation interface |

## Cache Backends

| Backend | File path | Description |
|---|---|---|
| DatabaseBackend | `core/lib/Drupal/Core/Cache/DatabaseBackend.php` | Default database cache backend |
| ApcuBackend | `core/lib/Drupal/Core/Cache/ApcuBackend.php` | APCu memory cache backend |
| MemoryBackend | `core/lib/Drupal/Core/Cache/MemoryBackend.php` | PHP memory cache backend (per-request) |
| PhpBackend | `core/lib/Drupal/Core/Cache/PhpBackend.php` | PHP file cache backend |
| NullBackend | `core/lib/Drupal/Core/Cache/NullBackend.php` | Null cache backend (no caching) |
| ChainedFastBackend | `core/lib/Drupal/Core/Cache/ChainedFastBackend.php` | Chained fast backend (APCu + consistent) |
| BackendChain | `core/lib/Drupal/Core/Cache/BackendChain.php` | Backend chain wrapper |

## Cache Contexts

| Context type | File path | Description |
|---|---|---|
| CacheContextInterface | `core/lib/Drupal/Core/Cache/Context/CacheContextInterface.php` | Cache context interface |
| CalculatedCacheContextInterface | `core/lib/Drupal/Core/Cache/Context/CalculatedCacheContextInterface.php` | Calculated context interface |
| UserCacheContext | `core/lib/Drupal/Core/Cache/Context/UserCacheContext.php` | User ID cache context |
| UserRolesCacheContext | `core/lib/Drupal/Core/Cache/Context/UserRolesCacheContext.php` | User roles cache context |
| UrlCacheContext | `core/lib/Drupal/Core/Cache/Context/UrlCacheContext.php` | URL cache context |
| LanguagesCacheContext | `core/lib/Drupal/Core/Cache/Context/LanguagesCacheContext.php` | Languages cache context |
| RouteCacheContext | `core/lib/Drupal/Core/Cache/Context/RouteCacheContext.php` | Route cache context |
| ThemeCacheContext | `core/lib/Drupal/Core/Cache/Context/ThemeCacheContext.php` | Theme cache context |
| SessionCacheContext | `core/lib/Drupal/Core/Cache/Context/SessionCacheContext.php` | Session cache context |

All cache contexts: `core/lib/Drupal/Core/Cache/Context/` directory

## Render Caching

| Component | File path | Description |
|---|---|---|
| RenderCache | `core/lib/Drupal/Core/Render/RenderCache.php` | Render cache implementation |
| Renderer | `core/lib/Drupal/Core/Render/Renderer.php` | Main renderer (handles cache metadata bubbling) |
| PlaceholderInterface | `core/lib/Drupal/Core/Render/Placeholder/PlaceholderInterface.php` | Placeholder interface |
| PlaceholderStrategy | `core/lib/Drupal/Core/Render/Placeholder/PlaceholderStrategy.php` | Placeholder strategy base |
| SingleFlushStrategy | `core/lib/Drupal/Core/Render/Placeholder/SingleFlushStrategy.php` | Single flush placeholder strategy |

Placeholder strategies: `core/lib/Drupal/Core/Render/Placeholder/` directory

## Page Caching

| Module/Component | File path | Description |
|---|---|---|
| Page Cache module | `core/modules/page_cache/` | Internal page cache for anonymous users |
| PageCache middleware | `core/modules/page_cache/src/StackMiddleware/PageCache.php` | Page cache HTTP middleware |
| Dynamic Page Cache module | `core/modules/dynamic_page_cache/` | Page cache for authenticated users |
| DynamicPageCacheSubscriber | `core/modules/dynamic_page_cache/src/EventSubscriber/DynamicPageCacheSubscriber.php` | Dynamic page cache event subscriber |
| BigPipe module | `core/modules/big_pipe/` | Progressive rendering module |
| BigPipe | `core/modules/big_pipe/src/Render/BigPipe.php` | BigPipe renderer |

## Services & Configuration

| Component | File path | Description |
|---|---|---|
| Cache service definitions | `core/core.services.yml` | Cache bin service definitions (search "cache.") |
| Cache backend factory | `core/lib/Drupal/Core/Cache/CacheFactory.php` | Cache backend factory |
| Default settings | `sites/default/default.settings.php` | Cache backend configuration examples |

## See Also

- All sections reference specific files in "Reference:" notes
- Reference: `/core/lib/Drupal/Core/Cache/` — Core cache directory
- Reference: [Drupal API documentation](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Cache!Cache.php/class/Cache)
