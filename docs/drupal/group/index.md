---
description: Drupal Group module 4.x — group types, roles, permissions, access control, membership, GroupRelationType plugins, and contrib integrations
tracks:
  - project: group
    channel: alpha
    reason: no stable release exists on the 4.0.x branch
    declared: 4.0.0-alpha1
    verified: 2026-08-16
guide-meta:
  concepts:
    - Group module
    - group types
    - group roles
    - group permissions
    - group relationships
    - group membership
    - gnode
    - group access control
    - GroupRelationType plugin
    - group actions
    - VBO group
    - GroupRelationship
    - group_membership
    - entity_access
    - user.group_permissions
    - Access Policy API
  not:
    - Organic Groups
    - OG
    - Domain Access
    - Permissions by Term
    - user roles
    - global permissions
  requires: []
  complements:
    - drupal/services
    - drupal/security
    - drupal/views
    - drupal/blocks
  specializes: ""
  category: drupal
---

# Drupal Group Module

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand how Group 4.x is structured | [Core Architecture](core-architecture.md) | Group 4.x uses the same data model as 3.x (group_relationship, scopes, GroupRelationBase) but drops all contrib dependencies — permission calculation moved to Drupal core's Access Policy API and all hooks became OOP classes. |
| Know which entity types Group provides | [Entity Types](entity-types.md) | Reference this when you need to know the exact entity type IDs, base tables, bundle systems, and key fields of every entity Group provides. |
| Create a custom relation type plugin | [Plugin System](plugin-system.md) | Read this when creating a custom group relation type plugin to allow a new entity type (or bundle) to be added to groups. |
| Understand how permissions work | [Permissions System](permissions-system.md) | Group 4.x calculates permissions via Drupal core's Access Policy API (IndividualGroupRoleAccessPolicy + SynchronizedGroupRoleAccessPolicy); custom calculators must be re-implemented as AccessPolicyBase subclasses tagged access_policy. |
| Control access to grouped content | [Access Control](access-control.md) | Read this when diagnosing access issues, understanding the "explicit forbid" pattern, or writing custom access control for group-related entities. |
| Write YAML config for group types / roles | [Configuration](configuration.md) | Reference this when writing or exporting configuration YAML for group types, group roles, relationship types, or plugin config. |
| Use the Group PHP API programmatically | [PHP API](php-api.md) | Reference this when writing PHP code to create groups, add members, relate content, or query group data programmatically. |
| Build Views with Group data | [Views Integration](views-integration.md) | Reference this when building Views that display groups, group members, or content within groups. |
| Hook into Group with custom code | [Hooks and Events](hooks-and-events.md) | Reference this when looking for extension points to react to Group events without altering core Group logic. |
| Add nodes to groups (gnode sub-module) | [Sub-modules](sub-modules.md) | Reference this when enabling node support, revision support for grouped entities, or looking at how official sub-modules structure their plugins. |
| Automate group operations with VBO or ECA | [Group Actions (contrib)](group-actions-contrib.md) | Automates group operations via VBO/ECA — but drupal/group_action 1.2.2 caps at Group ^3@beta and excludes 4.x entirely. On Group 4.0.x, write the actions yourself against the PHP API instead. |
| Understand how caching works | [Caching](caching.md) | Read this when debugging stale cached output for group-aware content, or when optimizing the performance of group membership and permission lookups. |
| Compare Group vs Domain vs Permissions by Term | [When to Use Group](when-to-use-group.md) | Read this before starting a project to choose the right access control approach. Picking the wrong module early is expensive to change. |
| Migrate from v1/v2 to v3, or v3 to v4 | [Migration from v1/v2](migration-from-v1v2.md) | Read this if you are moving an existing Group site to a newer major version. v2→v3 requires a full data migration (no in-place upgrade, and group2to3 is Unsupported/Obsolete — don't use it); v3→v4 requires an explicit @alpha stability flag since 4.0.x has no stable tag. |
| Avoid common mistakes | [Common Mistakes](common-mistakes.md) | Review this before shipping group-related code to catch frequent errors. |
| Review security considerations | [Security](security.md) | Review this before deploying a Group-based site to production to understand the trust model and potential vulnerabilities. |
