---
description: All entity types provided by Group 3.x — IDs, base tables, key fields, shared bundle classes, and membership loading
tldr: "Reference this when you need to know the exact entity type IDs, base tables, bundle systems, and key fields of every entity Group provides."
drupal_version: "11.x"
---

# Entity Types

## When to Use

> Reference this when you need to know the exact entity type IDs, base tables, bundle systems, and key fields of every entity Group provides.

## Decision

| Entity Type ID | Class | Type | Purpose |
|---|---|---|---|
| `group` | `Drupal\group\Entity\Group` | Content | The group container itself |
| `group_type` | `Drupal\group\Entity\GroupType` | Config (bundle for `group`) | Defines group types |
| `group_relationship` | `Drupal\group\Entity\GroupRelationship` | Content | Relates any entity to a group |
| `group_relationship_type` | `Drupal\group\Entity\GroupRelationshipType` | Config (bundle for `group_relationship`) | Internal — do not expose to users |
| `group_role` | `Drupal\group\Entity\GroupRole` | Config | Per-group-type role with permissions |
| `group_config_wrapper` | `Drupal\group\Entity\ConfigWrapper` | Content | Wraps config entities for group relations |

**GroupRelationship key fields:** `id`, `uuid`, `type` (bundle), `gid` (group reference), `entity_id` (related entity reference), `plugin_id` (denormalized), `group_type` (denormalized), `uid`, `created`, `changed`

**GroupRole ID format:** `{group_type_id}-{role_machine_name}` — e.g., `project-editor`

**GroupRole config file pattern:** `group.role.{group_type_id}-{role_id}.yml`

## Pattern

```php
use Drupal\group\Entity\GroupMembership;

// Load a single membership (cached via chained cache backend).
$membership = GroupMembership::loadSingle($group, $account);
if ($membership) {
  $roles = $membership->getRoles(); // includes synchronized roles
}

// Load all memberships for a user.
$memberships = GroupMembership::loadByUser($account);

// Load all memberships for a group.
$members = GroupMembership::loadByGroup($group);

// Load filtered by role.
$editors = GroupMembership::loadByGroup($group, 'project-editor');
```

## Common Mistakes

- **Wrong**: Calling `GroupRelationshipType::label()` and displaying it to users → **Right**: It is labeled "INTERNAL USE ONLY". Use the plugin's label instead.
- **Wrong**: Querying `group_relationship` with `accessCheck(TRUE)` in non-user-context code → **Right**: Use `accessCheck(FALSE)` in backend operations and apply manual authorization checks. Full permission calculation is expensive.

## See Also

- [PHP API](php-api.md)
- [Permissions System](permissions-system.md)
- Reference: `web/modules/contrib/group/src/Entity/GroupMembership.php`
