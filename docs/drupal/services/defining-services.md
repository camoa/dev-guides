---
description: Step-by-step guide to registering a new service — creating the class, writing the YAML definition, clearing cache, and choosing service IDs and visibility.
---

# Defining Services

## When to Use

When you need to register a new service with the Drupal container.

## Steps

1. **Create the service class**
   ```php
   // src/MyService.php
   namespace Drupal\my_module;

   use Drupal\Core\Database\Connection;
   use Psr\Log\LoggerInterface;

   class MyService {

     public function __construct(
       protected Connection $database,
       protected LoggerInterface $logger,
     ) {}

     public function doSomething() {
       $this->logger->info('Doing something');
     }
   }
   ```

2. **Define the service in my_module.services.yml**
   ```yaml
   services:
     my_module.my_service:
       class: Drupal\my_module\MyService
       arguments: ['@database', '@logger.channel.my_module']
   ```

3. **Clear cache to register the service**
   ```bash
   drush cr
   ```

4. **Use the service**
   ```php
   // Via dependency injection (preferred)
   $service = $container->get('my_module.my_service');

   // Via static helper (procedural code only)
   $service = \Drupal::service('my_module.my_service');
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Defining service ID | Service is public API | Use semantic name: `my_module.manager` |
| Defining service ID | Service is internal | Use FQCN or `my_module.internal.name` |
| Choosing arguments | Dependency is required | Constructor injection via `arguments:` |
| Choosing arguments | Dependency is optional | Setter injection via `calls:` |
| Setting public/private | Service used by other modules | `public: true` (default) |
| Setting public/private | Service is internal to module | `public: false` |

## Common Mistakes

- **Not clearing cache after adding service** — Service won't be available until cache rebuild
- **Circular dependencies** — Service A depends on B, B depends on A (container will throw exception)
- **Injecting deprecated services** — Check for deprecation notices; use modern replacements
- **Mixing public and private concerns** — Keep public API services separate from internal implementation services
- **Not using interfaces** — Type-hint against interfaces (`LoggerInterface`) not concrete classes for flexibility

## See Also

- [Autowiring](autowiring.md)
- [Services and dependency injection in Drupal](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/services-and-dependency-injection-in-drupal)
