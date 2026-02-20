---
description: Protect AJAX endpoints from CSRF attacks using Drupal's token system and request validation
drupal_version: "11.x"
---

# CSRF Protection

## When to Use

> Drupal's Form API handles CSRF automatically. For custom AJAX routes outside Form API, add `_csrf_token: 'TRUE'` and verify request type.

## Pattern

```yaml
# Route definition with CSRF protection
my_module.ajax_endpoint:
  path: '/my-module/ajax/endpoint'
  defaults:
    _controller: '\Drupal\my_module\Controller\AjaxController::ajaxEndpoint'
  requirements:
    _permission: 'access content'
    _csrf_token: 'TRUE'   # Enables CSRF protection for non-Form API routes
```

```php
use Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException;

public function ajaxEndpoint(Request $request) {
  // Drupal validates CSRF token automatically when _csrf_token: TRUE
  // Additional check: verify it's actually an AJAX request
  if (!$request->isXmlHttpRequest()) {
    throw new AccessDeniedHttpException('AJAX requests only');
  }

  return new AjaxResponse();
}
```

**Form API (automatic):**

```php
// No additional CSRF handling needed — Form API handles tokens automatically
$form['trigger'] = [
  '#type' => 'button',
  '#value' => t('Submit'),
  '#ajax' => ['callback' => '::ajaxCallback', 'wrapper' => 'target'],
];
```

Reference: `core/lib/Drupal/Core/Access/CsrfRequestHeaderAccessCheck.php`

## Common Mistakes

- **Wrong**: Disabling CSRF protection unnecessarily → **Right**: Drupal's AJAX system handles tokens automatically; don't remove protection
- **Wrong**: Not validating AJAX requests → **Right**: Attackers can call endpoints directly; check `$request->isXmlHttpRequest()`
- **Wrong**: Using GET for state-changing operations → **Right**: CSRF tokens protect POST; use POST for all data changes
- **Wrong**: Trusting X-Requested-With header alone → **Right**: Can be spoofed; combine with token validation
- **Wrong**: Not configuring trusted_host_patterns → **Right**: AJAX from untrusted origins; configure in settings.php

## See Also

- [Access Control Patterns](access-control-patterns.md)
- [Performance Optimization](performance-optimization.md)
- Reference: [OWASP CSRF Prevention](https://owasp.org/www-community/attacks/csrf)
