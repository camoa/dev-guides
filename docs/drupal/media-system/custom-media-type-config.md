---
description: Creating custom media types in Drupal — oEmbed providers, custom source plugins, field config, and naming conventions.
---

## 3. Custom Media Type Configuration

### When to Use

Core media types don't fit your needs — you need a custom media type for a specific use case.

### Decision

| If you need... | Source Plugin | Example |
|---|---|---|
| Non-oEmbed API (custom service) | Custom plugin | See `drupal_media_types_guide.md` |
| oEmbed service not in core | `oembed:video` or custom | Extend core oEmbed, add provider |
| Specialized file handling | `file` or `image` | Subclass with custom constraints |
| Instagram, TikTok, Spotify | `oembed:video` with custom provider | Add to providers list |

### Pattern

**Custom media type for oEmbed provider**:
```yaml
# config/sync/media.type.instagram.yml
langcode: en
status: true
dependencies: {}
id: instagram
label: Instagram
description: 'Instagram posts embedded via oEmbed.'
source: 'oembed:video'
queue_thumbnail_downloads: true
new_revision: true
source_configuration:
  source_field: field_media_oembed_url
  thumbnails_directory: 'public://instagram_thumbnails'
  providers:
    - Instagram
field_map:
  title: name
  author_name: field_author
```

**Source field config**:
```yaml
# config/sync/field.field.media.instagram.field_media_oembed_url.yml
langcode: en
status: true
dependencies:
  config:
    - field.storage.media.field_media_oembed_url
    - media.type.instagram
  module:
    - link
id: media.instagram.field_media_oembed_url
field_name: field_media_oembed_url
entity_type: media
bundle: instagram
label: 'Instagram URL'
description: 'Paste the Instagram post URL here.'
required: true
translatable: true
default_value: {}
default_value_callback: ''
settings:
  link_type: 16
  title: 0
field_type: link
```

### Common Mistakes

- Not setting `queue_thumbnail_downloads: true` for remote media → blocking requests slow page loads
- Wrong source plugin → `file` for remote media or `oembed` for local files creates validation errors
- Missing provider in `providers` list → oEmbed fails silently
- Not creating field storage first → field.field config depends on field.storage config
- Hardcoding field names → use consistent naming: `field_media_[type]` (e.g., `field_media_instagram`)

### See Also

- [Media Fields & Field Mapping](media-fields-field-mapping.md)
- Reference: `/core/modules/media/config/schema/media.schema.yml`
- Reference: https://www.drupal.org/docs/drupal-apis/entity-api/creating-a-custom-media-type
