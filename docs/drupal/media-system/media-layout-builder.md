---
description: Placing media in Layout Builder — inline blocks, custom block types with media fields, and view mode selection in layouts.
---

## 14. Media in Layout Builder

### When to Use

You need to place media in Layout Builder sections using inline blocks or custom blocks.

### Decision

| Approach | Use Case |
|---|---|
| Inline block with media field | Quick, contextual media placement |
| Custom block type with media field | Reusable media blocks across pages |
| Media library block (contrib) | Browse and place media directly |
| View block displaying media | Dynamic media galleries |

### Pattern

**Custom block type with media field**:
```yaml
# config/sync/block_content.type.media_block.yml
langcode: en
status: true
dependencies: {}
id: media_block
label: 'Media Block'
revision: 1
description: 'A block with a media reference field.'

# config/sync/field.field.block_content.media_block.field_media.yml
langcode: en
status: true
dependencies:
  config:
    - block_content.type.media_block
    - field.storage.block_content.field_media
    - media.type.image
  module:
    - entity_reference
id: block_content.media_block.field_media
field_name: field_media
entity_type: block_content
bundle: media_block
label: Media
required: true
translatable: false
settings:
  handler: 'default:media'
  handler_settings:
    target_bundles:
      image: image
      remote_video: remote_video

# Form display: media_library_widget
# View display: entity_reference_entity_view with view_mode: hero
```

**Layout Builder section with media block**:
```yaml
# In node layout config (simplified)
sections:
  - layout_id: layout_onecol
    layout_settings:
      label: 'Hero Section'
    components:
      - uuid: component-uuid-here
        region: content
        configuration:
          id: 'inline_block:media_block'
          label: 'Hero Image'
          provider: layout_builder
          block_serialized: '...'
          view_mode: full
```

**View mode selection in Layout Builder**:

When configuring the block in Layout Builder UI:
1. Place block → Select media block type
2. Configure block → Select media via Media Library
3. Configure display → Choose view mode (hero, card, embed)

The view mode dropdown comes from Layout Builder's block display settings.

### Common Mistakes

- Using "default" view mode for all Layout Builder blocks → inconsistent display; create context-specific view modes
- Not making inline blocks reusable → recreating same media block on every page; use custom block types for reusable patterns
- Hardcoding view mode in block template → breaks editorial control; respect view mode config
- Not enabling Layout Builder media integration → contrib module "Layout Builder Media" enhances experience
- Bypassing media reference → placing image fields directly in blocks loses media reusability

### See Also

- [The Responsive Image Strategy](responsive-image-strategy.md)
- [Media Reference Fields](media-reference-fields.md)
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/layout-builder-module
