---
description: Adding, removing, and modifying columns in existing custom fields with data using CustomFieldUpdateManager service.
---

# Schema Updates & Data Migration

## When to Use

You need to add, remove, or modify columns in a Custom Field that already has data, without losing existing content.

## Pattern

**Using CustomFieldUpdateManager service**:

```php
/** @var \Drupal\custom_field\CustomFieldUpdateManager $updateManager */
$updateManager = \Drupal::service('custom_field.update_manager');

// Add new column to existing field
$field_storage = FieldStorageConfig::loadByName('node', 'field_address');
$columns = $field_storage->getSetting('columns');
$columns['country'] = [
  'name' => 'country',
  'type' => 'string',
  'length' => 2, // ISO country code
];
$field_storage->setSetting('columns', $columns);
$updateManager->updateFieldSchema($field_storage);

// Remove column (data will be lost)
unset($columns['old_field']);
$field_storage->setSetting('columns', $columns);
$updateManager->updateFieldSchema($field_storage);
```

**The update process**:

1. Creates temporary table with new schema
2. Copies existing data
3. Drops old table
4. Renames temporary table
5. Updates field storage config
6. Clears property definitions cache

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Add optional column to existing field | updateFieldSchema() in update hook | Safe -- new column accepts NULL, no data loss |
| Remove unused column | updateFieldSchema() + backup data first | Column data permanently deleted |
| Change column type (string > text) | Export data, delete field, recreate, import | Safest for type changes; update service may fail on incompatible types |
| Change column length (string 50 > 100) | updateFieldSchema() | Safe if new length > max existing value length |
| Reduce column length (string 255 > 50) | Check data first, may truncate | Data loss if existing values exceed new limit |
| Rename column | Add new column, migrate data, remove old | No direct rename support |

## Common Mistakes

- **Not backing up before schema updates** -- Database exports mandatory before column removal or type changes
- **Changing column type without checking compatibility** -- String > Integer fails if non-numeric data exists. Export/reimport safer
- **Forgetting to update field config** -- After schema update, update FieldConfig with new widget/formatter settings for new columns
- **Running updates on production without testing** -- Test schema updates on copy of production database first
- **Not clearing caches after updates** -- Field property definitions are cached; `drush cr` required

## See Also

- Reference: [Add/remove columns to Custom fields with existing data](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field/addremove-columns-to-custom-fields-with-existing-data)
- Reference: `/modules/contrib/custom_field/src/CustomFieldUpdateManager.php`
