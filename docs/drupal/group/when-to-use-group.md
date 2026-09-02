---
description: When to use Group vs Domain Access vs Permissions by Term — decision table and performance considerations
tldr: "Read this before starting a project to choose the right access control approach. Picking the wrong module early is expensive to change."
drupal_version: "11.x"
---

# When to Use Group

## When to Use

> Read this before starting a project to choose the right access control approach. Picking the wrong module early is expensive to change.

## Decision

| Requirement | Group | Domain Access | Permissions by Term | Organic Groups |
|---|---|---|---|---|
| Content organized into discrete groups with members | **Yes** | No | No | Yes (less maintained) |
| Same content in multiple groups | **Yes** | No | Yes | Limited |
| Group-level roles and permissions | **Yes** | Limited | No | Partial |
| Sub-site / multi-domain model | No | **Yes** | No | No |
| Taxonomy-based content restriction | No | No | **Yes** | No |
| Config entities in groups | **Yes** | No | No | No |
| Complex nested group hierarchy | Via `subgroup` contrib (Group 3.x only) | No | No | No |
| Simple "hide content from role" | Overkill | Overkill | **Yes** | Overkill |
| Groups with their own menus | Via `group_content_menu` (Group 3.x only) | No | No | No |
| Runs on Drupal 11.4 | **Yes** — 3.3.5 stable, or 4.0.0-alpha2 (alpha-only) | Not checked | Not checked | Not checked |

The two rows marked *Group 3.x only* are the practical constraint on choosing 4.0.x: see [Sub-modules](sub-modules.md) for the full contrib compatibility picture. The maintenance status of Domain Access, Permissions by Term, and Organic Groups was not re-verified in the August 2026 sweep.

## Use Group When

- You have identifiable groups of users who need to collaborate on a shared set of content
- Group membership grants different capabilities (editors vs readers vs managers)
- The same node or media item may belong to multiple groups
- You want granular per-group permissions that override global Drupal permissions
- You need programmatic creation and management of groups and memberships

## Use Domain Access When

- You are running multiple sub-sites from one Drupal install with domain-specific content
- The primary requirement is content isolation by domain/subdomain, not user groups
- You need domain-specific admin roles

## Use Permissions by Term When

- Access control is based purely on how content is tagged (taxonomy terms)
- You do not need group management or membership
- The requirement is "users in role X can only see content tagged with term Y"
- You want a lightweight solution with minimal architecture

## Use Neither When

- The requirement is "only the author can edit their content" — use standard Drupal node access (`node_access` and author-based permissions)
- The requirement is simple role-based content access — use Drupal's core permissions system

## Performance Considerations

Group adds SQL JOINs and sub-queries to entity queries for all entity types with active plugins using `entity_access: TRUE`. On large sites:

- Minimize the number of `entity_access: TRUE` plugins — only enable this for entity types where group-level access control is actually needed
- Use the `user.group_permissions` cache context aggressively — the hash-based approach makes this efficient
- Consider Varnish/CDN with group-aware cache invalidation for anonymous users
- Large groups (thousands of members) may benefit from limiting use of insider roles (which require membership ID tracking in the hash)

## Common Mistakes

- Installing gnode on a site that does not need group-scoped node access. Once gnode is active with `entity_access: TRUE` plugins installed, ALL node access for grouped nodes goes through Group. If the permission configuration is incomplete, users may lose access to nodes they should be able to see.
- Using Group for a simple "hide some content from some users" scenario. Permissions by Term or simple node access grants are vastly simpler for this case.

## See Also

- [Access Control](access-control.md)
- [Sub-modules](sub-modules.md)
- Reference: https://www.drupal.org/project/group
