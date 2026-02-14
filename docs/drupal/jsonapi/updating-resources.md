---
description: "Modifying existing entities. Requires authentication, entity UUID, and update permissions."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Updating Resources (PATCH)

### When to Use

Modifying existing entities. Requires authentication, entity UUID, and update permissions.

### Steps

**1. Obtain entity UUID:**
   - From previous GET request
   - From entity load in Drupal

**2. Construct PATCH request:**
   - Method: `PATCH`
   - URL: `/jsonapi/{entity_type}/{bundle}/{uuid}`
   - Headers: Same as POST (Accept, Content-Type, Authorization)
   - Body: JSON:API document with `data.type`, `data.id`, changed attributes/relationships

**3. Send only changed fields:**
   - Include only attributes/relationships being modified
   - Omit unchanged fields

**4. Handle response:**
   - Success: `200 OK` with updated entity
   - Errors: `422 Unprocessable Entity`, `403 Forbidden`, `404 Not Found`

### Pattern

**Basic PATCH request:**
```bash
curl -X PATCH "https://example.com/jsonapi/node/article/{uuid}" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -d '{
    "data": {
      "type": "node--article",
      "id": "{uuid}",
      "attributes": {
        "title": "Updated Title"
      }
    }
  }'
```

**Update multiple fields:**
```json
{
  "data": {
    "type": "node--article",
    "id": "{uuid}",
    "attributes": {
      "title": "New Title",
      "body": {
        "value": "<p>Updated content</p>",
        "format": "html"
      },
      "status": 1
    }
  }
}
```

**Update relationships (replace):**
```json
{
  "data": {
    "type": "node--article",
    "id": "{uuid}",
    "relationships": {
      "field_tags": {
        "data": [
          { "type": "taxonomy_term--tags", "id": "{new-tag-uuid}" }
        ]
      }
    }
  }
}
```

**Clear relationship (set to null):**
```json
{
  "data": {
    "type": "node--article",
    "id": "{uuid}",
    "relationships": {
      "field_image": {
        "data": null
      }
    }
  }
}
```

### Decision Points

| Task | Approach |
|------|----------|
| Update single field | PATCH with one attribute |
| Publish draft | Set `status` attribute to 1 |
| Unpublish | Set `status` to 0 |
| Change author | Update `uid` relationship |
| Add tags | PATCH `field_tags` relationship with full array |
| Remove all tags | Set `field_tags.data` to `[]` |
| Clear single-value reference | Set relationship `data` to `null` |

### Common Mistakes

**Forgetting to include type and id:** PATCH body must have `data.type` and `data.id`. WHY: Server validates resource identifier matches URL. Missing these results in 400 error.

**Sending entire entity when updating one field:** Only include changed fields. WHY: Reduces payload size and avoids accidental overwrites.

**Expecting partial relationship updates:** Setting `field_tags` replaces entire array. WHY: PATCH relationships are full replacement, not merge. To add one tag, send entire new array including existing tags.

**Not handling validation errors:** 422 response includes detailed field errors. WHY: Entity validation applies. Check `errors` array in response for specific field issues.

**Trying to update immutable fields:** Some fields like `uuid`, `created` are read-only. WHY: System fields are protected. Attempting to change them is silently ignored or errors.

### See Also
- [Creating Resources (POST)](creating-resources.md)
- [Deleting Resources (DELETE)](deleting-resources.md)
- [Authentication Patterns](authentication-patterns.md)
- [Code Reference Map](code-reference-map.md) (`src/Controller/EntityResource.php`)
