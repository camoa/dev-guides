---
description: "Create custom BEF filter, sort, or pager widget plugins — PHP 8.1 attribute syntax, key methods, and plugin discovery alter"
tldr: "Use this guide when the built-in BEF widgets don't meet your needs and you want to create a custom filter, sort, or pager widget."
drupal_version: "11.x"
---

# Custom Widget Plugins

## When to Use

> When the built-in BEF widgets don't meet your needs and you want to create a custom filter, sort, or pager widget.

## Decision: Plugin Type

| Type | Attribute | Base Class | Namespace |
|---|---|---|---|
| Filter | `#[FiltersWidget]` | `FilterWidgetBase` | `Plugin\better_exposed_filters\filter` |
| Sort | `#[SortWidget]` | `SortWidgetBase` | `Plugin\better_exposed_filters\sort` |
| Pager | `#[PagerWidget]` | `PagerWidgetBase` | `Plugin\better_exposed_filters\pager` |

## Pattern: Creating a Custom Filter Widget

```php
<?php

namespace Drupal\my_module\Plugin\better_exposed_filters\filter;

use Drupal\better_exposed_filters\Attribute\FiltersWidget;
use Drupal\better_exposed_filters\Plugin\better_exposed_filters\filter\FilterWidgetBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[FiltersWidget(
  id: 'my_custom_widget',
  title: new TranslatableMarkup('My Custom Widget'),
)]
class MyCustomWidget extends FilterWidgetBase {

  public function defaultConfiguration(): array {
    return parent::defaultConfiguration() + [
      'my_option' => 'default_value',
    ];
  }

  public static function isApplicable(mixed $filter = NULL, array $filter_options = []): bool {
    // Return TRUE for filter types this widget supports.
    return is_a($filter, 'Drupal\views\Plugin\views\filter\InOperator');
  }

  public function buildConfigurationForm(array $form, FormStateInterface $form_state): array {
    $form = parent::buildConfigurationForm($form, $form_state);

    $form['my_option'] = [
      '#type' => 'textfield',
      '#title' => $this->t('My option'),
      '#default_value' => $this->configuration['my_option'],
    ];

    return $form;
  }

  public function exposedFormAlter(array &$form, FormStateInterface $form_state): void {
    $field_id = $this->getExposedFilterFieldId();
    parent::exposedFormAlter($form, $form_state);

    // Transform the form element.
    if (!empty($form[$field_id])) {
      $form[$field_id]['#type'] = 'my_custom_element';
      // Attach custom library.
      $form['#attached']['library'][] = 'my_module/my_widget';
    }
  }

}
```

## Pattern: Key Methods to Override

| Method | Purpose |
|---|---|
| `defaultConfiguration()` | Define configuration keys and defaults |
| `isApplicable()` | Control which filter types this widget works with |
| `buildConfigurationForm()` | Build the Views UI configuration form |
| `validateConfigurationForm()` | Validate configuration values |
| `submitConfigurationForm()` | Process submitted configuration |
| `exposedFormAlter()` | Transform the exposed form element at runtime |

## Pattern: Plugin Discovery Alter

To modify existing widget plugins, use the alter hook:
```php
function my_module_better_exposed_filters_better_exposed_filters_filter_widget_info_alter(&$definitions) {
  // Remove a widget.
  unset($definitions['bef_sliders']);

  // Modify a widget.
  $definitions['bef']['label'] = t('Enhanced Checkboxes');
}
```

## Common Mistakes

- **Wrong namespace** — Plugins must be in `Plugin\better_exposed_filters\{type}\` (e.g., `filter`, `sort`, or `pager`).
- **Not calling parent::exposedFormAlter()** — The parent handles collapsible, secondary, rewriting, sorting, and context. Always call parent first.
- **Missing config schema** — Custom widgets need a config schema entry in `config/schema/` for proper config export/import.

## See Also

- [Configuration Schema](configuration-schema.md) — schema requirements for custom widgets
- [Hooks & Alter Functions](hooks-alter.md) — alter hook for plugins
