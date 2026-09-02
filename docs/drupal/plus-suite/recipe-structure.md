---
description: Plus Suite recipe structure — dependencies, modules installed, configuration created, config actions, and strict:false behavior
tldr: "Reference this when troubleshooting recipe application, understanding what gets installed, or deciding whether to use recipe vs manual installation."
drupal_version: "11.x"
---

# Recipe Structure

## When to Use

> When you need to understand what the Plus Suite recipe installs, configures, and creates, or when troubleshooting recipe application.

## Recipe Dependencies

```yaml
recipes:
  - core/recipes/basic_block_type
  - core/recipes/basic_html_format_editor
  - core/recipes/full_html_format_editor
  - core/recipes/core_recommended_admin_theme
  - core/recipes/core_recommended_front_end_theme
  - core/recipes/restricted_html_format
  - core/recipes/administrator_role
  - core/recipes/content_editor_role
  - core/recipes/image_media_type
  - core/recipes/basic_shortcuts
```

## Modules Installed

**Core**: help, path, navigation, media_library, layout_discovery, layout_builder
**Contrib**: field_sample_value, tempstore_plus, navigation_plus, twig_events, edit_plus, lb_plus, dropzonejs, section_library, lb_plus_section_library
**Extras**: edit_plus_non_lb_node, edit_plus_header_block, edit_plus_cta_block, edit_plus_teaser_block

## Configuration Created

| Config | Purpose |
|---|---|
| `node.type.landing_page` | Landing Page content type with Edit Mode enabled |
| `block_content.type.layout_block` | Layout Block type for nested layouts |
| `block_content.type.image` | Image block type |
| `field.storage.node.layout_builder__layout` | Layout Builder field storage for nodes |
| `field.storage.block_content.layout_builder__layout` | Layout Builder field storage for block content |
| `field.storage.block_content.field_image` | Image field storage |
| Entity form/view displays | Default displays for all created types |

## Pattern: Config Actions

```yaml
config:
  actions:
    # Add alignment button to CKEditor Full HTML toolbar
    editor.editor.full_html:
      addItemToToolbar:
        item_name: alignment
        position: 13

    # Configure sample values and Edit+ on body field
    field.field.block_content.basic.body:
      setThirdPartySettings:
        - module: field_sample_value
          key: id
          value: random_text
        - module: edit_plus
          key: disable
          value: false
        - module: edit_plus
          key: handle
          value: form_item
```

## Content Included

The recipe includes a default media entity (Druplicon image) for use as placeholder content:

- `content/file/a8849bfa-*.yml` + `druplicon.png`
- `content/media/827cb6a9-*.yml`

## `strict: false`

The recipe uses `strict: false` for config imports, which means:

- Config that already exists will be skipped (not overwritten)
- Reduces conflicts on existing sites
- But means existing config won't be updated

## Decision: Recipe vs Module-by-Module

| Approach | Pros | Cons |
|---|---|---|
| Recipe | Complete setup, working defaults | Conflicts with existing LB config |
| Module-by-module | Granular control, works on existing sites | Manual configuration needed |
| Recipe + manual cleanup | Quick start, then customize | Requires understanding of recipe actions |

## Common Mistakes

- **Do not re-apply the recipe expecting existing config to update** — `strict: false` skips config that already exists, so changes must be made manually.

## See Also

- [Installation & Setup](installation-setup.md)
- [Common Mistakes & Known Issues](common-mistakes-known-issues.md)
- Reference: `recipes/plus_suite/recipe.yml`
