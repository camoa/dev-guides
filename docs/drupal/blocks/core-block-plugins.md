---
description: Reference of core block plugins available in Drupal — system, user, views, layout_builder
tldr: "Check here before creating a custom block. Many common needs (menus, branding, login, search, views) are covered by core plugins."
drupal_version: "11.x"
---

# Core Block Plugins Reference

## When to Use

> Finding existing core block plugins to reuse, extend, or understand patterns.

## Items

#### System Module Blocks
**Module:** `core/modules/system`

- **system_branding_block** — Site logo, name, slogan with toggles
- **system_breadcrumb_block** — Breadcrumb navigation trail
- **system_main_block** — Main page content (required for most pages)
- **system_menu_block** — Menu tree display with derivatives per menu
- **system_messages_block** — Status/error/warning messages
- **system_powered_by_block** — "Powered by Drupal" text
- **page_title_block** — Page title (h1)
- **local_actions_block** — Action links (e.g., "Add content")
- **local_tasks_block** — Tab navigation

**Notable pattern:** SystemMenuBlock uses derivatives for each menu

#### User Module Blocks
**Module:** `core/modules/user`

- **user_login_block** — User login form
  - Access: Anonymous users only
  - Uses `FormBuilderInterface` to render `UserLoginForm`
  - Lazy builder for dynamic form action URL

#### Search Module Blocks
**Module:** `core/modules/search`

- **search_form_block** — Search form
  - Renders search form for configured search pages

#### Help Module Blocks
**Module:** `core/modules/help`

- **help_block** — Context-sensitive help text
  - Shows help for current route

#### Views Module Blocks
**Module:** `core/modules/views`

- **views_block** — Generic block for Views displays
  - Derivative per Views block display
  - Plugin ID format: `views_block:{view_id}-{display_id}`

#### Block Content Module Blocks
**Module:** `core/modules/block_content`

- **block_content** — Wrapper for BlockContent entities
  - Derivative per content block instance
  - Plugin ID format: `block_content:{uuid}`

#### Layout Builder Blocks
**Module:** `core/modules/layout_builder`

- **inline_block** — Non-reusable inline blocks
  - Derivative per block content type
- **field_block** — Entity fields as blocks
  - Derivative per field on fieldable entities
- **extra_field_block** — Extra fields as blocks
  - Derivative for items from `hook_entity_extra_field_info()`

#### Statistics Module Blocks
**Module:** `core/modules/statistics` (if enabled)

- **statistics_popular_block** — Popular content listing

## Common Mistakes

- Recreating blocks that exist in core → Check core first; many common needs covered
- Not checking for derivatives → Many plugins use derivatives (menus, views, content blocks)
- Using deprecated block plugins → Core removes old blocks; check change records
- Assuming all core blocks are always available → Some depend on modules being enabled

## See Also

- [Creating Block Plugins](creating-block-plugins.md) (for custom blocks)
- [Programmatic Block Operations](programmatic-operations.md) (for listing plugins)
- Reference: Browse `core/modules/*/src/Plugin/Block/` directories
