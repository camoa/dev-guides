---
description: How Drupal's service container works — lifecycle phases, lazy instantiation, compilation vs runtime, and the role of ServiceProviders and compiler passes.
---

# Service Container Architecture

## When to Use

When you need to understand how Drupal's service container works under the hood — essential for debugging, optimization, and advanced patterns.

## Decision

| Component | Purpose | When It Runs |
|---|---|---|
| ServiceProviderInterface | Register new services programmatically | Container compilation (cache rebuild) |
| ServiceModifierInterface | Alter existing service definitions | Container compilation, after all services registered |
| Compiler passes | Process tagged services, validate definitions | Container compilation, multiple phases |
| ContainerBuilder | Build the service container from YAML + providers | Cache rebuild, install, update |
| Container (compiled) | Runtime service instantiation and dependency resolution | Every request |

## Pattern

**Container Lifecycle**:
```php
// 1. DrupalKernel initializes container
// 2. Load all *.services.yml files
// 3. Execute service providers (register phase)
// 4. Execute service providers (alter phase)
// 5. Execute compiler passes
// 6. Compile container to PHP code
// 7. Cache compiled container
// 8. Runtime: load cached container, instantiate services on-demand
```

**The container uses lazy instantiation** — services are only created when first requested, not at container build time.

Reference: `/core/lib/Drupal/Core/DrupalKernel.php`, `/core/lib/Drupal/Core/DependencyInjection/ContainerBuilder.php`

## Common Mistakes

- **Assuming container is available everywhere** — Container isn't initialized during install, some bootstrap phases
- **Modifying services after container compilation** — Changes to *.services.yml require cache rebuild
- **Expecting services to be singletons without 'shared: false'** — Services are shared (singleton) by default in Drupal
- **Not understanding compilation vs runtime** — Service providers run at compile time, services instantiate at runtime
- **Forgetting Symfony versioning** — Drupal 10 = Symfony 6.x, Drupal 11 = Symfony 7.x (check Symfony docs for version-specific features)

## See Also

- [Services & DI Overview](services-di-overview.md)
- [services.yml Schema](services-yml-schema.md)
- [Concept: Services and the Container](https://drupalize.me/tutorial/concept-services-and-container)
