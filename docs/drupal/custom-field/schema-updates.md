---
description: "Adding, removing, and modifying columns in existing custom fields with data using the custom_field.update_manager service."
tldr: "Use addColumn()/removeColumn() on custom_field.update_manager inside a hook_update_N() to change existing custom-field columns without data loss -- there is no updateFieldSchema(), and 5.x adds a one-time taxonomy-index backfill post-update."
drupal_version: "11.x"
---

# Schema Updates & Data Migration

## When to Use

You need to add, remove, or modify columns in a Custom Field that already has data, without losing existing content.

## Pattern

**Using the `custom_field.update_manager` service** (`\Drupal\custom_field\Service\UpdateManager`, interface `\Drupal\custom_field\Service\UpdateManagerInterface`):

```php
/** @var \Drupal\custom_field\Service\UpdateManagerInterface $updateManager */
$updateManager = \Drupal::service('custom_field.update_manager');

// Add a new column to a `custom` field that already holds content.
// Safe on live data: the service backs up rows, truncates, adds the column
// across both the data and revision tables, then restores rows in batches.
$updateManager->addColumn('node', 'field_card', 'link_url', 'string');

// Remove a column (its data is dropped).
$updateManager->removeColumn('node', 'field_card', 'link_url');
```

**Available methods** (there is NO `updateFieldSchema()`):

- `addColumn(string $entity_type_id, string $field_name, string $new_property, string $data_type, array $options = [])`
- `addExtraColumns(string $entity_type_id, string $field_name, array $extra_columns)`
- `removeColumn(string $entity_type_id, string $field_name, string $property)`

**Drush + deploy path** -- the module ships interactive drush commands that print a ready-to-paste update hook:

```
drush custom_field:add-column      # alias: cf-add-column
drush custom_field:remove-column   # alias: cf-remove-column
```

Deploy the schema change with a `hook_update_N()` so it runs on every environment:

```php
/**
 * Add column 'link_url' to 'field_card' on 'node'.
 */
function MY_MODULE_update_N() {
  \Drupal::service('custom_field.update_manager')->addColumn(
    'node',
    'field_card',
    'link_url',
    'string',
  );
}
```

**The update process** (handled by the service): backs up existing rows, truncates the table, adds or removes the column across both the data and revision tables, restores rows in batches, and clears the property definitions cache.

**Upgrading 4.x to 5.x:** the update manager, its three methods, and both drush commands are unchanged. The one thing 5.x adds is a post-update, `custom_field_post_update_bulk_populate_taxonomy_index()`, which `drush updb` runs once. It is a batched backfill of `taxonomy_index` across **every published node** that has an `entity_reference` sub-column targeting `taxonomy_term`. On a large content set this is slow -- budget for it in the deploy window rather than discovering it mid-update. `custom_field.post_update.php` contains no other function, and no 4.x to 5.x data migration beyond this one is documented upstream.

**Scope note:** this managed migration path is specific to the **custom_field module's** `custom` type. A field type you hand-build yourself (your own `FieldItemBase` with its own `schema()`) has **no** such service -- you own the schema change in your module's `hook_update_N()` directly.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Add optional column to existing field | `addColumn()` in update hook | Safe -- new column accepts NULL, no data loss |
| Remove unused column | `removeColumn()` + backup data first | Column data permanently deleted |
| Change column type (string > text) | Export data, delete field, recreate, import | Safest for type changes; there is no in-place type-change method |
| Change column length (string 50 > 100) | `addColumn()` new + migrate + `removeColumn()` old | No in-place length change; add the new shape, migrate, drop the old |
| Reduce column length (string 255 > 50) | Check data first, may truncate | Data loss if existing values exceed new limit |
| Rename column | `addColumn()` new, migrate data, `removeColumn()` old | No direct rename support |

## Common Mistakes

- **Not backing up before schema updates** -- Database exports mandatory before column removal or type changes
- **Changing column type without checking compatibility** -- String > Integer fails if non-numeric data exists. Export/reimport safer
- **Forgetting to update field config** -- After schema update, update FieldConfig with new widget/formatter settings for new columns
- **Running updates on production without testing** -- Test schema updates on copy of production database first
- **Not clearing caches after updates** -- Field property definitions are cached; `drush cr` required
- **Suggesting `drush entity:updates` (`entup`)** -- It does NOT exist in Drupal 10/11 and never managed field-storage column schema. Deploy column changes with the `custom_field.update_manager` service via a `hook_update_N()` (or the `cf-add-column` / `cf-remove-column` drush commands)

## See Also

- Reference: [Add/remove columns to Custom fields with existing data](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field/addremove-columns-to-custom-fields-with-existing-data)
- Reference: `/modules/contrib/custom_field/src/Service/UpdateManager.php`
- [Config-First Creation](config-first-creation.md)
