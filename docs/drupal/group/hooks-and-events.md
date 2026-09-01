---
description: Group hooks and events — OOP hooks in 4.x, available hooks, event subscribers, reacting to relationship CRUD, and extending permissions
tldr: "Reference this when looking for extension points to react to Group events without altering core Group logic. In 4.x Group has no .module file — all hooks are OOP methods in src/Hook/; do not call group_entity_access() or other procedural Group functions."
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
| Custom permission source | `AccessPolicyBase` subclass tagged `access_policy` | 4.x replaces `flexible_permissions_calculator` |

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

**4.x note:** Group 4.x has no `.module` file. All hook implementations are OOP methods in `src/Hook/` (`CoreHooks`, `EntityHooks`, `FieldHooks`, `FormHooks`, `QueryHooks`, etc.), each tagged with `#[Hook('hook_name')]`. Your own module can still use either procedural `.module` functions or OOP hook classes — the change only affects Group's own hooks.

Registered event subscribers by Group core:

| Service ID | Listens to | Purpose |
|---|---|---|
| `group.anonymous_user_response_subscriber` | `KernelEvents::RESPONSE` | Adds permission cache tags for anonymous users |
| `group.config_subscriber` | `ConfigEvents::SAVE` | Clears plugin caches on group type config changes |

## Standard Drupal Hooks Used by Group

Group also uses the following standard hooks for integration:

| Hook | Purpose |
|---|---|
| `hook_entity_bundle_info()` | Registers bundles for `group_config_wrapper` for installed config entity plugins |
| `hook_entity_access()` | Injects Group's access checks via `EntityHooks::entityAccess()` |
| `hook_entity_delete()` | Auto-deletes relationships and config wrappers when related entities are deleted |
| `hook_entity_field_access()` | Hides the `group_roles` field for non-admins on membership forms |
| `hook_form_alter()` | Enhances the entity-create form used when adding a brand-new entity to a group, via the `group.create_form_enhancer` service (`CreateFormEnhancer`). The 2-step wizard it altered in 3.x is gone. |
| `hook_modules_installed()` | Installs enforced plugins on new group types |
| `hook_query_entity_query_alter()` | Adds access conditions to entity queries |
| `hook_rebuild()` | Runs `installEnforced()` after a rebuild |
| `hook_user_cancel()` | Reassigns or deletes groups when a user is cancelled |
| `hook_user_delete()` | Deletes groups owned by a deleted user |
| `hook_ENTITY_TYPE_update(user)` | Resets the group role cache when a user's global roles change |
| `hook_views_query_alter()` | Adds access conditions to Views SQL queries |

## Event Subscribers

Group registers the following event subscribers:

| Service ID | Class | Listens to | Purpose |
|---|---|---|---|
| `group.anonymous_user_response_subscriber` | `AnonymousUserResponseSubscriber` | `KernelEvents::RESPONSE` (priority 5) | Adds permission cache tags to responses for anonymous users when `user.group_permissions` context is in use |
| `group.admin_path.route_subscriber` | `GroupAdminRouteSubscriber` | `RoutingEvents::ALTER` | Optionally moves group admin routes to use the admin theme |
| `group.latest_revision.route_subscriber` | `GroupLatestRevisionRouteSubscriber` | `RoutingEvents::ALTER` | Adds latest revision routes for groups |
| `group.config_subscriber` | `ConfigSubscriber` | `ConfigEvents::SAVE` | Clears plugin caches when group type config changes |

Group 4.x has no revision route subscriber of its own — plain revision routes come from Drupal core's revision UI, which is why `drupal/entity` was dropped as a dependency. There is no `group.revision.route_subscriber` service and no `GroupRevisionRouteSubscriber` class at tag `4.0.0-alpha2`; do not write code that expects one.

## Common Mistakes

- **Wrong**: Listening to Group-specific Symfony events for relationship changes → **Right**: Group does not dispatch custom Symfony events for relationship changes. Use entity hooks instead.
- **Wrong**: Not reacting before deletion → **Right**: If you need pre-deletion logic, implement `hook_ENTITY_TYPE_predelete` on the entity type being removed from the group (not on `group_relationship`).
- **Wrong**: Calling `group_entity_access()` directly in 4.x → **Right**: The procedural function no longer exists in 4.x. The equivalent is `EntityHooks::entityAccess()` inside Group's codebase, which you should not call directly.

## See Also

- [Plugin System](plugin-system.md)
- [PHP API](php-api.md)
- Reference: `web/modules/contrib/group/group.api.php`
