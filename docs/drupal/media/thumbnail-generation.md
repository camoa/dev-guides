---
description: Providing thumbnails for Media Library display and media entity views.
---

# Thumbnail Generation

### When to Use

Providing thumbnails for Media Library display and media entity views.

### Decision

| Media Type | Strategy | Implementation |
|------------|----------|----------------|
| Local images | Use image file itself | Return image field URI |
| Local non-image files | Use default icon | Return `icon_base_uri . default_thumbnail_filename` |
| Remote media with thumbnail URL | Download and cache | Hash URL (md5), download once, store in public://oembed_thumbnails/ |
| Remote media without thumbnail | Use default icon | Provide default PNG in module/images/ |
| Generated thumbnails (PDFs, videos) | Queue-based generation | Queue thumbnail generation, serve default until ready |

### Pattern

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

### Common Mistakes

- Downloading thumbnails on every request → Massive performance hit, bandwidth waste
- Not hashing URLs → Can't detect duplicates, re-downloads same thumbnail
- Storing in temp directory → Thumbnails deleted on cache clear, re-downloaded constantly
- No error handling → Network failures crash thumbnail display
- Blocking requests for generation → Long page loads waiting for thumbnail downloads

**WHY:**
- **Hashing prevents duplicates**: Multiple media items may reference same thumbnail URL; hashing detects this and reuses cached file
- **Public storage persistence**: Temp storage gets cleared; thumbnails should persist like uploaded files
- **Error handling**: Network requests fail; returning NULL allows fallback to default icon instead of white screen
- **Queue-based generation**: Generating thumbnails (especially for PDFs/videos) is expensive; queueing prevents timeout issues

### See Also

- Previous: [Field Mapping](index.md)
- Next: [Dependency Injection](index.md)
- Reference: core/modules/media/src/Plugin/media/Source/OEmbed.php (line 403-464)
- Reference: https://www.drupal.org/project/media_thumbnails