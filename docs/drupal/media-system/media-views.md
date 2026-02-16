---
description: Displaying media collections in Views — galleries, grids, contextual filters, and rendered entity display with view modes.
---

## 15. Media in Views

### When to Use

You need to display collections of media: galleries, media listings, search results.

### Decision

| Display Style | Use Case |
|---|---|
| Grid of rendered entities | Image gallery, media grid |
| Table of fields | Media management, metadata display |
| Slideshow/carousel (contrib) | Hero slideshows, featured media |
| Media Library (core view) | Admin media browser (see [Media Library Views](media-library-views.md)) |

### Pattern

**Media gallery view**:
```yaml
# config/sync/views.view.media_gallery.yml
langcode: en
status: true
dependencies:
  config:
    - core.entity_view_mode.media.card
    - media.type.image
  module:
    - media
    - user
id: media_gallery
label: 'Media Gallery'
module: views
description: 'A grid of media items.'
tag: media
base_table: media_field_data
base_field: mid
display:
  default:
    display_plugin: default
    display_options:
      title: 'Media Gallery'
      fields:
        rendered_entity:
          id: rendered_entity
          table: media
          field: rendered_entity
          plugin_id: rendered_entity
          label: ''
          view_mode: card
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
          value:
            image: image
          plugin_id: bundle
      sorts:
        created:
          id: created
          table: media_field_data
          field: created
          order: DESC
          plugin_id: date
      pager:
        type: full
        options:
          items_per_page: 12
      style:
        type: grid
        options:
          columns: 3
          row_class: 'media-card'
  page_1:
    display_plugin: page
    path: '/gallery'
  block_1:
    display_plugin: block
    block_description: 'Media Gallery'
```

**Contextual filter for media by taxonomy**:
```yaml
# Add to view display config:
arguments:
  field_tags_target_id:
    id: field_tags_target_id
    table: media__field_tags
    field: field_tags_target_id
    plugin_id: taxonomy_term_id
    default_action: 'not found'
    default_argument_type: fixed
    validate:
      type: taxonomy_term
```

### Common Mistakes

- Using fields display for galleries → loses view mode control; use rendered entity with view mode: card
- Not filtering by published status → shows unpublished media; add status filter: value: '1'
- Exposing all media types → mixed galleries confusing; filter by bundle
- Not setting view mode → uses "default" which may be too large; use context-appropriate view mode
- Using thumbnail field instead of rendered entity → bypasses formatter config; render full entity with view mode

### See Also

- [The Responsive Image Strategy](responsive-image-strategy.md)
- [Media Library Views](media-library-views.md)
- Reference: https://www.drupal.org/docs/user_guide/en/views-chapter.html
