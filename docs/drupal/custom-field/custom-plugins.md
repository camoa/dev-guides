---
description: "Creating custom field type, widget, and sub-field formatter plugins for Custom Field 5.x -- correct attribute namespaces, static method signatures, and the 5.x PropWidget extension point."
tldr: "schema()/propertyDefinitions()/generateSampleValue() are static on CustomFieldTypeBase; there is no #[CustomFieldFormatter] attribute -- sub-field formatters use core's #[FieldFormatter] and implement formatValue(), not format()."
drupal_version: "11.x"
---

# Custom Plugin Development

## When to Use

You need to create custom field type, widget, or formatter plugins specific to your application.

## Pattern

**Custom field type plugin**:

```php
<?php

namespace Drupal\my_module\Plugin\CustomField\FieldType;

use Drupal\Component\Utility\Random;
use Drupal\custom_field\Attribute\CustomFieldType;
use Drupal\custom_field\Plugin\CustomFieldTypeBase;
use Drupal\custom_field\Plugin\CustomFieldTypeInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[CustomFieldType(
  id: 'my_custom_type',
  label: new TranslatableMarkup('My Custom Type'),
  description: new TranslatableMarkup('Custom type description'),
  category: new TranslatableMarkup('Text'),
  default_widget: 'my_custom_widget',
  default_formatter: 'my_custom_formatter',
)]
class MyCustomType extends CustomFieldTypeBase {

  public static function schema(array $settings): array {
    return [
      $settings['name'] => [
        'type' => 'varchar',
        'length' => 255,
        'not null' => FALSE,
      ],
    ];
  }

  public static function propertyDefinitions(array $settings): mixed {
    $properties[$settings['name']] = DataDefinition::create('string')
      ->setLabel(new TranslatableMarkup('Custom value'));
    return $properties;
  }

  public function checkEmpty(): bool {
    return TRUE; // Affects field isEmpty() check
  }

  public static function generateSampleValue(CustomFieldTypeInterface $field, string $target_entity_type): mixed {
    return (new Random())->word(10);
  }

}
```

`schema()`, `propertyDefinitions()` and `generateSampleValue()` are **static** -- declaring them as instance methods breaks discovery. `checkEmpty()` is the odd one out and is a normal instance method. The attribute lives in `Drupal\custom_field\Attribute\`, *not* under `Plugin\CustomField\FieldType\Attribute\`. `column_groups` is a real attribute parameter but the shipped field types do not use it -- UI grouping comes from `category`.

**Custom widget plugin** (attribute: `Drupal\custom_field\Attribute\CustomFieldWidget`):

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

**Custom sub-field formatter plugin** -- there is **no** `#[CustomFieldFormatter]` attribute. Sub-field formatters are annotated with **core's** `Drupal\Core\Field\Attribute\FieldFormatter`; `CustomFieldFormatterManager` passes that class as its attribute class and scans `/Plugin/CustomField/FieldFormatter/`. All 33 shipped formatters do this.

```php
use Drupal\Core\Field\Attribute\FieldFormatter;
use Drupal\Core\Field\FieldItemInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\custom_field\Plugin\CustomFieldFormatterBase;

#[FieldFormatter(
  id: 'my_custom_formatter',
  label: new TranslatableMarkup('My Custom Formatter'),
  field_types: ['my_custom_type'],
)]
class MyCustomFormatter extends CustomFieldFormatterBase {

  public function formatValue(FieldItemInterface $item, mixed $value): mixed {
    if (empty($value)) {
      return NULL;
    }

    return $this->t('Value: @value', ['@value' => $value]);
  }

}
```

The method is `formatValue(FieldItemInterface $item, mixed $value): mixed` -- it takes the parent field item and the raw sub-field value, and returns a value (string, markup, or render array), not necessarily a render array.

## Decision

| To extend... | Create... | Attribute | Base class |
|---|---|---|---|
| New field type (column storage) | CustomFieldType plugin | `Drupal\custom_field\Attribute\CustomFieldType` | CustomFieldTypeBase |
| New widget for existing/custom type | CustomFieldWidget plugin | `Drupal\custom_field\Attribute\CustomFieldWidget` | CustomFieldWidgetBase |
| New formatter for existing/custom type | Sub-field formatter plugin | core's `Drupal\Core\Field\Attribute\FieldFormatter` | CustomFieldFormatterBase |
| Map a sub-field onto an SDC component prop | PropWidget plugin (5.x, in `src/Plugin/Components/PropWidget/`) | `Drupal\custom_field\Attribute\PropWidget` | `Drupal\custom_field\Plugin\PropWidgetBase` / `PropWidgetInterface` -- in `src/Plugin/`, one level above the plugin directory |

The prop-widget type is the fourth extension point, added in 5.x and discovered by `plugin.manager.custom_field_component_prop_widget`. It is what the `custom_field_sdc` formatter uses to decide how each sub-field feeds a component prop.

**Form element:** 5.x also ships `#[FormElement('custom_field_multivalue')]` (`src/Element/MultiValue.php`) -- the multi-value wrapper element, reusable from your own forms.

## Common Mistakes

- **Reaching for a `#[CustomFieldFormatter]` attribute** -- It does not exist in any version. Sub-field formatters use core's `#[FieldFormatter]`; only the directory and base class are custom_field's
- **Writing a `format()` method on a formatter** -- The base class method is `formatValue(FieldItemInterface $item, mixed $value)`. A `format()` method is simply never called
- **Declaring schema()/propertyDefinitions()/generateSampleValue() as instance methods** -- All three are static on `CustomFieldTypeBase`; only `checkEmpty()` is an instance method
- **Importing the attribute from the plugin namespace** -- Attributes live in `Drupal\custom_field\Attribute\`, not `Drupal\custom_field\Plugin\CustomField\FieldType\Attribute\`
- **Wrong plugin namespace** -- Must be under `/Plugin/CustomField/{FieldType|FieldWidget|FieldFormatter}/`
- **Not declaring field_types in widget/formatter** -- The attribute must list compatible field types
- **Forgetting to clear cache** -- Plugin discovery is cached; `drush cr` after creating plugins
- **Not handling empty values** -- Always check for NULL/empty in `formatValue()`

## See Also

- Reference: [Extending Custom Field formatter plugins](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field/extending-custom-field-formatter-plugins)
- Reference: `/modules/contrib/custom_field/src/Plugin/CustomFieldTypeBase.php`
