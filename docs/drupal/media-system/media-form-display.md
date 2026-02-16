---
description: Configuring media upload and edit forms — field widgets, image previews, Media Library form mode, and form optimization.
---

## 8. Media Form Display

### When to Use

You need to configure the media upload and edit form: field order, widgets, help text.

### Decision

| Field | Widget | Settings |
|---|---|---|
| Image field | `image_image` | progress_indicator: throbber, preview_image_style: thumbnail |
| File field | `file_generic` | progress_indicator: throbber |
| oEmbed URL | `string_textfield` | size, placeholder |
| Alt text | part of image_image widget | alt_field: true, alt_field_required: true |
| Title, credits | `string_textfield` | size, placeholder |
| Status (published) | `boolean_checkbox` | display_label: true |

### Pattern

**Image media form display**:
```yaml
# config/sync/core.entity_form_display.media.image.default.yml
langcode: en
status: true
dependencies:
  config:
    - field.field.media.image.field_media_image
    - image.style.thumbnail
    - media.type.image
  module:
    - image
id: media.image.default
targetEntityType: media
bundle: image
mode: default
content:
  field_media_image:
    type: image_image
    weight: 0
    region: content
    settings:
      progress_indicator: throbber
      preview_image_style: thumbnail
    third_party_settings: {}
  status:
    type: boolean_checkbox
    weight: 100
    region: content
    settings:
      display_label: true
    third_party_settings: {}
  uid:
    type: entity_reference_autocomplete
    weight: 5
    region: content
    settings:
      match_operator: CONTAINS
      match_limit: 10
      size: 60
      placeholder: ''
    third_party_settings: {}
  created:
    type: datetime_timestamp
    weight: 10
    region: content
    settings: {}
    third_party_settings: {}
hidden:
  name: true
```

**Media Library form mode** (optimized for quick upload):
```yaml
# config/sync/core.entity_form_display.media.image.media_library.yml
langcode: en
status: true
dependencies:
  config:
    - core.entity_form_mode.media.media_library
    - field.field.media.image.field_media_image
    - image.style.thumbnail
    - media.type.image
  module:
    - image
    - media_library
id: media.image.media_library
targetEntityType: media
bundle: image
mode: media_library
content:
  field_media_image:
    type: image_image
    weight: 0
    region: content
    settings:
      progress_indicator: throbber
      preview_image_style: thumbnail
    third_party_settings: {}
  status:
    type: boolean_checkbox
    weight: 100
    region: content
    settings:
      display_label: true
    third_party_settings: {}
hidden:
  created: true
  name: true
  uid: true
```

### Common Mistakes

- Requiring name field → auto-generated from filename; hide or leave optional
- Not setting preview_image_style → huge upload previews; use thumbnail
- Showing created and uid in Media Library mode → clutters quick upload form; hide non-essential fields
- Not using media_library form mode → uses default form even in Media Library modal; create optimized form mode
- Using generic file widget for images → loses alt text and preview; use image_image widget

### See Also

- [Media Library Widget](media-library-widget.md)
- Reference: `/core/profiles/standard/config/optional/core.entity_form_display.media.image.default.yml`
