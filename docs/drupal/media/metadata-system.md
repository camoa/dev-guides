---
description: Defining what information a media source can provide and implementing the extraction logic.
---

# Metadata System

### When to Use

Defining what information a media source can provide and implementing the extraction logic.

### Decision

| Metadata Type | Example Attributes | Field Mapping Use |
|---------------|-------------------|-------------------|
| **Required core** | default_name, thumbnail_uri | Always implement for Media Library |
| **Display info** | title, author, description | Map to fields for searchability |
| **Technical** | width, height, duration, filesize | Map for filtering/sorting in views |
| **Provider-specific** | shortcode (Instagram), tweet_id (Twitter) | Use programmatically, rarely map |

### Pattern

Complete metadata implementation (10 lines):
```php
public function getMetadataAttributes(): array {
  return [
    'title' => $this->t('Title'),
    'author' => $this->t('Author'),
    'published_date' => $this->t('Published'),
    'duration' => $this->t('Duration (seconds)'),
    'thumbnail_uri' => $this->t('Thumbnail'),
  ];
}

public function getMetadata(MediaInterface $media, $attribute_name): mixed {
  $source_value = $this->getSourceFieldValue($media);

  return match($attribute_name) {
    'default_name' => $this->extractTitle($source_value),
    'thumbnail_uri' => $this->getThumbnailUri($source_value),
    'title', 'author', 'published_date', 'duration'
      => $this->fetchFromApi($source_value, $attribute_name),
    default => parent::getMetadata($media, $attribute_name),
  };
}
```

### Common Mistakes

- Not defining attributes in `getMetadataAttributes()` → Field mapping UI won't show them
- Returning arrays instead of scalar values → Field mapping expects strings/numbers
- Expensive operations without caching → Metadata fetched on every display/save
- Not handling missing data → NULL returns better than exceptions
- Forgetting parent fallback → Core metadata like default_name missing

**WHY:**
- **getMetadataAttributes() defines UI**: Field mappers see this list when configuring media types; missing attributes can't be mapped
- **Caching is critical**: Metadata is fetched during entity saves, displays, and field mapping; uncached API calls create performance bottlenecks
- **Graceful failures**: Third-party APIs fail; returning NULL prevents crashes and allows fallback to default values

### See Also

- Previous: [Extending OEmbed Sources](index.md)
- Next: [Field Mapping](index.md)
- Reference: core/modules/media/src/MediaSourceInterface.php (line 68-95)