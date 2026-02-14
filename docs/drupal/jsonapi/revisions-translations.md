---
description: "Access specific entity revisions or translations via JSON:API."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Revisions & Translations

### When to Use

Access specific entity revisions or translations via JSON:API.

### Revisions

**Get specific revision by ID:**
```bash
GET /jsonapi/node/article/{uuid}?resourceVersion=id:12345
```

**Get latest revision:**
```bash
GET /jsonapi/node/article/{uuid}?resourceVersion=rel:latest-version
```

**Get working copy (draft):**
```bash
GET /jsonapi/node/article/{uuid}?resourceVersion=rel:working-copy
```

**Revision parameters:**

| Parameter | Description | Use Case |
|-----------|-------------|----------|
| `resourceVersion=id:{revision_id}` | Specific revision by ID | View historical version |
| `resourceVersion=rel:latest-version` | Latest revision | Content moderation |
| `resourceVersion=rel:working-copy` | Working copy/draft | Preview unpublished changes |

**Gotchas:**
- Requires entity type to be revisionable
- User must have "view revisions" permission
- Not all entity types support revisions

### Translations

**Get specific translation:**
```bash
# Spanish translation
GET /jsonapi/es/node/article/{uuid}

# French translation
GET /jsonapi/fr/node/article/{uuid}
```

**Default language (no prefix):**
```bash
GET /jsonapi/node/article/{uuid}
```

**Create translation (POST):**
```bash
curl -X POST "https://example.com/jsonapi/es/node/article" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Basic ..." \
  -d '{
    "data": {
      "type": "node--article",
      "attributes": {
        "title": "Articulo en espanol",
        "langcode": "es"
      }
    }
  }'
```

**Update translation (PATCH):**
```bash
curl -X PATCH "https://example.com/jsonapi/es/node/article/{uuid}" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Basic ..." \
  -d '{
    "data": {
      "type": "node--article",
      "id": "{uuid}",
      "attributes": {
        "title": "Titulo actualizado"
      }
    }
  }'
```

### Common Mistakes

**Expecting revision history via GET collection:** JSON:API doesn't expose revision listings. WHY: Collections return current revisions only. Use Views with JSON:API integration for revision lists.

**Not checking translation availability:** Requesting translation that doesn't exist returns default. WHY: Fallback behavior. Check `langcode` in response to verify actual language.

**Assuming all fields are translatable:** Some fields are shared across translations. WHY: Field configuration determines translatability. Check field settings.

**Creating translation without langcode attribute:** Translation creation requires explicit `langcode`. WHY: Server needs to know target language. Missing langcode creates default language entity.

### See Also
- [URL Structure & Resource Types](url-structure-resource-types.md)
- [Creating Resources (POST)](creating-resources.md)
- [Updating Resources (PATCH)](updating-resources.md)
