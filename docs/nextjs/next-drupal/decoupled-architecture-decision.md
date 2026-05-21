---
description: "Choose decoupled Drupal with Next.js when you need modern frontend performance, independent backend/frontend development teams, or flexibility to serve multiple frontends from one Drupal backend."
tldr: "Choose decoupled Drupal with Next.js when you need modern frontend performance, independent backend/frontend development teams, or flexibility to serve multiple frontends from one Drupal backend. As of May 2026, next-drupal is minimally maintained and does not support Next.js 16 — weigh this before starting a long-lived build."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Decoupled Architecture Decision

### When to Use

Choose decoupled Drupal with Next.js when you need modern frontend performance, independent backend/frontend development teams, or flexibility to serve multiple frontends from one Drupal backend.

### Project Status (May 2026)

Before committing to next-drupal, weigh its current maintenance state:

- **Maintainer** — the project was created by Chapter Three, which **Kanopi Studios acquired in January 2026**. The GitHub repo is still `chapter-three/next-drupal`.
- **Maintenance** — Kanopi has publicly stated (GitHub issue #885) the project "has been **minimally maintained**" and is relying on **community volunteer maintainers**. A future-direction BoF was held at DrupalCon Chicago (March 2026); no public roadmap has been published since.
- **Next.js support** — `next-drupal` 2.0.1 supports `next ^14 || ^15` only. **Next.js 16 is not supported** (open type-incompatibility, issue #884), and **Next.js 15 reaches end-of-life in October 2026**. The supported stack therefore has a limited runway until next-drupal ships a 16-compatible release.

This is not a "don't use next-drupal" warning — it remains the standard JSON:API/GraphQL client for decoupled Drupal — but treat the Next.js version ceiling and maintenance cadence as real project risks when planning a long-lived build.

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
