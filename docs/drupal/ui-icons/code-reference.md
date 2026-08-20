---
description: "Key UI Icons classes, services, hooks, form elements, and cache tags — 2.0.0 file paths are unverified; the 1.1.2 layout is procedural .module files."
tldr: "Core service is plugin.manager.icon_pack; UI Icons adds ui_icons.search and ui_icons.twig_extension. The src/Hook/ layout is an unverified 2.0.0 claim — 1.1.2 has no src/Hook/ dir and uses procedural .module files instead."
drupal_version: "11.x"
---

# Code Reference Map

## Key Files & Classes

| Location | Role |
|---|---|
| `ui_icons.info.yml` | Module metadata |
| `ui_icons.services.yml` | Services (`ui_icons.search`, `ui_icons.twig_extension`) |
| `ui_icons.install` | `ui_icons_update_11201()` — clears the removed backport/iconify modules |
| `src/Hook/UiIconsHooks.php` | hook_help, hook_theme, hook_preprocess_icon_selector; `THEME_LIBRARIES` maps admin theme → picker CSS library |
| `src/IconSearch.php` | Fuzzy search across packs (cached) |
| `src/Template/IconPreviewTwigExtension.php` | The `icon_preview()` Twig function |
| `src/Element/IconAutocomplete.php` | The `icon_autocomplete` form element |
| `src/Controller/IconAutocompleteController.php` | Backend for autocomplete suggestions |
| `templates/icon-selector.html.twig` | Autocomplete UI |
| `templates/icon-preview.html.twig` | Per-icon preview |
| `modules/ui_icons_field/src/Plugin/Field/FieldType/IconType.php` | `ui_icon` field type — `target_id` schema, `ICON_ID_PCRE` |
| `modules/ui_icons_field/src/Hook/UiIconsFieldHooks.php` | hook_config_schema_info_alter |
| `modules/ui_icons_ckeditor5/` | CKEditor 5 plugin + dialog; `js/ckeditor5_plugins/icon/src/iconToolbar.js` is the in-place Edit balloon |
| `modules/ui_icons_text/src/Plugin/Filter/IconEmbed.php` | The `icon_embed` text filter |
| `modules/ui_icons_text/src/Hook/UiIconsTextHooks.php` | Filter-format validation: allowed HTML, filter order, `filter_html_escape` |
| `modules/ui_icons_picker/src/Element/IconPicker.php` | Modal picker form element |
| `modules/ui_icons_patterns/src/Plugin/UiPatterns/PropType/IconPropType.php` | Icon PropType for UI Patterns |
| `modules/ui_icons_menu/src/Hook/UiIconsMenuHooks.php` | Menu base-field alter + the three hooks that render icons into link titles |
| `modules/ui_icons_media/` | Media source plugin |
| `modules/ui_icons_canvas/src/Hook/UiIconsCanvasHooks.php` | Canvas widget transform + `x-canvas-prop: ui-icon` shape routing |
| `modules/ui_icons_library/src/Controller/LibraryIndex.php` | Admin browser |
| `modules/ui_icons_library/src/Hook/UiIconsLibraryHooks.php` | hook_theme |
| `modules/ui_icons_font/src/Plugin/IconExtractor/FontExtractor.php` | Font extractor |
| `modules/ui_icons_font/src/Hook/UiIconsFontRequirements.php` | Status-report check for `dompdf/php-font-lib` |

The project ships **no `.module` files** as of 2.0.0 — every hook is an attributed method on a `src/Hook/` class.

> **The file paths in the table above are 2.0.0 paths and are unverified.** On 1.1.2 the layout is
> the pre-OO one: there is no `src/Hook/` directory anywhere in the project, no `ui_icons.install`,
> and the hooks live in procedural `.module` files — `ui_icons.module` (`ui_icons_help()`,
> `ui_icons_theme()`, `template_preprocess_icon_selector()`) and `ui_icons_menu.module`
> (`ui_icons_menu_entity_base_field_info_alter()`, `ui_icons_menu_preprocess_menu()`,
> `ui_icons_menu_link_alter()`, `ui_icons_menu_navigation_menu_link_tree_alter()`). Note that the
> **hook set** is verified — those four menu hooks and their behaviour are exactly what
> [Menu Integration](menu.md) describes — it is only the class paths that are unread.
> `THEME_LIBRARIES` likewise does not exist on 1.1.2, where the same job is done by a private
> `_ui_icons_is_theme_active()` helper that special-cases `gin`, `ui_suite_daisyui` and
> `ui_suite_dsfr` (and nothing for Claro). `ui_icons.services.yml` and its two services
> (`ui_icons.search`, `ui_icons.twig_extension`) are verified on 1.1.2 and unchanged.

## Drupal Core Icon API (the engine)

- `\Drupal\Core\Theme\Icon\IconDefinition`
- `\Drupal\Core\Theme\Icon\IconDefinitionInterface`
- `\Drupal\Core\Theme\Icon\IconExtractorBase`
- `\Drupal\Core\Theme\Icon\IconPackManagerInterface`
- `#[\Drupal\Core\Theme\Icon\Attribute\IconExtractor]`
- Service: `plugin.manager.icon_pack`

## Hooks Used

All are `#[Hook]`-attributed methods on 2.0.0 (unverified — see caveat above); on 1.1.2 the same hook set is procedural functions in `.module` files.

- `hook_help` — admin help
- `hook_theme` — register icon-selector and icon-preview templates (also in ui_icons_library)
- `hook_preprocess_icon_selector` — attach theme-specific picker libraries (default admin/Claro, gin, daisyui, dsfr)
- `hook_entity_base_field_info_alter` (ui_icons_menu) — add icon to menu_link_content
- `hook_preprocess_menu`, `hook_navigation_menu_link_tree_alter`, `hook_link_alter` (ui_icons_menu) — render the icon into link titles
- `hook_form_filter_format_add_form_alter` / `hook_form_filter_format_edit_form_alter` (ui_icons_text) — attach the filter-order and allowed-HTML validation
- `hook_config_schema_info_alter` (ui_icons_field)
- `hook_runtime_requirements` (ui_icons_font) — the font-library status check
- `hook_field_widget_info_alter`, `hook_canvas_storable_prop_shape_alter` (ui_icons_canvas)

## Form Element Types

- `icon_autocomplete` — text + autocomplete dropdown
- `icon_picker` — modal grid picker (extends autocomplete)

## Cache

Cache tags: `icon_pack_plugin`, `icon_pack_collector`. Clear with `drush cr` or by invalidating these tags.

## Common Mistakes

- **Wrong**: looking for `src/Hook/UiIconsHooks.php` (or any `src/Hook/` class) on a 1.1.2 site → **Right**: that layout is 2.0.0-only and unverified; on 1.1.2 the same logic lives in `ui_icons.module` and `ui_icons_menu.module`
- **Wrong**: assuming `ui_icons.install` exists on every version → **Right**: 1.1.2 ships no install file at all; `ui_icons_update_11201()` can only run on 2.0.0

## See Also

- [Field API Integration](field-api.md)
- [Menu Integration](menu.md)
- Reference: `drupal-ui-styles.md` — apply utility classes around icons
- Reference: `drupal-ui-skins.md` — set CSS variables consumed by icon templates
- Reference: `drupal-ui-patterns.md` — declare icon-typed props on components
- Reference: `drupal-ui-suite-daisyui.md` — Heroicons preconfigured for DaisyUI
