---
description: Core media types in Drupal — Image, Document, Remote Video, Audio, Video — their source plugins, config, and field mappings.
---

## 2. Core Media Types

### When to Use

You need to understand what core provides before creating custom media types.

### Decision

| Media Type | Source Plugin | Use Case | Source Field Type |
|---|---|---|---|
| Image | `image` | Local image files with dimensions, EXIF | `image` field |
| Document | `file` | PDFs, docs, spreadsheets | `file` field |
| Remote Video | `oembed:video` | YouTube, Vimeo, oEmbed videos | `string` (URL) |
| Audio | `audio_file` | MP3, WAV, OGG files | `file` field with audio extensions |
| Video | `video_file` | Local video files (MP4, WebM) | `file` field with video extensions |

### Pattern

**Image media type config**:
```yaml
# config/sync/media.type.image.yml
langcode: en
status: true
dependencies: {}
id: image
label: Image
description: "A locally hosted image file."
source: image
queue_thumbnail_downloads: false
new_revision: true
source_configuration:
  source_field: field_media_image
field_map:
  name: name
```

**Remote Video media type config**:
```yaml
# config/sync/media.type.remote_video.yml
langcode: en
status: true
dependencies: {}
id: remote_video
label: 'Remote video'
description: 'A video hosted on an external site (YouTube or Vimeo).'
source: 'oembed:video'
queue_thumbnail_downloads: false
new_revision: true
source_configuration:
  source_field: field_media_oembed_video
  thumbnails_directory: 'public://oembed_thumbnails/[date:custom:Y-m]'
  providers:
    - YouTube
    - Vimeo
field_map:
  title: name
```

### Common Mistakes

- Creating custom media type for local images → use core Image type; it handles dimensions, EXIF, thumbnails
- Using Document type for images → loses image-specific metadata and responsive image support
- Hardcoding oEmbed providers → add to `providers` list in source_configuration
- Not configuring thumbnail directory for remote media → defaults to public, configure for organized storage
- Ignoring `field_map` → misses automatic metadata mapping (title, name)

### See Also

- [Custom Media Type Configuration](custom-media-type-config.md)
- [Media Fields & Field Mapping](media-fields-field-mapping.md)
- Reference: `/core/profiles/standard/config/optional/media.type.*.yml`
- Reference: `/core/modules/media/config/schema/media.schema.yml`
