---
description: Key files, classes, services, hooks, form elements, and cache tags for the UI Icons module.
tldr: Core services are plugin.manager.icon_pack (icon discovery/retrieval) and ui_icons.twig_extension (the icon_preview() Twig function). Form element types are icon_autocomplete and icon_picker. Cache tags are icon_pack_plugin and icon_pack_collector — clear with drush cr.
drupal_version: "11.x"
---

# Code Reference Map

## Key Files & Classes

| Location | Role |
|---|---|
| `ui_icons.services.yml` | Services (`ui_icons.search`, `ui_icons.twig_extension`) |
| `ui_icons.module` | hook_help, hook_theme, hook_preprocess_icon_selector |
| `src/IconSearch.php` | Fuzzy search across packs (cached) |
| `src/Template/IconPreviewTwigExtension.php` | The `icon_preview()` Twig function |
| `src/Element/IconAutocomplete.php` | The `icon_autocomplete` form element |
| `src/Controller/IconAutocompleteController.php` | Backend for autocomplete suggestions |
| `templates/icon-selector.html.twig` | Autocomplete UI |
| `templates/icon-preview.html.twig` | Per-icon preview |
| `modules/ui_icons_field/` | Field type, widget, formatter |
| `modules/ui_icons_ckeditor5/` | CKEditor 5 plugin + dialog |
| `modules/ui_icons_text/src/Plugin/Filter/IconEmbed.php` | The `icon_embed` text filter |
| `modules/ui_icons_picker/src/Element/IconPicker.php` | Modal picker form element |
| `modules/ui_icons_patterns/src/Plugin/UiPatterns/PropType/IconPropType.php` | Icon PropType for UI Patterns |
| `modules/ui_icons_menu/ui_icons_menu.module` | Menu link entity field info alter |
| `modules/ui_icons_media/` | Media source plugin |
| `modules/ui_icons_library/src/Controller/LibraryIndex.php` | Admin browser |
| `modules/ui_icons_font/src/Plugin/IconExtractor/FontExtractor.php` | Font extractor |

## Drupal Core Icon API

| Symbol | Role |
|---|---|
| `\Drupal\Core\Theme\Icon\IconDefinition` | Icon value object |
| `\Drupal\Core\Theme\Icon\IconExtractorBase` | Base class for extractor plugins |
| `\Drupal\Core\Theme\Icon\IconPackManagerInterface` | Plugin manager interface |
| `#[\Drupal\Core\Theme\Icon\Attribute\IconExtractor]` | Plugin attribute for extractor discovery |
| `plugin.manager.icon_pack` | Service for getting/listing icons |

## Form Element Types

| Element | Description |
|---|---|
| `icon_autocomplete` | Text input + autocomplete dropdown |
| `icon_picker` | Modal grid picker (extends autocomplete) |

## Hooks

| Hook | Location | Purpose |
|---|---|---|
| `hook_help` | `ui_icons.module` | Admin help |
| `hook_theme` | `ui_icons.module` | Register icon-selector and icon-preview templates |
| `hook_preprocess_icon_selector` | `ui_icons.module` | Attach theme-specific picker libraries |
| `hook_entity_base_field_info_alter` | `ui_icons_menu.module` | Add icon to menu_link_content |

## Cache

| Cache tag | When to invalidate |
|---|---|
| `icon_pack_plugin` | After changing pack YAML or icon files |
| `icon_pack_collector` | After enabling/disabling packs |

Clear both with `drush cr`.

## See Also

- [Overview](overview.md)
- [UI Styles](../ui-styles/index.md) — apply utility classes around icons
- [UI Skins](../ui-skins/index.md) — CSS variables consumed by icon templates
- [UI Patterns](../ui-patterns/index.md) — icon-typed props on components
- [UI Suite DaisyUI](../ui-suite-daisyui/index.md) — Heroicons preconfigured
