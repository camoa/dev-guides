---
description: Common DI anti-patterns to avoid — container injection, constructor logic, \Drupal in classes, eager collection, concrete type hints, circular dependencies, public properties, and missing AutowireTrait.
---

# Anti-Patterns & Common Mistakes

## When to Use

When you want to avoid the most common mistakes developers make with Drupal services and dependency injection.

## Anti-Patterns

### 1. Container Injection (Service Locator)
**Anti-Pattern**:
```php
class MyService {
  public function __construct(
    protected ContainerInterface $container,
  ) {}

  public function doSomething() {
    $db = $this->container->get('database');  // BAD
    $logger = $this->container->get('logger.factory')->get('my_module');  // BAD
  }
}
```

**Correct**:
```php
class MyService {
  public function __construct(
    protected Connection $database,
    protected LoggerInterface $logger,
  ) {}

  public function doSomething() {
    $this->database->select(...);  // GOOD
    $this->logger->info('message');  // GOOD
  }
}
```

**Why**: Hides dependencies, makes testing harder, defeats the purpose of DI.

---

### 2. Logic in Constructors
**Anti-Pattern**:
```php
public function __construct(
  protected Connection $database,
) {
  $this->results = $this->database->query('SELECT * FROM {node}')->fetchAll();  // BAD
  $this->config = \Drupal::config('system.site');  // BAD
}
```

**Correct**:
```php
public function __construct(
  protected Connection $database,
  protected ConfigFactoryInterface $configFactory,
) {
  // Only assign dependencies — no logic
}

public function getResults() {
  return $this->database->query('SELECT * FROM {node}')->fetchAll();
}
```

**Why**: Constructors should only assign dependencies. Logic in constructors can cause issues during container compilation, testing, and service instantiation.

---

### 3. Using \Drupal in Classes
**Anti-Pattern**:
```php
class MyController extends ControllerBase {
  public function content() {
    $db = \Drupal::database();  // BAD
    $config = \Drupal::config('system.site');  // BAD
    return ['#markup' => 'Hello'];
  }
}
```

**Correct**:
```php
class MyController extends ControllerBase {
  use AutowireTrait;

  public function __construct(
    protected Connection $database,
    protected ConfigFactoryInterface $configFactory,
  ) {}

  public function content() {
    // Use $this->database, $this->configFactory
    return ['#markup' => 'Hello'];
  }
}
```

**Why**: \Drupal is for procedural code only. Classes should use dependency injection.

---

### 4. Eager Service Collection
**Anti-Pattern**:
```yaml
services:
  my_module.manager:
    tags:
      - { name: service_collector, tag: my_handler }  # Instantiates ALL handlers immediately
```

**Correct**:
```yaml
services:
  my_module.manager:
    arguments: [!tagged_iterator my_handler]  # Lazy — instantiates on iteration
```

**Why**: service_collector eagerly creates all tagged services. Use !tagged_iterator for lazy loading.

---

### 5. Not Type-Hinting Interfaces
**Anti-Pattern**:
```php
public function __construct(
  protected EntityTypeManager $entityTypeManager,  // Concrete class
  protected LoggerChannel $logger,  // Concrete class
) {}
```

**Correct**:
```php
public function __construct(
  protected EntityTypeManagerInterface $entityTypeManager,  // Interface
  protected LoggerInterface $logger,  // Interface
) {}
```

**Why**: Type-hinting interfaces allows service swapping, easier mocking, follows dependency inversion principle.

---

### 6. Circular Dependencies
**Anti-Pattern**:
```yaml
services:
  my_module.service_a:
    arguments: ['@my_module.service_b']

  my_module.service_b:
    arguments: ['@my_module.service_a']  # Circular dependency
```

**Solution**:
- Extract shared logic to a third service
- Use event system instead of direct dependency
- One service can use the other via factory or lazy proxy

**Why**: Container can't resolve circular dependencies; will throw exception.

---

### 7. Public Properties for Services
**Anti-Pattern**:
```php
class MyService {
  public Connection $database;  // BAD

  public function __construct(Connection $database) {
    $this->database = $database;
  }
}
```

**Correct**:
```php
class MyService {
  public function __construct(
    protected Connection $database,  // GOOD
  ) {}
}
```

**Why**: Services are internal dependencies; should be protected. Exposing them publicly invites misuse.

---

### 8. Not Using AutowireTrait
**Anti-Pattern**:
```php
class MyController extends ControllerBase implements ContainerInjectionInterface {

  public function __construct(
    protected Connection $database,
    protected LoggerInterface $logger,
  ) {}

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('database'),
      $container->get('logger.channel.my_module'),
    );
  }
}
```

**Correct**:
```php
class MyController extends ControllerBase {
  use AutowireTrait;  // Generates create() automatically

  public function __construct(
    protected Connection $database,
    protected LoggerInterface $logger,
  ) {}
}
```

**Why**: AutowireTrait eliminates boilerplate. Use it unless you need custom create() logic.

Reference: [Dependency injection anti-patterns in Drupal](https://mglaman.dev/blog/dependency-injection-anti-patterns-drupal)

## Common Mistakes

- **Forgetting cache rebuild** — Service changes require `drush cr`
- **Mixing procedural and OOP** — Hooks use \Drupal, classes use DI; don't mix
- **Over-complicating** — Not everything needs DI; simple value objects are fine as-is
- **Ignoring deprecation warnings** — Service deprecations will break in next major version
- **Testing in prod** — Validate service definitions work via automated tests

## See Also

- [Best Practices & Patterns](best-practices-and-patterns.md)
- [Security & Performance](security-and-performance.md)
