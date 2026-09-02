---
description: Migrating Group versions — v1/v2 API changes, v2→v3 migration options, and v3→v4 upgrade (normal module update)
tldr: "Read this if you are moving an existing Group site to a newer major version. v1→v2 is an in-place update once the site has run updates through 8023; v2→v3 requires a full data migration (group2to3 is Unsupported/Obsolete — don't use it); v3→v4 requires an explicit @alpha stability flag since 4.0.x has no stable tag."
drupal_version: "11.x"
---

# Migration from v1/v2

## When to Use

> Read this if you are moving an existing Group site to a newer major version — v1→v2, v2→v3, or v3→v4.

## Decision

| From | To | Path |
|---|---|---|
| Group 1.x | Group 2.x | In-place update via `group_update_9200`–`group_update_9211` (installs `flexible_permissions`, converts fixed roles to the scope system) — the 1.x site must have run its own updates through `8023` first |
| Group 2.x | Group 3.x | No in-place upgrade — fresh install + migration required (do **not** use `group2to3`) |
| Group 3.x | Group 4.x | Normal module update on Drupal 11.2+ — same data model, but requires an explicit `@alpha` flag |

## Version Strategy Summary

Two branches are actionable on Drupal 11.4:

| Branch | Declared core compatibility | Status |
|---|---|---|
| 3.3.x | `^10.3 \|\| ^11` | **Latest stable — 3.3.5 (2025-05-06).** The only Group release with a stable tag, and the only one the contrib ecosystem supports. |
| 4.0.x | `^11.2` | Release branch whose newest tag is **`4.0.0-alpha2`** (2026-08-21, after `4.0.0-alpha1` on 2026-04-24) — infrastructure rewrite, BC breaks complete, no stable. Requires an `@alpha` install; not covered by Drupal security advisories. |

Group also still lists `8.x-1.` and `2.3.` as supported branches upstream (`8.x-1.6` declares `^9.5 || ^10`, `2.3.2` declares `^10.3 || ^11`). Treat both as legacy maintenance lines — start nothing new on them.

**v2 and v3 are functionally identical**. The only difference is machine names. There is no in-place database upgrade from v2 to v3.

