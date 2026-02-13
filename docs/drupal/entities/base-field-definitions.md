---
description: Base fields that exist on all bundles of an entity type
drupal_version: "11.x"
---

# Base Field Definitions

## When to Use

When adding fields that exist on ALL bundles of an entity type (e.g., title on all nodes, uid on all content), or creating non-configurable fields that store critical entity data.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Field on all bundles | Base field | Defined in code, always present, performant |
| Bundle-specific field | Configurable field | Field UI manageable, bundle-specific settings |
| Computed/virtual field | Computed base field | No storage needed, generated on demand |
| Entity metadata | Base field with display options | Core properties like created, changed, uid |

## Pattern

Define in entity's baseFieldDefinitions() method:

```php
public static function baseFieldDefinitions(EntityTypeInterface $type) {
  $fields = parent::baseFieldDefinitions($type);

  $fields['title'] = BaseFieldDefinition::create('string')
    ->setLabel(t('Title'))
    ->setRequired(TRUE)
    ->setSetting('max_length', 255)
    ->setDisplayConfigurable('form', TRUE)
    ->setDisplayConfigurable('view', TRUE);

  $fields['uid'] = BaseFieldDefinition::create('entity_reference')
    ->setLabel(t('Author'))
    ->setSetting('target_type', 'user')
    ->setDefaultValueCallback('getCurrentUserId')
    ->setDisplayOptions('form', [
      'type' => 'entity_reference_autocomplete',
      'weight' => 5,
    ]);

  return $fields;
}
```

Reference: `/core/modules/node/src/Entity/Node.php::baseFieldDefinitions()`

## Common Mistakes

- **Wrong**: Forgetting setDisplayConfigurable() → **Right**: Field won't appear in Field UI display management
- **Wrong**: Missing default value callbacks → **Right**: Use callbacks, not hardcoded values, for dynamic defaults
- **Wrong**: Not calling parent → **Right**: You'll lose ID, UUID, and other inherited base fields
- **Wrong**: Adding configurable fields as base fields → **Right**: Use Field UI for bundle-specific fields instead
- **Wrong**: Skipping validation constraints → **Right**: Add via addConstraint() for data integrity

**Security**: Always validate entity reference targets. Use ReferenceAccessConstraint or custom validation to prevent privilege escalation via field manipulation.

**Performance**: Base fields are loaded with every entity. Keep heavy fields (long text, files) as configurable fields that can be excluded from view modes.

## See Also

- [Bundle Entity Implementation](bundle-entity-implementation.md)
- [Field Type Selection](field-type-selection.md) for choosing field types
- Reference: [Defining base fields](https://www.drupal.org/docs/drupal-apis/entity-api/defining-and-using-content-entity-field-definitions)
