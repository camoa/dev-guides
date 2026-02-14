---
description: Foundation of Drupal services and dependency injection — what they are, when to use DI vs static helpers, and basic service definition patterns.
---

# Services & DI Overview

## When to Use

When you need to understand the foundation of modern Drupal architecture — services provide reusable functionality, dependency injection eliminates hard-coded dependencies.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Reusable functionality across modules | Service definition in *.services.yml | Single instance, shared state, testable |
| Access to Drupal APIs (database, cache, config) | Inject service dependencies | Decoupled, mockable in tests, follows SOLID principles |
| Procedural code (hooks, .module files) | \Drupal::service() static helper | Only option in procedural context, fallback pattern |
| Class-based code (controllers, forms, plugins) | Constructor injection via create() | Best practice, explicit dependencies, autowire-compatible |

## Pattern

**Service Definition (my_module.services.yml)**:
```yaml
services:
  my_module.example:
    class: Drupal\my_module\ExampleService
    arguments: ['@database', '@logger.factory']
```

**Using the Service**:
```php
// In a controller with DI
$this->exampleService->doSomething();

// In procedural code
\Drupal::service('my_module.example')->doSomething();
```

Reference: `/core/core.services.yml` (2,035 service definitions), `/core/lib/Drupal.php`

## Common Mistakes

- **Using \Drupal:: in classes** — Inject services via constructor; only use \Drupal in hooks
- **Defining services for simple value objects** — Services are for shared, stateful functionality, not DTOs
- **Injecting the entire container** — Inject only what you need; container injection is an anti-pattern
- **Over-engineering with services** — Not everything needs to be a service; static utility methods are fine for pure functions
- **Forgetting to rebuild cache after adding services** — Run `drush cr` after adding/modifying *.services.yml files

## See Also

- [Service Container Architecture](service-container-architecture.md)
- [Drupal Services & Dependency Injection documentation](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/services-and-dependency-injection-in-drupal)
