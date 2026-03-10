---
description: Group PHP API — CRUD, adding members, relationships, querying, services reference, and programmatic plugin installation
drupal_version: "11.x"
---

# PHP API

## When to Use

> Reference this when writing PHP code to create groups, add members, relate content, or query group data programmatically.

## Decision

| Task | Method | Notes |
|---|---|---|
| Create group | `Group::create([...])->save()` | Creator membership only auto-added via UI or when `creator_wizard: FALSE` |
| Add member with role | `$group->addMember($account, ['group_roles' => ['project-editor']])` | Pass roles explicitly for programmatic calls |
| Load membership | `GroupMembership::loadSingle($group, $account)` | Cached via chained cache |
| Add content to group | `$group->addRelationship($node, 'group_node:article')` | Both group and entity must be saved first |
| Load relationships | `$storage->loadByGroup($group, 'group_node:article')` | Use `GroupRelationshipStorageInterface` |
| Load groups for entity | `$storage->loadByEntity($node)` then `$r->getGroup()` | |

## Pattern

```php
use Drupal\group\Entity\Group;
use Drupal\group\Entity\GroupMembership;

// Create a group and add a member with a role.
$group = Group::create(['type' => 'project', 'label' => 'My Project']);
$group->save();
$group->addMember($account, ['group_roles' => ['project-editor']]);

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

## Common Mistakes

- **Wrong**: Calling `$group->addRelationship()` on an unsaved group → **Right**: Both the group and entity must be saved (have IDs) first.
- **Wrong**: Using `group.membership_loader` service → **Right**: Deprecated since 3.2.0. Use `GroupMembership::loadSingle()`, `::loadByGroup()`, or `::loadByUser()`.
- **Wrong**: Calling `$group->addMember()` expecting creator roles → **Right**: Creator roles are only applied in the `postSave` hook via UI. Pass roles explicitly when programmatic.
- **Wrong**: Using `accessCheck(TRUE)` in background/admin code → **Right**: Use `accessCheck(FALSE)`; Group's query access is expensive and context-dependent.

## See Also

- [Entity Types](entity-types.md)
- [Plugin System](plugin-system.md)
- Reference: `web/modules/contrib/group/src/Entity/Group.php`
