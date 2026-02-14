---
description: "Customize resource names, URLs, field visibility, and field transformations. Requires jsonapi_extras contrib module."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## JSON:API Extras Customization

### When to Use

Customize resource names, URLs, field visibility, and field transformations. Requires `jsonapi_extras` contrib module.

### Features

| Feature | Use Case |
|---------|----------|
| Rename resources | Change `node--article` to `article` |
| Customize URLs | Change `/jsonapi/node/article` to `/jsonapi/articles` |
| Disable resources | Hide internal entity types from API |
| Remove fields | Exclude sensitive or unnecessary fields |
| Field enhancers | Transform field values (dates, URLs, nested data) |
| Change base path | Move `/jsonapi` to `/api/v1` |

### Pattern

**Installation:**
```bash
composer require drupal/jsonapi_extras
drush en jsonapi_extras
```

**Access configuration:**
- Visit `/admin/config/services/jsonapi`
- Click "Resource overrides" tab
- Configure individual resource types

**Disable resource:**
```yaml
# config/install/jsonapi_extras.jsonapi_resource_config.taxonomy_term--tags.yml
id: taxonomy_term--tags
disabled: true
path: taxonomy_term/tags
resourceType: taxonomy_term--tags
resourceFields: []
```

**Rename resource and customize URL:**
```yaml
# config/install/jsonapi_extras.jsonapi_resource_config.node--article.yml
id: node--article
disabled: false
path: articles
resourceType: article
resourceFields:
  title:
    fieldName: title
    publicName: headline
    enhancer:
      id: ''
  body:
    fieldName: body
    publicName: content
    enhancer:
      id: ''
  field_image:
    disabled: true
```

**Result:**
```
Before: /jsonapi/node/article
After:  /jsonapi/articles

Field mapping:
  title -> headline
  body -> content
  field_image -> (removed)
```

**Change base path via services.yml:**
```yaml
# config/default/services.yml
parameters:
  jsonapi.base_path: /api/v1
```

**Result:** `/api/v1/node/article`

### Common Mistakes

**Renaming resources after clients are deployed:** Breaking change. WHY: Client code references old resource names. Version API or maintain backward compatibility.

**Not exporting configuration:** Changes made in UI aren't in version control. WHY: Configuration sync will revert changes. Export with `drush config:export`.

**Disabling fields that are required:** Validation still applies. WHY: POST/PATCH with missing required fields fails even if field is disabled in API. Only disable truly optional fields.

**Forgetting to clear cache after changes:** Resource type changes are cached. WHY: Drupal caches resource type repository. Run `drush cache:rebuild`.

**Over-complicating with too many renames:** Maintaining mapping between internal and public names becomes complex. WHY: Debugging and maintenance difficulty. Only rename when necessary.

### See Also
- [Core Architecture](core-architecture.md)
- [Security Best Practices](security-best-practices.md)
- [Field Enhancers](field-enhancers.md)
- JSON:API Extras project page: https://www.drupal.org/project/jsonapi_extras
