---
description: Making metadata searchable, filterable in views, or editable by site builders through the field mapping UI.
---

# Field Mapping

### When to Use

Making metadata searchable, filterable in views, or editable by site builders through the field mapping UI.

### Decision

| Use Case | Map to Field? | Why |
|----------|---------------|-----|
| Search/filter by author | Yes → Text field | Views/Search API need database columns |
| Display duration in views | Yes → Number field | Sorting/filtering requires field storage |
| Show thumbnail in Media Library | No | Handled automatically via thumbnail_uri metadata |
| Editor override API title | Yes → Text field | Allows manual editing, API value as default |
| Programmatic access only | No | Use `getMetadata()` directly, no storage overhead |

### Pattern

Field mapping happens automatically during media save (conceptual):
```php
// Configuration in media type
field_map:
  title: field_media_title
  author: field_media_author
  duration: field_media_duration

// Auto-population (MediaSourceBase does this)
foreach ($field_map as $metadata_attr => $field_name) {
  if ($media->get($field_name)->isEmpty()) {
    $value = $source->getMetadata($media, $metadata_attr);
    $media->set($field_name, $value);
  }
}
```

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

### Common Mistakes

- Mapping everything → Unnecessary database storage, slow saves
- Not mapping searchable data → Can't filter in views, search doesn't index
- Mapping frequently changing data → Stale field values, cache issues
- Wrong field type for data → Text field for numbers prevents numeric sorting
- Making fields required → Prevents fallback to API defaults

**WHY:**
- **Selective mapping**: Every mapped field adds database columns and save overhead; only map what needs searching/filtering
- **Field type matching**: Views sorting/filtering uses field type; storing "120" as text sorts as "1", "120", "20" instead of "1", "20", "120"
- **Optional fields**: Required fields block saves when API unavailable; optional allows graceful degradation

### See Also

- Previous: [Metadata System](index.md)
- Next: [Thumbnail Generation](index.md)
- Reference: core/modules/media/src/MediaTypeForm.php (line 164-200)