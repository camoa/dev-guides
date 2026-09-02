---
description: Search API content access — Content Access processor, access mechanisms, security caveats, and Solr index-only mode risks
tldr: "Use this when you need to ensure search results respect content access permissions. Search API does NOT restrict access by default."
drupal_version: "11.x"
---

# Content Access & Security

## When to Use

> When you need to ensure search results respect content access permissions.

## Decision: Content Access Processor

The Content Access processor adds node access grant data to the index and filters search results based on the current user's permissions.

**Critical:** Search API does NOT restrict access by default. Without this processor, all indexed content is visible to all users.

## Decision: Access Mechanisms

| Mechanism | Processor | How It Works |
|---|---|---|
| Node access grants | `content_access` | Indexes grant records, filters at query time |
| Role-based access | `role_access` | Filters by user role |
| Entity status | `entity_status` | Excludes unpublished at index time |
| Views access checks | Built-in | Entity-level access on each result item |

## Pattern: Security Caveats

| Issue | Impact | Mitigation |
|---|---|---|
| Access permission lag | After changing permissions, results stale until reindex | Frequent cron indexing (every 5 min) |
| Custom node access modules | Processor may not account for Group, Domain Access, etc. | Test thoroughly with custom access |
| Multi-domain grant bug | Nodes on one domain may leak to another | Known issue — monitor carefully |
| Solr index-only mode | "Skip item access checks" bypasses ALL access | Only use for fully public content |
| Unpublished nodes | Content access processor doesn't handle unpublished grant access | Open issue #3520474 |

## Pattern: Recommendations

1. **Always enable Content Access processor** if any content is restricted
2. **Reindex frequently** (every 5 minutes) if permissions change often
3. **Test as different user roles** before going live
4. **Never use "Skip item access checks"** on sites with restricted content
5. For Solr index-only mode on restricted sites, keep entity loads enabled for access checking

## Common Mistakes

- **Assuming search respects permissions by default** — It doesn't. You must enable the Content Access processor.
- **Using "Skip item access checks" on restricted sites** — This bypasses all access control for query performance. Restricted content will be visible.
- **Not testing with anonymous user** — Search may work perfectly for admins but leak restricted content to anonymous.

## See Also

- [Processor Recommendations](processor-recommendations.md) — processor enablement
- [Query Performance](query-performance.md) — Solr index-only mode trade-offs
