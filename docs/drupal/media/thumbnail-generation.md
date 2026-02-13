---
description: Downloading, caching, and generating thumbnails for media entities
drupal_version: "11.x"
---

# Thumbnail Generation

## When to Use

> Use thumbnail generation strategies when providing thumbnails for Media Library display and media entity views.

## Decision

| Media Type | Strategy | Implementation |
|------------|----------|----------------|
| Local images | Use image file itself | Return image field URI |
| Local non-image files | Use default icon | Return `icon_base_uri . default_thumbnail_filename` |
| Remote media with thumbnail URL | Download and cache | Hash URL (md5), download once, store in public://oembed_thumbnails/ |
| Remote media without thumbnail | Use default icon | Provide default PNG in module/images/ |
| Generated thumbnails (PDFs, videos) | Queue-based generation | Queue thumbnail generation, serve default until ready |

## Pattern

Remote thumbnail with caching (OEmbed pattern, 12 lines):
```php
public function getMetadata(MediaInterface $media, $attribute_name): mixed {
  if ($attribute_name === 'thumbnail_uri') {
    $thumbnail_url = $this->fetchFromApi($id, 'thumbnail_url');
    return $thumbnail_url ? $this->downloadThumbnail($thumbnail_url) : NULL;
  }
}

protected function downloadThumbnail(string $url): string {
  $hash = md5($url);
  $directory = 'public://media_thumbnails';
  $local_uri = "$directory/$hash.jpg";

  if (!file_exists($local_uri)) {
    $this->fileSystem->prepareDirectory($directory, FILE_CREATE_DIRECTORY);
    $response = $this->httpClient->get($url);
    file_put_contents($local_uri, $response->getBody());
  }

  return $local_uri;
}
```

## Common Mistakes

- **Wrong**: Downloading thumbnails on every request → **Right**: Download once, cache by URL hash
- **Wrong**: Not hashing URLs → **Right**: Hash with md5() to detect duplicates
- **Wrong**: Storing in temp directory → **Right**: Use public:// for persistence
- **Wrong**: No error handling → **Right**: Return NULL on failure for fallback icon
- **Wrong**: Blocking requests for generation → **Right**: Queue-based generation for expensive operations

## See Also

- Previous: [Field Mapping](field-mapping.md)
- Next: [Dependency Injection](dependency-injection.md)
- Reference: core/modules/media/src/Plugin/media/Source/OEmbed.php (line 403-464)
- Reference: https://www.drupal.org/project/media_thumbnails
