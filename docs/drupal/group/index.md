---
description: Drupal Group module 3.x — group types, roles, permissions, access control, membership, GroupRelationType plugins, and contrib integrations
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
| Understand how Group 3.x is structured | [Core Architecture](core-architecture.md) | Read this when you need to understand Group 3.x's data model and how it differs from earlier versions before writing any code. |
| Know which entity types Group provides | [Entity Types](entity-types.md) | Reference this when you need to know the exact entity type IDs, base tables, bundle systems, and key fields of every entity Group provides. |
| Create a custom relation type plugin | [Plugin System](plugin-system.md) | Read this when creating a custom group relation type plugin to allow a new entity type (or bundle) to be added to groups. |
| Understand how permissions work | [Permissions System](permissions-system.md) | Read this when you need to define custom group permissions, understand the scope system, or programmatically grant/check permissions. |
| Control access to grouped content | [Access Control](access-control.md) | Read this when diagnosing access issues, understanding the "explicit forbid" pattern, or writing custom access control for group-related entities. |
| Write YAML config for group types / roles | [Configuration](configuration.md) | Reference this when writing or exporting configuration YAML for group types, group roles, relationship types, or plugin config. |
| Use the Group PHP API programmatically | [PHP API](php-api.md) | Reference this when writing PHP code to create groups, add members, relate content, or query group data programmatically. |
| Build Views with Group data | [Views Integration](views-integration.md) | Reference this when building Views that display groups, group members, or content within groups. |
| Hook into Group with custom code | [Hooks and Events](hooks-and-events.md) | Reference this when looking for extension points to react to Group events without altering core Group logic. |
| Add nodes to groups (gnode sub-module) | [Sub-modules](sub-modules.md) | Reference this when enabling node support, revision support for grouped entities, or looking at how official sub-modules structure their plugins. |
| Automate group operations with VBO or ECA | [Group Actions (contrib)](group-actions-contrib.md) | Read this when you need to automate group operations — adding/removing members or content — via Views Bulk Operations (VBO), ECA workflows, or any Drupal action-based system. |
| Understand how caching works | [Caching](caching.md) | Read this when debugging stale cached output for group-aware content, or when optimizing the performance of group membership and permission lookups. |
| Compare Group vs Domain vs Permissions by Term | [When to Use Group](when-to-use-group.md) | Read this before starting a project to choose the right access control approach. Picking the wrong module early is expensive to change. |
| Migrate from v1/v2 to v3 | [Migration from v1/v2](migration-from-v1v2.md) | Read this if you are moving an existing Group 1.x or 2.x site to Group 3.x. |
| Avoid common mistakes | [Common Mistakes](common-mistakes.md) | Review this before shipping group-related code to catch frequent errors. |
| Review security considerations | [Security](security.md) | Review this before deploying a Group-based site to production to understand the trust model and potential vulnerabilities. |
