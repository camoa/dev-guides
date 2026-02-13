---
description: Custom input widgets for field types in entity forms
drupal_version: "11.x"
---

# Field Widget Development

## When to Use

When creating custom input interfaces for field types in entity forms, requiring specialized UI controls beyond core textfields/selects/checkboxes.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Simple input | Extend WidgetBase | Build form elements for field data entry |
| Multi-value handling | WidgetBase with formElement() | Handle cardinality > 1 automatically |
| AJAX interactions | Form API #ajax | Dynamic field behavior without page reload |
| Custom validation | Element validate callback | Field-specific validation beyond constraints |

## Pattern

Custom widget with PHP 8 attributes:

```php
namespace Drupal\my_module\Plugin\Field\FieldWidget;

use Drupal\Core\Field\Attribute\FieldWidget;
use Drupal\Core\Field\FieldItemListInterface;
use Drupal\Core\Field\WidgetBase;
use Drupal\Core\Form\FormStateInterface;

#[FieldWidget(
  id: "geolocation_default",
  label: new TranslatableMarkup("Geolocation"),
  field_types: ["geolocation"],
)]
class GeolocationWidget extends WidgetBase {

  public function formElement(
    FieldItemListInterface $items,
    $delta,
    array $element,
    array &$form,
    FormStateInterface $form_state
  ) {
    $element['lat'] = [
      '#type' => 'number',
      '#title' => $this->t('Latitude'),
      '#default_value' => $items[$delta]->lat ?? NULL,
      '#step' => 0.000001,
      '#min' => -90,
      '#max' => 90,
      '#required' => $element['#required'],
    ];

    $element['lng'] = [
      '#type' => 'number',
      '#title' => $this->t('Longitude'),
      '#default_value' => $items[$delta]->lng ?? NULL,
      '#step' => 0.000001,
      '#min' => -180,
      '#max' => 180,
      '#required' => $element['#required'],
    ];

    return $element;
  }
}
```

Place in `src/Plugin/Field/FieldWidget/GeolocationWidget.php`

Reference: `/core/modules/text/src/Plugin/Field/FieldWidget/TextfieldWidget.php`

## Common Mistakes

- **Wrong**: Not respecting $element['#required'] → **Right**: Field validation bypassed; data integrity issues
- **Wrong**: Forgetting #default_value → **Right**: Editing experience broken; values disappear on edit
- **Wrong**: Hardcoding labels → **Right**: Use $this->t() for translation support
- **Wrong**: Missing field_types → **Right**: Widget won't appear as option for your field type
- **Wrong**: Not handling $delta properly → **Right**: Multi-value fields break; use $items[$delta] for correct value
- **Wrong**: Skipping massageFormValues() → **Right**: Complex widgets need to transform form values to storage format

**Security**:
- NEVER trust form input. Rely on field type constraints for validation.
- Use Form API #element_validate for widget-specific validation only.
- Sanitize any JavaScript-exposed values with Html::escape().

**Performance**:
- Avoid loading entities in formElement() (called for every delta). Use AJAX or autocomplete.
- Cache expensive operations in widget settings, not per-element rendering.

**Development Standards**:
- Return render array from formElement(), not HTML strings
- Use dependency injection for services (inject via create() method)
- Implement settingsForm() and settingsSummary() for configurable widgets

## See Also

- [Custom Field Type Development](custom-field-type-development.md)
- [Field Formatter Development](field-formatter-development.md)
- Reference: [Create a custom field widget](https://www.drupal.org/docs/creating-custom-modules/creating-custom-field-types-widgets-and-formatters/create-a-custom-field-widget)
