---
description: Migrating Group versions — v1/v2 API changes, v2→v3 migration options, and v3→v4 upgrade (normal module update)
tldr: "Read this if you are moving an existing Group site to a newer major version. v2→v3 requires a full data migration (no in-place upgrade, and group2to3 is Unsupported/Obsolete — don't use it); v3→v4 requires an explicit @alpha stability flag since 4.0.x has no stable tag."
drupal_version: "11.x"
---

# Migration from v1/v2

## When to Use

> Read this if you are moving an existing Group site to a newer major version — v1→v2, v2→v3, or v3→v4.

## Decision

| From | To | Path |
|---|---|---|
| Group 1.x | Group 2.x | Upgrade path exists (hooks and DB updates) |
| Group 2.x | Group 3.x | No in-place upgrade — fresh install + migration required (do **not** use `group2to3`) |
| Group 3.x | Group 4.x | Normal module update on Drupal 11.2+ — same data model, but requires an explicit `@alpha` flag |
| Group 2.x | Group 2.x latest | Safe to update in place |

| Branch | Core compatibility | Status |
|---|---|---|
| `8.x-1.x` / `2.3.x` | `^9.5\|\|^10` / `^10.3\|\|^11` | Legacy maintenance lines — start nothing new here |
| `3.3.x` | `^10.3 \|\| ^11` | **Latest stable — 3.3.5** (2025-05-06). Only branch the contrib ecosystem supports. |
| `4.0.x` | `^11.2` | Only tag is `4.0.0-alpha1` (2026-04-24) — no stable; requires `@alpha` install; not covered by Drupal security advisories |

**v2 and v3 are functionally identical** — only machine names differ. There is no in-place database upgrade from v2 to v3.

**v3 and v4 share the same entity types, tables, and machine names** — unlike v2→v3, this is a normal contrib module update, not a data migration. It does require Drupal 11.2+ and config/code changes.

## Pattern

### v2 → v3: Migration Options

**Option A: Recommended (clean migration)**
1. Set up a clean Drupal 11 install with Group 3.x
2. Configure group types, roles, and relationship types
3. Migrate data using Drupal Migrate API

**Option B: Manual database rename (community-documented, risky)**
1. Rename `group_content__group_roles` → `group_relationship__group_roles`
2. Replace `group_content` → `group_relationship` in all config files
3. Replace `group.content_type.` → `group.relationship_type.` in config file names
4. Clear all caches, run database updates

**Do not use `group2to3`.** As of 2026-08-16 it is marked **Unsupported** and **Obsolete** on drupal.org and has never carried a tagged release — only `3.0.x-dev` and `3.x-dev`, last touched 2024-04-19. Use Option A or Option B.

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
2. Accept an alpha — the 4.0.x branch has exactly one tag, `4.0.0-alpha1`, and alpha releases are not covered by Drupal security advisories.
3. Require it with an explicit stability flag, then run database updates:
   ```bash
   composer require 'drupal/group:^4.0@alpha' --update-with-dependencies
   drush updb
   ```
   A plain `composer update drupal/group` will **not** cross from stable 3.3.5 to an alpha — a default project root ships `minimum-stability: stable`, and only the per-package `@alpha` flag on the require line overrides it. Only loosen the root (`composer config minimum-stability dev` + `composer config prefer-stable true`) if Group arrives *transitively* through a recipe, distribution, or site template — stability flags are not transitive.
4. Check contrib first — `group_content_menu`, `group_permissions`, `subgroup`, `group_flex`, and `group_action` all cap at Group 3.x and will block the require. See [Sub-modules](sub-modules.md) and [Group Actions (contrib)](group-actions-contrib.md).
5. Remove `drupal/flexible_permissions` and `drupal/entity` from `composer.json` if no other module needs them.

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

## Handler System Migration (v1 to v2/v3)

v1 plugin methods that were removed from `GroupRelationBase` and moved to handlers:

| Removed from plugin | Now in handler |
|---|---|
| `checkAccess()` | `access_control` handler |
| `getOperations()` | `operation_provider` handler |
| `getPermissions()` | `permission_provider` handler |
| `postInstall()` | `post_install` handler |

## Common Mistakes

- **Wrong**: Attempting a direct v2-to-v3 in-place upgrade → **Right**: The module maintainer explicitly states this is unsafe. There is no upgrade hook.
- **Wrong**: Forgetting to update Views and Panels config that reference `group_content` machine names → **Right**: Audit all Views, Panels, and contrib config for old machine names before migrating.
- **Wrong**: Installing Group 4.x on Drupal 11.0/11.1 → **Right**: Group 4.x requires Drupal 11.2+ for the Access Policy API. Upgrade core first.
- **Wrong**: Leaving `creator_wizard` / `use_creation_wizard` keys in config when upgrading to 4.x → **Right**: The 4.x config schema no longer defines them and config validation will flag them.
- **Wrong**: Not checking the 32-character ID limit when migrating v2→v3 → **Right**: Renamed config IDs may exceed Drupal's 32-character limit. Audit all config IDs before migration.
- **Wrong**: Reaching for `group2to3` to automate a v2→v3 upgrade → **Right**: It's Unsupported and Obsolete on drupal.org with no tagged release. Use Option A or Option B instead.
- **Wrong**: Expecting `composer update drupal/group` to reach 4.x → **Right**: It cannot — 4.0.x is alpha-only and a stable-only root will silently keep you on 3.3.5. Require it with `'drupal/group:^4.0@alpha'`.

## See Also

- [Core Architecture](core-architecture.md)
- [Configuration](configuration.md)
- Reference: https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/group/group-v2v3-guides/upgrading-from-v1-to-v2
