---
description: Security best practices - CSRF, XSS, SQL injection, and file upload security
drupal_version: "11.x"
---

# Security Best Practices

## CSRF Protection (Form Tokens)

**WHY CSRF Matters:** Attackers trick authenticated users into submitting forms without their knowledge. User logged into admin → visits attacker site → attacker's JavaScript submits delete form → content deleted without consent.

**Automatic Protection:**
- FormBuilder adds form_token (CSRF token unique per session)
- FormBuilder adds form_build_id (cache key)
- FormBuilder adds form_id (form identifier)
- Validation fails if token invalid/missing

**How It Works:**
```
1. Display form → Drupal generates token from:
   - User's session ID
   - Form ID
   - Private hash_salt
2. Token embedded as hidden field
3. Submit → FormValidator checks token
4. Invalid token → validation fails, no handlers run
5. Valid token → proceed
```

**Why Safe:** Attacker can't generate valid token without access to session ID, hash_salt, and cached form state.

**Never Bypass Tokens For:**
- User-submitted forms (account takeover possible)
- Forms modifying data (attacker can trigger actions)
- Forms with access restrictions (permission bypass)
- Forms in public pages (anonymous users vulnerable)

## Input Validation and Sanitization

**WHY Validation Matters:** Form API validation is your ONLY barrier between user input and database/filesystem/APIs. Skipping validation allows: SQL injection, XSS attacks, file traversal, API abuse, data corruption.

**Critical Rule: Never Trust User Input**

```php
// NEVER use directly:
$_POST, $_GET, $_REQUEST // Bypasses CSRF, no sanitization
$form_state->getUserInput() // Unsanitized raw input

// ALWAYS use:
$form_state->getValue('field') // CSRF validated, sanitized
```

**Validation Pattern:**
```php
public function validateForm(array &$form, FormStateInterface $form_state) {
  $value = $form_state->getValue('field');

  // Validate format (prevent "../../../etc/passwd")
  if (!preg_match('/^[a-z0-9]+$/', $value)) {
    $form_state->setErrorByName('field', $this->t('Invalid format.'));
  }

  // Validate range (prevent integer overflow)
  if ($value < 0 || $value > 100) {
    $form_state->setErrorByName('field', $this->t('Out of range.'));
  }

  // Validate uniqueness (prevent duplicates)
  $exists = $this->entityTypeManager
    ->getStorage('user')
    ->loadByProperties(['name' => $value]);
  if ($exists) {
    $form_state->setErrorByName('field', $this->t('Already taken.'));
  }
}
```

## XSS Prevention

**WHY XSS Matters:** Attackers inject JavaScript into pages viewed by others. Result: Session hijacking (steal admin cookies), phishing (fake login forms), malware distribution. One XSS = entire site compromised.

**Form API Auto-Escaping:**
- Render arrays: Automatically escaped via Twig
- t() function: Escapes by default with @ placeholder
- Form elements: Values auto-escaped on render

```php
// SAFE - automatic escaping
$form['field']['#title'] = $this->t('Title: @title', [
  '@title' => $user_input, // <script> becomes &lt;script&gt;
]);

// SAFE - plain text
$form['field']['#plain_text'] = $user_input; // Never interpreted as HTML

// SAFE - render element
$form['display'] = [
  '#type' => 'html_tag',
  '#tag' => 'div',
  '#value' => $user_input, // Auto-escaped
];

// UNSAFE - raw markup
$form['field']['#markup'] = '<div>' . $user_input . '</div>'; // XSS!

// UNSAFE - user input as translation source
$form['field']['#title'] = $this->t($user_input); // No escaping!
```

**XSS Checklist:**
- [ ] Never concatenate user input with HTML strings
- [ ] Always use t() placeholders (@, %, !)
- [ ] Use #plain_text for user-submitted content
- [ ] Never use Markup::create() with user input
- [ ] Use render arrays, not raw HTML

## SQL Injection Prevention

**WHY SQL Injection Matters:** Attackers execute arbitrary database queries. Result: Steal all data (emails, passwords), delete database, escalate privileges, read server files. One SQL injection = database completely compromised.

