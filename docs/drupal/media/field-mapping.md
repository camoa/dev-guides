---
description: Mapping metadata to entity fields for search, filtering, and editing
drupal_version: "11.x"
---

# Field Mapping

## When to Use

> Use field mapping when making metadata searchable, filterable in views, or editable by site builders through the field mapping UI.

## Decision

| Use Case | Map to Field? | Why |
|----------|---------------|-----|
| Search/filter by author | Yes → Text field | Views/Search API need database columns |
| Display duration in views | Yes → Number field | Sorting/filtering requires field storage |
| Show thumbnail in Media Library | No | Handled automatically via thumbnail_uri metadata |
| Editor override API title | Yes → Text field | Allows manual editing, API value as default |
| Programmatic access only | No | Use `getMetadata()` directly, no storage overhead |

## Pattern

Create mapped fields programmatically (7 lines):
```php
use Drupal\field\Entity\{FieldStorageConfig, FieldConfig};

FieldStorageConfig::create([
  'entity_type' => 'media',
  'field_name' => 'field_media_author',
  'type' => 'string',
])->save();

FieldConfig::create([
  'entity_type' => 'media',
  'bundle' => 'custom_media',
  'field_name' => 'field_media_author',
  'label' => 'Author',
])->save();
```

Field mapping auto-population (conceptual):
```php
// Configuration in media type
field_map:
  title: field_media_title
  author: field_media_author
  duration: field_media_duration

// MediaSourceBase does this automatically
foreach ($field_map as $metadata_attr => $field_name) {
  if ($media->get($field_name)->isEmpty()) {
    $value = $source->getMetadata($media, $metadata_attr);
    $media->set($field_name, $value);
  }
}
```

## Common Mistakes

- **Wrong**: Mapping everything → **Right**: Only map searchable/filterable data
- **Wrong**: Not mapping searchable data → **Right**: Map data needed in views/search
- **Wrong**: Mapping frequently changing data → **Right**: Keep volatile data in metadata only
- **Wrong**: Wrong field type for data → **Right**: Number fields for numeric data
- **Wrong**: Making fields required → **Right**: Optional fields allow API fallback

## See Also

- Previous: [Metadata System](metadata-system.md)
- Next: [Thumbnail Generation](thumbnail-generation.md)
- Reference: core/modules/media/src/MediaTypeForm.php (line 164-200)
