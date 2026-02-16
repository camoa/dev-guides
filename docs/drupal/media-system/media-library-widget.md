---
description: Adding media reference fields with the Media Library widget — field storage, instance config, widget settings, and view display formatters.
---

## 9. Media Library Widget

### When to Use

You need to add a media reference field to a content type with the Media Library browser.

### Decision

| Widget | Use Case |
|---|---|
| `media_library_widget` | Full Media Library browser with upload, select from existing, multi-select |
| `entity_reference_autocomplete` | Autocomplete by media name (no upload, no browse) |
| `options_select` | Dropdown of media items (only for small sets) |

### Pattern

**Media reference field storage**:
```yaml
# config/sync/field.storage.node.field_hero_image.yml
langcode: en
status: true
dependencies:
  module:
    - media
    - node
id: node.field_hero_image
field_name: field_hero_image
entity_type: node
type: entity_reference
settings:
  target_type: media
module: core
locked: false
cardinality: 1
translatable: true
indexes: {  }
persist_with_no_fields: false
custom_storage: false
```

**Media reference field instance**:
```yaml
# config/sync/field.field.node.article.field_hero_image.yml
langcode: en
status: true
dependencies:
  config:
    - field.storage.node.field_hero_image
    - media.type.image
    - node.type.article
id: node.article.field_hero_image
field_name: field_hero_image
entity_type: node
bundle: article
label: 'Hero Image'
description: 'Select or upload a hero image.'
required: false
translatable: true
default_value: {}
default_value_callback: ''
settings:
  handler: 'default:media'
  handler_settings:
    target_bundles:
      image: image
    sort:
      field: _none
    auto_create: false
    auto_create_bundle: ''
field_type: entity_reference
```

**Form display with Media Library widget**:
```yaml
# config/sync/core.entity_form_display.node.article.default.yml
content:
  field_hero_image:
    type: media_library_widget
    weight: 2
    region: content
    settings:
      media_types:
        - image
    third_party_settings: {}
```

**View display with rendered entity formatter**:
```yaml
# config/sync/core.entity_view_display.node.article.default.yml
content:
  field_hero_image:
    type: entity_reference_entity_view
    label: hidden
    settings:
      view_mode: hero
      link: false
    third_party_settings: {}
    weight: 1
    region: content
```

### Common Mistakes

- Not filtering media types → shows all media types in browser; set `media_types: [image]` to limit
- Using autocomplete widget → no upload capability, poor UX; use media_library_widget
- Not configuring target_bundles → allows any media type; restrict to needed types
- Using `entity_reference_label` formatter → shows media name as link; use `entity_reference_entity_view` with view mode
- Setting cardinality: -1 without limiting uploads → unbounded growth; set reasonable cardinality

### See Also

- [Media Library Views](media-library-views.md)
- [Media Reference Fields](media-reference-fields.md)
- Reference: `/core/modules/media_library/src/Plugin/Field/FieldWidget/MediaLibraryWidget.php`
