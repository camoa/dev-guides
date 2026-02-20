---
description: Restrict AJAX callbacks and routes with permission checks, custom access callbacks, and triggering element validation
drupal_version: "11.x"
---

# Access Control Patterns

## When to Use

> Every AJAX callback and route is an HTTP endpoint and requires access control. AJAX callbacks are not protected by the UI alone — attackers can call them directly.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Simple permission check | `_permission` in route | Built-in, automatic, covers 90% of cases |
| Complex permission logic | `_custom_access` callback | Supports multiple conditions, entity access checks |
| Form callback security | FormStateInterface checks | Validates user can access triggering element |
| Entity-specific access | EntityAccessCheck service | Proper entity operation checks (view, update, delete) |

## Pattern

```php
// Route with single permission
my_module.ajax_content:
  path: '/my-module/ajax/content'
  defaults:
    _controller: '\Drupal\my_module\Controller\AjaxController::getContent'
  requirements:
    _permission: 'access content'

// Route with custom access callback
my_module.ajax_restricted:
  path: '/my-module/ajax/restricted/{node}'
  defaults:
    _controller: '\Drupal\my_module\Controller\AjaxController::restrictedContent'
  requirements:
    _custom_access: '\Drupal\my_module\Controller\AjaxController::access'
```

```php
use Drupal\Core\Access\AccessResult;
use Drupal\Core\Session\AccountInterface;
use Drupal\node\NodeInterface;

public function access(NodeInterface $node, AccountInterface $account) {
  return AccessResult::allowedIf(
    $account->hasPermission('edit any article content')
    && $node->getType() === 'article'
    && $node->isPublished()
  );
}

// Form callback: verify triggering element
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $triggering_element = $form_state->getTriggeringElement();
  if (!$triggering_element || !isset($form[$triggering_element['#parents'][0]])) {
    throw new \Exception('Unauthorized AJAX request');
  }
  return $form['target'];
}
```

Reference: `core/lib/Drupal/Core/Access/AccessResult.php`

## Common Mistakes

- **Wrong**: Skipping access checks entirely → **Right**: AJAX callbacks are HTTP endpoints; always add protection
- **Wrong**: Using `_access: 'TRUE'` in routes → **Right**: Grants unrestricted access; always use proper access control
- **Wrong**: Not checking triggering element → **Right**: Users can manipulate requests to trigger callbacks on inaccessible elements
- **Wrong**: Trusting client-side data → **Right**: Validate all input server-side; JavaScript validation can be bypassed
- **Wrong**: `\Drupal::currentUser()` in wrong context → **Right**: Inject AccountInterface to avoid access bypass

## See Also

- [CSRF Protection](csrf-protection.md)
- [Best Practices: Security](best-practices-security.md)
- Reference: [Access control API](https://www.drupal.org/docs/drupal-apis/routing-system/access-checking-on-routes)
