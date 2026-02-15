---
description: Creating custom field type, widget, and formatter plugins with PHP attribute-based discovery and required base class methods.
---

# Custom Plugin Development

## When to Use

You need to create custom field type, widget, or formatter plugins specific to your application.

## Pattern

**Custom field type plugin**:

```php
<?php

namespace Drupal\my_module\Plugin\CustomField\FieldType;

use Drupal\custom_field\Plugin\CustomFieldTypeBase;
use Drupal\custom_field\Plugin\CustomField\FieldType\Attribute\CustomFieldType;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[CustomFieldType(
  id: 'my_custom_type',
  label: new TranslatableMarkup('My Custom Type'),
  description: new TranslatableMarkup('Custom type description'),
  default_widget: 'my_custom_widget',
  default_formatter: 'my_custom_formatter',
  column_groups: ['text'],
)]
class MyCustomType extends CustomFieldTypeBase {

  public function schema(array $settings): array {
    return [
      $settings['name'] => [
        'type' => 'varchar',
        'length' => 255,
        'not null' => FALSE,
      ],
    ];
  }

  public function propertyDefinitions(array $settings): array {
    $properties[$settings['name']] = DataDefinition::create('string')
      ->setLabel($this->t('Custom value'));
    return $properties;
  }

  public function checkEmpty(): bool {
    return TRUE; // Affects field isEmpty() check
  }

  public function generateSampleValue($custom_item, string $entity_type): mixed {
    return $this->getRandomGenerator()->word(10);
  }

}
```

**Custom widget plugin**:

```php
#[CustomFieldWidget(
  id: 'my_custom_widget',
  label: new TranslatableMarkup('My Custom Widget'),
  description: new TranslatableMarkup('Widget description'),
  field_types: ['my_custom_type'],
)]
class MyCustomWidget extends CustomFieldWidgetBase {

  public function widget(FieldItemListInterface $items, int $delta, array $element, array &$form, FormStateInterface $form_state, CustomFieldTypeInterface $field): array {
    $element = parent::widget($items, $delta, $element, $form, $form_state, $field);

    $element['#type'] = 'textfield';
    $element['#default_value'] = $items[$delta]->{$field->getName()} ?? '';
    $element['#maxlength'] = 255;

    return $element;
  }

}
```

**Custom formatter plugin**:

```php
#[CustomFieldFormatter(
  id: 'my_custom_formatter',
  label: new TranslatableMarkup('My Custom Formatter'),
  description: new TranslatableMarkup('Formatter description'),
  field_types: ['my_custom_type'],
)]
class MyCustomFormatter extends CustomFieldFormatterBase {

  public function format(CustomFieldTypeInterface $field, mixed $value, array $settings): array {
    if (empty($value)) {
      return [];
    }

    return [
      '#markup' => $this->t('Value: @value', ['@value' => $value]),
    ];
  }

}
```

## Decision

| To extend... | Create... | Base class |
|---|---|---|
| New field type (column storage) | CustomFieldType plugin | CustomFieldTypeBase |
| New widget for existing/custom type | CustomFieldWidget plugin | CustomFieldWidgetBase |
| New formatter for existing/custom type | CustomFieldFormatter plugin | CustomFieldFormatterBase |

## Common Mistakes

- **Not implementing required methods** -- schema() and propertyDefinitions() required for field types
- **Wrong plugin namespace** -- Must be under `/Plugin/CustomField/{FieldType|FieldWidget|FieldFormatter}/`
- **Not declaring field_types in widget/formatter** -- Attribute must list compatible field types
- **Forgetting to clear cache** -- Plugin discovery is cached; `drush cr` after creating plugins
- **Not handling empty values** -- Always check for NULL/empty in formatter format() method

## See Also

- Reference: [Extending Custom Field formatter plugins](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field/extending-custom-field-formatter-plugins)
- Reference: `/modules/contrib/custom_field/src/Plugin/CustomFieldTypeBase.php`
