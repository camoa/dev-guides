---
description: Defining and extracting metadata attributes from media sources
drupal_version: "11.x"
---

# Metadata System

## When to Use

> Use metadata attributes when defining what information a media source can provide and implementing the extraction logic for searchable, displayable data.

## Decision

| Metadata Type | Example Attributes | Field Mapping Use |
|---------------|-------------------|-------------------|
| **Required core** | default_name, thumbnail_uri | Always implement for Media Library |
| **Display info** | title, author, description | Map to fields for searchability |
| **Technical** | width, height, duration, filesize | Map for filtering/sorting in views |
| **Provider-specific** | shortcode (Instagram), tweet_id (Twitter) | Use programmatically, rarely map |

## Pattern

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

## Common Mistakes

- **Wrong**: Not defining attributes in `getMetadataAttributes()` → **Right**: Define all attributes for field mapping UI
- **Wrong**: Returning arrays instead of scalar values → **Right**: Return strings/numbers for field mapping
- **Wrong**: Expensive operations without caching → **Right**: Cache metadata fetches
- **Wrong**: Not handling missing data → **Right**: Return NULL instead of throwing exceptions
- **Wrong**: Forgetting parent fallback → **Right**: Call parent::getMetadata() in default case

## See Also

- Previous: [Extending OEmbed Sources](extending-oembed-sources.md)
- Next: [Field Mapping](field-mapping.md)
- Reference: core/modules/media/src/MediaSourceInterface.php (line 68-95)
