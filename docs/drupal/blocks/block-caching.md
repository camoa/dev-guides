---
description: Implement proper caching for block performance and correctness
drupal_version: "11.x"
---

# Block Caching Strategies

## When to Use

> Ensure blocks are cached properly for performance while varying by necessary contexts and invalidating when data changes. Wrong caching = slow site or incorrect content shown to users.

## Decision

| If your block... | Use... | Why |
|------------------|--------|-----|
| Same for all users, rarely changes | `Cache::PERMANENT`, no contexts | Maximum caching efficiency |
| Varies per user | Cache context `user` | Different cache entry per user |
| Varies by user roles | Cache context `user.roles` | More efficient than `user` |
| Varies by URL/page | Cache context `url.path` or `route` | Different cache per page |
| Depends on specific entity | Cache tags from that entity | Invalidates when entity changes |
| Changes on time-based schedule | `max-age` in seconds | Auto-expires after time period |
| Must always be fresh | `max-age = 0` | No caching (performance cost) |
| Uses configuration | Config cache tags | Invalidates when config changes |

## Pattern

Implementing cache metadata in blocks:

```php
use Drupal\Core\Cache\Cache;

public function build() {
  $build = [
    '#markup' => 'Content',
  ];

  // Method 1: Add to render array
  $build['#cache'] = [
    'contexts' => ['user.roles', 'url.path'],
    'tags' => ['node:1', 'config:system.site'],
    'max-age' => 3600, // 1 hour
  ];

  return $build;
}

// Method 2: Implement cache methods
public function getCacheContexts() {
  return Cache::mergeContexts(parent::getCacheContexts(), ['user.roles']);
}

public function getCacheTags() {
  return Cache::mergeTags(parent::getCacheTags(), ['node:1']);
}

public function getCacheMaxAge() {
  return 3600; // Override default (Cache::PERMANENT)
}
```

**Reference:** `core/modules/system/src/Plugin/Block/SystemBrandingBlock.php` (lines 172-177)

## Common Mistakes

- **Wrong**: Using `max-age = 0` without considering performance → **Right**: Every request hits the database; use cache contexts instead
- **Wrong**: Not adding cache contexts for varying content → **Right**: Wrong content shown to users (cache poisoning)
- **Wrong**: Adding too-specific cache contexts (e.g., `user` when `user.roles` suffices) → **Right**: Cache fragmentation, poor hit rates
- **Wrong**: Not invalidating with cache tags → **Right**: Stale content after entity updates
- **Wrong**: Forgetting to merge with `parent::getCacheTags()` → **Right**: Loses important base cache metadata
- **Wrong**: Setting `#cache` in both `build()` and `getCacheTags()` → **Right**: Redundant; choose one approach and stick with it

## See Also

- [Block Access Control](block-access-control.md)
- [Security & Performance](security-performance.md)
- Reference: https://www.drupal.org/docs/drupal-apis/cache-api/cache-contexts
- Reference: https://www.drupal.org/docs/drupal-apis/cache-api/cache-max-age
