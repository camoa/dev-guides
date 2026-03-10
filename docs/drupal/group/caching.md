---
description: Group caching — cache bins, cache contexts, cache tags, permission hash, and render caching best practices
drupal_version: "11.x"
---

# Caching

## When to Use

> Read this when debugging stale cached output for group-aware content, or when optimizing the performance of group membership and permission lookups.

## Decision

| Cache context | Use when | Notes |
|---|---|---|
| `user.group_permissions` | Content varies by user's group permissions | Most important; SHA-256 hash of full permission matrix |
| `user.is_group_member` | Content varies by whether user is a member of current route group | Binary; simpler than full permissions |
| `route.group` | Content varies by which group is active on the route | Identifies the group in context |

| Cache tag pattern | Invalidated when |
|---|---|
| `group_relationship_list:plugin:{plugin_id}` | Any relationship with this plugin is created/deleted |
| `group_relationship_list:plugin:group_membership:group:{gid}` | A membership in group `{gid}` changes |
| `group_relationship_list:plugin:group_membership:entity:{uid}` | User `{uid}` gains/loses any membership |

## Pattern

```php
// Block or controller that checks group permissions.
$build['content'] = [
  '#markup' => $this->buildGroupContent($group, $account),
  '#cache' => [
    'contexts' => ['user.group_permissions', 'route.group'],
    'tags' => $group->getCacheTags(),
  ],
];

// Content that varies by membership status only.
$build['join_button'] = [
  '#markup' => $this->buildJoinButton($group),
  '#cache' => [
    'contexts' => ['user.is_group_member'],
    'tags' => $group->getCacheTags(),
  ],
];
```

Group provides three cache bins:

| Service ID | Backend | Purpose |
|---|---|---|
| `cache.group_memberships_memory` | Memory (per-request) | Fast in-memory membership cache |
| `cache.group_memberships` | Persistent (default) | Cross-request membership cache |
| `cache.group_memberships_chained` | Chained (memory + persistent) | Used by all membership lookups |

## Common Mistakes

- **Wrong**: Missing `user.group_permissions` context in custom blocks that check `$group->hasPermission()` → **Right**: Without it, all users see the same cached output regardless of their group permissions.
- **Wrong**: Calling `GroupMembership::loadByUser()` in a loop per group → **Right**: Call it once; it loads all memberships for the user and caches them.
- **Wrong**: Not adding `group_relationship_list:plugin:group_membership:entity:{uid}` as a cache tag on membership-conditional pages → **Right**: Without this tag, pages won't be invalidated when a user's membership changes.

## See Also

- [Permissions System](permissions-system.md)
- [Access Control](access-control.md)
- Reference: `web/modules/contrib/group/src/Cache/`
