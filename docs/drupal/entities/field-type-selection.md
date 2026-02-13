---
description: Choosing the right field type for your data structure
drupal_version: "11.x"
---

# Field Type Selection

## When to Use

When adding fields to content types or entities, you must choose the appropriate field type that matches your data structure and validation requirements.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Short text (< 255 chars) | string | Single database column, fast, filterable |
| Long text with formatting | text_with_summary | Filtered HTML, optional summary, multiple formats |
| Reference to entities | entity_reference | Enforced referential integrity, target type validation |
| Images with derivatives | image | Automatic image styles, alt/title attributes, file validation |
| Files/documents | file | File upload, MIME validation, usage tracking |
| True/false values | boolean | Single bit storage, checkbox widget |
| Dates/times | datetime | Timezone support, date/time formats, range queries |
| Numbers | integer, decimal, float | Proper sorting, range validation, numeric operations |
| Email addresses | email | RFC validation, link formatter |
| URLs | link | URI validation, external link detection, title field |
| Multi-value lists | list_string, list_integer | Predefined options, select/checkbox widgets |

## Pattern

Field type determines storage schema and available widgets/formatters:

```php
// String field: 1 column, varchar(255)
BaseFieldDefinition::create('string')
  ->setSetting('max_length', 255);

// Entity reference: integer column with foreign key
BaseFieldDefinition::create('entity_reference')
  ->setSetting('target_type', 'taxonomy_term')
  ->setSetting('handler', 'default')
  ->setSetting('handler_settings', [
    'target_bundles' => ['tags' => 'tags'],
  ]);

// Image field: multiple columns (target_id, alt, title, width, height)
BaseFieldDefinition::create('image')
  ->setSetting('file_directory', 'images/[date:custom:Y]-[date:custom:m]')
  ->setSetting('file_extensions', 'png jpg jpeg')
  ->setSetting('max_filesize', '5 MB')
  ->setSetting('max_resolution', '3000x3000')
  ->setSetting('alt_field', TRUE)
  ->setSetting('alt_field_required', TRUE);
```

Reference: `/core/lib/Drupal/Core/Field/Plugin/Field/FieldType/`

## Common Mistakes

- **Wrong**: Using string for long text → **Right**: Limited to 255 chars; use text_long or text_with_summary
- **Wrong**: Using text for short text → **Right**: Wastes space with TEXT column; use string for < 255 chars
- **Wrong**: Not validating file extensions → **Right**: Security risk; always whitelist allowed extensions
- **Wrong**: Missing alt_field_required on images → **Right**: Accessibility failure; require alt text
- **Wrong**: Using string for numbers → **Right**: No numeric sorting/filtering; use integer/decimal/float
- **Wrong**: Not setting target_bundles on entity_reference → **Right**: Performance hit; filter by bundle when possible

**Security**:
- File fields: ALWAYS set file_extensions. Never allow .php, .exe, .js uploads. Use whitelist, not blacklist.
- Entity references: ALWAYS validate access. Use handler_settings to restrict target bundles.
- Text fields: Use text formats. Never trust user input; filter through text format system.

**Performance**:
- String fields are faster than text fields for short content (single VARCHAR vs TEXT column)
- Entity references with target_bundles set avoid loading all possible targets
- Image fields with file_directory tokens ([date:custom:Y]-[date:custom:m]) distribute files across directories

## See Also

- [Base Field Definitions](base-field-definitions.md)
- [Field Storage Configuration](field-storage-configuration.md)
- Reference: [Field types overview](https://www.drupal.org/docs/drupal-apis/entity-api/fieldtypes-fieldwidgets-and-fieldformatters)
