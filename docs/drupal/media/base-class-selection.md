---
description: Choosing MediaSourceBase, File, or OEmbed base class for custom plugins
drupal_version: "11.x"
---

# Base Class Selection

## When to Use

> Use MediaSourceBase when building a custom API integration. Use File when extending local file handling. Use OEmbed when service supports oEmbed protocol.

## Decision

| Base Class | Use When | Provides | Complexity |
|------------|----------|----------|------------|
| **MediaSourceBase** | Custom API, proprietary service, no existing fit | Config management, DI setup, field handling | Medium |
| **File** | Local files with custom extensions/validation | All MediaSourceBase + file entity handling, extension validation | Low |
| **OEmbed** | Service supports oEmbed protocol | All MediaSourceBase + resource fetching, URL validation, thumbnail downloading (11 injected services) | High |

## Pattern

Extending MediaSourceBase for custom API:
```php
#[MediaSource(
  id: "custom_api",
  label: new TranslatableMarkup("Custom API"),
  allowed_field_types: ["string", "link"],
  default_thumbnail_filename: "custom.png"
)]
class CustomApi extends MediaSourceBase {
  public function getMetadataAttributes(): array {
    return [
      'title' => $this->t('Title'),
      'author' => $this->t('Author'),
      'thumbnail_uri' => $this->t('Thumbnail'),
    ];
  }
}
```

## Common Mistakes

- **Wrong**: Extending OEmbed for non-oEmbed APIs → **Right**: Use MediaSourceBase, avoid 11 unused services
- **Wrong**: Extending MediaSourceBase for files → **Right**: Extend File class for file handling
- **Wrong**: Not checking provider oEmbed support → **Right**: Verify oEmbed endpoint exists
- **Wrong**: Using File base for remote media → **Right**: MediaSourceBase for URL-based media

## See Also

- Previous: [Media Type Selection Strategy](media-type-selection-strategy.md)
- Next: [Architecture Overview](architecture-overview.md)
- Reference: core/modules/media/src/MediaSourceBase.php
