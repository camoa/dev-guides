---
description: Protect AJAX endpoints from CSRF attacks using Drupal's token system and request validation
tldr: "Form API `#ajax` is CSRF-protected automatically. For custom POST AJAX routes use `_csrf_request_header_token: 'TRUE'` (validates X-CSRF-Token header). For GET action links use `_csrf_token: 'TRUE'` (validates `token=` query param)."
drupal_version: "11.x"
---

# CSRF Protection

## When to Use

> Drupal's Form API handles CSRF automatically for `#ajax` callbacks. For custom routes outside Form API, apply the correct requirement based on HTTP method.

## Decision

| Endpoint type | CSRF requirement | How it works |
|---|---|---|
| Custom AJAX POST route | `_csrf_request_header_token: 'TRUE'` | Validates X-CSRF-Token header Drupal AJAX sends automatically |
| Action link / GET with side-effects | `_csrf_token: 'TRUE'` | Validates `token` query parameter appended by `Url::toString(TRUE)` |
| Form API `#ajax` callback | Automatic — no route requirement needed | FormBuilder embeds and validates form token in every AJAX request |

## Pattern

```php
// Form API: CSRF handled automatically — no route changes needed.
$form['trigger'] = [
  '#type' => 'button',
  '#ajax' => ['callback' => '::ajaxCallback', 'wrapper' => 'target'],
];

// Custom POST AJAX route: use _csrf_request_header_token.
// Drupal.ajax sends X-CSRF-Token header automatically on POST.
// my_module.routing.yml:
// my_module.ajax_endpoint:
//   path: '/my-module/ajax/endpoint'
//   defaults:
//     _controller: '\Drupal\my_module\Controller\AjaxController::ajaxEndpoint'
//   requirements:
//     _permission: 'access content'
//     _csrf_request_header_token: 'TRUE'

// GET action link with token (destructive action via link):
// my_module.delete_item:
//   requirements:
//     _csrf_token: 'TRUE'   # token= query param validated
// (Url::toString(TRUE) appends the token automatically)
```

```php
use Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException;

public function ajaxEndpoint(Request $request) {
  // _csrf_request_header_token validates the token automatically.
  // Additional check: verify it's actually an AJAX request.
  if (!$request->isXmlHttpRequest()) {
    throw new AccessDeniedHttpException('AJAX requests only.');
  }
  return new AjaxResponse();
}
```

Reference: `core/lib/Drupal/Core/Access/CsrfRequestHeaderAccessCheck.php`, `core/lib/Drupal/Core/Access/CsrfAccessCheck.php`

## Common Mistakes

- **Wrong**: Using `_csrf_token: 'TRUE'` on a POST AJAX route → **Right**: `_csrf_token` validates a URL query param, not the X-CSRF-Token header; use `_csrf_request_header_token: 'TRUE'` for POST routes
- **Wrong**: Relying on X-Requested-With header alone → **Right**: Can be spoofed; it is not a substitute for token validation
- **Wrong**: Using GET for state-changing operations → **Right**: GET bypasses header-based CSRF checks; use POST for all data changes
- **Wrong**: Skipping CSRF entirely on custom routes → **Right**: Form API protects forms but custom routes need explicit requirements
- **Wrong**: Not configuring trusted_host_patterns → **Right**: Requests from untrusted origins; configure in settings.php

## See Also

- [Access Control Patterns](access-control-patterns.md)
- [Performance Optimization](performance-optimization.md)
- Reference: [OWASP CSRF Prevention](https://owasp.org/www-community/attacks/csrf)
