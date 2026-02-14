---
description: "Understanding URL patterns and resource type naming is fundamental for all API operations."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## URL Structure & Resource Types

### When to Use

Understanding URL patterns and resource type naming is fundamental for all API operations.

### URL Patterns

| Operation | URL Pattern | Example |
|-----------|-------------|---------|
| Collection GET | `/jsonapi/{entity_type}/{bundle}` | `/jsonapi/node/article` |
| Individual GET | `/jsonapi/{entity_type}/{bundle}/{uuid}` | `/jsonapi/node/article/a3b2c1d0-...` |
| POST (create) | `/jsonapi/{entity_type}/{bundle}` | `/jsonapi/node/article` |
| PATCH (update) | `/jsonapi/{entity_type}/{bundle}/{uuid}` | `/jsonapi/node/article/a3b2c1d0-...` |
| DELETE | `/jsonapi/{entity_type}/{bundle}/{uuid}` | `/jsonapi/node/article/a3b2c1d0-...` |
| Relationship GET | `/jsonapi/{entity_type}/{bundle}/{uuid}/{field}` | `/jsonapi/node/article/{uuid}/uid` |
| File upload | `/jsonapi/{entity_type}/{bundle}/{uuid}/{field}` | `/jsonapi/node/article/{uuid}/field_image` |

### Resource Type Format

**Pattern:** `{entity_type}--{bundle}`

| Entity Type | Bundle | Resource Type |
|-------------|--------|---------------|
| node | article | `node--article` |
| node | page | `node--page` |
| user | user | `user--user` |
| taxonomy_term | tags | `taxonomy_term--tags` |
| media | image | `media--image` |
| custom_entity | custom_bundle | `custom_entity--custom_bundle` |

### Translation URLs

**Pattern:** `/jsonapi/{langcode}/{entity_type}/{bundle}/{uuid}`

```
/jsonapi/es/node/article/{uuid}    # Spanish translation
/jsonapi/fr/node/article/{uuid}    # French translation
```

### Discovery Endpoint

```bash
# List all available resources
GET /jsonapi
```

Response includes links to all exposed resources:
```json
{
  "links": {
    "node--article": { "href": "/jsonapi/node/article" },
    "user--user": { "href": "/jsonapi/user/user" },
    "taxonomy_term--tags": { "href": "/jsonapi/taxonomy_term/tags" }
  }
}
```

### Common Mistakes

**Using node IDs instead of UUIDs:** JSON:API requires UUIDs, not integer IDs. WHY: UUIDs are globally unique and stable across environments. IDs vary between sites.

**Forgetting the double dash in resource types:** It's `node--article`, not `node-article`. WHY: The spec uses `--` as the separator between entity type and bundle.

**Not accounting for translation language in URLs:** Translations require language prefix. WHY: Each translation is a distinct resource version. Default language uses `/jsonapi/node/article/{uuid}`, others use `/jsonapi/{lang}/node/article/{uuid}`.

**Using entity type alone without bundle:** The URL must include both. WHY: Different bundles have different fields. `/jsonapi/node` is invalid; use `/jsonapi/node/article`.

### See Also
- [Fetching Resources (GET)](fetching-resources.md)
- [JSON:API Extras Customization](jsonapi-extras-customization.md) (custom URLs)
- [Revisions & Translations](revisions-translations.md)
