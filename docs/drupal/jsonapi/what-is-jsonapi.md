---
description: "Understanding JSON:API's purpose and determining if it fits your project requirements. JSON:API is a spec-compliant implementation built into Drupal core since 8.7."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## What is JSON:API

### When to Use

Understanding JSON:API's purpose helps determine if it fits your project requirements. JSON:API is a spec-compliant implementation built into Drupal core since 8.7.

**Use JSON:API when you need:**
- Decoupled frontend applications (React, Vue, Angular)
- Mobile app backends consuming Drupal content
- Spec-compliant APIs following jsonapi.org standards
- Zero-configuration entity exposure
- Rich querying capabilities (filtering, sorting, includes)

**Do NOT use JSON:API when you need:**
- Custom business logic endpoints
- Non-entity data exposure
- Aggregation or reporting endpoints
- Batch operations (create multiple at once)
- Real-time updates via WebSockets

### Core Features

| Feature | Description |
|---------|-------------|
| Zero Configuration | Automatic API for all entity types and bundles |
| Spec Compliance | Follows jsonapi.org specification exactly |
| Production Ready | Built-in caching, access control, validation |
| Automatic Discovery | Dynamic routes for all entities |
| Rich Querying | Filtering, sorting, pagination, includes out of the box |
| Security | Respects all Drupal entity and field access |

### Pattern

**Basic GET request:**
```bash
curl -X GET https://example.com/jsonapi/node/article \
  -H "Accept: application/vnd.api+json"
```

**Response structure:**
```json
{
  "data": [{
    "type": "node--article",
    "id": "uuid-here",
    "attributes": {
      "title": "Example Article"
    },
    "relationships": {
      "uid": {
        "data": { "type": "user--user", "id": "user-uuid" }
      }
    }
  }]
}
```

### Common Mistakes

**Not using required headers:** JSON:API requires `Accept: application/vnd.api+json` header. Missing this header returns HTML instead of JSON. WHY: The spec mandates this MIME type for proper content negotiation.

**Expecting all entities to be exposed automatically:** While JSON:API auto-exposes entities, access control still applies. WHY: Security is enforced at entity level--users without view permission won't see content.

**Assuming read-write is enabled:** Drupal enables read-only mode by default since Drupal 9. WHY: This prevents accidental data modification until explicitly configured.

### See Also
- [JSON:API vs REST vs GraphQL](jsonapi-vs-rest-vs-graphql.md)
- [Core Architecture](core-architecture.md)
- [URL Structure & Resource Types](url-structure-resource-types.md)
