---
description: Migrating to Group 3.x — version strategy, v1/v2 API changes, v2→v3 migration options, and custom code update patterns
drupal_version: "11.x"
---

# Migration from v1/v2

## When to Use

> Read this if you are moving an existing Group 1.x or 2.x site to Group 3.x.

## Decision

| From | To | Path |
|---|---|---|
| Group 1.x | Group 2.x | Upgrade path exists (hooks and DB updates) |
| Group 2.x | Group 3.x | No in-place upgrade — fresh install + migration required |
| Group 2.x | Group 2.x latest | Safe to update in place |

**v2 and v3 are functionally identical** — only machine names differ. There is no in-place database upgrade from v2 to v3.

## Pattern

**Option A: Recommended (clean migration)**
1. Set up a clean Drupal 10/11 install with Group 3.x
2. Configure group types, roles, and relationship types
3. Migrate data using Drupal Migrate API

**Option B: Manual database rename (community-documented, risky)**
1. Rename `group_content__group_roles` → `group_relationship__group_roles`
2. Replace `group_content` → `group_relationship` in all config files
3. Replace `group.content_type.` → `group.relationship_type.` in config file names
4. Clear all caches, run database updates

**Option C: Use contrib module `group2to3`**

Custom code search/replace for v1/v2 → v3:

```
GroupContent          → GroupRelationship
GroupContentType      → GroupRelationshipType
group_content         → group_relationship
addContent(           → addRelationship(
getContent(           → getRelationships(
getContentByEntityId( → getRelationshipsByEntity(
loadByContentPluginId → loadByPluginId
@GroupContentEnabler  → #[GroupRelationType(...)]
ContentEnablerBase    → GroupRelationBase
```

## Common Mistakes

- **Wrong**: Attempting a direct v2-to-v3 in-place upgrade → **Right**: The module maintainer explicitly states this is unsafe. There is no upgrade hook.
- **Wrong**: Forgetting to update Views and Panels config that reference `group_content` machine names → **Right**: Audit all Views, Panels, and contrib config for old machine names before migrating.
- **Wrong**: Running `drush entup` and assuming it fixes everything → **Right**: It updates entity schema definitions only, not database tables or stored data.
- **Wrong**: Not checking the 32-character ID limit → **Right**: When renaming config IDs, new IDs may exceed Drupal's 32-character limit. Audit all config IDs before migration.

## See Also

- [Core Architecture](core-architecture.md)
- [Configuration](configuration.md)
- Reference: https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/group/group-v2v3-guides/upgrading-from-v1-to-v2
