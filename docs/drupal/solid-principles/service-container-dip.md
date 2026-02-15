---
description: Use Drupal service container to depend on abstractions, not concrete implementations
drupal_version: "11.x"
---

# Service Container - Dependency Inversion (DIP)

## When to Use

The service container is Drupal's DIP foundation. Depend on abstractions (interfaces) defined in core.services.yml, not concrete implementations.

## Decision

| Dependency pattern | Good/Bad | Why |
|---|---|---|
| Constructor inject interface type-hint | Good | Follows DIP, testable, swappable |
| Type-hint concrete class | Bad | Tight coupling, can't swap implementation |
| Use `\Drupal::service()` | Bad | Static coupling, violates DIP, untestable |
| Define services in *.services.yml | Good | Container manages lifecycle |
| `new ClassName()` in business logic | Bad | Can't inject dependencies, hard to test |

## Pattern

**GOOD: Depending on abstraction (DIP)**

```yaml
# mymodule.services.yml
services:
  _defaults:
    autoconfigure: true

  mymodule.article_manager:
    class: Drupal\mymodule\ArticleManager
    autowire: true  # Automatically injects dependencies

  # Service alias for interface -> implementation
  Drupal\mymodule\ArticleManagerInterface: '@mymodule.article_manager'
```

```php
// Depend on interface, not implementation
class ArticleController extends ControllerBase {
  public function __construct(
    private ArticleManagerInterface $articleManager,  // Interface, not class
  ) {}
}
```

**BAD: Depending on concretions (violates DIP)**

```php
class ArticleController extends ControllerBase {
  public function build() {
    // Static call to container - violates DIP
    $manager = \Drupal::service('mymodule.article_manager');

    // Instantiating directly - violates DIP
    $helper = new ArticleHelper();

    // Type-hinting concrete class instead of interface
  }
}
```

Reference: `/core/core.services.yml` -- service definitions following DIP

## Common Mistakes

- Using `\Drupal::service()` static calls -- inject dependency. **WHY:** Can't swap implementation, can't mock in tests, hides dependencies
- Type-hinting concrete classes in constructor -- type-hint interface. **WHY:** Tight coupling; can't use service decorators, can't swap implementations
- Not defining service aliases for interfaces -- add alias in services.yml. **WHY:** Autowiring can't resolve interface to implementation without alias
- Creating objects with `new` in services/controllers -- inject as dependency. **WHY:** Hard to test, can't inject dependencies into created object

## See Also

- [Dependency Injection Patterns](dependency-injection-patterns-dip.md) for injection mechanics
- [Anti-Patterns](anti-patterns-dip.md) for what to avoid
- Reference: [Drupal Service Container Deep Dive](https://www.thedroptimes.com/65134/drupal-service-container-deep-dive-part-2-aliases-autowiring-and-named-arguments)
