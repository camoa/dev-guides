---
description: Create and invalidate custom cache tags for non-entity data
---

# Custom Cache Tags

## When to Use

When you need to invalidate cached content based on non-entity data. Custom cache tags let you create invalidation triggers for API data, computed values, or external resources.

## Steps

1. **Define custom tag naming convention** — Use module prefix to avoid collisions
   ```php
   // Convention: {module}:{type}:{identifier}
   'my_module:weather:portland'
   'my_module:stock_price:AAPL'
   'my_module:api_response:users'
   ```

2. **Add custom tags when caching**
   ```php
   $build = [
     '#cache' => [
       'tags' => ['my_module:weather:' . $location],
     ],
   ];
   ```

3. **Invalidate tags when source data changes**
   ```php
   // When weather data updates
   \Drupal::service('cache_tags.invalidator')
     ->invalidateTags(['my_module:weather:portland']);
   ```

4. **Consider tag granularity**
   ```php
   // Too specific: per-request tags (don't reuse)
   'my_module:weather:portland:2025-02-14-10:30:00'  // Bad

   // Good: reusable across requests
   'my_module:weather:portland'  // Good
   'my_module:weather_hourly:portland'  // Good (if hourly updates)
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Naming tags | Tag represents entity-like resource | Use `{module}:{type}:{id}` pattern |
| Naming tags | Tag represents collection | Use `{module}:{type}_list` pattern |
| Setting granularity | Data updates frequently | Use more specific tags to avoid over-invalidation |
| Setting granularity | Data updates rarely | Use broader tags to reduce tag count |
| Invalidating | Update affects multiple items | Invalidate all related tags in one call |

## Pattern

**Custom tags for API data**:
```php
// Cache API response with custom tag
$cache = \Drupal::cache('my_module');
$data = $cache->get('api:users');
if (!$data) {
  $users = api_fetch_users();
  $cache->set('api:users', $users, Cache::PERMANENT, [
    'my_module:api_response:users',
  ]);
}

// Invalidate when API data refreshes
\Drupal::service('cache_tags.invalidator')
  ->invalidateTags(['my_module:api_response:users']);
```

**Hierarchical tags**:
```php
// Use multiple tag levels for flexible invalidation
$build = [
  '#cache' => [
    'tags' => [
      'my_module:product:123',           // Specific product
      'my_module:product_category:shoes', // All shoes
      'my_module:products',              // All products
    ],
  ],
];

// Invalidate all shoes
$invalidator->invalidateTags(['my_module:product_category:shoes']);

// Or invalidate all products
$invalidator->invalidateTags(['my_module:products']);
```

Reference: `/core/lib/Drupal/Core/Cache/CacheTagsInvalidatorInterface.php`

## Common Mistakes

- Not using module prefix — Tag collision with other modules
- Creating too many unique tags — Cache tags table grows large; prefer reusable tags
- Using per-request identifiers in tags — Tags should be reusable across requests
- Forgetting to invalidate custom tags — Custom tags never auto-invalidate; must do manually
- Over-invalidating with broad tags — Invalidating `my_module:all_data` clears too much; be specific

## See Also

- [Cache Tags](cache-tags.md) — Core cache tags reference
- [Cache Invalidation Patterns](cache-invalidation-patterns.md) — How to invalidate tags
- Reference: [Custom cache tags best practices](https://www.drupal.org/docs/drupal-apis/cache-api/cache-tags)
