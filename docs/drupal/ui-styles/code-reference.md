---
description: Key files, services, classes, and hooks in the UI Styles module for developers.
tldr: Core services are plugin.manager.ui_styles (style definitions) and ui_styles.stylesheet_generator (optimized CSS). The ui_styles_styles form element type accepts selected+extra default_value. Use hook_ui_styles_styles_alter() to modify definitions programmatically.
drupal_version: "11.x"
---

# Code Reference Map

## Key Files & Classes

| Location | Role |
|---|---|
| `ui_styles.services.yml` | Service definitions (`plugin.manager.ui_styles`, `ui_styles.stylesheet_generator`) |
| `src/StylePluginManager.php` | Main plugin manager; YAML discovery; alter hook |
| `src/Definition/StyleDefinition.php` | Value object representing one parsed style |
| `src/Element/Styles.php` | The `ui_styles_styles` render-array element |
| `src/Render/Element.php` | Static helpers (`addClasses`) |
| `src/Service/StylesheetGenerator.php` | CSS parsing + optimized output |
| `src/Plugin/UiStyles/Source/Checkbox.php` | Single-option widget |
| `src/Plugin/UiStyles/Source/Toolbar.php` | Icon-button widget |
| `src/Plugin/UiStyles/Source/Select.php` | Dropdown widget (fallback) |
| `modules/ui_styles_block/` | Block layout integration |
| `modules/ui_styles_layout_builder/` | Layout Builder integration |
| `modules/ui_styles_ckeditor5/` | CKEditor 5 inline-text integration |
| `modules/ui_styles_views/` | Views display integration |
| `modules/ui_styles_page/` | Theme regions + page wrapper |
| `modules/ui_styles_entity_status/` | Status-conditional styles |
| `modules/ui_styles_ui_patterns/` | UI Patterns prop integration |
| `modules/ui_styles_library/` | Standalone showcase page |

## Hooks

- `hook_ui_styles_styles_alter(array &$definitions)` — modify discovered style definitions before caching
- `hook_preprocess_block()`, `hook_preprocess_region()`, `hook_preprocess_page()` — used internally by submodules to inject classes

## Form Element Type

```php
$form['styles'] = [
  '#type' => 'ui_styles_styles',
  '#default_value' => ['selected' => [...], 'extra' => ''],
  '#drupal_theme' => 'mytheme',  // optional
];
```

## Requirements

- Drupal `^10.3 || ^11`
- PHP 8.3+
- `sabberworm/php-css-parser ^9.0`

## See Also

- [Programmatic Use](programmatic.md)
- [Stylesheet Generation](stylesheet-generation.md)
- Reference: `drupal/ui_styles` on drupal.org
