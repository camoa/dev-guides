---
description: Building a custom media source plugin and choosing which base class to extend (MediaSourceBase, File, or OEmbed).
---

# Base Class Selection

### When to Use

Building a custom media source plugin and choosing which base class to extend (MediaSourceBase, File, or OEmbed).

### Decision

| Base Class | Use When | Provides | Complexity |
|------------|----------|----------|------------|
| **MediaSourceBase** | Custom API, proprietary service, no existing fit | Config management, DI setup, field handling | Medium |
| **File** | Local files with custom extensions/validation | All MediaSourceBase + file entity handling, extension validation | Low |
| **OEmbed** | Service supports oEmbed protocol | All MediaSourceBase + resource fetching, URL validation, thumbnail downloading (11 injected services) | High |

### Pattern

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

### Common Mistakes

- Extending OEmbed for non-oEmbed APIs → Adds 11 unused services, complex inheritance
- Extending MediaSourceBase for files → Reimplements file handling that File class provides
- Not checking provider oEmbed support → Build custom when core OEmbed would work
- Using File base for remote media → File entity required, inappropriate for URLs

### See Also

- Previous: [Media Type Selection Strategy](index.md)
- Next: [Architecture Overview](index.md)
- Reference: core/modules/media/src/MediaSourceBase.php