**CRITICAL: Form API Validation ≠ SQL Safety**

Validation checks business logic, NOT database safety. You MUST use parameterized queries even after validation.

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
// Attack: "'; DROP TABLE users; --"

// SAFEST - Entity Query (auto-parameterized + access control)
$query = \Drupal::entityQuery('node')
  ->condition('type', 'article')
  ->condition('title', $user_input) // Automatically parameterized
  ->accessCheck(TRUE); // Enforces permissions
$nids = $query->execute();
```

**SQL Injection Checklist:**
- [ ] NEVER concatenate user input into SQL
- [ ] ALWAYS use parameterized queries (:placeholder)
- [ ] Use Entity Query when possible
- [ ] Use Query Builder for complex queries
- [ ] Escape LIKE patterns with escapeLike()
- [ ] Whitelist field/table names (can't parameterize identifiers)
- [ ] Remember: Validation ≠ SQL safety

## File Upload Security

**WHY File Upload Security Matters:** Attackers upload "image.php.jpg" → Drupal stores as image.php → Attacker visits /sites/default/files/image.php → PHP executes → server compromised. One missing validator = complete takeover.

**Critical Rules:**
1. ALWAYS whitelist extensions (never blacklist)
2. ALWAYS set file size limits
3. ALWAYS use private:// for user uploads
4. NEVER trust client MIME type
5. NEVER allow .php .phtml .pl .py .cgi .exe

```php
// CORRECT - secure file upload
$form['file'] = [
  '#type' => 'managed_file',
  '#title' => $this->t('Upload Document'),
  '#upload_location' => 'private://uploads/', // CRITICAL: private
  '#upload_validators' => [
    'file_validate_extensions' => ['pdf doc docx'], // Whitelist
    'file_validate_size' => [5 * 1024 * 1024], // 5MB max
  ],
  '#description' => $this->t('Allowed: PDF, DOC, DOCX. Max 5MB.'),
];

// WRONG - missing validators
$form['file'] = [
  '#type' => 'managed_file',
  '#upload_location' => 'public://uploads/',
  // Missing #upload_validators = CRITICAL VULNERABILITY
];
```

**Public vs Private Storage:**

**public://** (sites/default/files/)
- Direct web access (Apache serves, no PHP)
- Use for: Site logos, CSS/JS, public downloads
- Access control: NONE
- Security risk: Executables can be executed

**private://** (sites/default/files/private/)
- Drupal access control required
- Use for: User documents, personal data, ALWAYS for user uploads
- Access control: hook_file_download() checks permissions
- Security: Even if PHP uploaded, served as download not executed

**File Upload Checklist:**
- [ ] #upload_validators ALWAYS present
- [ ] Extensions whitelisted (never empty)
- [ ] Size limit set (prevent DoS)
- [ ] private:// for user uploads
- [ ] No executable extensions
- [ ] Description tells user allowed types/size
- [ ] For images: Resolution limits

## Access Control

```php
// Form-level access
use Drupal\Core\Access\AccessResult;

public function access() {
  $account = \Drupal::currentUser();
  return AccessResult::allowedIfHasPermission($account, 'administer site');
}

// Element-level access
$form['admin_field']['#access'] = AccessResult::allowedIfHasPermission(
  $current_user,
  'administer site configuration'
);
```

## Common Mistakes

- **Wrong**: Trusting $_POST directly → **Right**: Use $form_state->getValue()
- **Wrong**: No file validators → **Right**: Always whitelist extensions
- **Wrong**: Concatenating user input in queries → **Right**: Use parameterized queries
- **Wrong**: Raw HTML with user input → **Right**: Use render arrays
- **Wrong**: Bypassing tokens → **Right**: Never disable for user forms

## See Also

- [Development Standards](development-standards.md)
- [File API Guide](https://www.drupal.org/docs/drupal-apis/file-api)
- Reference: [Drupal Security 2026](https://metadesignsolutions.com/drupal-security-best-practices-protecting-enterprise-websites-in-2026/)
- Reference: [CSRF Prevention](https://drupalzone.com/tutorial/drupal-form-api/82-preventing-csrf-attacks)
