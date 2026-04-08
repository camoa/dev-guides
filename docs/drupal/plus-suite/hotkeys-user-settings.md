---
description: Hotkeys and user settings — default keyboard shortcuts, per-user hotkey storage, SettingsSidebarEvent, and customization
drupal_version: "11.x"
---

# Hotkeys & User Settings

## When to Use

> Configure hotkeys during initial setup. Users can customize per-user via the Settings sidebar. Avoid key conflicts with browser shortcuts.

## Decision

| Tool | Default Key | Customizable? |
|------|------------|---------------|
| Pointer (Preview) | `p` | Yes |
| Place Block | `b` | Yes |
| Change (Edit+) | `c` | Yes |
| Move | `m` | Yes |
| Layout | `l` | Yes |
| Trash | `t` | Yes |
| Duplicate | `d` | Yes |
| Configure | `o` | Yes |
| Section Library | `s` | Yes |
| Show All Actions | `ALT` (hold) | Yes |

## Pattern

**Hotkey storage** (per-user on user entity):

```php
$user->navigation_plus_settings[0]['hotkeys'] = [
  'pointer' => 'p',
  'place_block' => 'b',
  'edit_plus' => 'c',
  // ...
];
```

**Save route:** `navigation_plus.settings.save_user_hotkey`
Path: `/navigation-plus/save-user-hotkey/{tool_id}/{hotkey}` (called via AJAX from Settings sidebar).

**Settings sidebar** dispatches `SettingsSidebarEvent` — subscribers add settings forms:

| Subscriber | Priority | Adds |
|------------|----------|------|
| `HotkeySettings` | 100 | Hotkey configuration UI |
| `NewMediaFileAssociationSettings` | default | File extension → block type mapping |

## Common Mistakes

- **Wrong**: Assigning hotkeys that conflict with browser shortcuts (`Ctrl+C`, `Ctrl+V`) → **Right**: Use single character keys that don't conflict with system shortcuts
- **Wrong**: Trying multi-key combinations → **Right**: System only supports single character keys and modifier hold keys (like ALT)

## See Also

- [Edit Mode & Navigation+](edit-mode-navigation-plus.md)
- [Sidebar System](sidebar-system.md)
- [Media Handling](media-handling.md)
