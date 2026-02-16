---
description: Media source plugin causes slow page loads, high API usage, or database performance issues.
---

# Performance Optimization

### When to Use

Media source plugin causes slow page loads, high API usage, or database performance issues.

### Decision

| Performance Issue | Solution | Impact |
|-------------------|----------|--------|
| **Repeated API calls** | Cache responses with cache tags | 10-100x faster, reduces API rate limits |
| **Thumbnail downloads on page load** | Queue-based generation, serve default until ready | Prevents timeout errors, async processing |
| **N+1 query problem** | Batch metadata fetching, preload in hook_media_load() | 1 query instead of N |
| **Large metadata responses** | Store in field map, avoid fetching on display | Reduces API calls by 90%+ |
| **Slow validation** | Move expensive checks to queue, validate basic format only | Fast form submissions |

### Pattern

Caching API responses with tags (10 lines):
```php
protected function fetchFromApi(string $id, string $field): mixed {
  $cache_key = "yourmodule:api:{$id}:{$field}";

  if ($cached = $this->cache->get($cache_key)) {
    return $cached->data;
  }

  try {
    $response = $this->httpClient->get("https://api.example.com/items/{$id}");
    $data = json_decode($response->getBody(), TRUE);
    $value = $data[$field] ?? NULL;

    // Cache for 1 hour, invalidate on media entity changes
    $this->cache->set($cache_key, $value, time() + 3600, ["media:{$id}"]);
    return $value;
  } catch (\Exception $e) {
    $this->logger->error('API error: @msg', ['@msg' => $e->getMessage()]);
    return NULL;
  }
}
```

Queue-based thumbnail generation (8 lines):
```php
public function getMetadata(MediaInterface $media, $attribute_name): mixed {
  if ($attribute_name === 'thumbnail_uri') {
    $local_uri = $this->checkLocalThumbnail($media->id());

    if (!$local_uri) {
      // Queue thumbnail generation
      $this->queue->createItem(['media_id' => $media->id()]);
      // Serve default until ready
      return $this->getPluginDefinition()['default_thumbnail_filename'];
    }

    return $local_uri;
  }
}
```

### Common Mistakes

- No caching → Every display hits API, rate limits exceeded quickly
- Cache without tags → Can't invalidate when content changes, shows stale data
- Synchronous thumbnail downloads → Page loads wait for network I/O, timeouts common
- Fetching all metadata when only one needed → Wastes bandwidth, slows responses
- Short cache TTL → Cache misses too frequent, negates performance benefits

**WHY these matter (performance reasoning):**
- **Caching is not optional**: APIs have rate limits (Instagram: 200/hour, Twitter: 300/15min); without caching, popular media items exhaust limits quickly
- **Cache tags enable invalidation**: Without tags, clearing cache requires flushing entire cache bin, impacting unrelated content
- **Queue-based processing**: Network operations (downloading thumbnails) are unpredictable; queuing prevents user-facing timeouts
- **Lazy loading**: Fetching all metadata eagerly wastes 80%+ of bandwidth; fetch only what's displayed
- **TTL tuning**: Too short (< 5min) causes frequent cache misses; too long (> 24hr) shows stale data when API content updates

### See Also

- Previous: [Security Best Practices](index.md)
- Next: [Testing Strategies](index.md)
- Reference: https://www.tutorials24x7.com/drupal/optimizing-drupal-website-performance-best-practices-for-2026
- Reference: https://pantheon.io/learning-center/drupal/caching
- Reference: https://www.drupal.org/project/media_thumbnails