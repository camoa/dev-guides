---
description: Mapping OWASP Top 10 2021 vulnerabilities to Drupal-specific mitigations, common pitfalls, and prevention patterns.
---

# OWASP Top 10 in Drupal

## When to Use
When evaluating Drupal applications against industry-standard security risks or conducting security audits.

## Items

### A01:2021 - Broken Access Control
**Description:** Unauthorized access to content, operations, or administrative functions.
**Drupal Mitigations:**
- Permission system with role-based access control (RBAC)
- Route access checks (`_permission`, `_custom_access`, `_entity_access`)
- Entity access handlers
- Node grants system for granular content access

**Common Drupal Vulnerabilities:**
- Missing route access checks
- Incorrectly returning `AccessResult::neutral()` instead of `::forbidden()`
- Bypassing entity access checks with direct database queries
- Not checking access in custom controllers

**Testing Pattern:**
```php
// Always check access before operations
$node = Node::load($nid);
if (!$node->access('update')) {
  throw new AccessDeniedHttpException();
}
```

### A02:2021 - Cryptographic Failures
**Description:** Exposure of sensitive data due to weak or missing encryption.
**Drupal Mitigations:**
- Password hashing via `\Drupal\Core\Password\PasswordInterface`
- CSRF token generation using cryptographically secure random
- Private key system (`\Drupal\Core\PrivateKey`)
- Encrypted cookie support

**Common Drupal Vulnerabilities:**
- Storing passwords in plain text
- Using predictable session IDs
- Exposing private keys in version control
- Not enforcing HTTPS for authenticated sessions

**Best Practice:**
```php
// Use Drupal's password hashing
$password_hasher = \Drupal::service('password');
$hashed = $password_hasher->hash($password);
```

### A03:2021 - Injection
**Description:** SQL injection, XSS, command injection from untrusted data.
**Drupal Mitigations:**
- Database API with parameterized queries
- Twig autoescape for output
- `Xss::filter()` and `Html::escape()` utilities
- `UrlHelper::filterBadProtocol()` for URL validation

**Common Drupal Vulnerabilities:**
- Using `db_query()` without placeholders in D7 (EOL Jan 2025)
- Direct PDO usage bypassing Database API
- Disabling Twig autoescape with `|raw` filter
- Using `#markup` with unsanitized user input

**Prevention Pattern:**
```php
// SQL: Use placeholders
$database->query('SELECT * FROM {node} WHERE nid = :nid', [':nid' => $nid]);

// XSS: Let Twig autoescape
{{ user_input }} {# Automatically escaped #}
```

### A04:2021 - Insecure Design
**Description:** Architectural flaws that can't be fixed by implementation.
**Drupal Mitigations:**
- Separation of configuration and content
- API-first architecture with access controls
- Form API with built-in CSRF protection
- Typed data for input validation

**Common Drupal Vulnerabilities:**
- Exposing administrative operations to untrusted users
- Not implementing rate limiting on authentication
- Allowing unrestricted file uploads
- Missing input validation on custom forms

### A05:2021 - Security Misconfiguration
**Description:** Default passwords, verbose errors, unpatched systems.
**Drupal Mitigations:**
- Configuration management system
- Update status module
- Secure default settings
- Environment-specific settings.php

**Common Drupal Vulnerabilities:**
- Leaving `$config['system.logging']['error_level'] = 'verbose'` on production
- Not restricting files directory permissions (should be 755/644)
- Exposing `.git` or `web.config` files
- Using default database prefixes

**Hardening Checklist:**
- Disable verbose error logging in production
- Set `$settings['update_free_access'] = FALSE`
- Remove `install.php` or restrict access
- Configure `trusted_host_patterns` in settings.php

### A06:2021 - Vulnerable and Outdated Components
**Description:** Using modules or libraries with known vulnerabilities.
**Drupal Mitigations:**
- Security advisory system at https://www.drupal.org/security
- Automated update notifications
- Composer-based dependency management
- Security coverage requirements for contrib

**Common Drupal Vulnerabilities:**
- Running unsupported Drupal versions (D7 EOL Jan 2025)
- Using contrib modules without security coverage
- Not applying security updates within 24 hours
- Including abandoned JavaScript libraries

**Update Strategy:**
```bash
# Check for security updates
composer outdated drupal/*
# Apply security updates immediately
composer update drupal/core --with-dependencies
drush updb -y
```

### A07:2021 - Identification and Authentication Failures
**Description:** Broken authentication allowing account compromise.
**Drupal Mitigations:**
- Brute force protection (flood control)
- Session management with secure cookies
- Two-factor authentication via contrib (TFA module)
- Password policy enforcement

**Common Drupal Vulnerabilities:**
- Not requiring strong passwords
- Missing brute force protection on custom login forms
- Not invalidating sessions on logout
- Predictable password reset tokens

**Hardening:**
```php
// Enforce flood control
$flood = \Drupal::flood();
if (!$flood->isAllowed('user.failed_login_ip', 5)) {
  throw new \Exception('Too many failed login attempts.');
}
```

### A08:2021 - Software and Data Integrity Failures
**Description:** Insecure deserialization, untrusted updates.
**Drupal Mitigations:**
- Trusted callback interface
- Render system with `#pre_render` validation
- Configuration import validation
- File integrity monitoring via Update module

**Common Drupal Vulnerabilities:**
- Using `unserialize()` on untrusted data
- Not implementing `TrustedCallbackInterface`
- Allowing untrusted code in PHP filter (disabled by default)
- Not validating configuration imports

**Safe Pattern:**
```php
// Use TrustedCallbackInterface for render callbacks
class MyClass implements TrustedCallbackInterface {
  public static function trustedCallbacks() {
    return ['preRenderCallback'];
  }
}
```

### A09:2021 - Security Logging and Monitoring Failures
**Description:** Insufficient logging to detect/respond to attacks.
**Drupal Mitigations:**
- Watchdog logging system
- Database logging (dblog) or syslog
- Security Kit module for intrusion detection
- Audit log contrib modules

**Common Drupal Vulnerabilities:**
- Not logging authentication failures
- Ignoring watchdog warnings
- No alerting for repeated 403/404 errors
- Missing audit trail for content changes

**Logging Best Practice:**
```php
\Drupal::logger('my_module')->warning(
  'Access denied for @user to @path',
  ['@user' => $account->getAccountName(), '@path' => $path]
);
```

### A10:2021 - Server-Side Request Forgery (SSRF)
**Description:** Forcing server to make requests to unintended locations.
**Drupal Mitigations:**
- `UrlHelper::isValid()` and `::isExternal()` checks
- HTTP client with configurable allowed domains
- No user-controlled URLs in file operations

**Common Drupal Vulnerabilities:**
- Using `file_get_contents()` with user-supplied URLs
- Not validating redirect destinations
- Allowing users to specify external image sources
- Missing URL validation in aggregators/importers

**Prevention:**
```php
// Validate external URLs
if (UrlHelper::isValid($url) && !UrlHelper::isExternal($url)) {
  // Safe for internal use
}
```

## Common Mistakes
- Treating OWASP as checklist rather than principles -- Understand the underlying vulnerabilities, not just the categories
- Only testing happy paths -- Security testing requires adversarial thinking
- Assuming Drupal core is bulletproof -- Stay updated on security advisories

## See Also
- Reference: https://owasp.org/www-project-top-ten/
- [Anti-Patterns and Common Mistakes](anti-patterns-and-common-mistakes.md) for specific Drupal mistakes
