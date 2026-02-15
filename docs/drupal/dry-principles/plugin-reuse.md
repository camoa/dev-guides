---
description: Reuse patterns in Drupal's plugin system - extending base plugins, creating shared bases, and using derivatives for dynamic generation.
---

# Plugin Reuse Patterns

## When to Use

When you need extensible, discoverable, swappable components (blocks, field types, filters, conditions, actions), or when multiple plugins share common patterns.

## Plugin Inheritance

| Pattern | Use When | Example |
|---------|----------|---------|
| Extend core plugin base | Creating new plugin of existing type | `MyBlock extends BlockBase` |
| Extend another plugin | Creating variation of existing plugin | `MyMenuBlock extends SystemMenuBlock` |
| Create shared base for project | Multiple similar custom plugins | `MyProjectBlockBase extends BlockBase` |
| Use plugin derivatives | Generating multiple plugins from one class | Menu links, contextual links, local tasks |

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Single new block | Extend `BlockBase` | Inherit caching, context, config scaffolding |
| Variation of core block | Extend specific core block class | Reuse logic, override specific methods |
| 5+ similar blocks with shared logic | Create `MyProjectBlockBase extends BlockBase` | Eliminate duplication across project blocks |
| Dynamic plugins based on config | Plugin deriver | One class generates multiple plugin instances |
| Shared logic across plugin types | Service injected into plugins | Avoid duplicating logic in each plugin |

## Pattern

```php
// Plugin extending core base
namespace Drupal\mymodule\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

#[Block(
  id: "my_custom_block",
  admin_label: new TranslatableMarkup("My Custom Block"),
)]
class MyCustomBlock extends BlockBase implements ContainerFactoryPluginInterface {

  public function __construct(
    array $configuration,
    $plugin_id,
    $plugin_definition,
    protected MyService $myService,
  ) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
  }

  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition) {
    return new static(
      $configuration,
      $plugin_id,
      $plugin_definition,
      $container->get('mymodule.my_service'),
    );
  }

  public function build() {
    return ['#markup' => $this->myService->getData()];
  }
}
```

## Plugin Derivatives Pattern

```php
// Deriver generates multiple plugins from one class
namespace Drupal\mymodule\Plugin\Deriver;

use Drupal\Component\Plugin\Derivative\DeriverBase;

class MyBlockDeriver extends DeriverBase {

  public function getDerivativeDefinitions($base_plugin_definition) {
    $config_entities = \Drupal::entityTypeManager()
      ->getStorage('my_entity_type')
      ->loadMultiple();

    foreach ($config_entities as $id => $entity) {
      $this->derivatives[$id] = $base_plugin_definition;
      $this->derivatives[$id]['admin_label'] = $entity->label();
    }

    return $this->derivatives;
  }
}
```

Reference: `core/lib/Drupal/Core/Block/BlockBase.php`, `core/lib/Drupal/Core/Plugin/PluginBase.php`, `core/modules/system/src/Plugin/Deriver/SystemMenuBlock.php`

## Common Mistakes

- **Not calling parent::__construct()** — Always call parent constructor in plugins to maintain plugin definition
- **Overriding create() without matching constructor** — Constructor parameters must match `create()` factory method
- **Duplicating logic across plugins** — Extract shared logic to injected service, not into each plugin
- **Using derivatives when simple plugin would work** — Only use derivatives for truly dynamic plugin generation
- **Forgetting ContainerFactoryPluginInterface** — Required for dependency injection in plugins

## See Also

- [Traits for Cross-Cutting Concerns](traits-cross-cutting.md)
- [Twig Template Inheritance](twig-template-inheritance.md)
- Reference: [Plugin API | Drupal.org](https://www.drupal.org/docs/drupal-apis/plugin-api)
- Reference: [Plugin Derivatives | Drupal.org](https://www.drupal.org/docs/drupal-apis/plugin-api/plugin-derivatives)
