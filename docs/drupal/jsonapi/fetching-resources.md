---
description: "Retrieving entity data from Drupal. Applies to collections (multiple entities) and individual entities."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Fetching Resources (GET)

### When to Use

Retrieving entity data from Drupal. Applies to collections (multiple entities) and individual entities.

### Steps

**1. Determine resource URL:**
   - Collection: `/jsonapi/{entity_type}/{bundle}`
   - Individual: `/jsonapi/{entity_type}/{bundle}/{uuid}`

**2. Set required header:**
   - `Accept: application/vnd.api+json`

**3. Add query parameters (optional):**
   - Filtering: `?filter[field]=value`
   - Includes: `?include=field_name`
   - Sparse fieldsets: `?fields[type]=field1,field2`
   - Sorting: `?sort=-created`
   - Pagination: `?page[limit]=10&page[offset]=0`

**4. Make GET request:**
   - Use curl, fetch, axios, or HTTP client

**5. Parse response:**
   - `data`: Resource object(s)
   - `included`: Related resources (if requested)
   - `links`: Pagination links
   - `meta`: Metadata

### Pattern

**Fetch collection:**
```bash
curl -X GET "https://example.com/jsonapi/node/article" \
  -H "Accept: application/vnd.api+json"
```

**Fetch individual:**
```bash
curl -X GET "https://example.com/jsonapi/node/article/{uuid}" \
  -H "Accept: application/vnd.api+json"
```

**Fetch with includes and sparse fields:**
```bash
curl -X GET "https://example.com/jsonapi/node/article?include=uid,field_image&fields[node--article]=title,created,uid&fields[user--user]=name" \
  -H "Accept: application/vnd.api+json"
```

**JavaScript with fetch:**
```javascript
fetch('/jsonapi/node/article?include=uid&page[limit]=10', {
  headers: { 'Accept': 'application/vnd.api+json' }
})
  .then(response => response.json())
  .then(data => {
    const articles = data.data;
    const users = data.included;
  });
```

### Decision Points

| Scenario | Query Parameters |
|----------|------------------|
| Get published articles only | `?filter[status]=1` |
| Get newest articles first | `?sort=-created` |
| Get 10 articles at a time | `?page[limit]=10` |
| Get articles with author info | `?include=uid` |
| Reduce response size | `?fields[node--article]=title,created` |
| Get specific revision | `?resourceVersion=id:123` |
| Get Spanish translation | Use `/jsonapi/es/node/article/{uuid}` |

### Common Mistakes

**Not handling pagination:** Collections default to 50 items max. WHY: Performance protection. Always check `links.next` for more results.

**Over-fetching data:** Requesting all fields when only a few are needed. WHY: Wastes bandwidth, especially on mobile. Use sparse fieldsets.

**Making separate requests for relationships:** Use `?include=uid` instead of separate requests. WHY: Reduces HTTP round trips. The "N+1 queries" problem applies to HTTP too.

**Ignoring cache headers:** JSON:API includes proper cache headers. WHY: Responses are cacheable. Leverage browser cache or CDN.

### See Also
- [Filtering](filtering.md)
- [Includes & Sparse Fieldsets](includes-sparse-fieldsets.md)
- [Sorting & Pagination](sorting-pagination.md)
- [Revisions & Translations](revisions-translations.md)
