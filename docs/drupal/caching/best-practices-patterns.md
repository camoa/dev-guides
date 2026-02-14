---
description: Follow proven caching best practices for maximum cache hit rates
---

# Best Practices & Patterns

## When to Use

When you need proven patterns for effective caching. These practices maximize cache hit rates, minimize stale content, and maintain performance.

## Decision

| Practice | Why | When to apply |
|---|---|---|
| Always set all three cache metadata properties | Missing tags/contexts/max-age causes bugs | Every cacheable render array |
| Prefer cache tags over max-age for data invalidation | Tags invalidate immediately when source changes; max-age waits | Content that updates irregularly |
| Use specific cache tags over list tags | `node:123` better than `node_list` | When you know which entities are used |
| Use minimal cache contexts | Each context multiplies cache variations | Only add contexts for actual variation |
| Add cache metadata at lowest level possible | Metadata bubbles up automatically | On child elements, not duplicated on parents |
| Use lazy builders for expensive per-user content | Enables caching of page structure | User-specific content >100ms render time |
| Use `Cache::mergeMaxAges()` when combining metadata | Ensures lowest max-age wins | Programmatically merging cache metadata |
| Rely on automatic cache tag invalidation | Entity system invalidates tags on save/delete | Entity-based content (most Drupal content) |
| Use custom cache bins for custom data | Isolates custom cache from core bins | Caching non-render-array data |
| Test cache metadata with Cache Metadata Debugging | Verifies tags/contexts/max-age correct | Development and debugging |

## Pattern

**Complete cache metadata**:
```php
$build = [
  '#cache' => [
    'tags' => $entity->getCacheTags(),  // What to invalidate
    'contexts' => ['user.roles'],       // How to vary
    'max-age' => Cache::PERMANENT,      // When to expire (rely on tags)
  ],
];
```

**Minimal contexts**:
```php
// Bad: too many contexts
'contexts' => ['user', 'url', 'theme', 'timezone']

// Good: only necessary contexts
'contexts' => ['user.roles', 'url.path']
```

**Hierarchical tags** (flexible invalidation):
```php
'tags' => [
  'node:123',               // Specific node
  'node_type:article',      // All articles
  'my_module:featured',     // All featured content
]
```

**Dependency injection for cache bins**:
```php
// Don't use static call
\Drupal::cache('my_bin')->set($cid, $data);

// Use DI
public function __construct(CacheBackendInterface $cache) {
  $this->cache = $cache;
}
```

Reference: [Drupal caching best practices](https://pantheon.io/learning-center/drupal/caching)

## Common Mistakes

- Setting cache metadata on parent and children — Metadata bubbles; set on children only
- Using `user` context when `user.roles` sufficient — Creates per-user cache entries unnecessarily
- Forgetting `#cache['keys']` on cached render arrays — Render cache not used without keys
- Clearing full cache instead of invalidating tags — Expensive and unnecessary; use tags
- Not testing cache invalidation — Verify that tag invalidation clears correct cache entries

## See Also

- [Cache Metadata Trinity](cache-metadata-trinity.md) — Required metadata properties
- [Anti-Patterns & Common Mistakes](anti-patterns-common-mistakes.md) — What to avoid
- Reference: [Add cache metadata to render arrays tutorial](https://drupalize.me/tutorial/add-cache-metadata-render-arrays)
