---
description: Set how long cached content remains valid using max-age expiration
---

# Cache Max-Age

## When to Use

When you need to set expiration on cached content. Max-age is the third pillar of cache metadata (alongside tags and contexts) and controls how long cached data remains valid.

## Decision

| If cached content... | Use max-age... | Why |
|---|---|---|
| Never changes | `Cache::PERMANENT` | Cache indefinitely; invalidate only via cache tags when source data changes |
| Depends on external data (API, time-based) | Seconds until next update | External data can't trigger Drupal cache tag invalidation |
| Updates on schedule (hourly, daily) | Seconds until next schedule | Time-based expiration simpler than cron-based invalidation |
| Includes uncacheable elements | `0` (uncacheable) | Child element with max-age 0 makes parent uncacheable |
| Varies by user action | Use cache tags instead | Let tags handle invalidation rather than guessing expiration time |

**Max-age merging**: When combining cache metadata, the **lowest** max-age wins. A child element with `max-age = 0` makes the entire parent uncacheable.

## Pattern

**Time-based expiration**:
```php
$build = [
  '#cache' => [
    'max-age' => 3600,  // 1 hour in seconds
  ],
];

// Common durations
Cache::PERMANENT;  // -1 (never expires, use tags for invalidation)
60;               // 1 minute
3600;             // 1 hour
86400;            // 24 hours
```

**Merging max-age** (always use lowest):
```php
use Drupal\Core\Cache\Cache;

$parent_max_age = 3600;
$child_max_age = 1800;
$merged = Cache::mergeMaxAges($parent_max_age, $child_max_age);  // 1800
```

**Uncacheable content**:
```php
$build = [
  '#cache' => [
    'max-age' => 0,  // Never cache this render array
  ],
];
```

Reference: `/core/lib/Drupal/Core/Cache/Cache.php`

## Common Mistakes

- Using `Cache::PERMANENT` for time-sensitive content — Content becomes stale; use time-based max-age instead
- Guessing max-age instead of using tags — Content updates don't invalidate cache until expiration; use cache tags for data-driven invalidation
- Not merging max-age from dependencies — Parent cached with high max-age while child needs lower max-age
- Setting high max-age on external API data — External changes don't propagate until expiration; set max-age based on API update frequency
- Using max-age for user-specific content — Use cache contexts instead; max-age is for time-based expiration, not variation

## See Also

- [Cache Metadata Trinity](cache-metadata-trinity.md) — How max-age fits with tags and contexts
- [BubbleableMetadata & Cache Bubbling](bubbleable-metadata-cache-bubbling.md) — How max-age bubbles up
- Reference: [Cache max-age documentation](https://www.drupal.org/docs/develop/drupal-apis/cache-api/cache-max-age)
