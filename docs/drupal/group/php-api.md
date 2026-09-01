---
description: Group PHP API — CRUD, adding members, relationships, querying, services reference, and programmatic plugin installation
tldr: "Reference this when writing PHP code to create groups, add members, relate content, or query group data programmatically. In 4.x: group.membership_loader is removed, $roles filter must be an array, and creator membership is form-only."
drupal_version: "11.x"
---

# PHP API

## When to Use

> Reference this when writing PHP code to create groups, add members, relate content, or query group data programmatically.

## Decision

| Task | Method | Notes |
|---|---|---|
| Create group | `Group::create([...])->save()` | Creator membership only auto-added via form submissions in 4.x |
| Add member with role | `$group->addMember($account, ['group_roles' => ['project-editor']])` | Pass roles explicitly for programmatic calls |
| Load membership | `GroupMembership::loadSingle($group, $account)` | Cached via chained cache |
| Add content to group | `$group->addRelationship($node, 'group_node:article')` | Both group and entity must be saved first |
| Load relationships | `$storage->loadByGroup($group, 'group_node:article')` | Use `GroupRelationshipStorageInterface` |
| Load groups for entity | `$storage->loadByEntity($node)` then `$r->getGroup()` | |
| Load members with role filter | `GroupMembership::loadByGroup($group, ['project-editor'])` | 4.x: filter must be an array |

## Pattern

```php
use Drupal\group\Entity\Group;
use Drupal\group\Entity\GroupMembership;

// Create a group. In 4.x, creator_membership is form-only —
// call addMember() explicitly when creating groups programmatically.
$group = Group::create(['type' => 'project', 'label' => 'My Project']);
$group->save();
$group->addMember($account, ['group_roles' => ['project-manager']]);

// Add content to the group.
$relationship = $group->addRelationship($node, 'group_node:article');

// Query all relationships in a group for a specific plugin.
$storage = \Drupal::entityTypeManager()->getStorage('group_relationship');
$articles = $storage->loadByGroup($group, 'group_node:article');

// Load all groups a node belongs to.
$relationships = $storage->loadByEntity($node);
$groups = array_map(fn($r) => $r->getGroup(), $relationships);
```

Injecting services:

```php
use Drupal\group\Access\GroupPermissionCheckerInterface;

class MyService {
  public function __construct(
    protected GroupPermissionCheckerInterface $permissionChecker,
  ) {}
}

# services.yml
mymodule.my_service:
  arguments: ['@group_permission.checker']
```

## Services Reference

| Service ID | Type | Purpose |
|---|---|---|
| `group_relation_type.manager` | `GroupRelationTypeManagerInterface` | Plugin manager for GroupRelationType plugins |
| `access_policy_processor` (core) | `AccessPolicyProcessorInterface` | Core service that processes Group's `access_policy` services into calculated permissions |
| `group_permission.calculator` | `GroupPermissionCalculatorInterface` | Calculate full permissions for an account |
| `group_permission.checker` | `GroupPermissionCheckerInterface` | Check a specific permission for an account in a group |
| `group.permissions` | `GroupPermissionHandler` | Enumerate all available group permissions |
| `group_permission.hash_generator` | `GroupPermissionsHashGeneratorInterface` | Generate permission hash for cache vary |
| `group.group_route_context` | context provider | Provides `group` context from the current route |

## Common Mistakes

- **Wrong**: Calling `$group->addRelationship()` on an unsaved group → **Right**: Both the group and entity must be saved (have IDs) first.
- **Wrong**: Using the `group.membership_loader` service → **Right**: Removed in 4.0.0 (deprecated since 3.2.0). Use `GroupMembership::loadSingle()`, `::loadByGroup()`, or `::loadByUser()`.
- **Wrong**: Calling `Group::save()` programmatically and expecting the creator membership to be created automatically → **Right**: In 4.x, `creator_membership` is applied only when the group is created through a form. Call `$group->addMember()` explicitly in programmatic code.
- **Wrong**: Passing a string to the `$roles` filter: `loadByGroup($group, 'project-editor')` → **Right**: In 4.x the filter must be an array: `loadByGroup($group, ['project-editor'])`.
- **Wrong**: Expecting `hook_ENTITY_TYPE_update()` to fire on the entity when adding it to a group → **Right**: In 4.x, adding an entity to a group no longer re-saves the entity. Only its cache tags are invalidated.
- **Wrong**: Using `accessCheck(TRUE)` in background/admin code → **Right**: Use `accessCheck(FALSE)`; Group's query access is expensive and context-dependent.

## See Also

- [Entity Types](entity-types.md)
- [Plugin System](plugin-system.md)
- Reference: `web/modules/contrib/group/src/Entity/Group.php`
