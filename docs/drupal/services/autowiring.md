---
description: Using autowiring to automatically resolve constructor arguments from type hints — enabling autowire, creating aliases for ambiguous interfaces, and the Autowire attribute.
---

# Autowiring

## When to Use

When you want the container to automatically resolve constructor arguments based on type hints — reduces YAML boilerplate for services with many dependencies.

## Steps

1. **Enable autowiring for your service**
   ```yaml
   services:
     my_module.autowired_service:
       class: Drupal\my_module\AutowiredService
       autowire: true
   ```

   Or enable for all services in the file:
   ```yaml
   services:
     _defaults:
       autowire: true

     my_module.autowired_service:
       class: Drupal\my_module\AutowiredService
   ```

2. **Type-hint constructor parameters**
   ```php
   namespace Drupal\my_module;

   use Drupal\Core\Database\Connection;
   use Drupal\Core\Entity\EntityTypeManagerInterface;
   use Psr\Log\LoggerInterface;

   class AutowiredService {

     public function __construct(
       protected Connection $database,
       protected EntityTypeManagerInterface $entityTypeManager,
       protected LoggerInterface $logger,
     ) {}
   }
   ```

3. **For ambiguous interfaces, create aliases**
   ```yaml
   services:
     # Alias tells autowire which logger to inject
     Psr\Log\LoggerInterface: '@logger.channel.my_module'

     my_module.autowired_service:
       class: Drupal\my_module\AutowiredService
       autowire: true
   ```

4. **Use #[Autowire] attribute for specific parameters (Drupal 11+ / PHP 8.1+)**
   ```php
   use Symfony\Component\DependencyInjection\Attribute\Autowire;

   public function __construct(
     #[Autowire(service: 'logger.channel.my_module')]
     protected LoggerInterface $logger,
   ) {}
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Enabling autowire | Service has 5+ dependencies | Autowiring reduces YAML boilerplate |
| Enabling autowire | Dependencies are core services with clear type hints | Safe to autowire |
| Creating aliases | Multiple services implement same interface | Create alias for autowire to resolve |
| Using #[Autowire] | Only 1-2 params need explicit service ID | Use attribute instead of full alias definition |
| Choosing autowire vs explicit | Service is public API | Explicit arguments are clearer for documentation |

## Common Mistakes

- **Autowiring without type hints** — Autowiring requires typed constructor parameters; remove autowire or add types
- **Expecting autowire to work for scalars** — Autowiring only works for service objects, not strings/integers/parameters
- **Not creating aliases for ambiguous interfaces** — If 10 services implement `FooInterface`, autowire can't choose
- **Autowiring in performance-critical services** — Autowiring uses reflection; slight overhead (usually negligible)
- **Not testing container compilation** — Autowire failures only appear at cache rebuild; test in CI
- **Using autowire for contrib/community modules** — Stick to explicit arguments for public APIs; autowire is best for internal services

## See Also

- [Defining Services](defining-services.md)
- [Constructor Injection](constructor-injection.md)
- [AutowireTrait allows ContainerInjectionInterface classes to be autowired](https://www.drupal.org/node/3396179)
- [Services can be autowired](https://www.drupal.org/node/3218156)
