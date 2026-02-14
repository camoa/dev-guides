---
description: Recognizing and avoiding dangerous security anti-patterns in Drupal including missing access checks, SQL injection, XSS holes, and CSRF bypass.
---

# Anti-Patterns and Common Mistakes

## When to Use
During code review or when debugging security issues -- recognize dangerous patterns to avoid them.

## Items

### Using `\Drupal::` Static Calls Everywhere
**Why It's Wrong:** Not testable, bypasses dependency injection, tight coupling.
**Correct Pattern:**
```php
// WRONG
$database = \Drupal::database();

// CORRECT (in service/controller)
public function __construct(Connection $database) {
  $this->database = $database;
}
```
**When Acceptable:** Procedural hooks, static utility methods (rare).

### No Access Check on Routes
**Why It's Wrong:** Anyone, including anonymous users, can access.
**Symptoms:** 403 errors reported by users for legitimate access.
**Correct Pattern:**
```yaml
# WRONG
mymodule.admin:
  path: '/admin/mymodule'
  defaults:
    _controller: '...'
  # No requirements!

# CORRECT
requirements:
  _permission: 'administer site configuration'
```

### Using `->accessCheck(FALSE)` in Entity Queries
**Why It's Wrong:** Bypasses entity access system, leaks protected content.
**When Legitimate:** Loading for system operations (cron, migration) where current user irrelevant.
**Correct Pattern:**
```php
// WRONG (unless you have a really good reason)
$nodes = \Drupal::entityQuery('node')->accessCheck(FALSE)->execute();

// CORRECT
$nodes = \Drupal::entityQuery('node')->accessCheck(TRUE)->execute();
```

### String Concatenation in Database Queries
**Why It's Wrong:** SQL injection vulnerability.
**Impact:** Database compromise, data theft, escalation to server compromise.
**Correct Pattern:**
```php
// WRONG - SQL INJECTION
$query = "SELECT * FROM {users} WHERE name = '" . $_GET['name'] . "'";

// CORRECT - Parameterized
$query = $database->query('SELECT * FROM {users} WHERE name = :name',
  [':name' => $_GET['name']]);
```

### Using `|raw` Filter in Twig
**Why It's Wrong:** Disables XSS protection.
**When Legitimate:** Trusted, pre-sanitized markup (must be `Markup` object).
**Correct Pattern:**
```twig
{# WRONG #}
{{ user_bio|raw }}

{# CORRECT #}
{{ user_bio }}  {# Autoescaped #}
```

### Direct `#markup` with User Input
**Why It's Wrong:** XSS vulnerability.
**Correct Pattern:**
```php
// WRONG
$build['#markup'] = $user_input;

// CORRECT
$build['#markup'] = Xss::filter($user_input);
// OR
$build['#plain_text'] = $user_input;
```

### Hardcoding User ID 1 Bypass
**Why It's Wrong:** Creates hidden superuser; not auditable.
**Symptoms:** "Why can user 1 do this but admin role can't?"
**Correct Pattern:**
```php
// WRONG
if ($account->id() == 1) {
  return AccessResult::allowed();
}

// CORRECT
return AccessResult::allowedIfHasPermission($account, 'bypass node access');
```

### Not Validating CSRF Tokens on State-Changing Operations
**Why It's Wrong:** CSRF attack allows unauthorized actions.
**Symptoms:** Users report actions they didn't perform.
**Correct Pattern:**
```yaml
# For non-form routes
requirements:
  _csrf_token: 'TRUE'
```

### Using GET Requests for Destructive Actions
**Why It's Wrong:** Prefetch, bots, CSRF all trigger unwanted actions.
**Correct Pattern:**
```php
// WRONG
Route: /delete/{id}  # GET request deletes!

// CORRECT
Route: /delete/{id}  # POST only
requirements:
  _csrf_token: 'TRUE'
```

### Trusting User Roles in Code Logic
**Why It's Wrong:** Roles are configurable; user can have role without intended permissions.
**Correct Pattern:**
```php
// WRONG
if (in_array('editor', $account->getRoles())) {
  // Allow
}

// CORRECT
if ($account->hasPermission('edit articles')) {
  // Allow
}
```

### Not Setting `trusted_host_patterns`
**Why It's Wrong:** Cache poisoning, session hijacking via Host header injection.
**Impact:** Attacker can hijack sessions, poison caches.
**Correct Pattern:**
```php
// settings.php
$settings['trusted_host_patterns'] = [
  '^example\.com$',
  '^.+\.example\.com$',
];
```

### Implementing Security from Scratch
**Why It's Wrong:** Easy to make mistakes; Drupal's systems are peer-reviewed.
**Examples:** Custom CSRF tokens, custom session management, custom sanitization.
**Correct Pattern:** Use Drupal's built-in security APIs.

### Allowing Executable File Uploads
**Why It's Wrong:** Remote code execution.
**File Extensions to NEVER Allow:** .php, .phtml, .php3, .php4, .php5, .phar, .exe, .sh, .pl, .py, .cgi
**Correct Pattern:**
```php
'extensions' => 'jpg jpeg png gif pdf'  // Whitelist only
```

## Common Mistakes
- Treating security as a feature to add later -- Build it in from the start
- Only testing happy paths -- Test malicious input, unauthorized access
- Copying code from Stack Overflow without understanding -- Especially security code
- Assuming "it's validated" upstream -- Defense in depth; validate again
- Not reading security advisories -- Subscribe to https://www.drupal.org/security

## See Also
- [Best Practices and Patterns](best-practices-and-patterns.md) for what TO do
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal
