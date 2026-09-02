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

## Group CRUD

```php
use Drupal\group\Entity\Group;

// Create a group.
$group = Group::create([
  'type' => 'project',
  'label' => 'My Project',
  'uid' => \Drupal::currentUser()->id(),
]);
$group->save();
// 4.x: the creator_membership config on the group type auto-adds the creator as a
// member ONLY when the group is created through a form. A purely programmatic
// Group::save() does NOT create the creator membership — add it explicitly with
// addMember() if you need it.
```

## Adding Members

```php
use Drupal\user\Entity\User;

$account = User::load($uid);

// Add a member with a specific role.
$group->addMember($account, [
  'group_roles' => ['project-editor'],
]);

// Add a member with no explicit roles (gets insider permissions only).
$group->addMember($account);

// Remove a member.
$group->removeMember($account);

// Check membership.
$membership = $group->getMember($account); // Returns GroupMembership or FALSE.

// Load all members of a group.
$members = $group->getMembers();

// Load members with a specific role.
// 4.x: the role filter must be an array.
$editors = $group->getMembers(['project-editor']);
```

## Adding Content / Relationships

```php
$node = Node::load($nid);

// Add an existing node to the group.
// Returns the GroupRelationship entity.
$relationship = $group->addRelationship($node, 'group_node:article');

// Add with extra fields on the relationship.
$relationship = $group->addRelationship($node, 'group_node:article', [
  'field_relationship_note' => 'Important article',
]);

// Remove: delete the relationship entity.
$relationships = $group->getRelationshipsByEntity($node, 'group_node:article');
foreach ($relationships as $rel) {
  $rel->delete();
}
```

> **3.x → 4.x:** In 4.x, adding an entity to a group no longer re-saves the entity itself — Group invalidates the entity's cache tags instead. Code or tests that relied on `hook_ENTITY_TYPE_update()` firing when an entity was added to a group will no longer see that side effect.

## Querying Relationships

```php
use Drupal\group\Entity\Storage\GroupRelationshipStorageInterface;

$storage = \Drupal::entityTypeManager()->getStorage('group_relationship');
assert($storage instanceof GroupRelationshipStorageInterface);

// All relationships in a group.
$all = $storage->loadByGroup($group);

// All relationships in a group for a specific plugin.
$articles = $storage->loadByGroup($group, 'group_node:article');

// All groups an entity belongs to (via any plugin).
$rels = $storage->loadByEntity($node);

// All groups an entity belongs to via a specific plugin.
$rels = $storage->loadByEntity($node, 'group_node:article');

// Relationships for entity+group pair.
$rels = $storage->loadByEntityAndGroup($node, $group, 'group_node:article');

// All relationships for a plugin globally.
$all_project_articles = $storage->loadByPluginId('group_node:article');
```

Alternatively, use the convenience methods on the `Group` entity:

```php
$group->getRelationships('group_node:article');
$group->getRelationshipsByEntity($node, 'group_node:article');
$group->getRelatedEntities('group_node:article');
```

## Loading Groups for an Entity

```php
// Get all groups a node belongs to.
$storage = \Drupal::entityTypeManager()->getStorage('group_relationship');
$relationships = $storage->loadByEntity($node);
$groups = array_map(fn($r) => $r->getGroup(), $relationships);
```

## Loading GroupMembership Statically

```php
use Drupal\group\Entity\GroupMembership;

// Get a user's membership in a specific group.
$membership = GroupMembership::loadSingle($group, $account);

// Get all groups the current user belongs to.
$memberships = GroupMembership::loadByUser(\Drupal::currentUser());

// Get all members of a group.
$memberships = GroupMembership::loadByGroup($group);

// Get all members with a specific role.
// 4.x: loadByGroup() and loadByUser() take the $roles filter as an array.
$memberships = GroupMembership::loadByGroup($group, ['project-editor']);
```

Membership lookups are cached in the `group_memberships` cache bin (chained memory + persistent cache) keyed by `group_memberships:entity_id[{uid}]:roles[any-roles]`.

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

## Injecting Services

```php
use Drupal\group\Plugin\Group\Relation\GroupRelationTypeManagerInterface;
use Drupal\group\Access\GroupPermissionCheckerInterface;

class MyService {
  public function __construct(
    protected GroupRelationTypeManagerInterface $pluginManager,
    protected GroupPermissionCheckerInterface $permissionChecker,
  ) {}
}

# services.yml
mymodule.my_service:
  class: 'Drupal\mymodule\MyService'
  arguments:
    - '@group_relation_type.manager'
    - '@group_permission.checker'
```

## Programmatic Plugin Installation

```php
use Drupal\group\Entity\GroupType;
use Drupal\group\Entity\Storage\GroupRelationshipTypeStorageInterface;

$group_type = GroupType::load('project');

// Install a plugin on a group type.
if (!$group_type->hasPlugin('group_node:article')) {
  $storage = \Drupal::entityTypeManager()->getStorage('group_relationship_type');
  assert($storage instanceof GroupRelationshipTypeStorageInterface);
  $storage->createFromPlugin($group_type, 'group_node:article', [
    'group_cardinality' => 0,
    'entity_cardinality' => 1,
  ])->save();
}
```

## Common Mistakes

- Calling `$group->addRelationship()` on an unsaved group. Both the group and the entity must be saved (have IDs) before a relationship can be created.
- Calling `$group->addMember()` in API context expecting creator roles. In 4.x, creator membership and creator roles are applied only when the group is created through a form — never on a purely programmatic `Group::save()`. If you're adding a member programmatically and want roles, call `addMember()` yourself and pass the roles explicitly.
- Using the `group.membership_loader` service. It was **removed in 4.0** (deprecated since 3.2.0). Use the `GroupMembership::loadSingle()`, `::loadByGroup()`, or `::loadByUser()` static methods instead.
- Forgetting `accessCheck(FALSE)` on entity queries in administrative/background code. Group's query access checks compute full permission calculations, which is expensive and context-dependent.

## See Also

- [Entity Types](entity-types.md)
- [Plugin System](plugin-system.md)
- Reference: `web/modules/contrib/group/src/Entity/Group.php`
