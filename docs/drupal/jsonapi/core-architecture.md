---
description: "Understanding the architecture is essential when customizing JSON:API behavior, debugging issues, or extending functionality."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Core Architecture

### When to Use

Understanding the architecture is essential when customizing JSON:API behavior, debugging issues, or extending functionality.

### Decision

| Task | Component | Location |
|------|-----------|----------|
| Understand entity to JSON transformation | ResourceObjectNormalizer | `core/modules/jsonapi/src/Normalizer/` |
| Discover available resources | ResourceTypeRepository | `core/modules/jsonapi/src/ResourceType/` |
| Handle CRUD operations | EntityResource controller | `core/modules/jsonapi/src/Controller/` |
| Parse filter/sort queries | Query system | `core/modules/jsonapi/src/Query/` |
| Customize resource types | ResourceTypeBuildEvent | `core/modules/jsonapi/src/ResourceType/` |
| Apply field transformations | Field enhancers (Extras) | `modules/contrib/jsonapi_extras/src/Plugin/` |

### Pattern

**Resource type discovery flow:**
```php
// 1. Repository discovers all entity types/bundles
$repository = \Drupal::service('jsonapi.resource_type.repository');

// 2. Get specific resource type
$resource_type = $repository->get('node', 'article');

// 3. Access resource type information
$type_name = $resource_type->getTypeName(); // "node--article"
$fields = $resource_type->getFields();
$public_name = $resource_type->getPublicName('field_image'); // "field_image"
```

**Normalization flow:**
```php
// 1. Entity loads
$entity = Node::load(1);

// 2. ResourceObjectNormalizer transforms to JSON:API
$normalizer = \Drupal::service('serializer.normalizer.resource_object');
$normalized = $normalizer->normalize($entity, 'api_json');

// 3. Result: { type, id, attributes, relationships }
```

### Key Components

**ResourceType System:**
- `ResourceType`: Represents entity type + bundle configuration
- `ResourceTypeRepository`: Discovers entities, generates ResourceType objects, caches
- `ResourceTypeBuildEvent`: Allows modules to alter resource types (used by JSON:API Extras)

**Normalization System:**
- `JsonApiDocumentTopLevelNormalizer`: Top-level document with data/links/meta/included
- `ResourceObjectNormalizer`: Individual resource objects, attributes/relationships separation
- `FieldItemNormalizer`: Field-level value normalization

**Controller System:**
- `EntityResource`: Handles GET, POST, PATCH, DELETE via `getIndividual()`, `getCollection()`, `createIndividual()`, `patchIndividual()`, `deleteIndividual()`
- `FileUpload`: Binary file uploads to entity fields

**Query System:**
- `Filter`: Parses filter parameters, supports 14 operators
- `Sort`: Parses sort parameters, multiple fields, asc/desc
- `OffsetPage`: Pagination with offset/limit, link generation

### Common Mistakes

**Modifying core normalizers directly:** Never edit core files. WHY: Updates overwrite changes. Instead, create decorating normalizers with higher priority in `services.yml`.

**Not clearing cache after resource type changes:** Resource types are cached. WHY: Performance optimization. Run `drush cache:rebuild` after altering resource types.

**Assuming field names match API names:** JSON:API Extras can rename fields. WHY: `field_publication_date` might be exposed as `published_at`. Always use `ResourceType::getPublicName()` and `getInternalName()`.

### See Also
- [JSON:API Extras Customization](jsonapi-extras-customization.md)
- [Code Reference Map](code-reference-map.md)
- [Field Enhancers](field-enhancers.md)
