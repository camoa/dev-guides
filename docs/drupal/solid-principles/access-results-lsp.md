---
description: Combine Drupal AccessResult objects correctly following LSP substitutability
drupal_version: "11.x"
---

# Access Results - Liskov Substitution (LSP)

## When to Use

AccessResult follows LSP via three immutable subclasses: Allowed, Forbidden, Neutral. They can be combined with `orIf()`/`andIf()` and always produce valid AccessResultInterface.

## Decision

| Result type | Returns | Use when |
|---|---|---|
| AccessResult::allowed() | AccessResultAllowed | Explicitly granting access |
| AccessResult::forbidden($reason) | AccessResultForbidden | Explicitly denying access (overrides all allows) |
| AccessResult::neutral($reason) | AccessResultNeutral | Not making a decision (default) |
| AccessResult::allowedIf($condition) | Allowed if true, Neutral if false | Conditional allow |
| AccessResult::forbiddenIf($condition, $reason) | Forbidden if true, Neutral if false | Conditional forbid |

## Pattern

**GOOD: LSP-compliant access results**

```php
function checkAccess(NodeInterface $node, $op, AccountInterface $account) {
  // All return AccessResultInterface - substitutable
  if ($account->hasPermission('bypass node access')) {
    return AccessResult::allowed()->cachePerPermissions();
  }

  if ($op === 'delete' && $node->getOwnerId() !== $account->id()) {
    return AccessResult::forbidden('Not the owner')->cachePerUser();
  }

  // Neutral lets other access checks decide
  return AccessResult::neutral()->cachePerPermissions();
}

// Combining results preserves LSP
$result1 = AccessResult::allowed();
$result2 = AccessResult::neutral();
$combined = $result1->orIf($result2);  // Returns AccessResultAllowed
```

**BAD: Violating access result contract**

```php
function checkAccess(NodeInterface $node, $op, AccountInterface $account) {
  // Returning boolean violates interface
  if ($account->hasPermission('bypass node access')) {
    return TRUE;  // Should return AccessResultInterface
  }

  // Don't use AccessResult as boolean
  if ($result) {  // WRONG - always truthy, security issue
    // Grant access
  }
}
```

Reference: `/core/lib/Drupal/Core/Access/AccessResult.php`

## Common Mistakes

- Returning boolean from access hooks -- return AccessResult. **WHY:** Boolean doesn't carry cacheability metadata; causes access bypass bugs
- Using `if ($access_result)` instead of `if ($access_result->isAllowed())` -- use isAllowed(). **WHY:** AccessResult objects are always truthy; creates critical security holes
- Not adding cache metadata (cachePerPermissions, cachePerUser) -- add cache context. **WHY:** Access results cache incorrectly without metadata; user A sees user B's content
- Returning NULL instead of neutral() -- return AccessResult::neutral(). **WHY:** NULL breaks type hints, causes fatal errors

## See Also

- [Form Hierarchy](form-hierarchy-lsp.md) for form LSP patterns
- [Hooks & Events](hooks-events-ocp.md) for access hook patterns
- Reference: `/core/lib/Drupal/Core/Access/AccessResultInterface.php`
