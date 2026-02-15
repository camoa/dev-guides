---
description: Use the correct focused Drupal injection interface for dependency injection
drupal_version: "11.x"
---

# Injection Interfaces - Interface Segregation (ISP)

## When to Use

Drupal provides focused interfaces for dependency injection. Use ContainerInjectionInterface for static::create() factory method, or AutowireTrait for automatic dependency resolution.

## Decision

| Interface | Use when | Provides |
|---|---|---|
| ContainerInjectionInterface | Class needs DI factory | create(ContainerInterface $container) |
| ContainerFactoryPluginInterface | Plugin needs DI | create(ContainerInterface, array $config, $plugin_id, $plugin_definition) |
| AutowireTrait | Want autowiring in forms/controllers (Drupal 10.2+) | Automatic constructor injection |
| ServiceProviderInterface | Need to alter service container | register(ContainerBuilder), alter(ContainerBuilder) |

## Pattern

**GOOD: Focused injection interfaces (ISP)**

```php
// Forms with AutowireTrait (Drupal 10.2+)
class MyForm extends FormBase {
  use AutowireTrait;  // Provides create() - no manual DI code needed

  public function __construct(
    private EntityTypeManagerInterface $entityTypeManager,
    private ConfigFactoryInterface $configFactory,
  ) {}
}

// Plugins with ContainerFactoryPluginInterface
class MyBlock extends BlockBase implements ContainerFactoryPluginInterface {
  public static function create(ContainerInterface $container, array $config, $plugin_id, $plugin_definition) {
    return new static(
      $config,
      $plugin_id,
      $plugin_definition,
      $container->get('entity_type.manager')
    );
  }
}
```

**BAD: Fat injection interface (violates ISP)**

```php
// Hypothetical bad design
interface DrupalClassInterface {
  public static function create(ContainerInterface $container);  // Forms/controllers
  public static function create(ContainerInterface $container, array $config, $plugin_id, $plugin_definition);  // Plugins
  public function register(ContainerBuilder $builder);  // Service providers
  // Can't implement all of these in one class - conflicting signatures
}
```

Reference:

- `/core/lib/Drupal/Core/DependencyInjection/ContainerInjectionInterface.php` -- focused
- `/core/lib/Drupal/Core/DependencyInjection/AutowireTrait.php` -- autowiring
- `/core/lib/Drupal/Core/Plugin/ContainerFactoryPluginInterface.php` -- plugin-specific

## Common Mistakes

- Not using AutowireTrait in Drupal 10.2+ -- use trait. **WHY:** Manual create() is 5-10 lines of boilerplate; trait does it automatically
- Implementing ContainerInjectionInterface in plugins -- use ContainerFactoryPluginInterface. **WHY:** Plugin signature needs $config, $plugin_id, $plugin_definition; wrong interface breaks plugins
- Mixing constructor injection with setter injection inconsistently -- pick one pattern. **WHY:** Inconsistent patterns confuse developers, make testing harder
- Not type-hinting interfaces in constructor -- type-hint interfaces, not classes. **WHY:** Tight coupling to implementation; can't swap service, can't mock in tests

## See Also

- [Entity Interfaces](entity-interfaces-isp.md) for entity ISP patterns
- [Dependency Injection Patterns](dependency-injection-patterns-dip.md) for injection mechanics
- Reference: [AutowireTrait for DI](https://www.drupal.org/node/3396179)
