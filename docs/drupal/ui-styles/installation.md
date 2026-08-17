---
description: "Install and enable UI Styles and its integration submodules on Drupal 11.4+."
tldr: "Require drupal/ui_styles via Composer, then enable only the integration submodules you need (block, layout_builder, ckeditor5, views, page, ui_patterns). The base module is the engine — enabling it alone adds no editor UI."
drupal_version: "11.x"
---

# UI Styles Installation

## When to Use

> Use this guide when setting up UI Styles for the first time on a Drupal 11.4+ site.

## Pattern

```bash
composer require drupal/ui_styles
drush en ui_styles
```

Enable only the relevant integration submodule(s):

| Submodule | Enables styles in |
|---|---|
| `ui_styles_block` | Block layout configuration form |
| `ui_styles_layout_builder` | Layout Builder block + section forms |
| `ui_styles_ckeditor5` | CKEditor 5 inline text formatting |
| `ui_styles_views` | Views display, pager, exposed filter forms |
| `ui_styles_page` | Theme regions and page wrapper |
| `ui_styles_entity_status` | Conditional styles based on entity publish status |
| `ui_styles_ui_patterns` | UI Patterns component prop integration |
| `ui_styles_library` | Standalone showcase page listing all defined styles |

## Compatibility

| Property | Value |
|---|---|
| Drupal core | `^11.4 \|\| ^12` |
| PHP | 8.3+ |
| External | `sabberworm/php-css-parser ^9.0` (via Composer for stylesheet generation) |

## Common Mistakes

- **Enabling `ui_styles` alone and wondering why nothing appears in forms** → The base module is the engine; integration submodules expose the UI
- **Forgetting Composer dependency on `php-css-parser`** → Stylesheet generation fails silently; check Composer install logs

## See Also

- [Overview](overview.md)
- [Style Definition Format](definition-format.md)
- [Stylesheet Generation](stylesheet-generation.md)
