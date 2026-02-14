---
description: "Fetch related entities in a single request (compound documents) and request only needed fields to reduce response size and processing time."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Includes & Sparse Fieldsets

### When to Use

**Includes:** Fetch related entities in a single request (compound documents). Reduces HTTP round trips.

**Sparse Fieldsets:** Request only needed fields. Reduces response size and processing time.

### Decision

| Scenario | Use Includes? | Use Sparse Fieldsets? |
|----------|---------------|------------------------|
| Article with author name | Yes: `?include=uid` | Yes: `?fields[user--user]=name` |
| Blog listing (title only) | No | Yes: `?fields[node--article]=title` |
| Article with tags and images | Yes: `?include=field_tags,field_image` | Optional |
| Mobile app (bandwidth concern) | Selective | Yes (critical) |
| Full entity needed | Optional | No |
| Deeply nested relationships | Yes: `?include=uid.user_picture` | Yes |

### Pattern

**Include single relationship:**
```bash
# Get article with author
GET /jsonapi/node/article/{uuid}?include=uid
```

Response includes author in `included` array:
```json
{
  "data": {
    "type": "node--article",
    "id": "uuid",
    "relationships": {
      "uid": { "data": { "type": "user--user", "id": "user-uuid" } }
    }
  },
  "included": [{
    "type": "user--user",
    "id": "user-uuid",
    "attributes": { "name": "admin" }
  }]
}
```

**Include multiple relationships:**
```bash
GET /jsonapi/node/article?include=uid,field_image,field_tags
```

**Nested includes (relationship of relationship):**
```bash
# Include author and author's profile picture
GET /jsonapi/node/article?include=uid.user_picture
```

**Sparse fieldsets on main resource:**
```bash
# Only return title and created date
GET /jsonapi/node/article?fields[node--article]=title,created
```

**Sparse fieldsets on included resources:**
```bash
# Include author but only their name and email
GET /jsonapi/node/article?include=uid&fields[user--user]=name,mail
```

**Combined (includes + sparse fieldsets):**
```bash
# Article title, author name, image URI
GET /jsonapi/node/article?include=uid,field_image&fields[node--article]=title,uid,field_image&fields[user--user]=name&fields[file--file]=uri
```

### Common Mistakes

**Including relationships not needed:** Over-inclusion increases response size dramatically. WHY: Each included entity adds significant data. Only include what's rendered.

**Not using sparse fieldsets with includes:** Including a user pulls ALL user fields. WHY: Default behavior is full entity. Combine with `?fields[user--user]=name` to limit.

**Requesting relationship field without include:** Relationships in `data` only contain type/id references. WHY: To get actual data, must use `?include=field_name`.

**Deeply nesting includes beyond 2 levels:** `?include=uid.user_picture.field_media` may fail or timeout. WHY: Performance degrades with nesting. Limit to 1-2 levels max.

**Forgetting type prefix in sparse fieldsets:** It's `?fields[node--article]=title`, not `?fields=title`. WHY: Must specify resource type since response can include multiple types.

### See Also
- [Fetching Resources (GET)](fetching-resources.md)
- [Performance Optimization](performance-optimization.md)
- [Sorting & Pagination](sorting-pagination.md)
