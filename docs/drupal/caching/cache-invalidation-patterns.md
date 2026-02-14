---
description: Invalidate caches when data changes using tags, bins, and time-based expiration
---

# Cache Invalidation Patterns

## When to Use

When you need to clear cached data when source data changes. Cache invalidation removes stale cache entries using cache tags, programmatic deletion, or time-based expiration.

## Steps

1. **Use cache tags for data-driven invalidation** (preferred)
   ```php
   // When rendering, add tags
   $build = [
     '#cache' => ['tags' => ['node:123']],
   ];

   // When data changes, invalidate tags
   \Drupal::service('cache_tags.invalidator')
     ->invalidateTags(['node:123']);
   ```
   Drupal invalidates all cache entries with that tag automatically.

2. **Use entity save/delete for automatic invalidation**
   ```php
   $node->save();  // Automatically invalidates node:123 tag
   $node->delete(); // Automatically invalidates node:123 and node_list tags
   ```
   Entity system handles tag invalidation automatically.

3. **Use cache bin operations for manual clearing**
   ```php
   // Clear specific cache item
   \Drupal::cache('render')->delete($cid);

   // Clear entire bin (expensive, avoid)
   \Drupal::cache('render')->deleteAll();
   ```
   Direct cache bin access for cases where tags don't apply.

4. **Use max-age for time-based expiration**
   ```php
   $build = [
     '#cache' => ['max-age' => 3600],  // Expires after 1 hour
   ];
   ```
   Cache item automatically expires; no manual invalidation needed.

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing invalidation method | Content depends on entities/config | Use cache tags (automatic via entity system) |
| Choosing invalidation method | Content depends on custom data | Create custom cache tags, invalidate programmatically |
| Choosing invalidation method | Content expires by time | Use max-age instead of tags |
| Timing invalidation | Invalidating many tags | Use queue or defer to post-request (avoid blocking response) |

## Pattern

**Tag-based invalidation** (preferred):
```php
// Add tags when caching
$build = [
  '#cache' => [
    'tags' => ['my_module:api_data', 'config:my_module.settings'],
  ],
];

// Invalidate when data changes
\Drupal::service('cache_tags.invalidator')
  ->invalidateTags(['my_module:api_data']);
```

**Bulk invalidation**:
```php
// Invalidate multiple tags at once
$invalidator = \Drupal::service('cache_tags.invalidator');
$invalidator->invalidateTags(['node:123', 'node:456', 'user:789']);
```

**Deferred invalidation** (for expensive operations):
```php
// Queue tag invalidation for post-request processing
$queue = \Drupal::queue('cache_tag_invalidation');
$queue->createItem(['tags' => $tags_to_invalidate]);
```

Reference: `/core/lib/Drupal/Core/Cache/CacheTagsInvalidatorInterface.php`

## Common Mistakes

- Using `deleteAll()` instead of tags — Clears entire bin including valid entries; use targeted tag invalidation
- Invalidating tags synchronously in loops — N tag invalidations in loop blocks response; batch or queue
- Creating per-request cache tags — Tags should be reusable across requests; per-request tags don't help
- Not invalidating custom tags — Custom tags never auto-invalidate; you must invalidate programmatically
- Clearing cache instead of invalidating tags — Full cache clear is nuclear option; use tags for surgical invalidation

## See Also

- [Cache Tags](cache-tags.md) — Understanding cache tags
- [Custom Cache Tags](custom-cache-tags.md) — Creating and managing custom tags
- Reference: [Cache tags invalidation documentation](https://www.drupal.org/docs/drupal-apis/cache-api/cache-tags)
