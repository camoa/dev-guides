---
description: Caching, queuing, and optimization strategies for media source plugins
drupal_version: "11.x"
---

# Performance Optimization

## When to Use

> Use these optimizations when media source plugin causes slow page loads, high API usage, or database performance issues.

## Decision

| Performance Issue | Solution | Impact |
|-------------------|----------|--------|
| **Repeated API calls** | Cache responses with cache tags | 10-100x faster, reduces API rate limits |
| **Thumbnail downloads on page load** | Queue-based generation, serve default until ready | Prevents timeout errors, async processing |
| **N+1 query problem** | Batch metadata fetching, preload in hook_media_load() | 1 query instead of N |
| **Large metadata responses** | Store in field map, avoid fetching on display | Reduces API calls by 90%+ |
| **Slow validation** | Move expensive checks to queue, validate basic format only | Fast form submissions |

## Pattern

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

## Common Mistakes

- **Wrong**: No caching → **Right**: Cache with 1-hour minimum TTL
- **Wrong**: Cache without tags → **Right**: Tag with media ID for invalidation
- **Wrong**: Synchronous thumbnail downloads → **Right**: Queue-based generation
- **Wrong**: Fetching all metadata when only one needed → **Right**: Lazy-load specific attributes
- **Wrong**: Short cache TTL → **Right**: 1-24 hour TTL based on update frequency

## See Also

- Previous: [Security Best Practices](security-best-practices.md)
- Next: [Testing Strategies](testing-strategies.md)
- Reference: https://www.tutorials24x7.com/drupal/optimizing-drupal-website-performance-best-practices-for-2026
- Reference: https://pantheon.io/learning-center/drupal/caching
- Reference: https://www.drupal.org/project/media_thumbnails
