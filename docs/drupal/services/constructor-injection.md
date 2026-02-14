---
description: Injecting services into controllers and forms via ContainerInjectionInterface — the create() pattern, AutowireTrait shortcut, and form injection examples.
---

# Constructor Injection (ContainerInjectionInterface)

## When to Use

When injecting services into controllers, forms, or any class that implements `ContainerInjectionInterface` — the standard Drupal dependency injection pattern.

## Steps

1. **Implement ContainerInjectionInterface**
   ```php
   namespace Drupal\my_module\Controller;

   use Drupal\Core\Controller\ControllerBase;
   use Drupal\Core\DependencyInjection\ContainerInjectionInterface;
   use Symfony\Component\DependencyInjection\ContainerInterface;
   use Drupal\Core\Database\Connection;
   use Psr\Log\LoggerInterface;

   class MyController extends ControllerBase implements ContainerInjectionInterface {

     public function __construct(
       protected Connection $database,
       protected LoggerInterface $logger,
     ) {}

     public static function create(ContainerInterface $container) {
       return new static(
         $container->get('database'),
         $container->get('logger.channel.my_module'),
       );
     }

     public function content() {
       $this->logger->info('Controller accessed');
       return ['#markup' => 'Hello'];
     }
   }
   ```

2. **Use AutowireTrait for automatic create() (Drupal 10.2+)**
   ```php
   namespace Drupal\my_module\Controller;

   use Drupal\Core\Controller\ControllerBase;
   use Drupal\Core\DependencyInjection\AutowireTrait;
   use Drupal\Core\Database\Connection;
   use Psr\Log\LoggerInterface;

   class MyController extends ControllerBase {

     use AutowireTrait;  // Provides create() automatically

     public function __construct(
       protected Connection $database,
       protected LoggerInterface $logger,
     ) {}

     public function content() {
       return ['#markup' => 'Hello'];
     }
   }
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing injection method | Class is a controller or form | Implement ContainerInjectionInterface |
| Choosing injection method | Class is a plugin | Use ContainerFactoryPluginInterface (see [Plugin Injection](plugin-injection.md)) |
| Writing create() method | You have many dependencies | Use AutowireTrait to reduce boilerplate |
| Writing create() method | You want explicit clarity | Manual create() shows exactly what's injected |

## Pattern

**Form Example**:
```php
namespace Drupal\my_module\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\DependencyInjection\ContainerInjectionInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\Core\Config\ConfigFactoryInterface;

class MyForm extends FormBase implements ContainerInjectionInterface {

  public function __construct(
    protected ConfigFactoryInterface $configFactory,
  ) {}

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('config.factory'),
    );
  }

  public function getFormId() {
    return 'my_module_my_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $config = $this->configFactory->get('my_module.settings');
    // ...
  }
}
```

Reference: `/core/lib/Drupal/Core/DependencyInjection/ContainerInjectionInterface.php`, `/core/modules/system/src/Controller/SystemController.php` (example)

## Common Mistakes

- **Not calling parent constructor** — If extending ControllerBase/FormBase with own __construct, parent may have protected properties you break
- **Type hinting Container instead of ContainerInterface** — Use the interface for testability
- **Static property assignment in create()** — create() must return a NEW instance, not modify static state
- **Putting logic in __construct** — Keep constructors simple; only assign dependencies to properties
- **Not using AutowireTrait when available** — Why write boilerplate when AutowireTrait generates create() for you?

## See Also

- [Autowiring](autowiring.md)
- [Plugin Injection](plugin-injection.md)
- [Dependency Injection in a form](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-a-form)
- [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection)
