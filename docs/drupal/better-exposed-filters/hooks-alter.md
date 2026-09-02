---
description: "BEF hooks — hook_better_exposed_filters_options_alter, plugin info alter, and theme-level alter patterns"
tldr: "Use hooks when you need to programmatically modify BEF behavior — changing options, setting slider ranges dynamically, or altering widget availability."
drupal_version: "11.x"
---

# Hooks & Alter Functions

## When to Use

> When you need to programmatically modify BEF behavior — changing options, setting slider ranges dynamically, or altering widget availability.

## Decision: Available Hooks

| Hook | Defined In | Purpose |
|---|---|---|
| `hook_better_exposed_filters_options_alter()` | `better_exposed_filters.api.php` | Alter BEF options before form build |
| `better_exposed_filters_better_exposed_filters_{type}_widget_info` | Plugin manager | Alter plugin definitions (add/remove/modify widgets) |
| `hook_form_views_ui_config_item_form_alter()` | `better_exposed_filters.module` | Adds token info to filter expose settings |

## Pattern: hook_better_exposed_filters_options_alter

```php
/**
 * Implements hook_better_exposed_filters_options_alter().
 */
function my_module_better_exposed_filters_options_alter(array &$options, ViewExecutable $view, DisplayPluginBase $displayHandler) {
  // Set dynamic slider min/max based on content.
  if ($view->id() === 'products' && $view->current_display === 'page_1') {
    $options['filter']['field_price_value']['slider_options']['bef_slider_min'] = 500;
    $options['filter']['field_price_value']['slider_options']['bef_slider_max'] = 5000;
  }
}
```

## Pattern: Plugin Info Alter

```php
/**
 * Alter filter widget plugin definitions.
 */
function my_module_better_exposed_filters_better_exposed_filters_filter_widget_info_alter(&$definitions) {
  // Remove a widget from the options.
  unset($definitions['bef_sliders']);

  // Change a widget's class.
  $definitions['bef']['class'] = 'Drupal\my_module\Plugin\better_exposed_filters\filter\EnhancedRadioButtons';
}
```

Replace `filter` with `sort` or `pager` for those widget types.

## Pattern: Theme-Level Alter

The `better_exposed_filters_options` alter hook is also invoked at the theme level, allowing themes to modify BEF behavior without a custom module.

## Common Mistakes

- **Wrong hook name** — The options alter hook is `hook_better_exposed_filters_options_alter`, not `hook_better_exposed_filters_alter`.
- **Modifying wrong array level** — The `$options` array has nested structure: `$options['filter']['field_name']['config_key']`. Check the exact key path.

## See Also

- [Custom Widget Plugins](custom-widget-plugins.md) — creating custom plugins
- [Sliders Widget](sliders-widget.md) — slider-specific options
- Reference: `web/modules/contrib/better_exposed_filters/better_exposed_filters.api.php`
