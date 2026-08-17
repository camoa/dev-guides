---
description: "Install UI Icons and enable only the submodules a site's integrations need, on Drupal core 11.3+."
tldr: "Composer-require drupal/ui_icons, enable it as the engine, then enable submodules per integration needed. Requires core 11.3+/12, PHP 8.3+; iconify_api and backport submodules were removed in 2.0.0."
drupal_version: "11.x"
---

# Installation

## When to Use

> Installing UI Icons for the first time, or deciding which submodules a site actually needs enabled.

## Pattern

```bash
composer require drupal/ui_icons
drush en ui_icons
```

The base module is the engine. Enable submodules per integration need:

| Submodule | Adds |
|---|---|
| `ui_icons_field` | `ui_icon` field type, widget, formatter; Link-field icon variants. Does **not** pull in `ui_icons_picker` |
| `ui_icons_ckeditor5` | "Icon" toolbar button + `<drupal-icon>` filter for CKEditor 5 |
| `ui_icons_text` | The `icon_embed` text filter (required for `ui_icons_ckeditor5` output) |
| `ui_icons_picker` | Modal grid picker form element (`icon_picker`). Depends on `ui_icons_field` |
| `ui_icons_patterns` | UI Patterns `icon` PropType + 4 data sources |
| `ui_icons_menu` | Icon field on `menu_link_content`, rendered automatically into link titles |
| `ui_icons_media` | Icon media source type. Depends on `ui_icons_field` |
| `ui_icons_canvas` | Makes the `ui_icon` field and its `icon_widget` editable as a Drupal Canvas component input. Depends on `canvas:canvas` + `ui_icons_field` |
| `ui_icons_library` | Admin browser at `/admin/appearance/ui/icons` |
| `ui_icons_font` | Font extractor (TTF/WOFF/codepoints/JSON/YAML) |

`ui_icons_iconify_api` and `ui_icons_backport` were **removed in 2.0.0** — they no longer exist on disk. If either was enabled on 1.x, `drush updatedb` runs `ui_icons_update_11201()`, which clears their leftover `core.extension` and `system.schema` entries. Do not try to uninstall them first; the module installer cannot resolve an extension that isn't there. For Iconify, the successor is the separate `drupal/iconify_icons` project.

## Decision: Compatibility

| Property | Value |
|---|---|
| Drupal core | `^11.3 \|\| ^12.0` — asserted in every `.info.yml`. Drupal 10 and 11.0–11.2 are not supported |
| PHP | 8.3+ (imposed by core) |
| Optional Composer | `dompdf/php-font-lib` (only for TTF/WOFF font extraction) |

The project's root `composer.json` carries no `require` block as of 2.0.0 — core compatibility is expressed solely through `core_version_requirement`. Nothing pins `dompdf/php-font-lib`; install it yourself if the font extractor needs to read binary font files.

## Common Mistakes

- **Wrong**: enabling `ui_icons_ckeditor5` without `ui_icons_text` → **Right**: the `<drupal-icon>` tag passes through to output untransformed without the filter module
- **Wrong**: forgetting `dompdf/php-font-lib` when using `.ttf` files → **Right**: install it, or use `.codepoints`/`.json`/`.yml` metadata to skip the dependency
- **Wrong**: trying to uninstall `ui_icons_field` and `ui_icons_picker` together on 1.x → **Right**: on 2.0.0 the dependency cycle is broken; picker depends on field, not the reverse

## See Also

- [UI Icons Overview](overview.md)
- [Icon Pack Format](pack-format.md)
- Reference: https://www.drupal.org/project/ui_icons
