---
description: Group 3.x data model — entities, scopes, v2 vs v3 differences, and key dependencies
drupal_version: "11.x"
---

# Core Architecture

## When to Use

> Read this when you need to understand Group 3.x's data model and how it differs from earlier versions before writing any code.

## Decision

| Situation | Choose | Why |
|---|---|---|
| New site, Drupal 10.3+/11 | Group 3.x | Active maintenance, PHP 8 attributes |
| Existing site on Drupal 9/10 with Group 2.x | Stay on 2.x | No in-place upgrade to 3.x exists |
| Migrating from Group 1.x | Upgrade to 2.x first | 1.x→2.x has an upgrade path; 2.x→3.x does not |

## Pattern

```
group_type (config entity, bundle of group)
    |
    +-- group (content entity, bundle = group_type id)
    |
    +-- group_relationship_type (config entity, bundle of group_relationship)
            |
            +-- group_relationship (content entity)
                    |-- gid          -> points to group
                    |-- entity_id    -> points to the related entity
                    |-- plugin_id    -> which GroupRelationType plugin handles this
                    |-- group_type   -> denormalized group type id (performance)
```

**Three scopes of users relative to a group:**

| Scope | Description | Constant |
|---|---|---|
| Outsider | Authenticated site user, NOT a member | `PermissionScopeInterface::OUTSIDER_ID` |
| Insider | Authenticated site user, IS a member | `PermissionScopeInterface::INSIDER_ID` |
| Individual | A specific member with an explicitly assigned role | `PermissionScopeInterface::INDIVIDUAL_ID` |
| Anonymous | Unauthenticated user (subset of outsider scope) | — |

## Common Mistakes

- **Wrong**: Treating Group 3.x like Group 1.x → **Right**: `GroupContent`, `addContent()`, and `GroupContentEnabler` are gone. Everything is now `GroupRelationship`, `addRelationship()`, and `GroupRelationBase`.
- **Wrong**: Installing v3 over v2 data → **Right**: There is no in-place upgrade. Migrate data or use the `group2to3` contrib module.

## See Also

- [Entity Types](entity-types.md)
- [Migration from v1/v2](migration-from-v1v2.md)
- Reference: `web/modules/contrib/group/src/Entity/`
