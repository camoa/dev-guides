---
description: Media source fields and metadata mapping — field types, image validation settings, and field_map configuration.
---

## 4. Media Fields & Field Mapping

### When to Use

You need to understand how source fields store media and how metadata maps to media entity fields.

### Decision

| Field Type | Use Case | Source Plugin |
|---|---|---|
| `image` | Local images with alt, title, dimensions | `image` |
| `file` | Local files (PDFs, audio, video) | `file`, `audio_file`, `video_file` |
| `string` (text) | Remote media URLs (oEmbed) | `oembed:video` |
| `string_long` (textarea) | Embed codes, iframes | Custom source plugin |
| `entity_reference` | Reference to another entity | Custom source plugin |

### Pattern

**Image source field with validation**:
```yaml
# config/sync/field.field.media.image.field_media_image.yml
langcode: en
status: true
dependencies:
  config:
    - field.storage.media.field_media_image
    - media.type.image
  module:
    - image
id: media.image.field_media_image
field_name: field_media_image
entity_type: media
bundle: image
label: Image
description: ''
required: true
translatable: true
default_value: {}
default_value_callback: ''
settings:
  handler: 'default:file'
  handler_settings: {}
  file_directory: '[date:custom:Y]-[date:custom:m]'
  file_extensions: 'png gif jpg jpeg webp'
  max_filesize: ''
  max_resolution: ''
  min_resolution: ''
  alt_field: true
  alt_field_required: true
  title_field: false
  title_field_required: false
  default_image:
    uuid: null
    alt: ''
    title: ''
    width: null
    height: null
field_type: image
```

**Field mapping in media type**:
```yaml
# In media.type.image.yml
source_configuration:
  source_field: field_media_image
field_map:
  name: name  # Maps file name to media name
  # Add custom mappings:
  # title: field_media_title
  # caption: field_media_caption
```

### Common Mistakes

- Not requiring alt text → accessibility failure; set `alt_field: true` and `alt_field_required: true`
- Allowing all file extensions → security risk; whitelist extensions: `png gif jpg jpeg webp`
- Not organizing uploads → use `file_directory: '[date:custom:Y]-[date:custom:m]'` for organized storage
- Ignoring max_filesize → allow unlimited uploads can exhaust disk; set reasonable limits
- Not mapping metadata → field_map is optional but powerful; map title, caption, credits

### See Also

- [Media View Modes](media-view-modes.md)
- [Media File System](media-file-system.md)
- Reference: `/core/profiles/standard/config/optional/field.field.media.image.field_media_image.yml`
- Reference: https://www.drupal.org/docs/drupal-apis/entity-api/fieldtypes-fieldwidgets-and-fieldformatters
