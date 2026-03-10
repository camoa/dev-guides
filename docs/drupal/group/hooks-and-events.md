---
description: Group hooks and events — available hooks, event subscribers, reacting to relationship CRUD, and extending permissions
drupal_version: "11.x"
---

# Hooks and Events

## When to Use

> Reference this when looking for extension points to react to Group events without altering core Group logic.

## Decision

| Need | Use | Why |
|---|---|---|
| Alter group operations block | `hook_group_operations_alter()` | Only Group-specific hook |
| React to relationship create/delete | `hook_ENTITY_TYPE_insert/delete` on `group_relationship` | No dedicated Group event for relationship CRUD |
| Dynamic permissions | `permission_callbacks` in `.group.permissions.yml` | Called at permission cache build time |
| Alter routes | Event subscriber on `RoutingEvents::ALTER` | Standard Symfony routing |

## Pattern

```php
// React to an article being added to a group.
function mymodule_group_relationship_insert(GroupRelationshipInterface $relationship) {
  if ($relationship->getPluginId() === 'group_node:article') {
    $group = $relationship->getGroup();
    $node = $relationship->getEntity();
    // custom logic...
  }
}

// Alter group operations block.
function mymodule_group_operations_alter(array &$operations, GroupInterface $group) {
  if ($group->bundle() === 'company') {
    unset($operations['group-leave']);
  }
}

// Dynamic permissions callback.
class MyModuleGroupPermissions {
  public function permissions(): array {
    $permissions = [];
    foreach (MyEntityType::loadMultiple() as $id => $type) {
      $permissions["manage $id content"] = [
        'title' => t('Manage @type content', ['@type' => $type->label()]),
        'allowed for' => ['member'],
      ];
    }
    return $permissions;
  }
}
```

Registered event subscribers by Group core:

| Service ID | Listens to | Purpose |
|---|---|---|
| `group.anonymous_user_response_subscriber` | `KernelEvents::RESPONSE` | Adds permission cache tags for anonymous users |
| `group.config_subscriber` | `ConfigEvents::SAVE` | Clears plugin caches on group type config changes |

## Common Mistakes

- **Wrong**: Listening to Group-specific Symfony events for relationship changes → **Right**: Group does not dispatch custom Symfony events for relationship changes. Use entity hooks instead.
- **Wrong**: Not reacting before deletion → **Right**: If you need pre-deletion logic, implement `hook_ENTITY_TYPE_predelete` on the entity type being removed from the group (not on `group_relationship`).

## See Also

- [Plugin System](plugin-system.md)
- [PHP API](php-api.md)
- Reference: `web/modules/contrib/group/group.api.php`
