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
| New site, Drupal 11.2+ | Group 4.x | No contrib dependencies, Access Policy API, OOP hooks — but `4.0.0-alpha2` is the newest tag on the 4.0.x branch (no stable release), requires an `@alpha` install, and is not covered by Drupal security advisories |
| Existing site on Drupal 11.2+ with Group 3.x | Upgrade to 4.x | Normal module update — same data model and machine names; the same alpha-only caveat applies |
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

**Version differences:**

| Version jump | What changed |
|---|---|
| v2 → v3 | Functionally identical; only machine names changed (`group_content` → `group_relationship`, `group_content_type` → `group_relationship_type`). No programmatic upgrade path. |
| v3 → v4 | Same data model, entities, and scopes. Infrastructure rewrite: permission calculation moved to the Access Policy API, all contrib dependencies dropped, procedural hooks became OOP hook classes, the two-step relationship-creation wizard removed, automatic creator membership restricted to form submissions. |

**v4 key dependencies** (core only — no contrib required):

- **Access Policy API (core 11.2+)** — replaces `flexible_permissions` contrib. Group registers `IndividualGroupRoleAccessPolicy` (priority -100) and `SynchronizedGroupRoleAccessPolicy` (priority -50) tagged `access_policy`.
- **Revision UI (core)** — replaces `drupal/entity` contrib.

## Common Mistakes

- **Wrong**: Treating Group 4.x like Group 1.x → **Right**: The `GroupContent` entity, `addContent()` method, and `GroupContentEnabler` plugin are all gone since 3.x. Use `GroupRelationship`, `addRelationship()`, and `GroupRelationBase`.
- **Wrong**: Installing v3 over v2 data expecting an in-place upgrade → **Right**: There is no in-place upgrade — migrate the data. Do not reach for the `group2to3` contrib module: it is marked **Unsupported** and **Obsolete** on drupal.org and has never had a tagged release.

## See Also

- [Entity Types](entity-types.md)
- [Migration from v1/v2](migration-from-v1v2.md)
- Reference: `web/modules/contrib/group/src/Entity/`
