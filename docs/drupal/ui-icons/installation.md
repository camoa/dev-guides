---
description: "Install UI Icons and enable only the submodules a site's integrations need — 2.0.0 claims vs what 1.1.2 actually does."
tldr: "Composer-require drupal/ui_icons, then enable submodules per integration needed. The submodule inventory and the ^11.3||^12.0 range are unverified 2.0.0 claims — 1.1.2's effective floor is Drupal 11.1+, since only ui_icons_backport states ^11.1 outright and the rest depend on the base module anyway."
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

The whole table above is a **2.0.0 claim taken from release notes, unread against 2.0.0 source** (see [Overview](overview.md)). On 1.1.2 the inventory and the dependency directions are different, and the differences are the ones a site builder trips over:

| Claim (2.0.0, unverified) | What 1.1.2 on disk actually does |
|---|---|
| `ui_icons_field` does **not** pull in `ui_icons_picker` | It does. `modules/ui_icons_field/ui_icons_field.info.yml` lists `ui_icons:ui_icons_picker`, and `ui_icons_picker.info.yml` lists `ui_icons:ui_icons_field` — the mutual cycle the 2.0.0 notes claim to have broken |
| `ui_icons_canvas` exists | No such directory. The 1.1.2 submodules are backport, ckeditor5, field, font, iconify_api, library, media, menu, patterns, picker, text |
| `ui_icons_iconify_api` and `ui_icons_backport` are gone | Both still ship, as `lifecycle: deprecated` **empty placeholders** — no code, only an `.info.yml` pointing at the successor. That is the state 2.0.0 is said to have finished cleaning up |

`ui_icons_iconify_api` and `ui_icons_backport` were **removed in 2.0.0** — they no longer exist on disk. If either was enabled on 1.x, `drush updatedb` runs `ui_icons_update_11201()`, which clears their leftover `core.extension` and `system.schema` entries. Do not try to uninstall them first; the module installer cannot resolve an extension that isn't there. For Iconify, the successor is the separate `drupal/iconify_icons` project. (Unverified: 1.1.2 ships no `ui_icons.install` at all, so this update hook can only exist in 2.0.0.)

## Decision: Compatibility

| Property | Value |
|---|---|
| Drupal core | `^11.3 \|\| ^12.0` — asserted in every `.info.yml`. Drupal 10 and 11.0–11.2 are not supported |
| PHP | 8.3+ (imposed by core: `core/composer.json` requires `>=8.3.0`) |
| Optional Composer | `dompdf/php-font-lib` (only for TTF/WOFF font extraction) |

The project's root `composer.json` carries **no `require` block** as of 2.0.0 — core compatibility is expressed solely through `core_version_requirement`. Nothing pins `dompdf/php-font-lib`; install it yourself if the font extractor needs to read binary font files.

> **Both rows above are unverified 2.0.0 claims, and 1.1.2 contradicts both.** On 1.1.2 the base
> `ui_icons.info.yml` asserts `core_version_requirement: ^11.1`, and its root `composer.json`
> requires `{"drupal/core": "^11"}` — so **1.1.2 needs Drupal 11.1+**. Ten of its eleven
> submodules declare a looser `^10.3 || ^11.0`, but every one depends on the base module, so that
> range is unreachable and the effective floor stays 11.1; `ui_icons_backport` is the exception
> and declares `^11.1` outright. If you are on 1.x, read your own `.info.yml`; do not apply the
> 2.0.0 range.

## Common Mistakes

- **Wrong**: enabling `ui_icons_ckeditor5` and expecting icons to render → **Right**: the module is only the editor half. `ui_icons_text` comes along as a hard dependency, but its `icon_embed` filter still has to be switched on per text format; until then `<drupal-icon>` passes through untransformed
- **Wrong**: forgetting `dompdf/php-font-lib` when using `.ttf` files → **Right**: the status report shows a "Missing Font library!" warning and the font pack yields no icons. Use `.codepoints`, `.json`, or `.yml` metadata if you don't want the dep
- **Wrong**: trying to uninstall `ui_icons_field` and `ui_icons_picker` together on 1.x → **Right**: they depended on each other, so neither could go. 2.0.0 broke the cycle; the dependency now runs picker → field only
- **Wrong**: enabling only `ui_icons_menu` expecting a narrow menu-only footprint → **Right**: it depends on `menu_ui` + `ui_icons_field`, so enabling it also pulls in the whole Field API integration
- **Wrong**: applying the `^11.3 || ^12.0` compatibility range to a 1.x install → **Right**: 1.1.2's effective floor is Drupal 11.1+ — the base module and `ui_icons_backport` both assert `^11.1`; the other ten submodules' looser `^10.3 || ^11.0` is unreachable since every one of them depends on the base module. Check your own `.info.yml` before assuming the 2.0.0 range applies

## See Also

- [UI Icons Overview](overview.md)
- [Icon Pack Format](pack-format.md)
- Reference: https://www.drupal.org/project/ui_icons
