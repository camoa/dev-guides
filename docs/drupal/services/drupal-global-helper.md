---
description: When to use the \Drupal static helper vs dependency injection — acceptable uses in procedural code, refactoring patterns, and anti-pattern examples.
---

# The \Drupal Global Helper

## When to Use

When you understand when the \Drupal static helper is appropriate versus when dependency injection is required.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Service access in class (controller, form, plugin) | Constructor injection | Testable, explicit dependencies, follows best practices |
| Service access in hook (procedural .module code) | \Drupal::service() | No other option in procedural context |
| Quick prototyping or debugging | \Drupal::service() | Fast, but refactor to DI before committing |
| Legacy code modernization | \Drupal::service() to DI refactor | Temporary bridge pattern |
| Service access in static utility class | \Drupal::service() | If class is truly stateless helpers, acceptable compromise |

## Pattern

**Acceptable \Drupal Usage (Procedural Code)**:
```php
// my_module.module
function my_module_cron() {
  $database = \Drupal::database();
  $database->delete('my_table')
    ->condition('created', strtotime('-30 days'), '<')
    ->execute();
}
```

**Refactoring to DI**:
```php
// Before: Controller using \Drupal
class MyController extends ControllerBase {
  public function content() {
    $database = \Drupal::database();
    $results = $database->query('SELECT * FROM {my_table}')->fetchAll();
    return ['#markup' => count($results)];
  }
}

// After: Controller with DI
class MyController extends ControllerBase {
  use AutowireTrait;

  public function __construct(
    protected Connection $database,
  ) {}

  public function content() {
    $results = $this->database->query('SELECT * FROM {my_table}')->fetchAll();
    return ['#markup' => count($results)];
  }
}
```

Reference: `/core/lib/Drupal.php` (lines 1-73 explain the philosophy)

## Common Mistakes

- **Using \Drupal in __construct()** — Constructor runs before container is available; inject dependencies instead
- **Using \Drupal:: in tests** — Mocking \Drupal is difficult; inject services for testability
- **Cargo-culting \Drupal usage** — Just because you see it in legacy code doesn't mean it's the right pattern today
- **Not understanding the performance cost** — \Drupal::service() is fast enough, but explicit injection is clearer and eliminates lookups
- **Defending \Drupal as "simpler"** — Short-term simplicity creates long-term technical debt; DI is worth the small upfront cost

## Anti-Pattern Examples

**Don't do this**:
```php
// Anti-pattern: \Drupal in a service
class MyService {
  public function doSomething() {
    $config = \Drupal::config('my_module.settings');  // BAD
    $database = \Drupal::database();  // BAD
  }
}

// Correct: Inject dependencies
class MyService {
  public function __construct(
    protected ConfigFactoryInterface $configFactory,
    protected Connection $database,
  ) {}

  public function doSomething() {
    $config = $this->configFactory->get('my_module.settings');
    // Use $this->database
  }
}
```

## See Also

- [Plugin Injection](plugin-injection.md)
- [Service Tags](service-tags.md)
- [Dependency injection anti-patterns in Drupal](https://mglaman.dev/blog/dependency-injection-anti-patterns-drupal)
