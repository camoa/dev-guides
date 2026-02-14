---
description: Learn the three pillars of cache metadata — tags, contexts, and max-age
---

# Cache Metadata Trinity

## When to Use

Every time you cache a render array or create a cacheable dependency. All three metadata properties — cache tags, cache contexts, and max-age — must be considered together. Missing any of them causes caching bugs.

## Decision

| Metadata property | Controls... | Use when... |
|---|---|---|
| Cache tags | **Invalidation** — when to throw away cached data | Cached content depends on entities, config, or custom data that can change |
| Cache contexts | **Variation** — different versions of cached data | Cached content differs by URL, user, language, or other request context |
| Cache max-age | **Expiration** — how long data is valid | Cached content becomes stale after time period or depends on external data |

**All three must be set** on every cacheable render array:
- **Tags** default to `[]` (never invalidates) — usually wrong unless truly static
- **Contexts** default to `[]` (same for all requests) — usually wrong unless global
- **Max-age** defaults to `Cache::PERMANENT` — usually wrong unless truly permanent

## Pattern

**Complete cache metadata** (all three properties):
```php
$build = [
  '#markup' => $content,
  '#cache' => [
    'tags' => ['node:123', 'user:456'],        // Invalidate when these change
    'contexts' => ['user.roles', 'url.path'],   // Vary by these request properties
    'max-age' => 3600,                          // Expire after 1 hour
  ],
];
```

**Using CacheableMetadata object**:
```php
$metadata = new CacheableMetadata();
$metadata->addCacheTags(['node:123']);
$metadata->addCacheContexts(['user']);
$metadata->setCacheMaxAge(3600);
$metadata->applyTo($build);
```

Reference: `/core/lib/Drupal/Core/Cache/CacheableMetadata.php`

## Common Mistakes

- Setting only tags without contexts — Content varies by user but served from cache to wrong users
- Setting only contexts without tags — Cache never invalidates when source data changes
- Using `Cache::PERMANENT` for entity-derived content — Content never updates when entity changes (use tags instead)
- Copying cache metadata without understanding — Each property serves different purpose; understand what you're declaring
- Forgetting to merge max-age (using lowest) — Child element with max-age 0 makes parent uncacheable; always use `Cache::mergeMaxAges()`

## See Also

- [Cache Tags](cache-tags.md) — Detailed cache tags reference
- [Cache Contexts](cache-contexts.md) — All available cache contexts
- [Cache Max-Age](cache-max-age.md) — How to set expiration
- Reference: [Cacheability of render arrays](https://www.drupal.org/docs/drupal-apis/render-api/cacheability-of-render-arrays)
