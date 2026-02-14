---
description: "Navigate JSON:API source code for debugging, customization, or understanding internals."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Code Reference Map

### When to Use

Navigate JSON:API source code for debugging, customization, or understanding internals.

### Core JSON:API Module

**Base Path:** `core/modules/jsonapi/`

#### Controllers

| File | Key Methods | Purpose |
|------|-------------|---------|
| `src/Controller/EntityResource.php` | `getCollection()`, `getIndividual()`, `createIndividual()`, `patchIndividual()`, `deleteIndividual()` | Main CRUD operations |
| `src/Controller/FileUpload.php` | `handleFileUploadForExistingResource()` | Binary file uploads |

#### Resource Type System

| File | Purpose |
|------|---------|
| `src/ResourceType/ResourceType.php` | Resource type value object, field mappings |
| `src/ResourceType/ResourceTypeRepository.php` | Discovers entities, generates ResourceTypes, caching |
| `src/ResourceType/ResourceTypeBuildEvent.php` | Extension point for altering resource types |
| `src/ResourceType/ResourceTypeField.php` | Field metadata |

#### Query System

| File | Purpose |
|------|---------|
| `src/Query/Filter.php` | Filter parsing, 14 operators, condition groups |
| `src/Query/Sort.php` | Sort parsing, multiple fields, asc/desc |
| `src/Query/OffsetPage.php` | Pagination with offset/limit, link generation |
| `src/Query/EntityCondition.php` | Individual filter conditions |
| `src/Query/EntityConditionGroup.php` | Filter groups (AND/OR logic) |

#### Normalizers

| File | Purpose |
|------|---------|
| `src/Normalizer/JsonApiDocumentTopLevelNormalizer.php` | Top-level document (data/links/meta/included) |
| `src/Normalizer/ResourceObjectNormalizer.php` | Resource objects, attributes/relationships |
| `src/Normalizer/FieldItemNormalizer.php` | Field-level value normalization |
| `src/Normalizer/EntityReferenceFieldNormalizer.php` | Relationship normalization |

#### Other Key Files

| File | Purpose |
|------|---------|
| `src/IncludeResolver.php` | Resolves included relationships |
| `src/Context/FieldResolver.php` | Public to internal field name resolution |
| `src/Routing/Routes.php` | Dynamic route generation |
| `src/Access/EntityAccessChecker.php` | Entity access integration |
| `src/EventSubscriber/ResourceResponseValidator.php` | Response validation against spec |

### JSON:API Extras Module

**Base Path:** `modules/contrib/jsonapi_extras/`

#### Configuration

| File | Purpose |
|------|---------|
| `src/Entity/JsonapiResourceConfig.php` | Resource override config entity |
| `src/ResourceType/ConfigurableResourceType.php` | Extended ResourceType with custom path/name |
| `src/ResourceType/ConfigurableResourceTypeRepository.php` | Overrides core repository, applies config |

#### Field Enhancers

**Base Path:** `src/Plugin/jsonapi/FieldEnhancer/`

| File | Purpose |
|------|---------|
| `DateTimeEnhancer.php` | Date/time formatting |
| `DateTimeFromStringEnhancer.php` | String to date conversion |
| `JSONFieldEnhancer.php` | JSON field parsing |
| `ListFieldEnhancer.php` | List field transformations |
| `SingleNestedEnhancer.php` | Nested value extraction |
| `UrlLinkEnhancer.php` | URL generation for links |
| `UuidLinkEnhancer.php` | UUID to resource link transformation |

#### Plugin Base

| File | Purpose |
|------|---------|
| `src/Plugin/ResourceFieldEnhancerBase.php` | Base class for enhancers, `doTransform()`, `doUndoTransform()` |
| `src/Plugin/ResourceFieldEnhancerManager.php` | Plugin manager for enhancers |

#### Normalizers

| File | Purpose |
|------|---------|
| `src/Normalizer/ResourceObjectNormalizer.php` | Decorates core normalizer, applies enhancers |

#### Event Subscribers

| File | Purpose |
|------|---------|
| `src/EventSubscriber/ConfigSubscriber.php` | Resource type building with config |

### Navigation Tips

**To understand CRUD operations:**
1. Start: `core/modules/jsonapi/src/Controller/EntityResource.php`
2. Trace normalization: `src/Normalizer/ResourceObjectNormalizer.php`
3. Check access: `src/Access/EntityAccessChecker.php`

**To understand filtering:**
1. Query parsing: `src/Query/Filter.php`
2. Condition building: `src/Query/EntityCondition.php`
3. Field resolution: `src/Context/FieldResolver.php`

**To create custom enhancer:**
1. Study existing: `jsonapi_extras/src/Plugin/jsonapi/FieldEnhancer/`
2. Extend: `ResourceFieldEnhancerBase`
3. Implement: `doTransform()` and `doUndoTransform()`

**To customize resource types:**
1. Listen to: `ResourceTypeBuildEvent` (see `src/ResourceType/ResourceTypeBuildEvent.php`)
2. JSON:API Extras example: `jsonapi_extras/src/EventSubscriber/ConfigSubscriber.php`

### See Also
- [Core Architecture](core-architecture.md)
- [JSON:API Extras Customization](jsonapi-extras-customization.md)
- [Field Enhancers](field-enhancers.md)
