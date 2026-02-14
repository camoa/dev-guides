---
description: "Creating new entities via the API. Requires authentication and proper permissions."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Creating Resources (POST)

### When to Use

Creating new entities via the API. Requires authentication and proper permissions.

### Steps

**1. Enable write operations:**
   - Visit `/admin/config/services/jsonapi`
   - Check "Accept all JSON:API create, read, update, and delete operations"
   - OR leave read-only and enable selectively via permissions

**2. Set up authentication:**
   - Enable `basic_auth` module for HTTP Basic Auth
   - OR configure OAuth2, JWT, or cookie-based auth
   - Grant "Restful POST" permission and entity create permissions

**3. Construct request:**
   - Method: `POST`
   - URL: `/jsonapi/{entity_type}/{bundle}`
   - Headers: `Accept: application/vnd.api+json`, `Content-Type: application/vnd.api+json`, `Authorization: Basic {credentials}`
   - Body: JSON:API document with `data.type`, `data.attributes`, `data.relationships`

**4. Handle response:**
   - Success: `201 Created` with created entity in response
   - Failure: `400 Bad Request`, `422 Unprocessable Entity`, `403 Forbidden`

### Pattern

**Basic POST request:**
```bash
curl -X POST "https://example.com/jsonapi/node/article" \
  -H "Accept: application/vnd.api+json" \
  -H "Content-Type: application/vnd.api+json" \
  -H "Authorization: Basic dXNlcjpwYXNz" \
  -d '{
    "data": {
      "type": "node--article",
      "attributes": {
        "title": "New Article",
        "body": {
          "value": "<p>Article content</p>",
          "format": "html"
        }
      }
    }
  }'
```

**Creating with relationships:**
```json
{
  "data": {
    "type": "node--article",
    "attributes": {
      "title": "Article with Author and Tags"
    },
    "relationships": {
      "uid": {
        "data": { "type": "user--user", "id": "{user-uuid}" }
      },
      "field_tags": {
        "data": [
          { "type": "taxonomy_term--tags", "id": "{tag-uuid-1}" },
          { "type": "taxonomy_term--tags", "id": "{tag-uuid-2}" }
        ]
      }
    }
  }
}
```

**JavaScript example:**
```javascript
fetch('/jsonapi/node/article', {
  method: 'POST',
  headers: {
    'Accept': 'application/vnd.api+json',
    'Content-Type': 'application/vnd.api+json',
    'Authorization': 'Basic ' + btoa('user:pass')
  },
  body: JSON.stringify({
    data: {
      type: 'node--article',
      attributes: {
        title: 'New Article',
        body: { value: 'Content', format: 'html' }
      }
    }
  })
})
  .then(res => res.json())
  .then(data => console.log('Created:', data.data.id));
```

### Decision Points

| Scenario | Approach |
|----------|----------|
| Simple content creation | POST with attributes only |
| Assign author | Include `uid` in relationships |
| Assign taxonomy terms | Include term references in relationships |
| Set publish status | Set `status` attribute to 1 |
| Upload files | Use separate file upload endpoint (see File Uploads guide) |
| Create with custom fields | Include in attributes with correct structure |

### Common Mistakes

**Forgetting Content-Type header:** Must be `application/vnd.api+json` for POST/PATCH. WHY: Drupal validates content type. Wrong header results in 400 error.

**Using node ID instead of UUID in relationships:** References must be UUIDs. WHY: JSON:API uses UUIDs as identifiers. Node IDs won't work.

**Not setting required fields:** Missing required fields triggers validation error. WHY: Entity validation applies. Check field configuration for required fields.

**Incorrect field value structure:** Complex fields (body, text_format) require object with `value` and `format`. WHY: Field type determines structure. Single-value text is string, formatted text is object.

**Creating without proper permissions:** 403 Forbidden means user lacks create permission. WHY: Entity access system enforces permissions. Grant bundle-specific create permission.

### See Also
- [Updating Resources (PATCH)](updating-resources.md)
- [File Uploads](file-uploads.md)
- [Authentication Patterns](authentication-patterns.md)
- [Code Reference Map](code-reference-map.md) (`src/Controller/EntityResource.php`)
