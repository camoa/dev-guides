---
description: Security patterns for configuration forms
drupal_version: "11.x"
---

# Security Best Practices

## When to Use

> All configuration forms must follow security best practices to prevent vulnerabilities.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| User input storage | Sanitize on output, not input | Preserve original data, context-aware escaping |
| Operations links | Url::fromRoute() with token | CSRF protection built-in |
| Permissions | _permission in routing.yml | Access control before form loads |
| External URLs in operations | TrustedRedirectResponse | Prevent open redirect vulnerabilities |
| File paths from config | Sanitize/validate before use | Prevent directory traversal |

## Pattern

**1. Access Control**:
```yaml
# mymodule.routing.yml
mymodule.settings:
  path: '/admin/config/mymodule/settings'
  defaults:
    _form: '\Drupal\mymodule\Form\SettingsForm'
  requirements:
    _permission: 'administer site configuration'
```

**2. Input Validation**:
```php
public function validateForm(array &$form, FormStateInterface $form_state) {
  $api_key = $form_state->getValue('api_key');

  // Validate format
  if (!preg_match('/^[a-zA-Z0-9]{32}$/', $api_key)) {
    $form_state->setErrorByName('api_key', $this->t('API key must be 32 alphanumeric characters.'));
  }

  // Validate URL if accepting external URLs
  $url = $form_state->getValue('callback_url');
  if (!UrlHelper::isValid($url, TRUE)) {
    $form_state->setErrorByName('callback_url', $this->t('Invalid URL.'));
  }
}
```

**3. Output Sanitization**:
```php
// WRONG: Storing sanitized HTML
$config->set('message', Xss::filter($value))->save();

// RIGHT: Store raw, sanitize on output
$config->set('message', $value)->save();

// Later, when displaying:
$message = Xss::filter($config->get('message'));
// Or use #markup which auto-escapes:
$form['display'] = ['#markup' => $config->get('message')]; // Auto-escaped
```

**4. CSRF Protection**:
```php
// Operations automatically include CSRF tokens via Url::fromRoute()
$operations['delete'] = [
  'title' => $this->t('Delete'),
  'url' => Url::fromRoute('mymodule.item.delete', ['id' => $id]), // Token added automatically
];

// For custom URLs, generate token manually if needed
$url = Url::fromRoute('mymodule.custom', ['id' => $id]);
$url->setOption('query', ['token' => \Drupal::csrfToken()->get($url->getInternalPath())]);
```

**5. Permission Checks**:
```php
// Check permissions in form logic when needed
public function buildForm(array $form, FormStateInterface $form_state) {
  if (!$this->currentUser()->hasPermission('administer mymodule advanced')) {
    $form['advanced']['#access'] = FALSE;
  }
}
```

**Security Checklist**:
- All routes have `_permission` requirement
- All user input validated in validateForm()
- Config schema defines constraints
- Operations use Url::fromRoute() (automatic CSRF)
- External URLs validated with UrlHelper::isValid()
- File paths validated before filesystem operations
- Sensitive data not logged or displayed to unauthorized users
- #config_target used for automatic validation (Drupal 11+)

## Common Mistakes

- **Wrong**: Sanitizing input on storage → **Right**: Stores escaped HTML, double-escaping on output
- **Wrong**: Not validating external URLs → **Right**: Open redirect vulnerability
- **Wrong**: Missing permission checks → **Right**: Unauthorized access to sensitive forms
- **Wrong**: Using raw user input in file paths → **Right**: Directory traversal vulnerability
- **Wrong**: Trusting config values without validation → **Right**: Config can be manipulated via drush/UI
- **Wrong**: Not using CSRF tokens on state-changing operations → **Right**: CSRF attacks possible

## See Also

- [Operations Implementation](operations-implementation.md)
- [Performance Best Practices](performance-best-practices.md)
- Reference: core/lib/Drupal/Component/Utility/UrlHelper.php
- Reference: core/lib/Drupal/Component/Utility/Xss.php
- Reference: OWASP Top 10, Drupal Security Team best practices
