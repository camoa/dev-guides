---
description: Security requirements for every Drupal AJAX implementation — access control, XSS prevention, CSRF, input validation
drupal_version: "11.x"
---

# Best Practices: Security

## When to Use

> Apply every item in this guide to every AJAX implementation. AJAX callbacks and routes are HTTP endpoints — they require the same security rigor as any web API.

## Decision

| Vulnerability | Attack Vector | Prevention |
|---------------|---------------|------------|
| XSS | Unsanitized user input in AJAX response | Use render arrays; `Html::escape()` for manual markup |
| CSRF | Forged requests to AJAX endpoints | Enable `_csrf_token` on routes; Form API handles automatically |
| Unauthorized access | Missing permission checks | Add `_permission` or `_custom_access` to every route |
| SQL injection | User input in queries | Use Entity Query API; never concatenate user input |
| File upload attacks | Malicious file uploads | Configure `#upload_validators` with extension, size, MIME |

## Pattern

```php
// 1. Access control on every route
my_module.ajax_endpoint:
  requirements:
    _permission: 'access content'
    _csrf_token: 'TRUE'

// 2. Return render arrays, not HTML strings
// BAD:
return '<div>' . $user_input . '</div>';

// GOOD:
return [
  '#markup' => $this->t('@content', ['@content' => $user_input]),
];

// 3. Validate upload files
$form['file'] = [
  '#type' => 'managed_file',
  '#upload_validators' => [
    'FileExtension' => ['extensions' => 'jpg jpeg png'],
    'FileSizeLimit' => ['fileLimit' => '2M'],
  ],
];

// 4. Verify triggering element
$triggering_element = $form_state->getTriggeringElement();
if (!$triggering_element) {
  throw new AccessDeniedHttpException();
}

// 5. Use Entity Query for database operations
$nids = $this->entityTypeManager->getStorage('node')->getQuery()
  ->condition('type', 'article')
  ->condition('field_value', $user_input)  // Safe: parameterized
  ->accessCheck(TRUE)
  ->execute();
```

## Common Mistakes

- **Wrong**: Skipping access checks on AJAX routes → **Right**: Always define `_permission` or `_custom_access`
- **Wrong**: Using `'#markup' => $user_input` without sanitization → **Right**: Use `$this->t('@var', ['@var' => $input])` or `Html::escape()`
- **Wrong**: Accepting file uploads without validators → **Right**: Always validate extension, size, and MIME type
- **Wrong**: Using inline JavaScript in AJAX responses → **Right**: Attach libraries via `#attached`; avoid inline scripts (CSP issues)
- **Wrong**: Trusting client-side validation → **Right**: JavaScript validation can be bypassed; always validate server-side

## See Also

- [Access Control Patterns](access-control-patterns.md)
- [CSRF Protection](csrf-protection.md)
- Reference: [Writing secure code for Drupal](https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal), [OWASP Top 10](https://owasp.org/www-project-top-ten/)
