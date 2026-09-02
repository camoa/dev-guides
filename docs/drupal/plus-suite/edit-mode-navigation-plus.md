---
description: "Edit Mode and Navigation+ — toolbar configuration, cookie-based state, bundle settings, and ShouldNotEditMode event"
tldr: "Use Edit Mode for any content type using Layout Builder where editors need WYSIWYG page building. Disable it for read-only, API-sourced, or admin-form-based content types."
drupal_version: "11.x"
---

# Edit Mode & Navigation+

## When to Use

> When you need to understand or configure the Edit Mode toggle, the Photoshop-like toolbar, and how Navigation+ orchestrates the editing experience.

## How Edit Mode Works

Edit Mode replaces the traditional Edit/Layout tabs with a unified editing experience accessible from the Navigation sidebar. When activated:

1. **Cookie-based state**: Mode stored in `navigationMode` cookie (e.g., `edit`)
2. **Toolbar transforms**: Navigation sidebar becomes a tool palette
3. **WYSIWYG rendering**: Published page renders with editing capabilities overlaid
4. **Tool system activates**: Tools like Place Block, Move, Trash become available

## Activation Flow

```
User clicks Edit Mode button in Navigation sidebar
  → JavaScript sets cookie: navigationMode=edit
  → Page reloads
  → navigation_plus_preprocess_navigation() detects cookie
  → Edit mode toolbar renders with tool buttons
  → Layout Builder element replaced with LayoutBuilderPlus element
  → User sees WYSIWYG page with tool indicators
```

## Configuration Per Content Type

Navigate to **Structure → Content Types → [Type] → Edit**. Under "Navigation+" section:

| Setting | Purpose |
|---|---|
| **Initial Mode** | Which mode activates when first editing (default: `edit`) |
| **Enabled Modes** | Toggle Edit Mode on/off per bundle |
| **Default Tool** | Which tool is active when entering Edit Mode (default: `place_block`) |

These are stored as third-party settings on `node.type.*`:

```yaml
third_party_settings:
  navigation_plus:
    initial_mode: edit
    status:
      edit: true
    modes:
      edit:
        default_tool: place_block
```

## Global Settings

Navigate to **Admin → Configuration → Content → Plus Suite** (`/admin/config/content/plus-suite`):

| Setting | Purpose |
|---|---|
| Main color | Primary UI color (hex) |
| Secondary color | Secondary UI color |
| Highlight color | Active element highlight |

## ShouldNotEditMode Event

Controls when Edit Mode should NOT activate. Default conditions:

- Bundle doesn't have Edit Mode enabled
- User lacks `use toolbar plus edit mode` permission
- Route is admin page, node add form, or node edit form
- Path is `/` (front page — use EditFrontPage mode instead)
- User lacks edit access to entity

Modules can subscribe to `ShouldNotEditModeEvent` to add custom conditions.

## Decision

| Scenario | Action |
|---|---|
| Content type doesn't use Layout Builder | Don't enable Edit Mode |
| Read-only content types (API-sourced) | Disable Edit Mode |
| Content type uses custom admin forms | Disable Edit Mode |
| All page-building content types | Enable Edit Mode with `place_block` default tool |

## Common Mistakes

- **Enabling Edit Mode on a content type without Layout Builder** — enable Layout Builder first, then configure Edit Mode.
- **Forgetting per-bundle configuration** — Edit Mode must be enabled individually per content type under Navigation+ settings.

## See Also

- [Mode Plugins](mode-plugins.md)
- [Tool Plugins](tool-plugins.md)
- [Permissions & Access](permissions-access.md)
- [Hotkeys & User Settings](hotkeys-user-settings.md)
