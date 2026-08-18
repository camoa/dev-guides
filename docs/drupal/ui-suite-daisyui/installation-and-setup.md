---
description: "Composer install, theme enable, dependency requirements, and post-installation verification"
tldr: "Composer install, theme enable, hard dependencies (ui_patterns, ui_icons) vs. optional submodules (ui_patterns_library, ui_styles_library, ui_patterns_layouts) that gate the admin browsers and Layout Builder grids -- most 404s are a missing submodule, not a broken theme."
---

# Installation & Setup

## Requirements

- Drupal 10.3+ or 11.x
- PHP 8.3+
- `ui_patterns` 2.x, `ui_icons` 2.0+ (hard dependencies)
- `ui_styles` 1.11+, `ui_skins` 1.1+ (recommended, not required since alpha6)

## Installation

```bash
composer require 'drupal/ui_suite_daisyui:^5.0@alpha'
```

This pulls in all required dependencies. Then enable:

```bash
# Hard dependencies -- the theme's info.yml refuses to install without these.
drush en ui_patterns ui_icons ui_icons_patterns

# The admin browsers the verification step below uses. Neither is a theme
# dependency, so nothing enables them for you.
drush en ui_patterns_library ui_styles_library

# Layout Builder integration -- without this submodule NO component appears
# in the "Choose a layout" dialog, grids included.
drush en ui_patterns_layouts

# Optional but recommended:
drush en ui_styles_block ui_skins
drush theme:enable ui_suite_daisyui
drush config:set system.theme default ui_suite_daisyui
```

## Post-Installation Verification

After enabling the theme, verify these admin paths:

| Path | Provided by | Purpose |
|---|---|---|
| `/admin/appearance/ui/components` | `ui_patterns_library` | Browse all 51 SDC components with live previews |
| `/admin/appearance/ui/styles` | `ui_styles_library` | Browse the 10 style plugins |
| `/admin/appearance/css-variables` | `ui_skins` | Configure 28 CSS variables |
| `/admin/appearance/settings/ui_suite_daisyui` | the theme itself | Theme settings, including the DaisyUI theme selector and the form display/label radios |

Three of these four are **submodule routes, not theme routes**. A 404 means the module in the middle column is not enabled, not that the theme is broken.

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

- **Enabling only the hard dependencies and expecting the admin UI** -- `ui_patterns`, `ui_icons` and `ui_icons_patterns` are the theme's declared dependencies, so Drupal installs them for you; `ui_patterns_library`, `ui_styles_library` and `ui_patterns_layouts` are not, so nothing does. The components render fine without them -- you just cannot browse, style or place them. WHY: the theme depends on the rendering engine, not on the authoring tools built on top of it.
- **Enabling `ui_styles` but not `ui_patterns_layouts` and then hunting for grid layouts** -- The "Choose a layout" dialog is populated by `ui_patterns_layouts` alone. Without it, Layout Builder shows only core's one/two/three-column layouts.
- **Using the 4.0.x branch** -- The 4.0.x branch targets DaisyUI 4 and is minimally maintained. WHY: DaisyUI 5 has breaking class name changes, and the 5.0.x branch is the active development target.

## See Also

- `drupal-ui-patterns.md` -- UI Patterns installation details
