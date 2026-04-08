---
description: Edit Mode and Navigation+ — toolbar configuration, cookie-based state, bundle settings, and ShouldNotEditMode event
drupal_version: "11.x"
---

# Edit Mode & Navigation+

## When to Use

> Use Edit Mode for any content type using Layout Builder where editors need WYSIWYG page building. Disable it for read-only, API-sourced, or admin-form-based content types.

## Decision

| Scenario | Action |
|----------|--------|
| Content type uses Layout Builder | Enable Edit Mode with `place_block` default tool |
| Content type doesn't use Layout Builder | Don't enable Edit Mode |
| Read-only content types (API-sourced) | Disable Edit Mode |
| Content type uses custom admin forms | Disable Edit Mode |

## Pattern

**Activation flow:**
```
User clicks Edit Mode button in Navigation sidebar
  → JS sets cookie: navigationMode=edit
  → Page reloads
  → navigation_plus_preprocess_navigation() detects cookie
  → Edit mode toolbar renders with tool buttons
  → Layout Builder element replaced with LayoutBuilderPlus
  → User sees WYSIWYG page with tool indicators
```

**Configuration per content type** (Structure → Content Types → [Type] → Edit → "Navigation+" section):

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

**Global settings** (`/admin/config/content/plus-suite`):

| Setting | Purpose |
|---------|---------|
| Main color | Primary UI color (hex) |
| Secondary color | Secondary UI color |
| Highlight color | Active element highlight |

**ShouldNotEditModeEvent** — controls when Edit Mode should NOT activate:
- Bundle doesn't have Edit Mode enabled
- User lacks `use toolbar plus edit mode` permission
- Route is admin page, node add/edit form
- Path is `/` (front page)
- User lacks edit access to entity

Subscribe to `ShouldNotEditModeEvent` to add custom conditions.

## Common Mistakes

- **Wrong**: Enabling Edit Mode on a content type without Layout Builder → **Right**: Enable Layout Builder first, then configure Edit Mode
- **Wrong**: Forgetting per-bundle configuration → **Right**: Edit Mode must be enabled individually per content type under Navigation+ settings

## See Also

- [Mode Plugins](mode-plugins.md)
- [Tool Plugins](tool-plugins.md)
- [Permissions & Access](permissions-access.md)
- [Hotkeys & User Settings](hotkeys-user-settings.md)
