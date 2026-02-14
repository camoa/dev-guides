---
description: Reference of core block plugins available in Drupal
drupal_version: "11.x"
---

# Core Block Plugins Reference

## When to Use

Finding existing core block plugins to reuse, extend, or understand patterns.

## Decision

| Module | Notable Blocks | Pattern |
|--------|----------------|---------|
| system | branding, breadcrumb, main, menu, messages, page_title, local_tasks | SystemMenuBlock uses derivatives |
| user | user_login_block | Access: anonymous only, uses FormBuilder |
| search | search_form_block | Renders search form |
| help | help_block | Context-sensitive help |
| views | views_block | Derivative per Views block display |
| block_content | block_content | Derivative per content block UUID |
| layout_builder | inline_block, field_block, extra_field_block | Derivatives per type/field |

## Pattern

**System Module Blocks:**
- `system_branding_block` — Site logo, name, slogan with toggles
- `system_breadcrumb_block` — Breadcrumb navigation trail
- `system_main_block` — Main page content (required for most pages)
- `system_menu_block` — Menu tree display with derivatives per menu
- `system_messages_block` — Status/error/warning messages
- `system_powered_by_block` — "Powered by Drupal" text
- `page_title_block` — Page title (h1)
- `local_actions_block` — Action links (e.g., "Add content")
- `local_tasks_block` — Tab navigation

**User Module Blocks:**
- `user_login_block` — User login form
  - Access: Anonymous users only
  - Uses `FormBuilderInterface` to render `UserLoginForm`
  - Lazy builder for dynamic form action URL

**Views Module Blocks:**
- `views_block` — Generic block for Views displays
  - Derivative per Views block display
  - Plugin ID format: `views_block:{view_id}-{display_id}`

**Block Content Module Blocks:**
- `block_content` — Wrapper for BlockContent entities
  - Derivative per content block instance
  - Plugin ID format: `block_content:{uuid}`

**Layout Builder Blocks:**
- `inline_block` — Non-reusable inline blocks (derivative per block content type)
- `field_block` — Entity fields as blocks (derivative per field on fieldable entities)
- `extra_field_block` — Extra fields as blocks (derivative from `hook_entity_extra_field_info()`)

**Reference:** Browse `core/modules/*/src/Plugin/Block/` directories

## Common Mistakes

- **Wrong**: Recreating blocks that exist in core → **Right**: Check core first; many common needs covered
- **Wrong**: Not checking for derivatives → **Right**: Many plugins use derivatives (menus, views, content blocks)
- **Wrong**: Using deprecated block plugins → **Right**: Core removes old blocks; check change records
- **Wrong**: Assuming all core blocks are always available → **Right**: Some depend on modules being enabled

## See Also

- [Creating Block Plugins](creating-block-plugins.md)
- [Programmatic Block Operations](programmatic-operations.md)
- Reference: Browse `core/modules/*/src/Plugin/Block/` directories
