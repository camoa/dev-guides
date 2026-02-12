---
description: Development standards and anti-patterns — code quality, maintainability, best practices
drupal_version: "11.x"
---

# Development Standards & Anti-Patterns

**Purpose:** This section provides the "experienced developer perspective" - what a senior Drupal developer would tell you during code review. It explains not just WHAT to do, but WHY it matters and what breaks if you don't follow these patterns.

### Core Development Standards

**1. Always Use Dependency Injection via create()**

**WHY:** Breaks testability, violates SOLID principles, creates hidden dependencies, prevents service substitution.

```php
// WRONG - static service container calls
public function buildForm(array $form, FormStateInterface $form_state) {
  $config = \Drupal::config('mymodule.settings');
  $entity_manager = \Drupal::entityTypeManager();
  // Forms instantiated directly can't mock these services in tests
}

// CORRECT - dependency injection
protected $config;
protected $entityTypeManager;

public function __construct(ConfigFactoryInterface $config_factory, EntityTypeManagerInterface $entity_type_manager) {
  $this->config = $config_factory->get('mymodule.settings');
  $this->entityTypeManager = $entity_type_manager;
}

public static function create(ContainerInterface $container) {
  return new static(
    $container->get('config.factory'),
    $container->get('entity_type.manager')
  );
}
```

