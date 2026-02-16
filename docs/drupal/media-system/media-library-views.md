---
description: Customizing the Media Library browser view — filters, sort order, fields, pager settings, and image dimensions display.
---

## 10. Media Library Views

### When to Use

You need to customize the Media Library browser: filters, sort order, fields displayed.

### Decision

| Customization | Approach |
|---|---|
| Filter by media type | Add exposed filter on `bundle` field |
| Search by filename | Add exposed filter on `name` field with `contains` operator |
| Sort by upload date | Add sort on `created` field, descending |
| Show additional metadata | Add fields to display (author, file size, dimensions) |
| Change items per page | Modify pager settings |
| Custom thumbnail display | Override `thumbnail` field display with custom formatter |

### Pattern

**Media Library view configuration** (simplified excerpt):
```yaml
# config/sync/views.view.media_library.yml
langcode: en
status: true
dependencies:
  config:
    - core.entity_view_mode.media.media_library
    - image.style.media_library
  module:
    - image
    - media
    - media_library
    - user
id: media_library
label: 'Media library'
module: views
description: 'Find and manage media.'
base_table: media_field_data
base_field: mid
display:
  default:
    display_options:
      title: Media
      fields:
        media_bulk_form:
          id: media_bulk_form
          table: media
          field: media_bulk_form
          plugin_id: bulk_form
        rendered_entity:
          id: rendered_entity
          table: media
          field: rendered_entity
          plugin_id: rendered_entity
          view_mode: media_library
      pager:
        type: mini
        options:
          items_per_page: 24
      filters:
        status:
          id: status
          table: media_field_data
          field: status
          value: '1'
          plugin_id: boolean
        bundle:
          id: bundle
          table: media_field_data
          field: bundle
          exposed: true
          plugin_id: bundle
      sorts:
        created:
          id: created
          table: media_field_data
          field: created
          order: DESC
          plugin_id: date
```

**Customizing for image dimensions display**:
Add to views.view.media_library.yml:
```yaml
fields:
  field_media_image__width:
    id: field_media_image__width
    table: media__field_media_image
    field: field_media_image__width
    label: Width
    plugin_id: field
  field_media_image__height:
    id: field_media_image__height
    table: media__field_media_image
    field: field_media_image__height
    label: Height
    plugin_id: field
```

### Common Mistakes

- Modifying core view in place → lost on updates; export to config/sync or create view override
- Removing bulk operations field → breaks bulk actions; keep `media_bulk_form` field
- Changing view mode from `media_library` → breaks Media Library styling; use custom CSS overrides instead
- Not exposing bundle filter → users see all media types mixed; expose bundle filter for clarity
- Using full entity display → slow rendering; use `media_library` view mode for optimized thumbnails

### See Also

- [Media Library Widget](media-library-widget.md)
- Reference: `/core/modules/media_library/config/install/views.view.media_library.yml`
