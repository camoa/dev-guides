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
| Runs on Drupal 11.4 | **Yes** — 3.3.5 stable, or 4.0.0-alpha1 (alpha-only) | Not checked | Not checked | Not checked |

The two rows marked *Group 3.x only* are the practical constraint on choosing 4.0.x — see [Sub-modules](sub-modules.md) for the full contrib compatibility picture. The maintenance status of Domain Access, Permissions by Term, and Organic Groups was not re-verified in the August 2026 sweep.

## Pattern

Use Group when:
- Identifiable groups of users who need to collaborate on a shared set of content
- Group membership grants different capabilities (editors vs readers vs managers)
- The same node or media item may belong to multiple groups
- Granular per-group permissions that override global Drupal permissions
- Programmatic creation and management of groups and memberships

Use Domain Access when:
- Multiple sub-sites from one Drupal install with domain-specific content
- Content isolation by domain/subdomain, not user groups

Use Permissions by Term when:
- Access control based purely on taxonomy tags
- Lightweight solution with minimal architecture
- No group management or membership needed

Use neither when:
- "Only the author can edit their content" — use standard node access
- Simple role-based content access — use Drupal's core permissions system

Performance note: Group adds SQL JOINs to entity queries for all entity types with `entity_access: TRUE` plugins. On large sites, minimize the number of `entity_access: TRUE` plugins.

## Common Mistakes

- **Wrong**: Installing gnode without understanding the access implications → **Right**: Once `entity_access: TRUE` plugins are installed, ALL node access for grouped nodes goes through Group. Incomplete config can lock users out.
- **Wrong**: Using Group for a "hide content from some users" scenario → **Right**: Permissions by Term or simple node access grants are vastly simpler.

## See Also

- [Access Control](access-control.md)
- [Sub-modules](sub-modules.md)
- Reference: https://www.drupal.org/project/group
