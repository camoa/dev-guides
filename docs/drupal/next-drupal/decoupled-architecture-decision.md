---
description: "Choose decoupled Drupal with Next.js when you need modern frontend performance, independent backend/frontend development teams, or flexibility to serve multiple frontends from one Drupal backend."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Decoupled Architecture Decision

### When to Use

Choose decoupled Drupal with Next.js when you need modern frontend performance, independent backend/frontend development teams, or flexibility to serve multiple frontends from one Drupal backend.

### Decision

| Approach | Best For | Trade-offs |
|----------|----------|------------|
| **Fully Decoupled (Next.js)** | High-traffic sites, mobile apps, multiple frontends, headless commerce | More complexity, two deployments, no Layout Builder preview |
| **Progressively Decoupled** | Incremental migration, mixed teams, selective performance optimization | Coordination overhead, dual architecture |
| **Traditional Drupal** | Content-heavy sites, simple editorial workflow, limited dev resources | Limited frontend flexibility, slower page loads |

### Pattern

```typescript
// lib/drupal.ts
import { NextDrupal } from "next-drupal"

export const drupal = new NextDrupal(
  process.env.NEXT_PUBLIC_DRUPAL_BASE_URL,
  {
    auth: {
      clientId: process.env.DRUPAL_CLIENT_ID,
      clientSecret: process.env.DRUPAL_CLIENT_SECRET,
    },
  }
)
```

### Common Mistakes

- **Using decoupled for simple brochure sites** — Adds unnecessary complexity. WHY: Two systems to maintain for minimal benefit.
- **Not planning authentication upfront** — OAuth setup is complex. WHY: Retrofitting auth is harder than planning it initially.
- **Ignoring content modeling differences** — Drupal fields don't map 1:1 to frontend needs. WHY: JSON:API structure differs from template requirements.

### See Also

- Next.js Project Setup
- Drupal Setup
- drupal-jsonapi.md (for JSON:API details)
