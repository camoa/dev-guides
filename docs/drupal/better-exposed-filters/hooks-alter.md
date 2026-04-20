---
description: BEF hooks — hook_better_exposed_filters_options_alter, plugin info alter, and theme-level alter patterns
tldr: "Use hooks when you need to programmatically modify BEF behavior — changing options, setting slider ranges dynamically, or altering widget availability — without creating a custom widget plugin."
drupal_version: "11.x"
---

# Hooks & Alter Functions

## When to Use

> Use hooks when you need to programmatically modify BEF behavior — changing options, setting slider ranges dynamically, or altering widget availability — without creating a custom widget plugin.

## Decision

| Hook | Purpose |
|---|---|
| `hook_better_exposed_filters_options_alter()` | Alter BEF options before form build (slider range, per-view config overrides) |
| `better_exposed_filters_better_exposed_filters_{type}_widget_info_alter` | Add/remove/modify widget plugin definitions |

## Pattern

```php
/**
 * Implements hook_better_exposed_filters_options_alter().
 */
function my_module_better_exposed_filters_options_alter(
  array &$options,
  ViewExecutable $view,
  DisplayPluginBase $displayHandler
): void {
  // Set dynamic slider min/max based on content.
  if ($view->id() === 'products' && $view->current_display === 'page_1') {
    $options['filter']['field_price_value']['slider_options']['bef_slider_min'] = 500;
    $options['filter']['field_price_value']['slider_options']['bef_slider_max'] = 5000;
  }
}

/**
 * Alter filter widget plugin definitions.
 */
function my_module_better_exposed_filters_better_exposed_filters_filter_widget_info_alter(
  &$definitions
): void {
  unset($definitions['bef_sliders']); // Remove a widget
  $definitions['bef']['class'] = 'Drupal\my_module\...\EnhancedRadioButtons';
}
// Replace 'filter' with 'sort' or 'pager' for those types.
```

The `better_exposed_filters_options` alter hook is also invoked at the theme level — themes can modify BEF behavior without a custom module.

## Common Mistakes

- **Wrong**: Using `hook_better_exposed_filters_alter` as the hook name → **Right**: The hook is `hook_better_exposed_filters_options_alter`.
- **Wrong**: Setting `$options['field_price_value']` directly → **Right**: The nested path is `$options['filter']['field_name']['config_key']`. Check the exact key path.

## See Also

- [Custom Widget Plugins](custom-widget-plugins.md)
- [Sliders Widget](sliders-widget.md)
- Reference: `web/modules/contrib/better_exposed_filters/better_exposed_filters.api.php`
