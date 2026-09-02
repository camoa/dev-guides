---
description: Protect AJAX endpoints from CSRF attacks using Drupal's token system and request validation
tldr: "Form API `#ajax` is CSRF-protected automatically. For custom POST AJAX routes use `_csrf_request_header_token: 'TRUE'` (validates X-CSRF-Token header). For GET action links use `_csrf_token: 'TRUE'` (validates `token=` query param)."
drupal_version: "11.x"
---

# CSRF Protection

## When to Use

You need to protect AJAX endpoints from Cross-Site Request Forgery attacks.

## Decision

| Endpoint type | CSRF requirement | How it works |
|---|---|---|
| Custom AJAX POST route | `_csrf_request_header_token: 'TRUE'` | Validates X-CSRF-Token header Drupal AJAX sends automatically |
| Action link / GET with side-effects | `_csrf_token: 'TRUE'` | Validates `token` query parameter appended by Url::toString() |
| Form API `#ajax` callback | Automatic — no route requirement needed | FormBuilder embeds and validates form token in every AJAX request |

## Pattern

```php
// Form API: CSRF handled automatically — no route changes needed.
$form['trigger'] = [
  '#type' => 'button',
  '#ajax' => ['callback' => '::ajaxCallback', 'wrapper' => 'target'],
];

// Custom AJAX POST route: use _csrf_request_header_token.
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

public function ajaxEndpoint(Request $request) {
  if (!$request->isXmlHttpRequest()) {
    throw new AccessDeniedHttpException('AJAX requests only.');
  }
  return new AjaxResponse();
}
```

Reference: `core/lib/Drupal/Core/Access/CsrfRequestHeaderAccessCheck.php`, `core/lib/Drupal/Core/Access/CsrfAccessCheck.php`

## Common Mistakes

- Using `_csrf_token: 'TRUE'` on a POST AJAX route → `_csrf_token` validates a URL query param, not the X-CSRF-Token header; Drupal AJAX POST requests send the header, so use `_csrf_request_header_token: 'TRUE'` instead
- Relying on X-Requested-With header alone → Can be spoofed; it is not a substitute for token validation
- Using GET requests for state-changing operations → GET bypasses header-based CSRF checks; use POST for all data changes
- Skipping CSRF entirely on custom routes → Security vulnerability; Form API protects forms but custom routes need explicit requirements
- Not configuring trusted_host_patterns → Requests from untrusted origins; configure in settings.php

## See Also

- ← Previous: [Access Control Patterns](access-control-patterns.md) | Next: [Performance Optimization](performance-optimization.md)
- Reference: [OWASP CSRF Prevention](https://owasp.org/www-community/attacks/csrf)
