---
description: "Both JSON:API and GraphQL work with next-drupal. JSON:API is simpler and built into Drupal core. GraphQL requires additional modules but offers more flexibility."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## JSON:API vs GraphQL Decision

### When to Use

Both JSON:API and GraphQL work with next-drupal. JSON:API is simpler and built into Drupal core. GraphQL requires additional modules but offers more flexibility.

### Decision

| Approach | Pros | Cons |
|----------|------|------|
| **JSON:API** | Core support, no extra modules, spec-compliant, easier debugging | Verbose responses, multiple requests for relationships, rigid structure |
| **GraphQL** | Single request for complex data, flexible queries, typed schema | Requires graphql_compose module, steeper learning curve, caching complexity |

### Pattern

JSON:API setup:

```typescript
// Drupal modules: next, next_jsonapi (included with next)
const articles = await drupal.getResourceCollection("node--article", {
  params: {
    include: "field_image,uid",
    "fields[node--article]": "title,body,created",
  },
})
```

GraphQL setup:

```typescript
// Drupal modules: next, next_graphql, graphql_compose
// Requires separate GraphQL client configuration
```

### Common Mistakes

- **Using GraphQL without understanding caching implications** — GraphQL caching is complex. WHY: Next.js ISR works better with REST-based JSON:API.
- **Not using sparse fieldsets with JSON:API** — Fetches unnecessary data. WHY: Bandwidth waste and slower responses.
- **Mixing JSON:API and GraphQL in one project** — Maintenance nightmare. WHY: Two API paradigms, two auth flows, two caching strategies.

### See Also

- Fetching Content
- drupal-jsonapi.md
- NextDrupal Client Configuration
