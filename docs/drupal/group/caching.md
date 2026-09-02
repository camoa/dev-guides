---
description: Group caching — cache bins, cache contexts, cache tags, permission hash, and render caching best practices
tldr: "Read this when debugging stale cached output for group-aware content, or when optimizing the performance of group membership and permission lookups."
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

## Cache Bins

Group provides three cache bins:

| Service ID | Backend | Purpose |
|---|---|---|
| `cache.group_memberships_memory` | Memory (per-request) | Fast in-memory membership cache |
| `cache.group_memberships` | Persistent (default) | Cross-request membership cache |
| `cache.group_memberships_chained` | Chained (memory + persistent) | Used by all membership lookups |

## Cache Contexts

| Context | Class | Varies on |
|---|---|---|
| `user.group_permissions` | `GroupPermissionsCacheContext` | User's full calculated group permissions (hash) |
| `user.is_group_member` | `IsGroupMemberCacheContext` | Whether the user is a member of the current route group |
| `route.group` | `RouteGroupCacheContext` | Which group is in the current route context |

`user.group_permissions` is the most important. It generates a SHA-256 hash of the user's complete permission matrix across all scopes and groups. This hash is stored in a static cache keyed by user ID.

For anonymous users: because reverse proxies cache full responses without calculating context values, the `AnonymousUserResponseSubscriber` adds the permission cache tags to responses that vary by `user.group_permissions`. This ensures proxy caches are invalidated when anonymous group permissions change.

## Cache Tags

Group uses cache tags to invalidate membership and access caches:

| Tag pattern | Invalidated when |
|---|---|
| `group_relationship_list:plugin:{plugin_id}` | Any relationship with this plugin is created/deleted |
| `group_relationship_list:plugin:group_membership:group:{gid}` | A membership in group `{gid}` changes |
| `group_relationship_list:plugin:group_membership:entity:{uid}` | User `{uid}` gains/loses any membership |

## Permission Hash Optimization

The hash generator (`GroupPermissionsHashGenerator`) must track membership IDs for synchronized (outsider/insider) roles. Without this, two users with the same insider permissions but membership in different groups could share a cache entry and see each other's group lists.

The trade-off: users with synchronized roles produce per-membership-set hashes with lower cache hit rates. If you have a site with many users who all have the same insider permissions, consider whether insider roles are actually needed vs. just using individual roles.

## Render Caching Best Practices

```php
// In a block or controller that checks group permissions:
$build['content'] = [
  '#markup' => $this->buildGroupContent($group, $account),
  '#cache' => [
    'contexts' => ['user.group_permissions', 'route.group'],
    'tags' => $group->getCacheTags(),
  ],
];
```

```php
// When displaying content that varies by membership status:
$build['join_button'] = [
  '#markup' => $this->buildJoinButton($group),
  '#cache' => [
    'contexts' => ['user.is_group_member'],
    'tags' => $group->getCacheTags(),
  ],
];
```

## Common Mistakes

- Missing `user.group_permissions` context in custom blocks that check `$group->hasPermission()`. Without it, all users see the same cached output.
- Calling `GroupMembership::loadByUser()` in a loop per group in a list. The static method loads all memberships for the user at once and caches them. Call it once and index the result yourself.
- Not adding `group_relationship_list:plugin:group_membership:entity:{uid}` as a cache tag on custom pages that display membership-conditional content. When a user's membership changes, these pages will not be invalidated.

## See Also

- [Permissions System](permissions-system.md)
- [Access Control](access-control.md)
- Reference: `web/modules/contrib/group/src/Cache/`