**v3 and v4 share the same data model and machine names** — unlike v2→v3, upgrading v3→v4 is a normal module update (no data rename), but it requires Drupal 11.2+ and code/config changes. See [Upgrading v3 to v4](#upgrading-v3-to-v4) below.

## v1 to v2: Key API Changes

**v1→v2 is an in-place update, unlike v2→v3.** Group 2.x ships database update hooks — `group_update_9200()` through `group_update_9211()` — that convert a 1.x site in place: they install the (then required) `flexible_permissions` module, swap the `group_content` / `group_content_type` entity classes and rework the relationship tables, and rewrite the fixed v1 roles into the scope system. The role conversion is mechanical: `{group_type}-anonymous` becomes `scope: outsider` / `global_role: anonymous`, `{group_type}-outsider` becomes `scope: outsider` / `global_role: authenticated`, `{group_type}-member` becomes `scope: insider` / `global_role: authenticated`, and every user-created role becomes `scope: individual`. Synchronized roles that carried no permissions and no admin flag are deleted rather than converted.

One prerequisite: `group_update_last_removed()` at `2.3.2` returns `8023`, so the 1.x site must have run its own updates through `8023` before you require 2.x and run `drush updb`. A site further behind has to catch up on 1.x first. (Verified by reading `group.install` at tag `2.3.2`.)

| v1.x | v2.x / v3.x |
|---|---|
| `GroupContent` entity | `GroupRelationship` entity |
| `GroupContentType` | `GroupRelationshipType` |
| `GroupContentStorage` | `GroupRelationshipStorage` |
| `GroupContentEnablerInterface` | `GroupRelationInterface` |
| `$group->addContent($entity, $plugin_id)` | `$group->addRelationship($entity, $plugin_id)` |
| `$group->getContent($plugin_id)` | `$group->getRelationships($plugin_id)` |
| `$group->getContentByEntityId($entity)` | `$group->getRelationshipsByEntity($entity)` |
| `GroupContent::loadByContentPluginId($id)` | `GroupRelationship::loadByPluginId($id)` |
| `GroupContent::loadByEntity($entity)` | `GroupRelationship::loadByEntity($entity)` |
| Annotation `@GroupContentEnabler` | Attribute `#[GroupRelationType(...)]` |
| Plugin base: `ContentEnablerBase` | Plugin base: `GroupRelationBase` |
| Fixed roles: anonymous, outsider, member | Scope system: outsider/insider/individual |
| DB table: `group_content_field_data` (v2) | DB table: `group_relationship_field_data` (v3) |
| Machine name: `group_content` (v2) | Machine name: `group_relationship` (v3) |

## v2 to v3: Migration Path

There is no automatic in-place upgrade. The official recommended approach is a fresh install + content migration:

**Option A: Recommended (clean migration)**

1. Set up a clean Drupal 11 install with Group 3.x
2. Configure group types, roles, and relationship types in the new install
3. Migrate group, membership, and relationship data using Drupal Migrate API or a custom script
4. Key: use `GroupRelationshipTypeStorage::getRelationshipTypeId($group_type_id, $plugin_id)` to calculate the correct bundle ID in the new system

**Option B: Manual database rename (risky, community-documented)**

1. Rename database table `group_content__group_roles` to `group_relationship__group_roles`
2. In all configuration files: replace `group_content` with `group_relationship` and `group_content_type` with `group_relationship_type`
3. In config file names: replace `group.content_type.` with `group.relationship_type.`
4. Clear all caches
5. Run database updates
6. Validate with Drupal status report

**Do not use `group2to3`.** Older write-ups (including earlier revisions of this guide) offer the `group2to3` contrib module as a third option that automates the Option B steps. As of 2026-08-16 it is marked **Unsupported** and **Obsolete** on drupal.org and has never carried a tagged release — only `3.0.x-dev` and `3.x-dev`, last touched 2024-04-19. Use Option A or Option B.

**32-character ID limit gotcha**: When renaming configuration IDs, the new IDs may exceed Drupal's 32-character config ID limit, especially if your group type IDs are long. Audit all config IDs before migration.

## Custom Code Updates for v2 → v3

Grep for these patterns in your custom code and update:

```
GroupContent          → GroupRelationship
GroupContentType      → GroupRelationshipType
group_content         → group_relationship (in entity type IDs, service calls, routing)
addContent(           → addRelationship(
getContent(           → getRelationships(
getContentByEntityId( → getRelationshipsByEntity(
loadByContentPluginId → loadByPluginId
```

## Handler System Migration (v1 to v2/v3)

v1 plugin methods that were removed from `GroupRelationBase` and moved to handlers:

| Removed from plugin | Now in handler |
|---|---|
| `checkAccess()` | `access_control` handler |
| `getOperations()` | `operation_provider` handler |
| `getPermissions()` | `permission_provider` handler |
| `postInstall()` | `post_install` handler |

## Upgrading v3 to v4

Because v3 and v4 share the same entity types, tables, and machine names, this is a **normal contrib module update** — not a data migration. There is no equivalent of the v2→v3 table rename.

**Prerequisites**

1. Upgrade the site to **Drupal 11.2 or newer** first. Group 4.x will not install on Drupal 11.0/11.1.
2. Confirm you accept an alpha. The newest tag on the 4.0.x branch is `4.0.0-alpha2`, and alpha releases are not covered by Drupal security advisories.
3. Move to 4.x with an explicit stability flag, then run database updates:

   ```bash
   composer require 'drupal/group:^4.0@alpha' --update-with-dependencies
   drush updb
   ```

   A plain `composer update drupal/group` will **not** cross from stable 3.3.5 to an alpha: a default project root ships `minimum-stability: stable`, and only the per-package `@alpha` flag on the require line overrides it. You only need to loosen the root (`composer config minimum-stability dev` plus `composer config prefer-stable true`) if Group arrives transitively through a recipe, distribution, or site template — stability flags are not transitive. See [Pre-Stable Template Deps Require Consumer minimum-stability](../best-practices/camoa/pre-stable-template-consumer-minimum-stability.md).
4. Check your contrib modules first. `group_content_menu`, `group_permissions`, `subgroup`, `group_flex`, and `group_action` all cap at Group 3.x and will block the require — see [Sub-modules](sub-modules.md) and [Group Actions (contrib)](group-actions-contrib.md).
5. You may remove `drupal/flexible_permissions` and `drupal/entity` from `composer.json` *if no other module needs them* — Group 4.x no longer requires either.

**Config changes**

- Remove `creator_wizard` from every `group.type.*` config file.
- Remove `use_creation_wizard` from the `plugin_config` of every `group.relationship_type.*` config file.
- Re-export config after the update so exported YAML matches the 4.x schema.

**Custom code changes**

| 3.x | 4.x |
|---|---|
| `group.membership_loader` service | Removed — use `GroupMembership::loadSingle()` / `::loadByGroup()` / `::loadByUser()` |
| `loadByGroup($group, 'role_id')` / `loadByUser($account, 'role_id')` | `$roles` filter must be an **array**: `loadByGroup($group, ['role_id'])` |
| Custom `flexible_permissions_calculator` services | Re-implement as core `AccessPolicyBase` subclasses tagged `access_policy` |
| Calls to procedural Group hook functions (e.g. `group_entity_access()`) | Gone — Group's hooks are OOP methods in `src/Hook/`; do not call them directly |
| Code relying on an entity being re-saved when added to a group | Entities are no longer re-saved; only cache tags are invalidated |
| Programmatic `Group::save()` expecting an auto-created creator membership | Auto creator membership is form-only — call `addMember()` explicitly |

## Common Mistakes

- Attempting a direct v2-to-v3 schema upgrade without a migration plan. The module maintainer explicitly states this is unsafe and there is no upgrade hook.
- Forgetting to update entity references in Views, Panels, and other config that references `group_content` or `group_content_type` machine names.
- Installing Group 4.x on Drupal 11.0/11.1. Group 4.x requires Drupal **11.2+** for the Access Policy API; upgrade core first.
- Expecting `composer update drupal/group` to reach 4.x. It cannot — 4.0.x is alpha-only and a stable-only root will silently keep you on 3.3.5. Require it with `'drupal/group:^4.0@alpha'`.
- Leaving `creator_wizard` / `use_creation_wizard` keys in config when upgrading to 4.x. The 4.x config schema no longer defines them and config validation will flag them.

## See Also

- [Core Architecture](core-architecture.md)
- [Configuration](configuration.md)
- Reference: https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/group/group-v2v3-guides/upgrading-from-v1-to-v2
