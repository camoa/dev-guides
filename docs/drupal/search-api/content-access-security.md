---
description: Search API content access — Content Access processor, access mechanisms, security caveats, and Solr index-only mode risks
tldr: "Use this when you need to ensure search results respect content access permissions. Search API does NOT restrict access by default."
drupal_version: "11.x"
---

# Content Access & Security

## When to Use

> Use this when you need to ensure search results respect content access permissions. Search API does NOT restrict access by default.

## Decision

| Mechanism | Processor | How It Works |
|---|---|---|
| Node access grants | `content_access` | Indexes grant records, filters at query time |
| Role-based access | `role_access` | Filters by user role |
| Entity status | `entity_status` | Excludes unpublished at index time |
| Views access checks | Built-in | Entity-level access on each result item |

## Pattern

**Security caveats:**

| Issue | Impact | Mitigation |
|---|---|---|
| Access permission lag | After permission changes, results stale until reindex | Frequent cron indexing (every 5 min) |
| Custom node access modules | Processor may not account for Group, Domain Access, etc. | Test thoroughly |
| Solr index-only mode | "Skip item access checks" bypasses ALL access | Only use for fully public content |
| Unpublished nodes | Content access processor doesn't handle unpublished grant access | Open issue #3520474 |

**Recommendations:**
1. Always enable Content Access processor if any content is restricted
2. Reindex frequently (every 5 minutes) if permissions change often
3. Test as different user roles before going live
4. Never use "Skip item access checks" on sites with restricted content

## Common Mistakes

- **Wrong**: Assuming search respects permissions by default → **Right**: It doesn't. Enable the Content Access processor explicitly.
- **Wrong**: Using "Skip item access checks" on restricted sites → **Right**: This bypasses all access control for query performance. Restricted content will be visible.
- **Wrong**: Not testing with anonymous user → **Right**: Search may work for admins but leak restricted content to anonymous.

## See Also

- [Processor Recommendations](processor-recommendations.md)
- [Query Performance](query-performance.md) — Solr index-only mode trade-offs
