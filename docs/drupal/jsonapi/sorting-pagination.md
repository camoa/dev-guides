---
description: "Control result order and break large result sets into pages. Essential for chronological listings, alphabetical lists, and unbounded collections."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Sorting & Pagination

### When to Use

**Sorting:** Control result order. Essential for chronological listings, alphabetical lists, and custom ordering.

**Pagination:** Break large result sets into pages. Required for collections that can grow unbounded.

### Sorting Syntax

| Pattern | Description | Example |
|---------|-------------|---------|
| `?sort=field` | Sort ascending by field | `?sort=title` |
| `?sort=-field` | Sort descending by field | `?sort=-created` |
| `?sort=field1,field2` | Multi-field sort | `?sort=-created,title` |
| `?sort=relationship.field` | Sort by relationship field | `?sort=uid.name` |

### Sorting Examples

```bash
# Newest articles first
GET /jsonapi/node/article?sort=-created

# Alphabetical by title
GET /jsonapi/node/article?sort=title

# Newest first, then alphabetical
GET /jsonapi/node/article?sort=-created,title

# Sort by author name
GET /jsonapi/node/article?sort=uid.name
```

### Pagination Syntax

| Parameter | Description | Default |
|-----------|-------------|---------|
| `page[limit]` | Items per page | 50 |
| `page[offset]` | Skip N items | 0 |

**Offset-based pagination:**
```
Page 1: ?page[limit]=25&page[offset]=0
Page 2: ?page[limit]=25&page[offset]=25
Page 3: ?page[limit]=25&page[offset]=50
```

### Pagination Response

JSON:API includes pagination links:
```json
{
  "data": [...],
  "links": {
    "self": { "href": "...?page[offset]=0&page[limit]=25" },
    "first": { "href": "...?page[offset]=0&page[limit]=25" },
    "prev": { "href": "...?page[offset]=0&page[limit]=25" },
    "next": { "href": "...?page[offset]=25&page[limit]=25" },
    "last": { "href": "...?page[offset]=100&page[limit]=25" }
  }
}
```

### Pattern

**Paginated, sorted collection:**
```bash
# Published articles, newest first, 10 per page
GET /jsonapi/node/article?filter[status]=1&sort=-created&page[limit]=10&page[offset]=0
```

**Client-side pagination loop:**
```javascript
async function fetchAllArticles() {
  let articles = [];
  let nextUrl = '/jsonapi/node/article?page[limit]=50';

  while (nextUrl) {
    const response = await fetch(nextUrl, {
      headers: { 'Accept': 'application/vnd.api+json' }
    });
    const data = await response.json();
    articles = articles.concat(data.data);
    nextUrl = data.links.next?.href || null;
  }

  return articles;
}
```

### Common Mistakes

**Not implementing pagination:** Fetching unbounded collections can timeout or exhaust memory. WHY: Large sites have thousands of nodes. Always use `page[limit]`.

**Using huge page limits:** Setting `page[limit]=1000` defeats pagination purpose. WHY: Performance degrades with large pages. Stick to 10-50 items.

**Sorting by non-indexed fields:** Sorting by body text or complex fields is slow. WHY: Database can't efficiently sort non-indexed columns. Sort by created, title, or indexed fields.

**Forgetting to handle missing next link:** When `links.next` is absent, you're on the last page. WHY: No more results exist. Check for link existence before fetching.

**Combining offset pagination with rapidly changing data:** Items can appear twice or get skipped. WHY: If new items are created between requests, offsets shift. For real-time data, use cursor-based pagination (requires custom implementation).

### See Also
- [Fetching Resources (GET)](fetching-resources.md)
- [Filtering](filtering.md)
- [Performance Optimization](performance-optimization.md)
