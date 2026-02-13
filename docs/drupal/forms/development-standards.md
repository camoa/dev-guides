---
description: Development standards and anti-patterns - opinionated best practices and critical mistakes to avoid
drupal_version: "11.x"
---

# Development Standards and Anti-Patterns

## Core Standards

### 1. Always Use Dependency Injection

**WHY:** Breaks testability, violates SOLID principles, creates hidden dependencies.

```php
// WRONG
public function buildForm(array $form, FormStateInterface $form_state) {
  $config = \Drupal::config('mymodule.settings');
  $entity_manager = \Drupal::entityTypeManager();
}

// CORRECT
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

**What breaks:** Unit tests fail, service overrides ignored, hard to track dependencies.

### 2. Use #config_target for Config Forms

**WHY:** Reduces code, automatic validation, works outside forms.

```php
// OLD WAY
public function buildForm(array $form, FormStateInterface $form_state) {
  $config = $this->config('mymodule.settings');
  $form['api_key']['#default_value'] = $config->get('api_key');
}
public function submitForm(array &$form, FormStateInterface $form_state) {
  $this->config('mymodule.settings')
    ->set('api_key', $form_state->getValue('api_key'))
    ->save();
}

// NEW WAY (Drupal 10.2+)
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['api_key'] = [
    '#type' => 'textfield',
    '#config_target' => 'mymodule.settings:api_key', // Auto sync
  ];
  // submitForm() not needed
}
```

**What breaks:** Manual save bugs, forgot to save, validation bypassed.

### 3. Use Specific Form Alter Hooks

**WHY:** Performance - hook_form_alter() runs on EVERY form.

```php
// WRONG
function mymodule_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  if ($form_id == 'user_login_form') { /* ... */ }
}

// CORRECT
function mymodule_form_user_login_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  // Runs ONLY for login form
}
```

**What breaks:** Every form on site takes performance hit.

### 4. Use Route Names for Redirects

**WHY:** Routes can change, language prefix breaks paths.

```php
// WRONG
$form_state->setRedirectUrl(Url::fromUri('internal:/admin/content'));

// CORRECT
$form_state->setRedirect('system.admin_content');
```

**What breaks:** 404 errors when path changes, multilingual sites broken.

### 5. FormState Storage for Multi-Step

**WHY:** Forms are stateless - new instance every request.

```php
// WRONG
protected $step = 1; // Lost after page reload

// CORRECT
public function buildForm(array $form, FormStateInterface $form_state) {
  $form_state->setCached(TRUE); // REQUIRED
  $step = $form_state->get('step') ?? 1;
}
```

**What breaks:** Multi-step forms reset to step 1, user data lost.

## Critical Anti-Patterns

### Anti-Pattern 1: Business Logic in buildForm()

**WHY:** buildForm() runs on EVERY display including AJAX, validation errors, multi-step navigation.

```php
// WRONG
public function buildForm(array $form, FormStateInterface $form_state) {
  $data = $this->externalApi->fetchData(); // Runs on every AJAX callback!
}

// CORRECT
public function submitForm(array &$form, FormStateInterface $form_state) {
  $data = $this->externalApi->fetchData(); // Runs once on submit
}
```

**What breaks:** Massive performance hit, timeout on slow APIs.

### Anti-Pattern 2: Using $_POST/$_GET

**WHY:** Bypasses Form API security (CSRF check skipped), no sanitization.

```php
// WRONG
$email = $_POST['email']; // NO VALIDATION, NO CSRF CHECK

// CORRECT
$email = $form_state->getValue('email'); // Validated, sanitized, CSRF checked
```

**What breaks:** CSRF attacks work, XSS possible, SQL injection if used in queries.

### Anti-Pattern 3: Storing Objects in FormState

**WHY:** Serialization fails, memory bloat in cache_form table.

```php
// WRONG
$form_state->set('entity', $node); // Cache errors

// CORRECT
$form_state->set('entity_id', $node->id());
// Then load when needed:
$node = $this->entityTypeManager->getStorage('node')->load($nid);
```

**What breaks:** "Cannot serialize" errors, forms can't cache.

### Anti-Pattern 4: Not Limiting File Extensions

**WHY:** PHP files uploaded = remote code execution.

```php
// WRONG
$form['file'] = [
  '#type' => 'managed_file',
  '#upload_location' => 'public://uploads/',
  // No validators = SECURITY HOLE
];

// CORRECT
$form['file'] = [
  '#type' => 'managed_file',
  '#upload_location' => 'private://uploads/',
  '#upload_validators' => [
    'file_validate_extensions' => ['pdf doc docx'],
    'file_validate_size' => [2 * 1024 * 1024], // 2MB
  ],
];
```

**What breaks:** Attackers upload .php files, execute code, take over server.

### Anti-Pattern 5: Hardcoding Entity IDs

**WHY:** IDs change between environments.

```php
// WRONG
$node = Node::load(42); // Doesn't exist on other environments

// CORRECT
$nodes = $this->entityTypeManager
  ->getStorage('node')
  ->loadByProperties(['title' => 'About Us', 'type' => 'page']);
```

**What breaks:** Code works in dev, fails in production.

### Anti-Pattern 6: No Cache Contexts on Conditional Alters

**WHY:** Cache serves same form to all users even when should differ.

```php
// WRONG
function mymodule_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  if (\Drupal::currentUser()->hasPermission('administer site')) {
    $form['admin_field'] = [...]; // Cached for anonymous!
  }
}

// CORRECT
function mymodule_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  if (\Drupal::currentUser()->hasPermission('administer site')) {
    $form['admin_field'] = [...];
  }
  $form['#cache']['contexts'][] = 'user.permissions';
}
```

**What breaks:** Permission checks bypassed by cache, security leak.

## Development Checklist

- [ ] All services via dependency injection (no \Drupal::)
- [ ] ConfigFormBase uses #config_target (Drupal 10.2+)
- [ ] Specific form alter hooks (not generic)
- [ ] Errors with setErrorByName() not setError()
- [ ] All output via render arrays (no raw HTML)
- [ ] Redirects use route names (not hardcoded paths)
- [ ] Multi-step uses FormState storage + setCached(TRUE)
- [ ] All user-facing strings use $this->t()
- [ ] No business logic in buildForm()
- [ ] Never use $_POST/$_GET
- [ ] File uploads have extension validators
- [ ] No hardcoded entity/config IDs
- [ ] Cache contexts when output varies by user/permission
- [ ] Forms are testable (DI enables mocking)

## See Also

- [Security Best Practices](security-best-practices.md)
- [Performance Optimization](performance-optimization.md)
- [Form Alter System](form-alter-system.md)
- Reference: [Dependency Injection](https://www.thedroptimes.com/54436/mastering-dependency-injection-in-drupal-best-practices-and-real-world-examples)
