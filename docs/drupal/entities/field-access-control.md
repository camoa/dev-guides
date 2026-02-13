---
description: Field-level access control with cache metadata
drupal_version: "11.x"
---

# Field Access Control

## When to Use

When restricting field visibility or editability based on user permissions, entity state, or custom business logic, requiring fine-grained access control beyond entity-level permissions.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Permission-based field access | hook_entity_field_access() | Role-based field visibility |
| State-based field access | Access handlers checking entity state | Conditional field access based on status |
| Field-level permissions | Field permissions module | Per-field permission grants |
| Custom field access | FieldItemList::access() | Override in custom field types |

## Pattern

Field access hook:

```php
/**
 * Implements hook_entity_field_access().
 */
function my_module_entity_field_access($operation, FieldDefinitionInterface $field_definition, AccountInterface $account, ?FieldItemListInterface $items = NULL) {
  // Restrict field_internal to admins
  if ($field_definition->getName() === 'field_internal') {
    if ($operation === 'view' && !$account->hasPermission('view internal fields')) {
      return AccessResult::forbidden()->cachePerPermissions();
    }
    if ($operation === 'edit' && !$account->hasPermission('edit internal fields')) {
      return AccessResult::forbidden()->cachePerPermissions();
    }
  }

  // Restrict editing published content's embargo field
  if ($field_definition->getName() === 'field_embargo' && $operation === 'edit') {
    if ($items && $items->getEntity()->isPublished()) {
      return AccessResult::forbidden()
        ->cachePerPermissions()
        ->addCacheableDependency($items->getEntity());
    }
  }

  return AccessResult::neutral();
}
```

Custom field access in field type:

```php
class SensitiveDataItem extends FieldItemBase {

  public function access($operation = 'view', AccountInterface $account = NULL, $return_as_object = FALSE) {
    $account = $account ?: \Drupal::currentUser();

    if ($operation === 'view' && !$account->hasPermission('view sensitive data')) {
      $access = AccessResult::forbidden()->cachePerPermissions();
    }
    else {
      $access = AccessResult::allowed()->cachePerPermissions();
    }

    return $return_as_object ? $access : $access->isAllowed();
  }
}
```

Reference: `/core/lib/Drupal/Core/Entity/EntityAccessControlHandler.php`

## Common Mistakes

- **Wrong**: Returning TRUE/FALSE → **Right**: Return AccessResult objects with cache metadata
- **Wrong**: Missing cache metadata → **Right**: Access checks cached incorrectly; security issue or cache pollution
- **Wrong**: Not checking operation → **Right**: Apply to both 'view' and 'edit' operations appropriately
- **Wrong**: Forgetting addCacheableDependency() → **Right**: Dynamic access not recalculated when dependency changes
- **Wrong**: Using access hooks instead of permissions → **Right**: Create permissions for reusable access rules
- **Wrong**: Not handling NULL $items → **Right**: Items can be NULL; check before accessing entity

**Security (CRITICAL)**:
- ALWAYS return AccessResult objects, never boolean TRUE/FALSE
- Use cachePerPermissions() for permission-based access
- Use cachePerUser() for user-specific access (expensive, avoid if possible)
- Use addCacheableDependency() for entity-state-based access
- Return AccessResult::neutral() when not making decision (let other hooks decide)
- AccessResult::forbidden() wins over allowed(). Use carefully.
- Check both 'view' and 'edit' operations. They're independent.

**Performance**:
- Field access checked on EVERY field access. Keep logic fast.
- Use cachePerPermissions() instead of cachePerUser() when possible
- Avoid loading entities in access checks. Use $items->getEntity() (already loaded)
- Cache expensive access decisions with cache API

**Development Standards**:
- Document access rules in hook implementation
- Create custom permissions for reusable access logic
- Use AccessResult::allowedIfHasPermission() helper when appropriate
- Test access hooks with different user roles

## See Also

- [Entity Query Patterns](entity-query-patterns.md)
- [Entity Query Performance](entity-query-performance.md)
- Reference: [Entity access API](https://www.drupal.org/docs/drupal-apis/entity-api/working-with-the-entity-api)
