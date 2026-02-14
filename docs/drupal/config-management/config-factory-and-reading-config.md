---
description: Read and write configuration values in custom code — forms, controllers, services, hooks.
---

# Config Factory & Reading Config

## When to Use

When you need to read configuration values in custom code — forms, controllers, services, hooks.

## Steps

1. **Choose read method** — Immutable (`config()`) or editable (`getEditable()`)
2. **Inject ConfigFactory** — Via dependency injection in services
3. **Get config object** — `$config = $this->configFactory->get('module.settings');`
4. **Read values** — `$value = $config->get('key');` or `$all = $config->get();`
5. **Handle nested keys** — Use dot notation: `$config->get('parent.child.key')`
6. **Check for overrides** — `$config->hasOverrides('key')` if needed
7. **Get original values** — `$config->getOriginal('key', FALSE)` for override-free value

## Example: Reading Config in Service

```php
namespace Drupal\mymodule\Service;

use Drupal\Core\Config\ConfigFactoryInterface;

class MyService {

  protected ConfigFactoryInterface $configFactory;

  public function __construct(ConfigFactoryInterface $config_factory) {
    $this->configFactory = $config_factory;
  }

  public function doSomething() {
    // Read config (immutable)
    $config = $this->configFactory->get('mymodule.settings');
    $api_key = $config->get('api_key');
    $enabled = $config->get('enabled');

    // All values
    $all = $config->get();

    // Nested keys
    $timeout = $config->get('api.timeout');
  }
}
```

## Example: Editing Config

```php
// Get editable config
$config = \Drupal::service('config.factory')->getEditable('mymodule.settings');

// Set single value
$config->set('api_key', 'new_value');

// Set nested value
$config->set('api.timeout', 30);

// Clear value
$config->clear('old_key');

// Save changes
$config->save();

// Chain methods
$config->set('key1', 'value1')
  ->set('key2', 'value2')
  ->save();
```

**Reference:** `/core/lib/Drupal/Core/Config/ConfigFactory.php`, `/core/lib/Drupal/Core/Config/ConfigFactoryInterface.php`

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing access method | Read-only access | Use `$this->configFactory->get()` (ImmutableConfig) |
| Choosing access method | Need to modify | Use `$this->configFactory->getEditable()` (Config) |
| In service/controller | Proper DI | Inject ConfigFactoryInterface in constructor |
| In procedural code | No DI available | Use `\Drupal::config()` or `\Drupal::service('config.factory')` |
| After modifications | Changes need persistence | Call `->save()` |

## Common Mistakes

- Using `\Drupal::config()` in classes — Inject ConfigFactoryInterface instead
- Calling `set()` on immutable config — Use `getEditable()` first
- Forgetting to call `save()` — Changes are in memory only, not persisted
- Hardcoding config names — Use constants or derive from entity type
- Not checking if config exists — `get()` returns NULL for missing keys, check first
- Accessing overridden config for comparison — Use `getOriginal()` for unmodified values

## See Also

- [Config System Overview](config-system-overview.md) — config architecture
- [Config Override System](config-override-system.md) — applying overrides
- [Best Practices & Patterns](best-practices-and-patterns.md) — dependency injection patterns
- Reference: [Configuration API](https://api.drupal.org/api/drupal/core!core.api.php/group/config_api)
