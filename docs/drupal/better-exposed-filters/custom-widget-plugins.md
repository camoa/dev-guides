---
description: Create custom BEF filter, sort, or pager widget plugins — PHP 8.1 attribute syntax, key methods, and plugin discovery alter
drupal_version: "11.x"
---

# Custom Widget Plugins

## When to Use

> Use this guide when the built-in BEF widgets don't meet your needs and you want to create a custom filter, sort, or pager widget. Use `hook_better_exposed_filters_options_alter()` for simpler runtime changes that don't require a new plugin.

## Decision

| Type | Attribute | Base Class | Namespace |
|---|---|---|---|
| Filter | `#[FiltersWidget]` | `FilterWidgetBase` | `Plugin\better_exposed_filters\filter` |
| Sort | `#[SortWidget]` | `SortWidgetBase` | `Plugin\better_exposed_filters\sort` |
| Pager | `#[PagerWidget]` | `PagerWidgetBase` | `Plugin\better_exposed_filters\pager` |

## Pattern

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

  public static function isApplicable(mixed $filter = NULL, array $filter_options = []): bool {
    return is_a($filter, 'Drupal\views\Plugin\views\filter\InOperator');
  }

  public function exposedFormAlter(array &$form, FormStateInterface $form_state): void {
    $field_id = $this->getExposedFilterFieldId();
    parent::exposedFormAlter($form, $form_state); // ALWAYS call parent first

    if (!empty($form[$field_id])) {
      $form[$field_id]['#type'] = 'my_custom_element';
      $form['#attached']['library'][] = 'my_module/my_widget';
    }
  }
}
```

**Key methods to override:**

| Method | Purpose |
|---|---|
| `defaultConfiguration()` | Define config keys and defaults |
| `isApplicable()` | Control which filter types this works with |
| `buildConfigurationForm()` | Build Views UI config form |
| `exposedFormAlter()` | Transform exposed form element at runtime |

**Plugin discovery alter:**
```php
function my_module_better_exposed_filters_better_exposed_filters_filter_widget_info_alter(&$definitions) {
  unset($definitions['bef_sliders']); // Remove a widget
  $definitions['bef']['label'] = t('Enhanced Checkboxes'); // Modify a widget
}
```

Replace `filter` with `sort` or `pager` for those types.

## Common Mistakes

- **Wrong**: Plugin in wrong namespace → **Right**: Must be in `Plugin\better_exposed_filters\{filter|sort|pager}\`.
- **Wrong**: Not calling `parent::exposedFormAlter()` → **Right**: The parent handles collapsible, secondary, rewriting, sorting, and context. Always call parent first.
- **Wrong**: Missing config schema for custom widget → **Right**: Custom widgets need a schema entry in `config/schema/` for proper config export/import.

## See Also

- [Configuration Schema](configuration-schema.md)
- [Hooks & Alter Functions](hooks-alter.md)
- Reference: `web/modules/contrib/better_exposed_filters/src/Plugin/BetterExposedFiltersWidgetBase.php`
