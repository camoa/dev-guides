---
description: Custom container compilation logic — compiler pass types and phases, processing tagged services, validating definitions, collecting service IDs, and core compiler passes.
---

# Compiler Passes

## When to Use

When you need custom processing of service definitions during container compilation — validate services, process custom tags, or modify the container graph.

## Compiler Pass Types

| Type | Phase | Purpose |
|------|-------|---------|
| TYPE_BEFORE_OPTIMIZATION | Early | Initial container manipulation before optimization |
| TYPE_OPTIMIZE | Middle (default) | Most passes run here — tag processing, validation |
| TYPE_BEFORE_REMOVING | Late | Before unused services are removed |
| TYPE_AFTER_REMOVING | Latest | Final cleanup after dead code elimination |

## Steps

1. **Create a compiler pass class**
   ```php
   namespace Drupal\my_module;

   use Symfony\Component\DependencyInjection\Compiler\CompilerPassInterface;
   use Symfony\Component\DependencyInjection\ContainerBuilder;

   class MyCompilerPass implements CompilerPassInterface {

     public function process(ContainerBuilder $container): void {
       // Find all services tagged with 'my_custom_tag'
       $tagged = $container->findTaggedServiceIds('my_custom_tag');

       foreach ($tagged as $id => $tags) {
         $definition = $container->getDefinition($id);
         // Process the service definition
         $definition->addMethodCall('setCustomProperty', ['value']);
       }
     }
   }
   ```

2. **Register the compiler pass in your service provider**
   ```php
   namespace Drupal\my_module;

   use Drupal\Core\DependencyInjection\ServiceProviderBase;
   use Drupal\Core\DependencyInjection\ContainerBuilder;
   use Symfony\Component\DependencyInjection\Compiler\PassConfig;

   class MyModuleServiceProvider extends ServiceProviderBase {

     public function alter(ContainerBuilder $container) {
       $container->addCompilerPass(
         new MyCompilerPass(),
         PassConfig::TYPE_OPTIMIZE
       );
     }
   }
   ```

## Core Compiler Passes

| Pass | Purpose |
|------|---------|
| TaggedHandlersPass | Process `service_collector` and `service_id_collector` tags |
| RegisterEventSubscribersPass | Register event subscribers |
| RegisterAccessChecksPass | Register access checkers |
| BackendCompilerPass | Process cache backend services |
| ModifyServiceDefinitionsPass | Allow service providers to alter services |

Reference: `/core/lib/Drupal/Core/CoreServiceProvider.php` (lines 67-99), `/core/lib/Drupal/Core/DependencyInjection/Compiler/`

## Pattern

**Validating Tagged Services**:
```php
public function process(ContainerBuilder $container): void {
  $tagged = $container->findTaggedServiceIds('my_validator');

  foreach ($tagged as $id => $tags) {
    $definition = $container->getDefinition($id);
    $class = $definition->getClass();

    if (!is_subclass_of($class, ValidatorInterface::class)) {
      throw new \LogicException(
        sprintf('Service "%s" must implement ValidatorInterface', $id)
      );
    }
  }
}
```

**Collecting Service IDs**:
```php
public function process(ContainerBuilder $container): void {
  if (!$container->has('my_module.manager')) {
    return;
  }

  $manager = $container->findDefinition('my_module.manager');
  $tagged = $container->findTaggedServiceIds('my_handler');

  $handler_ids = array_keys($tagged);
  $manager->setArgument(0, $handler_ids);
}
```

## Common Mistakes

- **Modifying services after removal passes** — Use TYPE_BEFORE_REMOVING if you need to prevent service removal
- **Not checking if service exists** — Always use `$container->has()` before `getDefinition()`
- **Heavy processing** — Compiler passes run at cache rebuild; keep them fast
- **Order assumptions** — Within same phase, pass order isn't guaranteed across modules
- **Forgetting cache rebuild** — Compiler passes only run at container compilation

## See Also

- [Service Providers & Altering](service-providers-and-altering.md)
- [Core Services Reference](core-services-reference.md)
- [TaggedHandlersPass.php](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!DependencyInjection!Compiler!TaggedHandlersPass.php/)
