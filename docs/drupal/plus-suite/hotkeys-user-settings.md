---
description: "Hotkeys and user settings — default keyboard shortcuts, per-user hotkey storage, SettingsSidebarEvent, and customization"
tldr: "Configure or customize keyboard shortcuts for tools. Hotkeys are stored per-user and customized via the Settings sidebar."
drupal_version: "11.x"
---

# Hotkeys & User Settings

## When to Use

> When configuring or customizing keyboard shortcuts for tools, or understanding how user preferences are stored.

## Default Hotkeys

| Tool | Default Key | Customizable? |
|---|---|---|
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

## Hotkey Storage

Per-user, stored in the `navigation_plus_settings` base field on user entities:

```php
$user->navigation_plus_settings[0]['hotkeys'] = [
  'pointer' => 'p',
  'place_block' => 'b',
  'edit_plus' => 'c',
  // ...
];
```

## Saving Hotkeys

Route: `navigation_plus.settings.save_user_hotkey`
Path: `/navigation-plus/save-user-hotkey/{tool_id}/{hotkey}`

Called via AJAX from the Settings sidebar → Hotkey configuration section.

## Settings Sidebar

The right sidebar has a Settings panel that dispatches `SettingsSidebarEvent`:

```php
$event = new SettingsSidebarEvent();
$this->eventDispatcher->dispatch($event);
// Subscribers add their settings forms to the sidebar
```

| Subscriber | Priority | Adds |
|---|---|---|
| `HotkeySettings` | 100 | Hotkey configuration UI |
| `NewMediaFileAssociationSettings` | default | File extension → block type mapping |

## Common Mistakes

- **Do not** assign hotkeys that conflict with browser shortcuts (e.g., `Ctrl+C`, `Ctrl+V`).
- **Do not** use multi-key combinations — the system only supports single character keys and modifier hold keys.

## See Also

- [Edit Mode & Navigation+](edit-mode-navigation-plus.md)
- [Sidebar System](sidebar-system.md)
- [Media Handling](media-handling.md)
