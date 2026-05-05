---
description: Install UI Icons and choose which submodules to enable per integration need.
tldr: Require drupal/ui_icons via Composer and enable only the submodules for integrations the site uses (field, ckeditor5, patterns, menu, etc.). Enabling ui_icons_ckeditor5 without ui_icons_text leaves drupal-icon tags unrendered in output.
drupal_version: "11.x"
---

# UI Icons Installation

## When to Use

> Installing UI Icons for the first time or adding a new integration submodule.

## Pattern

```bash
composer require drupal/ui_icons
drush en ui_icons
```

Enable submodules per integration need:

| Submodule | Adds |
|---|---|
| `ui_icons_field` | `ui_icon` field type, widget, formatter; Link-field icon variants |
| `ui_icons_ckeditor5` | "Icon" toolbar button + `<drupal-icon>` filter for CKEditor 5 |
| `ui_icons_text` | The `icon_embed` text filter (required for ui_icons_ckeditor5 output) |
| `ui_icons_picker` | Modal grid picker form element (`icon_picker`) |
| `ui_icons_patterns` | UI Patterns `icon` PropType + 4 data sources |
| `ui_icons_menu` | Icon widget on menu_link_content entity |
| `ui_icons_media` | Icon media source type |
| `ui_icons_library` | Admin browser at `/admin/appearance/ui-libraries/icons` |
| `ui_icons_font` | Font extractor (TTF/WOFF/codepoints/JSON/YAML) |

Do not enable `ui_icons_iconify_api` or `ui_icons_backport` — both are deprecated/empty.

## Decision: Drupal version compatibility

| UI Icons version | Drupal core requirement | Notes |
|---|---|---|
| 1.1.x | `^11.1` | Uses core Icon API; backport submodule is empty |
| 1.0.x | `^10.4 \|\| ^11` | Ships `ui_icons_backport` with the core API shim |

## Common Mistakes

- **Wrong**: enabling `ui_icons_ckeditor5` without `ui_icons_text` → **Right**: both must be enabled; the text filter transforms `<drupal-icon>` tags at render time
- **Wrong**: forgetting `dompdf/php-font-lib` when using `.ttf` font files → **Right**: add it via Composer, or use `.codepoints`/`.json`/`.yml` metadata instead
- **Wrong**: enabling all submodules "just in case" → **Right**: each adds form alters and routes; enable only what the site uses

## See Also

- [Overview](overview.md)
- [Icon Pack Format](pack-format.md)
- [Font Extractor](extractors.md)
