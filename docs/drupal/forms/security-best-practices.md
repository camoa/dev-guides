---
description: Security best practices — CSRF, XSS, SQL injection, file uploads, access control
drupal_version: "11.x"
---

# Security Best Practices

### CSRF Protection (Form Tokens)

**WHY CSRF Protection Matters:**

Cross-Site Request Forgery (CSRF) attacks trick authenticated users into submitting forms without their knowledge. Without tokens, an attacker's site can submit forms to your site using the victim's session. Example: User is logged into your Drupal admin → visits attacker's site → attacker's JavaScript submits delete form using victim's session → content deleted without user consent.

**Automatic Token System:**
```
FormBuilder adds to all forms:
- form_token: CSRF token (unique per user session)
- form_build_id: Cache key (links to cached form state)
- form_id: Form identifier (prevents token reuse across forms)
```

**Token Validation Flow:**
```
1. User displays form → Drupal generates unique token based on:
   - User's session ID
   - Form ID
   - Private key (sites/default/settings.php hash_salt)
2. Token embedded in form as hidden field
3. User submits form → FormValidator checks form_token (line 110-120)
4. Compares submitted token against regenerated token using same inputs
5. Invalid/missing token → validation fails, no handlers run, error message
6. Valid token → proceed with validation/submission
```

**WHY This Works:** Attacker's site can't generate valid token because it doesn't have access to:
- User's session ID (httponly cookie)
- Drupal's private hash_salt
- Form state cached on server

