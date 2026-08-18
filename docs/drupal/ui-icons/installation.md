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
| `ui_icons_ckeditor5` | "Icon" toolbar button + `<drupal-icon>` dialog for CKEditor 5. Depends on `ckeditor5` + `ui_icons_text`, so enabling it pulls the filter module in |
| `ui_icons_text` | The `icon_embed` text filter that turns `<drupal-icon>` into markup |
| `ui_icons_picker` | Modal grid picker form element (`icon_picker`). Depends on `ui_icons_field` |
| `ui_icons_patterns` | UI Patterns `icon` PropType + 4 data sources |
| `ui_icons_menu` | Icon field on `menu_link_content`, rendered automatically into link titles. Depends on `menu_ui` + `ui_icons_field`, so it pulls the whole Field API integration in |
| `ui_icons_media` | Icon media source type. Depends on `ui_icons_field` |
| `ui_icons_canvas` | Makes the `ui_icon` field and its `icon_widget` editable as a Drupal Canvas component input. Depends on `canvas:canvas` + `ui_icons_field` |
| `ui_icons_library` | Admin browser at `/admin/appearance/ui/icons` |
| `ui_icons_font` | Font extractor (TTF/WOFF/codepoints/JSON/YAML) |

`ui_icons_iconify_api` and `ui_icons_backport` were **removed in 2.0.0** — they no longer exist on disk. If either was enabled on 1.x, `drush updatedb` runs `ui_icons_update_11201()`, which clears their leftover `core.extension` and `system.schema` entries. Do not try to uninstall them first; the module installer cannot resolve an extension that isn't there. For Iconify, the successor is the separate `drupal/iconify_icons` project.

## Decision: Compatibility

| Property | Value |
|---|---|
| Drupal core | `^11.3 \|\| ^12.0` — asserted in every `.info.yml`. Drupal 10 and 11.0–11.2 are not supported |
| PHP | 8.3+ (imposed by core: `core/composer.json` requires `>=8.3.0`) |
| Optional Composer | `dompdf/php-font-lib` (only for TTF/WOFF font extraction) |

The project's root `composer.json` carries **no `require` block** as of 2.0.0 — core compatibility is expressed solely through `core_version_requirement`. Nothing pins `dompdf/php-font-lib`; install it yourself if the font extractor needs to read binary font files.

## Common Mistakes

- **Wrong**: enabling `ui_icons_ckeditor5` and expecting icons to render → **Right**: the module is only the editor half. `ui_icons_text` comes along as a hard dependency, but its `icon_embed` filter still has to be switched on per text format; until then `<drupal-icon>` passes through untransformed
- **Wrong**: forgetting `dompdf/php-font-lib` when using `.ttf` files → **Right**: the status report shows a "Missing Font library!" warning and the font pack yields no icons. Use `.codepoints`, `.json`, or `.yml` metadata if you don't want the dep
- **Wrong**: trying to uninstall `ui_icons_field` and `ui_icons_picker` together on 1.x → **Right**: they depended on each other, so neither could go. 2.0.0 broke the cycle; the dependency now runs picker → field only
- **Wrong**: enabling only `ui_icons_menu` expecting a narrow menu-only footprint → **Right**: it depends on `menu_ui` + `ui_icons_field`, so enabling it also pulls in the whole Field API integration

## See Also

- [UI Icons Overview](overview.md)
- [Icon Pack Format](pack-format.md)
- Reference: https://www.drupal.org/project/ui_icons
