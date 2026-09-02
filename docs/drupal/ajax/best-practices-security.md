---
description: Security requirements for every Drupal AJAX implementation — access control, XSS prevention, CSRF, input validation
tldr: "Apply every item in this guide to every AJAX implementation. AJAX callbacks and routes are HTTP endpoints — they require the same security rigor as any web API."
drupal_version: "11.x"
---

# Best Practices: Security

## When to Use

Every AJAX implementation requires security considerations.

## Critical Security Measures

**Critical Security Measures:**

1. **Access Control**
   - Every AJAX callback and route needs `_permission` or `_custom_access`
   - Check triggering element accessibility in Form API callbacks
   - Never trust client-sent data; validate server-side

2. **Input Validation**
   - Validate and sanitize all user input
   - Use FormStateInterface validation, not JavaScript-only
   - Apply upload validators for file uploads (extension, size, MIME type)

3. **CSRF Protection**
   - Drupal handles CSRF for Form API automatically
   - Add `_csrf_request_header_token: 'TRUE'` to custom POST AJAX routes (validates the X-CSRF-Token header Drupal AJAX sends automatically; `_csrf_token: 'TRUE'` validates a URL query param instead — see [CSRF Protection](csrf-protection.md))
   - Verify `$request->isXmlHttpRequest()` to prevent direct calls

4. **XSS Prevention**
   - Always return render arrays, not HTML strings
   - Use `Html::escape()` for user input in markup
   - MessageCommand and AnnounceCommand auto-escape content
   - Never use `'#markup' => $user_input` without sanitization

5. **SQL Injection Prevention**
   - Use Entity Query API, not direct database queries
   - Never concatenate user input into queries
   - Use parameterized queries for custom database operations

6. **Content Security Policy (CSP)**
   - Avoid inline JavaScript in AJAX responses
   - Use attached libraries instead of inline scripts
   - Configure CSP headers in settings.php

## Common Vulnerabilities

**Common Vulnerabilities:**

| Vulnerability | Attack Vector | Prevention |
|---|---|---|
| XSS | Unsanitized user input in AJAX response | Use render arrays, escape manually if needed |
| CSRF | Forged requests to AJAX endpoints | Form API handles automatically; add `_csrf_request_header_token: 'TRUE'` on custom POST AJAX routes |
| Unauthorized access | Missing permission checks | Add `_permission` or `_custom_access` |
| SQL injection | User input in queries | Use Entity Query API |
| File upload attacks | Malicious file uploads | Configure upload validators |

## Pattern

```php
// 1. Access control on every route
my_module.ajax_endpoint:
  requirements:
    _permission: 'access content'
    _csrf_request_header_token: 'TRUE'   // POST AJAX route: validates X-CSRF-Token header

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

## See Also

- Next: [Best Practices: Performance](best-practices-performance.md)
- [Access Control Patterns](access-control-patterns.md)
- [CSRF Protection](csrf-protection.md)
- Reference: [Writing secure code for Drupal](https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal), [OWASP Top 10](https://owasp.org/www-project-top-ten/)