**Reference Files:**
- Validator: `/web/core/lib/Drupal/Core/Form/FormValidator.php` lines 110-120
- Generator: `/web/core/lib/Drupal/Core/Access/CsrfTokenGenerator.php`
- Documentation: [CSRF Prevention with Form Tokens](https://drupalzone.com/tutorial/drupal-form-api/82-preventing-csrf-attacks)

**When Tokens Are NOT Added:**
```php
// Dangerous - avoid unless search form
$form['#token'] = FALSE; // WHY DANGEROUS: CSRF attacks work, any site can submit

// GET method forms (search only)
$form['#method'] = 'get'; // Auto-disables token
// WHY: GET should be idempotent (no side effects), tokens in URL leak via referer
```

**Never Bypass Tokens For:**
- User-submitted forms (WHY: Account takeover possible)
- Forms modifying data (WHY: Attacker can trigger actions)
- Forms with access restrictions (WHY: Permission bypass)
- Forms in public pages (WHY: Anonymous users still vulnerable)

### Input Validation and Sanitization

**WHY Validation Matters:**

Form API validation is your ONLY security barrier between user input and your database/filesystem/external APIs. Skipping validation or using wrong methods allows: SQL injection, XSS attacks, file system traversal, API abuse, data corruption.

**Critical Rule: Never Trust User Input**

```php
// NEVER use directly:
$_POST, $_GET, $_REQUEST // WHY: Bypasses CSRF check, no sanitization, validation skipped
$form_state->getUserInput() // WHY: Unsanitized raw input, bypasses element processing

// ALWAYS use:
$form_state->getValue('field_name') // WHY: CSRF validated, sanitized, processed by Form API
$form_state->getValues() // WHY: All values validated and sanitized
```

**What getUserInput() Bypasses:**
- CSRF token validation (security hole)
- Element #value_callback processing
- Element #process callbacks
- Sanitization via form elements

**When getUserInput() Is Needed (Rare):**
- Custom validation needs raw input to compare
- AJAX callbacks rebuilding form with errors
- NEVER for final processing - only for validation logic

**Validation in Handlers:**
```php
public function validateForm(array &$form, FormStateInterface $form_state) {
  $value = $form_state->getValue('field');

  // Validate format
  // WHY: Prevent malicious input like "../../../etc/passwd" in file paths
  if (!preg_match('/^[a-z0-9]+$/', $value)) {
    $form_state->setErrorByName('field', $this->t('Invalid format.'));
  }

  // Validate range
  // WHY: Prevent integer overflow, business logic violations
  if ($value < 0 || $value > 100) {
    $form_state->setErrorByName('field', $this->t('Out of range.'));
  }

  // Validate uniqueness
  // WHY: Prevent duplicate usernames, email addresses, machine names
  $exists = $this->entityTypeManager
    ->getStorage('user')
    ->loadByProperties(['name' => $value]);
  if ($exists) {
    $form_state->setErrorByName('field', $this->t('Username already taken.'));
  }
}
```

**Validation Best Practice:** Validate in validateForm(), sanitize automatically via getValue(), never trust $_POST.

**Reference:** [Drupal Security Best Practices 2026](https://metadesignsolutions.com/ensuring-top-notch-security-best-practices-for-protecting-your-drupal-site-in-2025-tips-from-a-leading-drupal-web-development-company/)

### XSS Prevention

**WHY XSS Prevention Matters:**

Cross-Site Scripting (XSS) allows attackers to inject JavaScript into pages viewed by other users. Result: Session hijacking (steal admin cookies), phishing (fake login forms), malware distribution, defacement. One XSS vulnerability = entire site compromised.

**Form API Auto-Escaping (Your Safety Net):**
```
Render arrays: Automatically escaped via Twig
t() function: Escapes by default with @ placeholder
Twig templates: Auto-escape enabled (can't be disabled)
Form elements: Values auto-escaped on render
```

**WHY Auto-Escaping Works:** Form API converts user input to safe HTML entities before output:
- `<script>` becomes `&lt;script&gt;` (displays as text, doesn't execute)
- `"` becomes `&quot;` (can't break out of attributes)
- All render arrays processed through XSS filter

**Safe Patterns:**
```php
// SAFE - automatic escaping via @ placeholder
$form['field']['#title'] = $this->t('Title: @title', [
  '@title' => $user_input, // <script> becomes &lt;script&gt;
]);

// SAFE - plain text (guaranteed no HTML interpretation)
$form['field']['#plain_text'] = $user_input;
// WHY SAFE: Renders as TextNode, browser never parses as HTML

// SAFE - filtered markup with text format
$form['markup'] = [
  '#type' => 'processed_text',
  '#text' => $user_input,
  '#format' => 'basic_html', // Drupal's input filter strips dangerous tags
];
// WHY SAFE: Xss::filterAdmin() removes <script>, <iframe>, event handlers

// SAFE - render element
$form['display'] = [
  '#type' => 'html_tag',
  '#tag' => 'div',
  '#value' => $user_input, // Auto-escaped
];
```

**Unsafe Patterns (DO NOT USE):**
```php
// UNSAFE - raw markup concatenation
$form['field']['#markup'] = '<div>' . $user_input . '</div>';
// WHY UNSAFE: User input "<script>alert('xss')</script>" executes as JavaScript

// UNSAFE - user input as translation source
$form['field']['#title'] = $this->t($user_input);
// WHY UNSAFE: User controls entire string, can inject HTML, no escaping

// UNSAFE - HTML in default value without sanitization
$form['field']['#default_value'] = '<script>alert("xss")</script>';
// WHY UNSAFE: Default values rendered without escaping in some widgets

// UNSAFE - Markup::create() with user input
$form['markup'] = [
  '#markup' => Markup::create('<div>' . $user_input . '</div>'),
];
// WHY UNSAFE: Markup::create() tells Drupal "this is safe, don't escape" - LIES!
```

**Correct Pattern for User Content:**
```php
$form['display'] = [
  '#type' => 'item',
  '#title' => $this->t('User submitted:'),
  '#plain_text' => $form_state->getValue('user_field'), // Guarantees safety
];
// WHY: #plain_text never interpreted as HTML, even if contains <script>
```

**XSS Security Checklist:**
- [ ] Never concatenate user input with HTML strings
- [ ] Always use t() placeholders (@, %, !) not string interpolation
- [ ] Use #plain_text for displaying user-submitted content
- [ ] Never use Markup::create() with user input
- [ ] Never put user input in #default_value without sanitization
- [ ] Use render arrays, not raw HTML strings

**Reference:** [Drupal Security Best Practices](https://kinematic.digital/index.php/2025/09/04/drupal-security/)

### SQL Injection Prevention

**WHY SQL Injection Matters:**

SQL injection allows attackers to execute arbitrary database queries. Result: Steal all user data (emails, passwords), delete entire database, escalate privileges (make themselves admin), read server files via SELECT INTO OUTFILE. One SQL injection = database completely compromised.

**CRITICAL: Form API Validation Does NOT Prevent SQL Injection**

This is a common misconception. validateForm() checks business logic, NOT database safety. You MUST use parameterized queries even after validation.

```php
// VALIDATED but still VULNERABLE:
public function validateForm(array &$form, FormStateInterface $form_state) {
  // Validation passed, but...
  if (strlen($form_state->getValue('name')) > 3) {
    // Still vulnerable to SQL injection in submit!
  }
}

public function submitForm(array &$form, FormStateInterface $form_state) {
  $name = $form_state->getValue('name'); // Validated but NOT SQL-safe
  // STILL VULNERABLE if concatenated in query
}
```

**Database API Usage:**
```php
// SAFE - parameterized query (prepared statement)
$result = \Drupal::database()->query(
  'SELECT * FROM {table} WHERE field = :value',
  [':value' => $user_input]
);
// WHY SAFE: Database driver escapes :value parameter, SQL parser treats as literal string

// UNSAFE - concatenated query (even if validated!)
$result = \Drupal::database()->query(
  "SELECT * FROM {table} WHERE field = '" . $user_input . "'"
);
// WHY UNSAFE: User input "'; DROP TABLE users; --" becomes SQL code, executes

// ATTACK EXAMPLE:
// User submits: admin' OR '1'='1
// Concatenated: SELECT * FROM {users} WHERE name = 'admin' OR '1'='1'
// Result: Returns ALL users (OR '1'='1' always true)
```

**Entity Query (Safest - Recommended):**
```php
$query = \Drupal::entityQuery('node')
  ->condition('type', 'article')
  ->condition('title', $user_input) // Automatically parameterized
  ->accessCheck(TRUE); // CRITICAL: Enforces access control
$nids = $query->execute();
// WHY SAFEST: Entity API auto-parameterizes AND enforces permissions
```

**Query Builder (Also Safe):**
```php
$query = \Drupal::database()->select('node_field_data', 'n')
  ->fields('n', ['nid', 'title'])
  ->condition('title', $user_input) // Parameterized automatically
  ->execute();
// WHY SAFE: Query builder auto-parameterizes all conditions
```

**Common Mistakes:**
```php
// WRONG - field name from user input (can't parameterize identifiers)
$field = $form_state->getValue('sort_field');
$query = "SELECT * FROM {table} ORDER BY :field"; // Doesn't work!
// FIX: Whitelist field names
$allowed = ['title', 'created', 'nid'];
$field = in_array($field, $allowed) ? $field : 'title';

// WRONG - LIKE with user input not escaped
$result = \Drupal::database()->query(
  "SELECT * FROM {table} WHERE field LIKE :pattern",
  [':pattern' => '%' . $user_input . '%']
);
// ATTACK: User submits "%", returns entire table
// FIX: Escape LIKE wildcards
$pattern = '%' . \Drupal::database()->escapeLike($user_input) . '%';
```

**SQL Injection Security Checklist:**
- [ ] NEVER concatenate user input into SQL strings
- [ ] ALWAYS use parameterized queries (:placeholder)
- [ ] Use Entity Query when possible (enforces access control)
- [ ] Use Query Builder for complex queries (auto-parameterizes)
- [ ] Escape LIKE patterns with escapeLike()
- [ ] Whitelist field/table names (can't parameterize identifiers)
- [ ] Remember: Validation ≠ SQL safety

**Reference:** [Drupal Security Best Practices](https://metadesignsolutions.com/ensuring-top-notch-security-best-practices-for-protecting-your-drupal-site-in-2025-tips-from-a-leading-drupal-web-development-company/)

### File Upload Security

**WHY File Upload Security Matters:**

File uploads are the #1 way attackers compromise Drupal sites. Scenario: Attacker uploads "image.php.jpg" → Drupal stores as image.php → Attacker visits https://yoursite.com/sites/default/files/image.php → PHP executes → attacker has shell access → entire server compromised. One missing extension validator = complete site takeover.

**Critical Security Rules:**
1. ALWAYS whitelist extensions (never blacklist)
2. ALWAYS set file size limits
3. ALWAYS use private:// for user uploads unless explicitly public
4. NEVER trust client MIME type (easily spoofed)
5. NEVER allow executable extensions (.php, .phtml, .pl, .py, .cgi, .exe)

**Managed File Element (Secure Pattern):**
```php
$form['file'] = [
  '#type' => 'managed_file',
  '#title' => $this->t('Upload Document'),
  '#upload_location' => 'private://uploads/', // CRITICAL: private, not public
  '#upload_validators' => [
    // CRITICAL: Whitelist only - never accept "all files"
    'file_validate_extensions' => ['pdf doc docx odt'], // No .php .exe .sh
    'file_validate_size' => [5 * 1024 * 1024], // 5MB limit - prevents DoS
    // For images only:
    'file_validate_image_resolution' => ['5000x5000'], // Prevent huge images
  ],
  '#description' => $this->t('Allowed: PDF, DOC, DOCX, ODT. Max 5MB.'),
];
// WHY SAFE: Extensions whitelisted, size limited, private storage, description informs user
```

**UNSAFE Patterns (DO NOT USE):**
```php
// WRONG - no extension validation = PHP upload possible
$form['file'] = [
  '#type' => 'managed_file',
  '#upload_location' => 'public://uploads/',
  // Missing #upload_validators = CRITICAL VULNERABILITY
];
// ATTACK: Upload shell.php, visit /sites/default/files/uploads/shell.php, control server

// WRONG - blacklist instead of whitelist
'file_validate_extensions' => ['exe com bat'], // What about .php .phtml .php5?
// FIX: Whitelist only safe types

// WRONG - public:// for user-uploaded files
'#upload_location' => 'public://documents/',
// WHY WRONG: Public files bypass access control, directly web-accessible
// FIX: Use private:// and implement access callback
```

**Upload Validators Explained:**
```
file_validate_extensions: Whitelist by extension (not MIME type)
  - WHY: MIME type spoofed easily ("image/jpeg" but actually PHP code)
  - Drupal checks actual extension, not client-provided MIME
  - Common safe: ['jpg jpeg png gif pdf doc docx xls xlsx']
  - NEVER include: ['php phtml php3 php4 php5 pl py cgi exe sh']

file_validate_size: Max bytes (int)
  - WHY: Prevent disk space DoS, upload timeout, memory exhaustion
  - Recommended: 5MB for documents, 10MB for images, 50MB for video
  - Example: 5 * 1024 * 1024 = 5242880 bytes

file_validate_image_resolution: ['MAXWIDTHxMAXHEIGHT', 'MINWIDTHxMINHEIGHT']
  - WHY: Huge images cause memory exhaustion (GD library)
  - Recommended max: ['5000x5000'] (25MP limit)
  - Optional min: ['100x100'] for profile pictures
```

**Public vs Private Storage:**
```
public:// (sites/default/files/)
  - Direct web access (Apache serves, no PHP)
  - Use for: Site logos, CSS/JS aggregates, public downloads
  - Access control: NONE - anyone with URL can download
  - Security risk: If executable uploaded, can be executed

private:// (sites/default/files/private/)
  - Drupal access control required
  - Use for: User documents, invoices, personal data
  - Access control: Drupal hook_file_download() checks permissions
  - Security: Even if PHP uploaded, never executed (served as download)
```

**Correct Upload Destination Decision:**
```
Public data (site logo, CSS)? → public://
User-submitted files? → private:// (ALWAYS)
Personal documents? → private://
Medical/financial records? → private:// + encrypt
Unknown use case? → private:// (safer default)
```

**File Upload Security Checklist:**
- [ ] #upload_validators ALWAYS present (never omit)
- [ ] Extensions whitelisted (never empty, never blacklist)
- [ ] Size limit set (prevent DoS)
- [ ] private:// for user uploads (not public://)
- [ ] No executable extensions (.php .pl .py .exe .sh .cgi .phtml)
- [ ] Description tells user allowed types/size
- [ ] For images: Resolution limits prevent memory exhaustion
- [ ] For private files: Implement hook_file_download() access check

**Advanced Security (If Needed):**
```php
// Rename uploaded files to prevent extension exploits
use Drupal\Core\File\FileSystemInterface;

$file = $form_state->getValue('file');
$file_path = $file_system->realpath($file->getFileUri());
$safe_name = md5($file->getFilename()) . '.pdf'; // Force extension
$file_system->move($file->getFileUri(), 'private://uploads/' . $safe_name);

// Scan with ClamAV (contrib module: clamav)
// Check file magic bytes match extension
// Implement hook_file_download() for private file access control
```

**Reference:**
- `/web/core/modules/file/src/Element/ManagedFile.php`
- [Drupal Security Best Practices](https://metadesignsolutions.com/ensuring-top-notch-security-best-practices-for-protecting-your-drupal-site-in-2025-tips-from-a-leading-drupal-web-development-company/)

### Access Control

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

**Common Mistakes:**
- Using #access without cache contexts (stale permissions)
- Bypassing access checks inappropriately
- Not checking access in custom submit handlers
- Assuming validation = access control (different concerns)

**See Also:**
- Access Control Guide
- File Security Guide
- XSS Prevention Guide
- Official: [Drupal Security Best Practices](https://metadesignsolutions.com/drupal-security-best-practices-protecting-enterprise-websites-in-2026/)
