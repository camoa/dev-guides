---
description: Generate multiple plugin instances from one class using DeriverBase and ContainerDeriverInterface
drupal_version: "11.x"
---

# Plugin Derivers

## When to Use

> Use plugin derivers to generate multiple plugin instances from a single class definition. This enables creating variant plugins based on external data (like tamper plugins, field widgets, or AI models) without code duplication.

## Decision

| Generate Plugins From | Use Deriver | Pattern |
|-----------------------|-------------|---------|
| External plugin manager | Yes | Query manager for available plugins |
| Database/config entities | Yes | Load entities and create derivatives |
| Static list | No | Use `static::definitions()` instead |
| Event definitions | Yes | Standard ECA event pattern |

## Pattern

**Deriver Class:**
```php
namespace Drupal\my_module\Plugin\Action;

use Drupal\Core\Plugin\Discovery\ContainerDeriverInterface;
use Drupal\Component\Plugin\Derivative\DeriverBase;
use Symfony\Component\DependencyInjection\ContainerInterface;

class MyActionDeriver extends DeriverBase implements ContainerDeriverInterface {

  protected $externalPluginManager;

  public function __construct($external_plugin_manager) {
    $this->externalPluginManager = $external_plugin_manager;
  }

  public static function create(ContainerInterface $container, $base_plugin_id) {
    return new static(
      $container->get('plugin.manager.external')
    );
  }

  public function getDerivativeDefinitions($base_plugin_definition) {
    // Generate derivative for each external plugin
    foreach ($this->externalPluginManager->getDefinitions() as $plugin_id => $definition) {
      $this->derivatives[$plugin_id] = $base_plugin_definition;
      $this->derivatives[$plugin_id]['label'] = $definition['label'];
      $this->derivatives[$plugin_id]['description'] = $definition['description'];
      $this->derivatives[$plugin_id]['external_plugin_id'] = $plugin_id;
    }

    return $this->derivatives;
  }
}
```

**Action Using Deriver:**
```php
#[Action(
  id: 'my_module_dynamic_action',
  deriver: 'Drupal\my_module\Plugin\Action\MyActionDeriver',
)]
#[EcaAction(version_introduced: '1.0.0')]
class MyDynamicAction extends ConfigurableActionBase {

  public function execute(): void {
    // Get the derivative-specific plugin ID
    $external_plugin_id = $this->getPluginDefinition()['external_plugin_id'];

    // Use the external plugin
    $external_plugin = $this->externalPluginManager->createInstance($external_plugin_id);
    $result = $external_plugin->process($data);

    $this->tokenService->addTokenData($this->configuration['result_token'], $result);
  }
}
```

## Common Mistakes

- **Wrong**: Not implementing `ContainerDeriverInterface` → **Right**: Can't inject services into deriver
- **Wrong**: Missing `getDerivativeDefinitions()` → **Right**: No derivatives generated
- **Wrong**: Not setting unique derivative keys → **Right**: Plugins overwrite each other
- **Wrong**: Derivative logic in main plugin → **Right**: Should be in deriver class
- **Wrong**: Not updating derivatives when source changes → **Right**: Stale plugin list

## See Also

- [Advanced Action Patterns](advanced-action-patterns.md) for deriver usage
- [Event Plugin Basics](event-plugin-basics.md) for event derivers
- [Service Injection](service-injection.md) for deriver service injection

**References:**
- Core: `/modules/contrib/eca_tamper/src/Plugin/Action/TamperDeriver.php`
- Drupal: https://api.drupal.org/api/drupal/core!lib!Drupal!Component!Plugin!Derivative!DeriverInterface.php
