---
description: Source code locations for DI components in Drupal core — key files, interfaces, traits, container components, compiler passes, example services, and documentation URLs.
---

# Code Reference Map

## When to Use

When you need to find the actual source code for services, interfaces, and DI components in Drupal core.

## Core DI Files

| File | Description | Key Contents |
|------|-------------|--------------|
| `/core/lib/Drupal.php` | Static service container wrapper | \Drupal::service(), \Drupal::database(), etc. |
| `/core/core.services.yml` | Core service definitions (2,035 lines) | All core services, parameters, defaults |
| `/core/lib/Drupal/Core/DrupalKernel.php` | Kernel, container initialization | Container build, service providers, bootstrap |
| `/core/lib/Drupal/Core/CoreServiceProvider.php` | Core service provider, compiler passes | All core compiler passes registered here |

## Interfaces

| Interface | Location | Purpose |
|---|---|---|
| ContainerInjectionInterface | `/core/lib/Drupal/Core/DependencyInjection/` | Controllers, forms DI pattern |
| ContainerFactoryPluginInterface | `/core/lib/Drupal/Core/Plugin/` | Plugins DI pattern |
| ServiceProviderInterface | `/core/lib/Drupal/Core/DependencyInjection/` | Service provider interface |
| ServiceModifierInterface | `/core/lib/Drupal/Core/DependencyInjection/` | Service alteration interface |

## Traits

| Trait | Location | Purpose |
|---|---|---|
| AutowireTrait | `/core/lib/Drupal/Core/DependencyInjection/` | Auto-generate create() method |
| DependencySerializationTrait | `/core/lib/Drupal/Core/DependencyInjection/` | Serialize/unserialize services safely |

## Container Components

| Component | Location |
|---|---|
| ContainerBuilder | `/core/lib/Drupal/Core/DependencyInjection/ContainerBuilder.php` |
| Container | `/core/lib/Drupal/Core/DependencyInjection/Container.php` |
| YamlFileLoader | `/core/lib/Drupal/Core/DependencyInjection/YamlFileLoader.php` |

## Compiler Passes

| Pass | Location | Purpose |
|---|---|---|
| TaggedHandlersPass | `/core/lib/Drupal/Core/DependencyInjection/Compiler/` | Process service_collector, service_id_collector |
| RegisterEventSubscribersPass | `/core/lib/Drupal/Core/DependencyInjection/Compiler/` | Register event subscribers |
| ModifyServiceDefinitionsPass | `/core/lib/Drupal/Core/DependencyInjection/Compiler/` | Allow service provider alterations |
| BackendCompilerPass | `/core/lib/Drupal/Core/DependencyInjection/Compiler/` | Process cache backends |

All compiler passes: `/core/lib/Drupal/Core/DependencyInjection/Compiler/` (32 files)

## Example Services Files

| Module | Location |
|---|---|
| System module | `/core/modules/system/system.services.yml` |
| Node module | `/core/modules/node/node.services.yml` |
| User module | `/core/modules/user/user.services.yml` |

## Example Service Classes

| Example | Location | Pattern |
|---|---|---|
| SystemController | `/core/modules/system/src/Controller/SystemController.php` | Controller DI |
| SystemBrandingBlock | `/core/modules/system/src/Plugin/Block/SystemBrandingBlock.php` | Plugin DI |
| LoggerChannelFactory | `/core/lib/Drupal/Core/Logger/LoggerChannelFactory.php` | Factory service |
| PathBasedBreadcrumbBuilder | `/core/modules/system/src/PathBasedBreadcrumbBuilder.php` | Tagged service (breadcrumb_builder) |

## Finding Services

**Search core.services.yml**:
```bash
grep -n "service_name:" /path/to/drupal/core/core.services.yml
```

**Find service class**:
```bash
grep -r "class: Drupal\\Core\\Database\\Connection" /path/to/drupal/core/core.services.yml
```

**Find all tagged services**:
```bash
grep -A2 "name: event_subscriber" /path/to/drupal/core/core.services.yml
```

## Documentation References

| Topic | URL |
|---|---|
| Services & DI overview | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection |
| Service file structure | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/structure-of-a-service-file |
| Service tags | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/service-tags |
| Dependency injection in forms | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-a-form |
| Dependency injection in plugins | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-plugin-block |
| Altering services | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/altering-existing-services-providing-dynamic-services |
| Subscribe to events | https://www.drupal.org/docs/develop/creating-modules/subscribe-to-and-dispatch-events |

## See Also

- [Security & Performance](security-and-performance.md)
