---
description: "Choose the right API approach based on your project's requirements and constraints."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## JSON:API vs REST vs GraphQL

### When to Use

Choose the right API approach based on your project's requirements and constraints.

### Decision

| Scenario | Recommended API | Why |
|----------|----------------|-----|
| Decoupled frontend (React/Vue/Angular) | JSON:API | Spec compliance, rich querying, zero config |
| Mobile app backend | JSON:API | Efficient data fetching, includes reduce API calls |
| Custom business logic endpoints | REST Module | Not entity-based, custom response formats |
| Complex nested data requirements | GraphQL | Client controls exact data shape |
| Legacy API compatibility | REST Module | Match existing API format |
| Content syndication | JSON:API | Standardized format, multiple consumers |
| Real-time updates | GraphQL + Subscriptions | WebSocket support, live updates |
| Admin dashboard with aggregations | Custom Controllers | Non-entity operations, reports |
| Rapid prototyping | JSON:API | Zero configuration, immediate availability |

### Pattern

**Comparison matrix:**
```
Feature Comparison:
+----------------------+------------+----------+----------+
| Feature              | JSON:API   | REST     | GraphQL  |
+----------------------+------------+----------+----------+
| Configuration        | Zero       | Required | Required |
| Entity CRUD          | Automatic  | Manual   | Manual   |
| Querying             | Rich       | Limited  | Powerful |
| Response Format      | Spec only  | Flexible | Flexible |
| Relationships        | Built-in   | Manual   | Built-in |
| Specification        | jsonapi.org| None     | GraphQL  |
+----------------------+------------+----------+----------+
```

**JSON:API for blog with mobile app:**
```bash
# Single request fetches articles with authors and images
GET /jsonapi/node/article?include=uid,field_image&page[limit]=10
```

**REST for custom reports:**
```php
// Custom endpoint for aggregated data
GET /api/custom/sales-report?year=2026
```

### Common Mistakes

**Using JSON:API for non-entity data:** Custom reports, calculations, or aggregations don't map to entities. WHY: JSON:API is entity-centric--it normalizes entities, not arbitrary data structures. Use custom controllers instead.

**Not using sparse fieldsets:** Requesting all fields wastes bandwidth and processing time. WHY: Mobile apps especially benefit from requesting only needed fields (`?fields[node--article]=title,created`).

**Exposing all entity types:** Internal or administrative entities shouldn't be in the API. WHY: Security through minimization--only expose what consumers need. Use JSON:API Extras to disable unused resources.

**Forgetting authentication for write operations:** POST/PATCH/DELETE require authentication. WHY: Drupal's access system prevents anonymous writes. Enable `basic_auth` module or OAuth2.

### See Also
- [What is JSON:API](what-is-jsonapi.md)
- [Authentication Patterns](authentication-patterns.md)
- [Security Best Practices](security-best-practices.md)
