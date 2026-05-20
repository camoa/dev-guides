---
description: Group 4.x data model — entities, scopes, v3 vs v4 differences, and key dependencies
tldr: "Group 4.x uses the same data model as 3.x (group_relationship, scopes, GroupRelationBase) but drops all contrib dependencies — permission calculation moved to Drupal core's Access Policy API and all hooks became OOP classes."
drupal_version: "11.x"
---

# Core Architecture

## When to Use

> Read this when you need to understand Group 4.x's data model and how it differs from earlier versions before writing any code.

## Decision

| Situation | Choose | Why |
|---|---|---|
| New site, Drupal 11.2+ | Group 4.x | No contrib dependencies, Access Policy API, OOP hooks |
| Existing site on Drupal 10 | Group 3.3.5 | 4.x requires Drupal 11.2+; 3.x is the latest stable for Drupal 10 |
| Existing site on Drupal 11.2+ with Group 3.x | Upgrade to 4.x | Normal module update — same data model and machine names |
| Migrating from Group 2.x | Upgrade to 3.x first | Same data model as 3.x; then upgrade core to 11.2+ and upgrade to 4.x |

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

**v4 key dependencies** (core only — no contrib required):

- **Access Policy API (core 11.2+)** — replaces `flexible_permissions` contrib. Group registers `IndividualGroupRoleAccessPolicy` (priority -100) and `SynchronizedGroupRoleAccessPolicy` (priority -50) tagged `access_policy`.
- **Revision UI (core)** — replaces `drupal/entity` contrib.

## Common Mistakes

- **Wrong**: Treating Group 4.x like Group 1.x → **Right**: `GroupContent`, `addContent()`, and `GroupContentEnabler` are gone since 3.x. Use `GroupRelationship`, `addRelationship()`, and `GroupRelationBase`.
- **Wrong**: Registering a `flexible_permissions_calculator`-tagged service → **Right**: In 4.x the tag is `access_policy`. Re-implement custom calculators as `AccessPolicyBase` subclasses.
- **Wrong**: Installing Group 4.x on Drupal 10 or Drupal 11.0/11.1 → **Right**: Group 4.x requires Drupal 11.2+ for the Access Policy API.

## See Also

- [Entity Types](entity-types.md)
- [Migration from v1/v2](migration-from-v1v2.md)
- Reference: `web/modules/contrib/group/src/Entity/`