**What Breaks:** Unit tests fail (can't mock \Drupal::), service overrides ignored, hard to track dependencies.

**Reference:** [Mastering Dependency Injection](https://www.thedroptimes.com/54436/mastering-dependency-injection-in-drupal-best-practices-and-real-world-examples)

**2. Use #config_target for Config Forms (Drupal 10.2+)**

**WHY:** Reduces code, automatic validation, works outside forms (recipes, drush), prevents bugs from manual save logic.

```php
// OLD WAY - manual config management
public function buildForm(array $form, FormStateInterface $form_state) {
  $config = $this->config('mymodule.settings');
  $form['api_key'] = [
    '#type' => 'textfield',
    '#default_value' => $config->get('api_key'), // Manual get
  ];
}

public function submitForm(array &$form, FormStateInterface $form_state) {
  $this->config('mymodule.settings')
    ->set('api_key', $form_state->getValue('api_key')) // Manual set
    ->save();
}

// NEW WAY - declarative config binding
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['api_key'] = [
    '#type' => 'textfield',
    '#config_target' => 'mymodule.settings:api_key', // Auto sync
  ];
  // submitForm() not needed - automatic save
}
```

**What Breaks:** Manual save logic bugs (forgot to save, wrong key name, validation bypassed).

**Reference:** [#config_target Documentation](https://www.drupal.org/node/3373502)

**3. Use Proper Form Alter Hooks**

**WHY:** Performance - hook_form_alter() runs on EVERY form. Specific hooks run only when needed.

```php
// WRONG - runs on every single form submission sitewide
function mymodule_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  if ($form_id == 'user_login_form') {
    // Only need this for login form
  }
}

// CORRECT - runs only for specific form
function mymodule_form_user_login_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  // Runs ONLY for login form
}
```

**What Breaks:** Every form on site takes performance hit checking form_id unnecessarily.

**4. Validate by Element Name, Not Generic setError()**

**WHY:** Screen readers, proper focus, better UX, clearer error location for users.

```php
// WRONG - generic error, screen readers confused
$form_state->setError($form, $this->t('Something is wrong'));

// CORRECT - specific field error with focus
$form_state->setErrorByName('email', $this->t('Email address is invalid.'));
```

**What Breaks:** Accessibility failures, users can't find which field has error, focus doesn't jump to problem.

**5. Always Use Render Arrays, Never Raw HTML**

**WHY:** Bypasses security (XSS), theme layer (can't style), caching (breaks page cache), alters (other modules can't modify).

```php
// WRONG - XSS vulnerability, no theme integration
$form['markup'] = [
  '#markup' => '<div class="error">' . $user_input . '</div>',
];

// CORRECT - render array with proper escaping
$form['markup'] = [
  '#type' => 'html_tag',
  '#tag' => 'div',
  '#attributes' => ['class' => ['error']],
  '#value' => $user_input, // Auto-escaped
];

// OR use #plain_text for user content
$form['display'] = [
  '#plain_text' => $user_input, // Guaranteed safe
];
```

**What Breaks:** XSS attacks possible, can't theme, cache breaks, hook_form_alter() can't modify markup.

**6. Use Route Names for Redirects, Never Hardcoded Paths**

**WHY:** Routes can change, language prefix breaks paths, alias changes break hardcoded URLs.

```php
// WRONG - breaks if route changes or site has language prefixes
$form_state->setRedirectUrl(Url::fromUri('internal:/admin/content'));

// CORRECT - route name is stable contract
$form_state->setRedirect('system.admin_content');

// With parameters
$form_state->setRedirect('entity.node.canonical', ['node' => $nid]);
```

**What Breaks:** 404 errors when path changes, multilingual sites broken, no route-level access check.

**7. FormState Storage for Multi-Step, Not Class Properties**

**WHY:** Forms are stateless - new instance every request. Class properties lost between page loads.

```php
// WRONG - $this->step lost after page reload
protected $step = 1;

public function buildForm(array $form, FormStateInterface $form_state) {
  if ($this->step == 2) { // Always 1 on new request!
  }
}

// CORRECT - FormState persists with caching
public function buildForm(array $form, FormStateInterface $form_state) {
  $form_state->setCached(TRUE); // REQUIRED
  $step = $form_state->get('step') ?? 1;
  if ($step == 2) { // Correct value after rebuild
  }
}
```

**What Breaks:** Multi-step forms reset to step 1, user data lost, workflow breaks.

**8. Translation for All User-Facing Strings**

**WHY:** Multilingual sites broken, accessibility tools need proper language markup, professional requirement.

```php
// WRONG - English hardcoded
$form['submit'] = [
  '#type' => 'submit',
  '#value' => 'Save Configuration',
];

// CORRECT - translatable
$form['submit'] = [
  '#type' => 'submit',
  '#value' => $this->t('Save Configuration'),
];

// With placeholders (auto-escaped)
$message = $this->t('Updated @count items.', ['@count' => $count]);
```

**What Breaks:** Non-English sites show English text, translation teams can't find strings, fails accessibility audit.

### Critical Anti-Patterns

**Anti-Pattern 1: Business Logic in buildForm()**

**WHY:** buildForm() runs on EVERY form display including AJAX rebuilds, validation errors, multi-step navigation.

```php
// WRONG - API call on every rebuild
public function buildForm(array $form, FormStateInterface $form_state) {
  $data = $this->externalApi->fetchData(); // Runs on every AJAX callback!
  $form['field']['#options'] = $data;
}

// CORRECT - business logic in submit only
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['field']['#type'] = 'textfield'; // UI only
}

public function submitForm(array &$form, FormStateInterface $form_state) {
  $data = $this->externalApi->fetchData(); // Runs once on submit
  $this->processData($data);
}
```

**What Breaks:** Massive performance hit, timeout on slow APIs, unnecessary external calls, race conditions.

**Anti-Pattern 2: Using $_POST/$_GET/$_REQUEST**

**WHY:** Bypasses Form API security (CSRF token check skipped), no sanitization, validation bypassed.

```php
// WRONG - CSRF vulnerability, unsanitized
public function submitForm(array &$form, FormStateInterface $form_state) {
  $email = $_POST['email']; // NO VALIDATION, NO CSRF CHECK
}

// CORRECT - validated and sanitized
public function submitForm(array &$form, FormStateInterface $form_state) {
  $email = $form_state->getValue('email'); // Validated, sanitized, CSRF checked
}
```

**What Breaks:** CSRF attacks work, XSS possible, SQL injection if used in queries, validation bypassed.

**Anti-Pattern 3: Storing Objects in form_state**

**WHY:** Serialization fails on many objects, memory bloat in cache_form table, can't cache forms properly.

```php
// WRONG - objects don't serialize properly
$form_state->set('entity', $node); // Causes cache errors
$form_state->set('service', $this->myService); // Serialization fails

// CORRECT - store IDs only, load when needed
$form_state->set('entity_id', $node->id());

// Then in next step:
$nid = $form_state->get('entity_id');
$node = $this->entityTypeManager->getStorage('node')->load($nid);
```

**What Breaks:** "Cannot serialize" errors, cache_form table bloat, forms can't be cached properly.

**Anti-Pattern 4: Not Limiting File Upload Extensions**

**WHY:** PHP files uploaded = remote code execution, server compromised, data stolen.

```php
// WRONG - accepts ANY file type including .php
$form['file'] = [
  '#type' => 'managed_file',
  '#upload_location' => 'public://uploads/',
  // No validators = SECURITY HOLE
];

// CORRECT - whitelist safe extensions only
$form['file'] = [
  '#type' => 'managed_file',
  '#upload_location' => 'private://uploads/', // Not public for sensitive files
  '#upload_validators' => [
    'file_validate_extensions' => ['pdf doc docx'], // Whitelist only
    'file_validate_size' => [2 * 1024 * 1024], // 2MB max
  ],
];
```

**What Breaks:** Attackers upload .php files to public://, execute code, take over server.

**Anti-Pattern 5: Hardcoding Config/Entity IDs**

**WHY:** IDs change between environments (dev/staging/prod), import/export breaks, can't share code.

```php
// WRONG - node ID 42 doesn't exist on other environments
$node = Node::load(42);

// CORRECT - use machine names or lookups
$nodes = $this->entityTypeManager
  ->getStorage('node')
  ->loadByProperties(['title' => 'About Us', 'type' => 'page']);

// OR use config for reference
$config = $this->config('mymodule.settings');
$nid = $config->get('about_page_id');
```

**What Breaks:** Code works in dev, fails in production, deployments create different IDs, config import fails.

**Anti-Pattern 6: Using hook_init for Form-Specific Logic**

**WHY:** hook_init runs on EVERY page load sitewide, even pages that don't use your form.

```php
// WRONG - runs on every single page
function mymodule_init() {
  if (\Drupal::routeMatch()->getRouteName() == 'mymodule.form') {
    // Only needed on one form
  }
}

// CORRECT - only in form class
class MyForm extends FormBase {
  public function buildForm(array $form, FormStateInterface $form_state) {
    // Logic only runs when form is displayed
  }
}
```

**What Breaks:** Performance hit on every page, even /user/login, /admin, everywhere.

**Anti-Pattern 7: Forgetting Cache Contexts on Conditional Alters**

**WHY:** Cache serves same form to all users even when it should differ by role/permission.

```php
// WRONG - admin sees special field, cache serves it to anonymous users too
function mymodule_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  if (\Drupal::currentUser()->hasPermission('administer site')) {
    $form['admin_field'] = [...]; // Cached for anonymous users!
  }
}

// CORRECT - add cache context
function mymodule_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  if (\Drupal::currentUser()->hasPermission('administer site')) {
    $form['admin_field'] = [...];
  }
  $form['#cache']['contexts'][] = 'user.permissions'; // Vary cache by permission
}
```

**What Breaks:** Permission checks bypassed by cache, security leak, wrong UI shown to users.

### Development Standards Checklist

Use this checklist during code review:

- [ ] All services accessed via dependency injection (no \Drupal::)
- [ ] ConfigFormBase uses #config_target (Drupal 10.2+)
- [ ] Form alter uses specific hook (not generic hook_form_alter)
- [ ] Errors set with setErrorByName() not setError()
- [ ] All output via render arrays (no raw HTML concatenation)
- [ ] Redirects use route names (not hardcoded paths)
- [ ] Multi-step forms use FormState storage and setCached(TRUE)
- [ ] All user-facing strings use $this->t()
- [ ] No business logic in buildForm() (only UI definition)
- [ ] Never use $_POST/$_GET (always $form_state->getValue())
- [ ] File uploads have extension validators
- [ ] No hardcoded entity/config IDs
- [ ] Cache contexts added when form output varies by user/permission/config
- [ ] Forms are testable (dependency injection enables mocking)

**See Also:**
- Security Best Practices (next section)
- Performance Optimization
- Form Alter System
- Configuration API Guide
- Testing Forms Guide
