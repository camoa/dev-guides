---
description: Migrating Group versions — v1/v2 API changes, v2→v3 migration options, and v3→v4 upgrade (normal module update)
tldr: "Read this if you are moving an existing Group site to a newer major version. v2→v3 requires a full data migration (no in-place upgrade); v3→v4 is a normal module update on Drupal 11.2+ but requires removing creator_wizard config and re-implementing flexible_permissions calculators as core access policies."
drupal_version: "11.x"
---

# Migration from v1/v2

## When to Use

> Read this if you are moving an existing Group site to a newer major version — v1→v2, v2→v3, or v3→v4.

## Decision

| From | To | Path |
|---|---|---|
| Group 1.x | Group 2.x | Upgrade path exists (hooks and DB updates) |
| Group 2.x | Group 3.x | No in-place upgrade — fresh install + migration required |
| Group 3.x | Group 4.x | Normal module update on Drupal 11.2+ — same data model |
| Group 2.x | Group 2.x latest | Safe to update in place |

**v2 and v3 are functionally identical** — only machine names differ. There is no in-place database upgrade from v2 to v3.

**v3 and v4 share the same entity types, tables, and machine names** — unlike v2→v3, this is a normal contrib module update, not a data migration. It does require Drupal 11.2+ and config/code changes.

## Pattern

### v2 → v3: Migration Options

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

Custom code search/replace for v1/v2 → v3/v4:

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

### v3 → v4: Upgrade Steps

**Prerequisites:**
1. Upgrade the site to **Drupal 11.2 or newer** first.
2. `composer update drupal/group` to a 4.x release, then `drush updb`.
3. Remove `drupal/flexible_permissions` and `drupal/entity` from `composer.json` if no other module needs them.

**Config changes:**
- Remove `creator_wizard` from every `group.type.*` config file.
- Remove `use_creation_wizard` from the `plugin_config` of every `group.relationship_type.*` config file.
- Re-export config after the update.

**Custom code changes for v3 → v4:**

| 3.x | 4.x |
|---|---|
| `group.membership_loader` service | Removed — use `GroupMembership::loadSingle()` / `::loadByGroup()` / `::loadByUser()` |
| `loadByGroup($group, 'role_id')` | `$roles` filter must be an array: `loadByGroup($group, ['role_id'])` |
| Custom `flexible_permissions_calculator` services | Re-implement as `AccessPolicyBase` subclasses tagged `access_policy` |
| Calls to procedural Group hook functions (e.g. `group_entity_access()`) | Gone — hooks are OOP in `src/Hook/`; do not call them directly |
| Code relying on entity re-save when added to a group | Entities are no longer re-saved; only cache tags are invalidated |
| Programmatic `Group::save()` expecting auto-created creator membership | Auto creator membership is form-only — call `addMember()` explicitly |

## Common Mistakes

- **Wrong**: Attempting a direct v2-to-v3 in-place upgrade → **Right**: The module maintainer explicitly states this is unsafe. There is no upgrade hook.
- **Wrong**: Forgetting to update Views and Panels config that reference `group_content` machine names → **Right**: Audit all Views, Panels, and contrib config for old machine names before migrating.
- **Wrong**: Installing Group 4.x on Drupal 10 or Drupal 11.0/11.1 → **Right**: Group 4.x requires Drupal 11.2+. Upgrade core first.
- **Wrong**: Leaving `creator_wizard` / `use_creation_wizard` keys in config when upgrading to 4.x → **Right**: The 4.x config schema no longer defines them and config validation will flag them.
- **Wrong**: Not checking the 32-character ID limit when migrating v2→v3 → **Right**: Renamed config IDs may exceed Drupal's 32-character limit. Audit all config IDs before migration.

## See Also

- [Core Architecture](core-architecture.md)
- [Configuration](configuration.md)
- Reference: https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/group/group-v2v3-guides/upgrading-from-v1-to-v2
