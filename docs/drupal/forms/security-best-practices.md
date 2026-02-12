---
description: Security best practices — CSRF, XSS, SQL injection, file uploads, access control
drupal_version: "11.x"
---

# Security Best Practices

## When to Use

> Always validate user input. Never bypass CSRF tokens. Use getValue() not getUserInput(). Validate file extensions.

## Decision

| Security Need | Solution | Why |
|---------------|----------|-----|
| User input | `getValue()` | Sanitized |
| Raw input | Never use `getUserInput()` | Unsanitized |
| Display user data | Render arrays, t() | Auto-escaped |
| File uploads | #upload_validators | Whitelist extensions |
| Sensitive files | private:// | Access control |
| Database queries | Parameterized | Prevent SQL injection |

## CSRF Protection (Form Tokens)

**Automatic Token System:**
```
FormBuilder adds to all forms:
- form_token: CSRF token
- form_build_id: Cache key
- form_id: Form identifier
```

**Token Validation Flow:**
```
1. User submits form
2. FormValidator checks form_token
3. Compares against session-based token (CsrfTokenGenerator)
4. Invalid token → validation fails, no handlers run
5. Valid token → proceed with validation/submission
```

Reference: `/web/core/lib/Drupal/Core/Form/FormValidator.php` lines 110-120

**Never Bypass Tokens For:**
- User-submitted forms
- Forms modifying data
- Forms with access restrictions
- Forms in public pages

## Input Validation and Sanitization

**Never Trust User Input:**
```php
// NEVER use directly:
$_POST, $_GET, $_REQUEST
$form_state->getUserInput() // Unsanitized

// ALWAYS use:
$form_state->getValue('field_name') // Sanitized
$form_state->getValues() // All sanitized
```

**Validation in Handlers:**
```php
public function validateForm(array &$form, FormStateInterface $form_state) {
  $value = $form_state->getValue('field');

  // Validate format
  if (!preg_match('/^[a-z0-9]+$/', $value)) {
    $form_state->setErrorByName('field', $this->t('Invalid format.'));
  }

  // Validate range
  if ($value < 0 || $value > 100) {
    $form_state->setErrorByName('field', $this->t('Out of range.'));
  }
}
```

## XSS Prevention

**Form API Auto-Escaping:**
```
Render arrays: Automatically escaped
t() function: Escapes by default
Twig templates: Auto-escape enabled
```

**Safe Patterns:**
```php
// SAFE - automatic escaping
$form['field']['#title'] = $this->t('Title: @title', [
  '@title' => $user_input,
]);

// SAFE - plain text
$form['field']['#plain_text'] = $user_input;

// SAFE - filtered markup
$form['markup'] = [
  '#type' => 'processed_text',
  '#text' => $user_input,
  '#format' => 'basic_html',
];
```

**Unsafe Patterns:**
```php
// UNSAFE - raw markup
$form['field']['#markup'] = '<div>' . $user_input . '</div>';

// UNSAFE - unescaped t()
$form['field']['#title'] = $this->t($user_input);

// UNSAFE - HTML in default value
$form['field']['#default_value'] = '<script>alert("xss")</script>';
```

## SQL Injection Prevention

**Database API Usage:**
```php
// SAFE - parameterized query
$result = \Drupal::database()->query(
  'SELECT * FROM {table} WHERE field = :value',
  [':value' => $user_input]
);

// UNSAFE - concatenated query
$result = \Drupal::database()->query(
  "SELECT * FROM {table} WHERE field = '" . $user_input . "'"
);
```

**Entity Query (Safest):**
```php
$query = \Drupal::entityQuery('node')
  ->condition('type', 'article')
  ->condition('title', $user_input)
  ->accessCheck(TRUE);
$nids = $query->execute();
```

Note: Validation doesn't prevent SQL injection. Always use proper API.

## File Upload Security

**Managed File Element:**
```php
$form['file'] = [
  '#type' => 'managed_file',
  '#title' => $this->t('Upload File'),
  '#upload_location' => 'private://uploads/',
  '#upload_validators' => [
    'file_validate_extensions' => ['pdf doc docx'],
    'file_validate_size' => [2 * 1024 * 1024], // 2MB
  ],
];
```

**Upload Validators:**
- file_validate_extensions: Whitelist allowed types
- file_validate_size: Max file size in bytes
- file_validate_image_resolution: Max width/height for images
- Never trust client-provided filename or MIME type

**Public vs Private:**
```
public:// - Direct web access, for public files
private:// - Access control, sensitive documents
```

**Security Checklist:**
- Always validate file extensions (whitelist)
- Set reasonable size limits
- Use private:// for sensitive files
- Never execute uploaded files
- Scan for malware if needed (contrib module)

## Access Control

**Form-Level Access:**
```php
use Drupal\Core\Access\AccessResult;

public function access() {
  $account = \Drupal::currentUser();
  return AccessResult::allowedIfHasPermission($account, 'administer site');
}
```

**Element-Level Access:**
```php
// Boolean
$form['admin_field']['#access'] = $current_user->hasPermission('admin');

// AccessResult (cacheable)
$form['admin_field']['#access'] = AccessResult::allowedIfHasPermission(
  $current_user,
  'administer site configuration'
);
```

**Access Bypass (Dangerous):**
```php
// Only for programmatic submission
$form_state->setProgrammedBypassAccessCheck(TRUE);
// NEVER for user-submitted forms
```

## Common Mistakes

- **Wrong**: Using #access without cache contexts → **Right**: Add proper cache contexts
- **Wrong**: Bypassing access checks inappropriately → **Right**: Only for programmatic submission
- **Wrong**: Not checking access in custom submit handlers → **Right**: Verify permissions
- **Wrong**: Assuming validation = access control → **Right**: Different concerns

## See Also

- [Validation Architecture](validation-architecture.md)
- [File Upload Elements](elements-selection.md)
- Documentation: [Drupal Security Best Practices](https://metadesignsolutions.com/drupal-security-best-practices-protecting-enterprise-websites-in-2026/)
- Reference: `/web/core/lib/Drupal/Core/Form/FormValidator.php`
- Reference: `/web/core/lib/Drupal/Core/Access/CsrfTokenGenerator.php`
