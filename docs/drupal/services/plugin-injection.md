---
description: Injecting services into Drupal plugins (blocks, field formatters, widgets) via ContainerFactoryPluginInterface — parameter order, parent constructors, and formatter examples.
---

# Plugin Injection (ContainerFactoryPluginInterface)

## When to Use

When injecting services into plugins (blocks, field formatters, field widgets, condition plugins, etc.) — plugins receive additional arguments (configuration, plugin_id, plugin_definition) that must be handled.

## Steps

1. **Implement ContainerFactoryPluginInterface**
   ```php
   namespace Drupal\my_module\Plugin\Block;

   use Drupal\Core\Block\BlockBase;
   use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
   use Symfony\Component\DependencyInjection\ContainerInterface;
   use Drupal\Core\Database\Connection;
   use Psr\Log\LoggerInterface;

   /**
    * @Block(
    *   id = "my_module_example",
    *   admin_label = @Translation("Example Block"),
    * )
    */
   class ExampleBlock extends BlockBase implements ContainerFactoryPluginInterface {

     public function __construct(
       array $configuration,
       $plugin_id,
       $plugin_definition,
       protected Connection $database,
       protected LoggerInterface $logger,
     ) {
       parent::__construct($configuration, $plugin_id, $plugin_definition);
     }

     public static function create(
       ContainerInterface $container,
       array $configuration,
       $plugin_id,
       $plugin_definition
     ) {
       return new static(
         $configuration,
         $plugin_id,
         $plugin_definition,
         $container->get('database'),
         $container->get('logger.channel.my_module'),
       );
     }

     public function build() {
       return ['#markup' => 'Hello'];
     }
   }
   ```

2. **Constructor Parameter Order**:
   - **First 3 params**: `$configuration`, `$plugin_id`, `$plugin_definition` (in that order)
   - **Remaining params**: Your injected services
   - **Call parent::__construct()** with first 3 params

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing parameter order | Always | Put $configuration, $plugin_id, $plugin_definition first (required) |
| Calling parent constructor | Plugin extends base class (BlockBase, FormatterBase) | Call parent::__construct() with plugin params |
| Adding services | Service is required for plugin functionality | Inject via constructor |
| Adding services | Service is optional or rarely used | Inject or use \Drupal::service() in method (less ideal) |

## Pattern

**Field Formatter Example**:
```php
namespace Drupal\my_module\Plugin\Field\FieldFormatter;

use Drupal\Core\Field\FormatterBase;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\Core\Entity\EntityTypeManagerInterface;

/**
 * @FieldFormatter(
 *   id = "my_custom_formatter",
 *   label = @Translation("My Custom Formatter"),
 *   field_types = {"string"}
 * )
 */
class MyCustomFormatter extends FormatterBase implements ContainerFactoryPluginInterface {

  public function __construct(
    $plugin_id,
    $plugin_definition,
    $field_definition,
    array $settings,
    $label,
    $view_mode,
    array $third_party_settings,
    protected EntityTypeManagerInterface $entityTypeManager,
  ) {
    parent::__construct(
      $plugin_id,
      $plugin_definition,
      $field_definition,
      $settings,
      $label,
      $view_mode,
      $third_party_settings
    );
  }

  public static function create(
    ContainerInterface $container,
    array $configuration,
    $plugin_id,
    $plugin_definition
  ) {
    return new static(
      $plugin_id,
      $plugin_definition,
      $configuration['field_definition'],
      $configuration['settings'],
      $configuration['label'],
      $configuration['view_mode'],
      $configuration['third_party_settings'],
      $container->get('entity_type.manager'),
    );
  }
}
```

Reference: `/core/lib/Drupal/Core/Plugin/ContainerFactoryPluginInterface.php`, `/core/modules/system/src/Plugin/Block/SystemBrandingBlock.php` (example)

## Common Mistakes

- **Wrong parameter order in create()** — Must be ($container, $configuration, $plugin_id, $plugin_definition)
- **Wrong parameter order in __construct()** — Plugin params first, then your services
- **Not calling parent::__construct()** — Parent constructor often sets critical protected properties
- **Forgetting $configuration is an array** — Extract values like $configuration['settings'], not use it directly
- **Assuming $configuration structure** — Different plugin types have different $configuration arrays (check parent class)

## See Also

- [Constructor Injection](constructor-injection.md)
- [The Drupal Global Helper](drupal-global-helper.md)
- [Dependency injection in Plugin (Block)](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/dependency-injection-in-plugin-block)
