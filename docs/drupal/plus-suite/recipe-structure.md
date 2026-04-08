---
description: Plus Suite recipe structure — dependencies, modules installed, configuration created, config actions, and strict:false behavior
drupal_version: "11.x"
---

# Recipe Structure

## When to Use

> Reference this when troubleshooting recipe application, understanding what gets installed, or deciding whether to use recipe vs manual installation.

## Decision

| Approach | Pros | Cons |
|----------|------|------|
| Recipe | Complete setup, working defaults | Conflicts with existing LB config |
| Module-by-module | Granular control, works on existing sites | Manual configuration needed |
| Recipe + manual cleanup | Quick start, then customize | Requires understanding of recipe actions |

## Pattern

**Recipe dependencies** (core recipes applied):
- `basic_block_type`, `basic_html_format_editor`, `full_html_format_editor`
- `core_recommended_admin_theme`, `core_recommended_front_end_theme`
- `administrator_role`, `content_editor_role`
- `image_media_type`, `basic_shortcuts`

**Modules installed:**
- Core: `help`, `path`, `navigation`, `media_library`, `layout_discovery`, `layout_builder`
- Contrib: `field_sample_value`, `tempstore_plus`, `navigation_plus`, `twig_events`, `edit_plus`, `lb_plus`, `dropzonejs`, `section_library`, `lb_plus_section_library`
- Extras: `edit_plus_non_lb_node`, `edit_plus_header_block`, `edit_plus_cta_block`, `edit_plus_teaser_block`

**Configuration created:**

| Config | Purpose |
|--------|---------|
| `node.type.landing_page` | Landing Page content type with Edit Mode enabled |
| `block_content.type.layout_block` | Layout Block type for nested layouts |
| `block_content.type.image` | Image block type |
| `field.storage.node.layout_builder__layout` | Layout Builder field storage |

**Config actions example:**
```yaml
config:
  actions:
    field.field.block_content.basic.body:
      setThirdPartySettings:
        - module: field_sample_value
          key: id
          value: random_text
        - module: edit_plus
          key: handle
          value: form_item
```

**`strict: false`** — existing config is skipped (not overwritten). Reduces conflicts but means existing config won't be updated by re-applying the recipe.

## Common Mistakes

- **Wrong**: Applying recipe on existing site with LB configured → **Right**: Recipe fails on `field.storage.node.layout_builder__layout` conflict; install manually
- **Wrong**: Re-applying recipe expecting config updates → **Right**: `strict: false` skips existing config; changes must be made manually

## See Also

- [Installation & Setup](installation-setup.md)
- [Common Mistakes & Known Issues](common-mistakes-known-issues.md)
- Reference: `drupal/plus_suite/recipes/plus_suite/recipe.yml`
