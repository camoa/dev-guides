---
description: Composer install, theme enable, dependency requirements, and post-installation verification
---

# Installation & Setup

## Requirements

- Drupal 10.3+ or 11.x
- PHP 8.3+
- `ui_patterns` 2.x, `ui_icons` 1.1+ (hard dependencies)
- `ui_styles` 1.11+, `ui_skins` 1.1+ (recommended, not required since alpha6)

## Installation

```bash
composer require 'drupal/ui_suite_daisyui:^5.0@alpha'
```

This pulls in all required dependencies. Then enable:

```bash
drush en ui_patterns ui_icons ui_icons_patterns
# Optional but recommended:
drush en ui_styles_block ui_skins
drush theme:enable ui_suite_daisyui
drush config:set system.theme default ui_suite_daisyui
```

## Post-Installation Verification

After enabling the theme, verify these admin paths:

| Path | Purpose |
|---|---|
| `/admin/appearance/ui/components` | Browse all 51 SDC components with live previews |
| `/admin/appearance/ui/styles` | Browse 30+ style utility categories |
| `/admin/appearance/css-variables` | Configure 25 CSS variables |
| `/admin/appearance/settings/ui_suite_daisyui` | Theme settings including DaisyUI theme selector |

## Default Block Configuration

The theme ships with 10 optional block configs that auto-install when the theme is enabled:

| Block | Region | Weight | Plugin |
|---|---|---|---|
| Site branding | `navbar_start` | -5 | `system_branding_block` |
| Main navigation | `navbar_center` | -4 | `system_menu_block:main` |
| User account menu | `navbar_end` | 0 | `system_menu_block:account` |
| Breadcrumbs | `content` | -6 | `system_breadcrumb_block` |
| Page title | `content` | -5 | `page_title_block` |
| Messages | `content` | -4 | `system_messages_block` |
| Primary admin actions | `content` | -3 | `local_actions_block` |
| Primary tabs | `content` | -2 | `local_tasks_block` (primary) |
| Secondary tabs | `content` | -1 | `local_tasks_block` (secondary) |
| Content | `content` | 1 | `system_main_block` |

## Common Mistakes

- **Not enabling `ui_icons_patterns`** -- Without this sub-module, icon props on components (button, step, timeline_item) will not render. WHY: `ui_icons_patterns` provides the bridge between UI Icons and UI Patterns prop types.
- **Using the 4.0.x branch** -- The 4.0.x branch targets DaisyUI 4 and is minimally maintained. WHY: DaisyUI 5 has breaking class name changes, and the 5.0.x branch is the active development target.

## See Also

- `drupal-ui-patterns.md` -- UI Patterns installation details
