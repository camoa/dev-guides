---
description: Custom Salesforce field mapping plugin — extend PropertiesBase, implement value() and pullValue(), @SalesforceMappingField annotation
drupal_version: "11.x"
---

# Custom Field Mapping Plugin

## When to Use

> Create a custom field mapping plugin when built-in plugins (`Properties`, `Token`, `Constant`, etc.) cannot express the mapping logic needed — calculated values, custom field types, or complex transformations reusable across multiple mappings.

## Decision

| Approach | Use When |
|---|---|
| Extend `PropertiesBase` | Standard field mapping with custom push/pull logic |
| Implement `SalesforceMappingFieldPluginInterface` directly | Fully custom mapping logic not fitting standard patterns |
| Use built-in `Token` plugin | Value expressible via Drupal token |
| Use built-in `Constant` plugin | Static hardcoded value |

## Pattern

```php
namespace Drupal\my_module\Plugin\SalesforceMappingField;

use Drupal\salesforce_mapping\Plugin\SalesforceMappingField\PropertiesBase;

/**
 * @SalesforceMappingField(
 *   id = "my_custom_field",
 *   label = @Translation("My Custom Field"),
 * )
 */
class MyCustomField extends PropertiesBase {

  // Value sent to Salesforce during push
  public function value(EntityInterface $entity, SalesforceMappingInterface $mapping) {
    return $entity->get('field_my_data')->value;
  }

  // Value applied to Drupal entity during pull
  public function pullValue(SObject $sf_object, EntityInterface $entity, SalesforceMappingInterface $mapping) {
    $entity->set('field_my_data', $sf_object->field('My_Field__c'));
  }

}
```

**Required methods:**
- `value()` — returns value for push to Salesforce
- `pullValue()` — applies Salesforce value to Drupal entity during pull

## Common Mistakes

- **Wrong**: Only implementing `value()` and expecting pull to work → **Right**: Both `value()` and `pullValue()` must be implemented for bidirectional mappings
- **Wrong**: Instantiating the plugin directly with `new MyCustomField()` → **Right**: Plugins are managed by the plugin manager; use dependency injection via `ContainerFactoryPluginInterface`

## See Also

- [Mapping Framework](mapping-framework.md)
- [Decision Framework](decision-framework.md)
- Reference base class: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/Plugin/SalesforceMappingField/PropertiesBase.php`
- Reference example: `/web/modules/contrib/salesforce/modules/salesforce_example/src/Plugin/SalesforceMappingField/Hardcoded.php`
- Reference interface: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/SalesforceMappingFieldPluginInterface.php`
