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

## Architecture Overview

Group 4.x organizes site content into discrete containers called **groups**. Every group is a content entity with a bundle called a **group type**. The relationship between a group and any other entity (user, node, media, config) is called a **group relationship** — a content entity in its own right.

The architecture mirrors Drupal core's node/node_type pattern:

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

Permissions are layered: a user gets outsider permissions based on their global Drupal roles, insider permissions based on their global roles while also being a member, and individual permissions from explicitly assigned group roles.

## Version Differences (One Line Each)

**v2 vs v3** — functionally identical; the only difference is machine names: `group_content` became `group_relationship`, and `group_content_type` became `group_relationship_type`. No programmatic upgrade path; separate major versions.

**v3 vs v4** — same data model, same entity types, same scope system. v4 is an *infrastructure* rewrite, not a feature rewrite: permission calculation moved to Drupal core's Access Policy API, all contrib dependencies were dropped, procedural hooks became OOP hook classes, the two-step relationship-creation wizard was removed, and automatic creator membership is now restricted to form submissions. See [Migration from v1/v2](migration-from-v1v2.md) for the full v3→v4 change list.

## Key Dependencies

Group 4.x depends only on **Drupal core `^11.2`** and core's **Options** module. It no longer requires any contrib module.

- **Access Policy API (core)** — Group's permission calculation runs on Drupal core's Access Policy API (stabilized in core 11.2). Group registers two access policies, both tagged `access_policy`: `access_policy.individual_group_role` (`IndividualGroupRoleAccessPolicy`, priority -100) and `access_policy.synchronized_group_role` (`SynchronizedGroupRoleAccessPolicy`, priority -50). See [Permissions System](permissions-system.md).
- **Revision UI (core)** — entity revision routes and revision handling now come from Drupal core.

> **3.x:** Group 3.x depended on two contrib modules: **`flexible_permissions`** (which provided chain permission calculators `IndividualGroupPermissionCalculator` and `SynchronizedGroupPermissionCalculator`) and **`drupal/entity`** (revision routes). Both were dropped in 4.x — `flexible_permissions` was absorbed into core as the Access Policy API, and core gained the revision UI Group needed. Custom code that registered `flexible_permissions_calculator` services must be ported to core access policies.

## Common Mistakes

- Treating Group 4.x like Group 1.x. The `GroupContent` entity, `addContent()` method, and `GroupContentEnabler` plugin are all gone. Everything is now `GroupRelationship`, `addRelationship()`, and `GroupRelationBase`.
- Installing v3 over v2 data. There is no in-place upgrade — you must migrate the data. Do not reach for the `group2to3` contrib module: it is marked **Unsupported** and **Obsolete** on drupal.org and has never had a tagged release.

## See Also

- [Entity Types](entity-types.md)
- [Migration from v1/v2](migration-from-v1v2.md)
- Reference: `web/modules/contrib/group/src/Entity/`
