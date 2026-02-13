---
description: Computed fields — virtual fields with dynamic values from stored data
drupal_version: "11.x"
---

# Computed Field Patterns

## When to Use

When creating virtual/derived fields that calculate values from other fields without storing data, requiring dynamic values that update when dependencies change.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Derived value | Computed field property | No storage, generated on access |
| Cached computed value | Stored field with update hook | Performance, avoid recalculation |
| Display-only field | View-only formatter | No form widget needed |
| Complex calculation | Custom field type with computed properties | Full control over logic |

## Pattern

Computed property in custom field type:

```php
namespace Drupal\my_module\Plugin\Field\FieldType;

use Drupal\Core\Field\FieldItemBase;
use Drupal\Core\TypedData\DataDefinition;

class FullNameItem extends FieldItemBase {

  public static function propertyDefinitions(FieldStorageDefinitionInterface $def) {
    $properties['first_name'] = DataDefinition::create('string')
      ->setLabel(t('First name'))
      ->setRequired(TRUE);

    $properties['last_name'] = DataDefinition::create('string')
      ->setLabel(t('Last name'))
      ->setRequired(TRUE);

    // Computed property - no storage
    $properties['full_name'] = DataDefinition::create('string')
      ->setLabel(t('Full name'))
      ->setComputed(TRUE)
      ->setClass(FullNameComputed::class);

    return $properties;
  }

  public static function schema(FieldStorageDefinitionInterface $def) {
    return [
      'columns' => [
        'first_name' => ['type' => 'varchar', 'length' => 255],
        'last_name' => ['type' => 'varchar', 'length' => 255],
        // Note: full_name has NO column (computed)
      ],
    ];
  }
}
```

Computed class:

```php
namespace Drupal\my_module\TypedData;

use Drupal\Core\TypedData\ComputedItemListTrait;
use Drupal\Core\TypedData\DataDefinitionInterface;
use Drupal\Core\TypedData\TypedData;

class FullNameComputed extends TypedData {
  use ComputedItemListTrait;

  protected function computeValue() {
    $item = $this->getParent();
    $first = $item->first_name;
    $last = $item->last_name;
    $this->value = trim("$first $last");
  }
}
```

Reference: `/core/modules/file/src/ComputedFileUrl.php`

## Common Mistakes

- **Wrong**: Including computed properties in schema() → **Right**: Database error; computed properties have no storage
- **Wrong**: Not setting ->setComputed(TRUE) → **Right**: Drupal tries to load from database
- **Wrong**: Expensive computations without caching → **Right**: Performance issue; cache or denormalize
- **Wrong**: Forgetting ComputedItemListTrait → **Right**: Compute logic never triggers
- **Wrong**: Not implementing isEmpty() → **Right**: Empty check includes computed values incorrectly

**Performance**:
- Computed properties calculated on EVERY access. Cache expensive operations.
- For heavy computations, consider stored field + update hook instead.
- Use computeValue() lazily. Don't precompute in constructor.

**Development Standards**:
- Computed properties for simple derivations only (concatenation, formatting)
- Denormalize complex aggregations to stored fields
- Document dependencies clearly (which properties does computation use?)

## See Also

- [File and Image Field Patterns](file-and-image-field-patterns.md)
- [Entity Query Patterns](entity-query-patterns.md)
- Reference: [Computed field values](https://www.drupal.org/docs/drupal-apis/entity-api/dynamicvirtual-field-values-using-computed-field-property-classes)
