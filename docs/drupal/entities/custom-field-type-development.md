---
description: Building custom field types with custom storage and validation
drupal_version: "11.x"
---

# Custom Field Type Development

## When to Use

When core field types don't meet your data structure needs, requiring custom storage schema, validation, or business logic for a specific data pattern.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Simple data structure | Extend FieldItemBase | Full control over schema and properties |
| Map-style data | Multiple properties in schema() | Store related values in single field item |
| Complex validation | Custom constraints | Enforce business rules at field level |
| Computed properties | ::propertyDefinitions() | Derived values from stored properties |

## Pattern

Custom field type with PHP 8 attributes:

```php
namespace Drupal\my_module\Plugin\Field\FieldType;

use Drupal\Core\Field\Attribute\FieldType;
use Drupal\Core\Field\FieldItemBase;
use Drupal\Core\Field\FieldStorageDefinitionInterface;
use Drupal\Core\TypedData\DataDefinition;

#[FieldType(
  id: "geolocation",
  label: new TranslatableMarkup("Geolocation"),
  description: new TranslatableMarkup("Stores latitude and longitude."),
  default_widget: "geolocation_default",
  default_formatter: "geolocation_default",
)]
class GeolocationItem extends FieldItemBase {

  public static function schema(FieldStorageDefinitionInterface $def) {
    return [
      'columns' => [
        'lat' => [
          'type' => 'numeric',
          'precision' => 10,
          'scale' => 6,
        ],
        'lng' => [
          'type' => 'numeric',
          'precision' => 10,
          'scale' => 6,
        ],
      ],
      'indexes' => [
        'lat_lng' => ['lat', 'lng'],
      ],
    ];
  }

  public static function propertyDefinitions(FieldStorageDefinitionInterface $def) {
    $properties['lat'] = DataDefinition::create('float')
      ->setLabel(t('Latitude'))
      ->setRequired(TRUE);

    $properties['lng'] = DataDefinition::create('float')
      ->setLabel(t('Longitude'))
      ->setRequired(TRUE);

    return $properties;
  }

  public function isEmpty() {
    $lat = $this->get('lat')->getValue();
    $lng = $this->get('lng')->getValue();
    return $lat === NULL || $lat === '' || $lng === NULL || $lng === '';
  }
}
```

Place in `src/Plugin/Field/FieldType/GeolocationItem.php`

Reference: `/core/modules/link/src/Plugin/Field/FieldType/LinkItem.php`

## Common Mistakes

- **Wrong**: Not implementing isEmpty() → **Right**: Field won't properly detect empty values; required validation fails
- **Wrong**: Missing indexes in schema() → **Right**: Poor query performance on multi-value fields
- **Wrong**: Hardcoding default_widget/formatter → **Right**: Use plugin IDs that exist or field UI breaks
- **Wrong**: Not validating in constraints → **Right**: Validation belongs in constraints, not widgets
- **Wrong**: Using wrong data types in schema → **Right**: Match SQL types: varchar, text, int, numeric, blob
- **Wrong**: Forgetting to call parent in propertyDefinitions() → **Right**: Lose inherited properties

**Security**:
- ALWAYS validate untrusted input in constraint validators, not widgets
- Use DataDefinition constraints for SQL injection prevention (setRequired, addConstraint)
- Sanitize output in formatters, never trust stored values in output

**Performance**:
- Add database indexes for columns used in entity queries
- Use appropriate SQL types: varchar vs text, int vs numeric
- Consider storage implications of complex schemas (more columns = wider rows)

**Development Standards**:
- Implement FieldItemInterface completely (schema, propertyDefinitions, isEmpty, etc.)
- Use dependency injection for services in validators/constraints
- Follow typed data API for property definitions

## See Also

- [Field Instance Configuration](field-instance-configuration.md)
- [Field Widget Development](field-widget-development.md)
- Reference: [Create a custom field type](https://www.drupal.org/docs/creating-custom-modules/creating-custom-field-types-widgets-and-formatters/create-a-custom-field-type)
