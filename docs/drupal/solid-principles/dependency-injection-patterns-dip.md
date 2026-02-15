---
description: Drupal dependency injection patterns - constructor injection, autowiring, service decorators
drupal_version: "11.x"
---

# Dependency Injection Patterns - DIP

## When to Use

Inject all dependencies through constructor. Use autowiring in Drupal 10.2+ to reduce boilerplate. Use service decorators to extend existing services.

## Decision

| Pattern | Use when | How |
|---|---|---|
| Constructor injection | Always for required dependencies | Type-hint in __construct() |
| Autowiring | Drupal 10.2+, own module services | `autowire: true` in services.yml |
| Manual DI | Need precise control, complex dependencies | Explicit arguments in services.yml |
| Service decorators | Extend existing service | `decorates:` key in services.yml |
| Setter injection | Optional dependencies (rare) | Setter methods, avoid if possible |

## Pattern

**GOOD: Constructor injection with autowiring**

```yaml
# mymodule.services.yml
services:
  _defaults:
    autoconfigure: true

  mymodule.node_publisher:
    class: Drupal\mymodule\NodePublisher
    autowire: true  # Auto-injects type-hinted dependencies
```

```php
class NodePublisher {
  public function __construct(
    private EntityTypeManagerInterface $entityTypeManager,
    private CurrentUserInterface $currentUser,
    private LoggerInterface $logger,
  ) {}
}
```

**GOOD: Service decorator (extending service without modification)**

```yaml
# mymodule.services.yml
services:
  mymodule.path_validator:
    class: Drupal\mymodule\CustomPathValidator
    decorates: path.validator
    arguments: ['@mymodule.path_validator.inner']
    decoration_priority: 5
```

```php
class CustomPathValidator implements PathValidatorInterface {
  public function __construct(
    private PathValidatorInterface $innerValidator,  // Original service
  ) {}

  public function isValid($path) {
    // Add custom logic before/after original
    $result = $this->innerValidator->isValid($path);
    // Custom processing
    return $result;
  }
}
```

**BAD: Static calls (violates DIP)**

```php
class NodePublisher {
  public function publish($nid) {
    // Static service calls
    $node = \Drupal::entityTypeManager()->getStorage('node')->load($nid);
    \Drupal::logger('mymodule')->notice('Published');
  }
}
```

Reference:

- `/core/modules/node/node.services.yml` -- autowire examples
- [Service Decorators](https://www.axelerant.com/blog/drupal-8-service-decorators)

## Common Mistakes

- Using `\Drupal::` static calls in services -- constructor injection. **WHY:** Static calls are global state; impossible to mock in tests, violates DIP
- Not using autowiring in Drupal 10.2+ -- enable autowiring. **WHY:** Manual DI is 10+ lines of boilerplate per service; autowiring does it automatically
- Setter injection for required dependencies -- constructor injection. **WHY:** Object in inconsistent state if setter not called; constructor ensures valid object
- Not using decoration_priority when multiple decorators -- set priority. **WHY:** Unpredictable decorator order; conflicts between modules
- Injecting too many services (>8) into one class -- refactor class, violates SRP. **WHY:** High dependency count indicates class doing too much

## See Also

- [Service Container](service-container-dip.md) for container architecture
- [Anti-Patterns](anti-patterns-dip.md) for patterns to avoid
- Reference: [Autowiring in Drupal](https://www.oliverdavies.uk/daily/2025/07/11/easier-dependency-injection-autowiring)
