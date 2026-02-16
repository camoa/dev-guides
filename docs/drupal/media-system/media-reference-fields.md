---
description: Configuring media reference fields on content types — single, multiple, unlimited, and mixed media type references with appropriate widgets and formatters.
---

## 13. Media Reference Fields

### When to Use

You need to add media reference fields to content types, paragraphs, or other entities.

### Decision

| Cardinality | Widget | Display Formatter |
|---|---|---|
| Single (1) | `media_library_widget` | `entity_reference_entity_view` with view mode |
| Multiple (limited) | `media_library_widget` | `entity_reference_entity_view` with view mode |
| Unlimited (-1) | `media_library_widget` with drag-drop sort | `entity_reference_entity_view` with view mode |
| Small fixed set | `options_select` | `entity_reference_entity_view` with view mode |
| Autocomplete only | `entity_reference_autocomplete` | `entity_reference_label` or `entity_reference_entity_view` |

### Pattern

**Single hero image field** (see [Media Library Widget](media-library-widget.md) for full config):
```yaml
# Field storage: cardinality: 1, target_type: media
# Field instance: target_bundles: {image: image}
# Form display: type: media_library_widget, media_types: [image]
# View display: type: entity_reference_entity_view, view_mode: hero
```

**Multiple image gallery field**:
```yaml
# config/sync/field.storage.node.field_gallery.yml
langcode: en
status: true
dependencies:
  module:
    - media
    - node
id: node.field_gallery
field_name: field_gallery
entity_type: node
type: entity_reference
settings:
  target_type: media
module: core
cardinality: -1  # Unlimited
translatable: true

# config/sync/field.field.node.article.field_gallery.yml
settings:
  handler: 'default:media'
  handler_settings:
    target_bundles:
      image: image
    sort:
      field: _none

# In form display:
field_gallery:
  type: media_library_widget
  settings:
    media_types:
      - image

# In view display:
field_gallery:
  type: entity_reference_entity_view
  label: hidden
  settings:
    view_mode: card
    link: false
```

**Mixed media types field** (images and videos):
```yaml
# In field instance:
settings:
  handler_settings:
    target_bundles:
      image: image
      remote_video: remote_video

# In form display:
field_mixed_media:
  type: media_library_widget
  settings:
    media_types:
      - image
      - remote_video
```

### Common Mistakes

- Not setting target_bundles → allows all media types; restrict to needed types
- Using `entity_reference_label` formatter → shows "Image: filename.jpg" link; use `entity_reference_entity_view` with view mode
- Not selecting view mode in display settings → uses "default" view mode; select context-appropriate view mode (card, embed, etc.)
- Unlimited cardinality without sort → no reordering; use drag-drop sort via field widget settings
- Not hiding label → shows "Hero Image" above image; set label: hidden for clean display

### See Also

- [The Responsive Image Strategy](responsive-image-strategy.md)
- [Media Library Widget](media-library-widget.md)
- Reference: https://www.drupal.org/docs/drupal-apis/entity-api/entity-types/entityreference-field-type
