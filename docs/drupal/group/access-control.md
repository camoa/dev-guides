---
description: Group access control — explicit forbid philosophy, access check flow, query access, GroupAccessResult, custom handlers, and revision access
tldr: "Read this when diagnosing access issues, understanding the \"explicit forbid\" pattern, or writing custom access control for group-related entities."
drupal_version: "11.x"
---

# Access Control

## When to Use

> Read this when diagnosing access issues, understanding the "explicit forbid" pattern, or writing custom access control for group-related entities.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Entity in a group, `entity_access: TRUE` | Group owns access | Either allows or forbids — never neutral |
| Entity NOT in any group | Neutral result | Other modules handle access normally |
| Entity in group, `entity_access: FALSE` (default) | Neutral result | Group defers to other modules |
| Unsaved entity | Always neutral | No ID means no relationships can exist |
| Custom access logic | Override `access_control` handler | Decorator pattern, preserves defaults |

## Pattern

```php
use Drupal\group\Access\GroupAccessResult;

// Allow if the user has a single permission.
$result = GroupAccessResult::allowedIfHasGroupPermission($group, $account, 'edit group');

// Allow if the user has any of multiple permissions (OR).
$result = GroupAccessResult::allowedIfHasGroupPermissions(
  $group, $account, ['edit group', 'administer group'], 'OR'
);
// These automatically add the group entity and user.group_permissions cache context.
```

Custom access handler:

```yaml
# mymodule.services.yml
group.relation_handler.access_control.my_plugin:
  class: 'Drupal\mymodule\Plugin\Group\RelationHandler\MyAccessControl'
  arguments: ['@group.relation_handler.access_control']
  shared: false
```

```php
class MyAccessControl implements AccessControlInterface {
  use AccessControlTrait;
  public function __construct(AccessControlInterface $decorated) {
    $this->decorated = $decorated;
  }
  public function entityAccess(EntityInterface $entity, $operation, AccountInterface $account, $return_as_object = FALSE) {
    return $this->decorated->entityAccess($entity, $operation, $account, $return_as_object);
  }
}
```

## Common Mistakes

- **Wrong**: Assuming ungrouped entities are affected by Group → **Right**: Group only checks entities that have at least one `group_relationship` record. Ungrouped entities return neutral.
- **Wrong**: Checking access on new (unsaved) entities → **Right**: Group explicitly returns neutral for new entities — they have no ID and cannot have relationships.
- **Wrong**: Disabling `disable_sql_rewrite` in Views for group-aware content → **Right**: Group hooks into Views query via `hook_views_query_alter()`. Disabling SQL rewrite removes Group's access filtering.

## See Also

- [Permissions System](permissions-system.md)
- [Caching](caching.md)
- Reference: `web/modules/contrib/group/src/Plugin/Group/RelationHandler/AccessControlTrait.php`
