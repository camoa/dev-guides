---
description: Implementing node grants for database-level content access filtering based on taxonomy, groups, or user-specific rules.
---

# Content Access (Node Grants)

## When to Use
When entity access handlers are insufficient -- node grants enable database-level access filtering for complex content access rules (e.g., organic groups, taxonomy access, workflow states).

## Decision
| If you need... | Use... | Why |
|---|---|---|
| Simple ownership/role access | Entity access handler | Simpler, sufficient for most cases |
| Per-node access by user ID | Node grants | Enables "grant view to users 5,7,9" |
| Access based on taxonomy/groups | Node grants | Query-level filtering, scalable |
| Workflow-based access (draft/published) | Node access handler first | Grants are complex; try handler |

**How Node Grants Work:**
1. Modules implement `hook_node_grants()` to declare grants for a user
2. Modules implement `hook_node_access_records()` to store grants per node
3. System writes grants to `node_access` table
4. Queries automatically filter by grants (database-level)

## Pattern
Implementing node grants for taxonomy-based access:
```php
// Declare what grants this user has
function mymodule_node_grants(AccountInterface $account, $op) {
  $grants = [];
  if ($op == 'view') {
    // User gets grants for their department term IDs
    $user = User::load($account->id());
    $term_ids = $user->get('field_department')->getValue();
    foreach ($term_ids as $delta => $item) {
      $grants['mymodule_department'][] = $item['target_id'];
    }
  }
  return $grants;
}

// Store grants on node
function mymodule_node_access_records(NodeInterface $node) {
  $grants = [];
  if ($node->hasField('field_department')) {
    foreach ($node->get('field_department') as $item) {
      $grants[] = [
        'realm' => 'mymodule_department',
        'gid' => $item->target_id,
        'grant_view' => 1,
        'grant_update' => 0,
        'grant_delete' => 0,
      ];
    }
  }
  return $grants;
}

// Rebuild grants when needed
node_access_rebuild();
```
Reference: `/core/modules/node/node.module` (hook implementations)

## Common Mistakes
- Using grants when entity access handler would suffice -- Grants are complex, hard to debug
- Forgetting to rebuild grants after changes -- `drush php-eval 'node_access_rebuild();'`
- Not implementing both hooks -- Grants won't work (need grants + records)
- Returning empty grants array -- Node becomes inaccessible to all
- Using grants for non-node entities -- Only works for nodes; use entity access for others
- Not testing with multiple users -- Grants can leak between users if realm/gid wrong

## See Also
- Reference: https://www.drupal.org/docs/8/api/node-access-api
- [Entity Access Control](entity-access-control.md) for simpler alternative
