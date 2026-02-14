---
description: Specialized caching beyond time-based and tag-based: per-user caching, geolocation-based, A/B testing variants, external cache backends.
drupal_version: "11.x"
---

## 27. Custom Cache Plugin

### When to Use
Specialized caching beyond time-based and tag-based: per-user caching, geolocation-based, A/B testing variants, external cache backends.

### Steps

1. **Create cache plugin** — In `src/Plugin/views/cache/MyCustomCache.php`
   ```php
   namespace Drupal\mymodule\Plugin\views\cache;

   use Drupal\views\Plugin\views\cache\CachePluginBase;
   use Drupal\views\Attribute\ViewsCache;

   #[ViewsCache(
     id: "my_custom_cache",
     title: "Custom Cache",
     help: "Custom caching strategy",
   )]
   class MyCustomCache extends CachePluginBase {
     protected function cacheGet($type) {
       $cid = $this->generateCacheId($type);
       return \Drupal::cache()->get($cid);
     }

     protected function cacheSet($type) {
       $cid = $this->generateCacheId($type);
       \Drupal::cache()->set($cid, [
         'result' => $this->view->result,
         'total_rows' => $this->view->total_rows ?? 0,
       ], CacheBackendInterface::CACHE_PERMANENT, $this->getCacheTags());
     }
   }
   ```

2. **Generate cache ID** — Create unique key per view state
   ```php
   protected function generateCacheId($type) {
     $parts = [
       'views',
       $this->view->id(),
       $this->view->current_display,
       $type,
       \Drupal::currentUser()->id(),  // Per-user cache
     ];
     return implode(':', $parts);
   }
   ```

3. **Define cache tags** — For tag-based invalidation
   ```php
   public function getCacheTags() {
     $tags = parent::getCacheTags();
     $tags[] = 'user:' . \Drupal::currentUser()->id();
     return $tags;
   }
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Cache granularity | Per-user caching | Include user ID in cache ID generation |
| Invalidation | Tag-based clearing | Override getCacheTags() to return relevant tags |
| Expiration | Time-based expiration | Use cache expiration timestamp in set() |
| Storage | Custom backend | Inject custom cache backend via create() |

### Common Mistakes
- Not invalidating on relevant changes → Set proper cache tags; stale results confuse users
- Too granular cache keys → Per-argument caching can explode cache size; balance specificity vs. storage
- Missing cache context → If results vary by language/theme/etc., include in cache ID
- Caching sensitive data → Ensure per-user caching for views with access-controlled content
- Not implementing cacheFlush() → Cache should clear when view config changes

### See Also
- Section 13: Caching Configuration — tag-based and time-based strategies
- Reference: `core/modules/views/src/Plugin/views/cache/CachePluginBase.php`
- Reference: `core/modules/views/src/Plugin/views/cache/Tag.php` — tag-based cache example
