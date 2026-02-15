---
description: Step-by-step creation of custom fields through the Drupal UI using config-first approach with column definitions and widget configuration.
---

# Creating a Custom Field (Config-First)

## When to Use

You want to create a compound field through the Drupal UI using configuration, not code -- the recommended approach for site builders and most use cases.

## Steps

1. **Navigate to field management**
   - Structure > Content types > [Type] > Manage fields
   - Click "Add field"

2. **Select field type**
   - Choose "Custom field" from the field type dropdown
   - Enter label and machine name
   - Save field settings

3. **Define columns (sub-fields)**
   - Click "Add sub-field" for each column
   - Configure each column:
     - **Name**: Machine name (letters, numbers, single underscores only)
     - **Type**: Select from 27 field types
     - **Type-specific settings**: Length (string/telephone), size/unsigned (numeric), precision/scale (decimal), datetime type, target type (entity reference), URI scheme (file/image)
   - Remove unwanted columns before saving
   - **After data exists**: Column types are locked; use update service to modify

4. **Optional: Clone from existing field**
   - Before adding data, use "Clone settings from" dropdown
   - Copies column definitions from another custom field
   - Does NOT copy widget/formatter settings

5. **Configure field settings (per sub-field)**
   - Expand each sub-field detail
   - Set widget type and widget-specific settings
   - Set required, default value, help text
   - Configure translatable (per sub-field)
   - Set `check_empty` behavior

6. **Save field storage and field instance**
   - Storage: Creates database table with all columns
   - Instance: Saves per-bundle configuration

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Step 3 (column type) | Storing short text (names, labels) | Use `string` with length <=255 |
| Step 3 (column type) | Storing long text (descriptions) | Use `string_long` (TEXT column) |
| Step 3 (column type) | Storing precise money values | Use `decimal` with precision=10, scale=2 |
| Step 3 (column type) | Referencing taxonomy terms or content | Use `entity_reference` with target_type |
| Step 4 (cloning) | Have similar field on another content type | Clone to save setup time |
| Step 5 (widget) | Need autocomplete for entity reference | Use EntityReferenceAutocompleteWidget |
| Step 5 (required) | Sub-field is optional within required parent field | Mark field required, sub-field optional with `check_empty = FALSE` |

## Common Mistakes

- **Changing column types after adding data** -- Column schema is locked once data exists. Plan ahead or use `CustomFieldUpdateManager` service with caution (data loss risk)
- **Machine name too long** -- Max length calculated as `64 - strlen($field_name) - 12`. For field `field_custom_address`, sub-field max is ~38 characters
- **Using double underscores in column names** -- `__` is reserved separator for extended properties. Use single underscores only
- **Not setting decimal precision/scale correctly** -- Precision is total digits, scale is decimal places. For money: precision=10, scale=2 allows up to $99,999,999.99
- **Forgetting to configure check_empty** -- Fields with `check_empty=TRUE` (default for most) will fail validation if empty and field is required. UUID and similar have `never_check_empty` in plugin definition

## See Also

- Reference: [Custom Field documentation](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field)
