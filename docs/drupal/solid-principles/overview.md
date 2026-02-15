---
description: How Drupal 11 architecture embodies SOLID principles - services, plugins, entities, forms, hooks
drupal_version: "11.x"
---

# SOLID in Drupal Overview

## When to Use

Understanding how Drupal's architecture embodies SOLID principles guides you to write code that aligns with core patterns rather than fighting them.

## Decision

| SOLID Principle | Drupal Manifestation | Core Example |
|---|---|---|
| Single Responsibility | Services handle one concern, hook classes organized by domain | `node.grant_storage` service |
| Open/Closed | Plugin system, hooks, events, config overrides | Block plugins, hook_alter() |
| Liskov Substitution | Entity hierarchy, form base classes, access results | ContentEntityBase -> Node |
| Interface Segregation | Role-specific interfaces, focused injection interfaces | EntityInterface, ContainerInjectionInterface |
| Dependency Inversion | Service container, dependency injection, interface-based services | core.services.yml definitions |

## Pattern

Drupal's architecture makes SOLID natural if you follow established patterns:

```php
// GOOD: Following Drupal's SOLID patterns
class MyService {
  public function __construct(
    private EntityTypeManagerInterface $entityTypeManager,
    private CacheBackendInterface $cache,
  ) {}
}

// Services defined in mymodule.services.yml
services:
  mymodule.my_service:
    class: Drupal\mymodule\MyService
    autowire: true
```

Reference: `/core/core.services.yml` for service definitions following DIP

## Common Mistakes

- Creating "god classes" that violate SRP -- controllers/services doing too much
- Using `\Drupal::service()` static calls -- violates DIP, prevents testability
- Modifying core/contrib code directly -- violates OCP, breaks upgrades
- Extending wrong form base class -- violates LSP behavioral contracts
- Fat interfaces requiring unused methods -- violates ISP, forces fake implementations

**WHY these matter:**

- **God classes** become unmaintainable -- 1000-line services are impossible to test, debug, or extend. One change breaks 10 features
- **Static service calls** make testing impossible -- can't mock dependencies, can't swap implementations, can't isolate behavior
- **Modifying core directly** destroys upgradeability -- patches get lost, security updates break your changes, merge conflicts everywhere
- **Wrong base class** creates broken inheritance -- FormBase methods don't work in ConfigFormBase context, validation breaks, config doesn't save
- **Fat interfaces** force fake implementations -- implementing 10 methods you don't use creates dead code, confuses developers, bloats classes

## See Also

- Reference: [Drupal API Best Practices](https://api.drupal.org/api/drupal/core!core.api.php/group/best_practices/11.x)
