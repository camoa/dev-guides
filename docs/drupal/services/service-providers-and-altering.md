---
description: Altering existing services and adding services programmatically — ServiceProviderBase, alter() vs register(), decorating services, conditional registration, and compiler pass integration.
---

# Service Providers & Altering

## When to Use

When you need to alter existing service definitions, add new services programmatically, or register compiler passes — advanced container manipulation beyond YAML.

## Steps

1. **Create a service provider class**
   ```php
   // src/MyModuleServiceProvider.php
   namespace Drupal\my_module;

   use Drupal\Core\DependencyInjection\ContainerBuilder;
   use Drupal\Core\DependencyInjection\ServiceProviderBase;

   class MyModuleServiceProvider extends ServiceProviderBase {

     public function alter(ContainerBuilder $container) {
       // Alter existing service definitions
       if ($container->hasDefinition('path_alias.manager')) {
         $definition = $container->getDefinition('path_alias.manager');
         $definition->setClass('Drupal\my_module\MyCustomAliasManager');
       }
     }

     public function register(ContainerBuilder $container) {
       // Register new services (alternative to YAML)
       $container->register('my_module.dynamic_service', 'Drupal\my_module\DynamicService')
         ->addArgument('@database');
     }
   }
   ```

2. **File naming convention**
   - File: `src/MyModuleServiceProvider.php` (camel case module name + ServiceProvider)
   - Class: `Drupal\my_module\MyModuleServiceProvider`
   - Extends: `ServiceProviderBase`

3. **No registration needed** — Drupal auto-discovers ServiceProvider classes

4. **Clear cache to activate** — Service providers only run during container compilation
   ```bash
   drush cr
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing alter vs register | Modifying existing service | Use `alter()` |
| Choosing alter vs register | Adding new service | Use `register()` or YAML (prefer YAML) |
| Modifying service definition | Changing class | `$definition->setClass()` |
| Modifying service definition | Adding argument | `$definition->addArgument()` |
| Modifying service definition | Changing argument | `$definition->setArgument(index, value)` |
| Adding compiler pass | Need custom tag processing | Register in `alter()` with `$container->addCompilerPass()` |

## Pattern

**Decorating a Service**:
```php
public function alter(ContainerBuilder $container) {
  $definition = $container->getDefinition('entity_type.manager');
  $definition->setClass('Drupal\my_module\MyEntityTypeManager')
    ->setDecoratedService('entity_type.manager');
}
```

**Adding a Compiler Pass**:
```php
use Drupal\my_module\MyCompilerPass;
use Symfony\Component\DependencyInjection\Compiler\PassConfig;

public function alter(ContainerBuilder $container) {
  $container->addCompilerPass(new MyCompilerPass(), PassConfig::TYPE_OPTIMIZE);
}
```

**Conditional Service Registration**:
```php
use Drupal\Core\Site\Settings;

public function register(ContainerBuilder $container) {
  if (Settings::get('my_feature_enabled')) {
    $container->register('my_module.feature', 'Drupal\my_module\Feature');
  }
}
```

Reference: `/core/lib/Drupal/Core/CoreServiceProvider.php`, [Altering existing services](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/altering-existing-services-providing-dynamic-services)

## Common Mistakes

- **Wrong file name** — Must be `[ModuleName]ServiceProvider.php` in camel case
- **Altering in register() instead of alter()** — Use `register()` for new services, `alter()` for modifying existing
- **Not clearing cache** — Service providers only run at container compilation
- **Over-using service providers** — Prefer YAML for static service definitions; use providers for dynamic/conditional logic only
- **Modifying core services without understanding impact** — Changing core services can break other modules; test thoroughly
- **Assuming execution order** — Can't control order of service providers across modules; use compiler passes for ordered operations

## See Also

- [Event Subscribers](event-subscribers.md)
- [Compiler Passes](compiler-passes.md)
- [Altering existing services](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/altering-existing-services-providing-dynamic-services)
- [Deep Dive into Drupal's Service Container](https://www.thedroptimes.com/55750/deep-dive-drupals-service-container-tags-compiler-passes-providers-and-autoconfiguration)
