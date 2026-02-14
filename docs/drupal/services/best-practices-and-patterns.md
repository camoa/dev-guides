---
description: Established Drupal community standards for services and DI — interface injection, constructor simplicity, autoconfigure, AutowireTrait, testing considerations, and performance patterns.
---

# Best Practices & Patterns

## When to Use

When you want to follow established Drupal community standards for services and dependency injection.

## Best Practices

| Practice | Rationale |
|---|---|
| **Inject interfaces, not concrete classes** | Allows service swapping, easier testing, follows SOLID |
| **Use constructor injection for required dependencies** | Explicit, immutable after instantiation, clear dependencies |
| **Use setter injection for optional dependencies** | Allows service to function without optional deps |
| **Never inject the entire container** | Service locator anti-pattern; hides dependencies |
| **Keep constructors simple** | Only assign dependencies; no logic, no method calls |
| **Type-hint all constructor parameters** | Enables autowiring, self-documenting, type safety |
| **Prefer `autoconfigure: true` in _defaults** | Automatic tagging reduces YAML boilerplate |
| **Use AutowireTrait for create() methods** | Eliminates repetitive create() boilerplate |
| **Make services immutable** | No setters for dependencies after construction (except optional deps) |
| **One responsibility per service** | SRP; if service does >1 thing, split it |
| **Document custom service tags** | Other devs need to know how to use your extensibility points |
| **Use semantic service IDs** | `my_module.node_manager` not `my_module.service1` |

## Dependency Injection Patterns

**Good**:
```php
class MyService {
  public function __construct(
    protected EntityTypeManagerInterface $entityTypeManager,  // Interface
    protected LoggerInterface $logger,  // Generic interface
  ) {}
}
```

**Bad**:
```php
class MyService {
  public function __construct(
    protected EntityTypeManager $entityTypeManager,  // Concrete class
    protected LoggerChannel $logger,  // Concrete class
    protected ContainerInterface $container,  // Container injection (anti-pattern)
  ) {}

  public function doSomething() {
    $db = $this->container->get('database');  // Service locator (anti-pattern)
  }
}
```

## Service Definition Best Practices

**Good**:
```yaml
services:
  _defaults:
    autoconfigure: true  # Auto-tag based on interfaces

  my_module.manager:
    class: Drupal\my_module\NodeManager
    arguments:
      - '@entity_type.manager'
      - '@logger.channel.my_module'
      - '%site.path%'
```

**Bad**:
```yaml
services:
  my_module.manager:
    class: Drupal\my_module\NodeManager
    arguments: ['@service_container']  # Container injection (anti-pattern)
    # Missing autoconfigure, manual tags needed
```

## Testing Considerations

- **Dependency injection makes testing easy** — Mock services in unit tests
- **\Drupal::service() makes testing hard** — Can't easily swap dependencies
- **Small, focused services are testable** — Large god-objects are not
- **Interfaces enable test doubles** — Can't mock final classes

## Performance Best Practices

- **Use lazy services for heavy dependencies** — `lazy: true` defers instantiation
- **Use tagged iterators over service_collector** — Lazy loading prevents eager instantiation
- **Don't inject rarely-used services** — Fetch on-demand via injected factory
- **Cache compiled container** — Production: ensure opcache is enabled, container is cached

Reference: [Mastering Dependency Injection in Drupal](https://www.thedroptimes.com/54436/mastering-dependency-injection-in-drupal-best-practices-and-real-world-examples)

## Common Mistakes

- **Over-engineering simple utilities** — Not everything needs to be a service; static helpers are fine for pure functions
- **Under-injecting** — Using \Drupal:: in classes that could use DI
- **Circular dependencies** — A depends on B, B depends on A; refactor shared logic to C
- **Forgetting cache rebuild** — Service changes require `drush cr`
- **Mixing concerns** — Services should have one clear responsibility

## See Also

- [Anti-Patterns & Common Mistakes](anti-patterns-and-common-mistakes.md)
- [Dependency Injection Best Practices](https://drupalize.me/topic/dependency-injection)
