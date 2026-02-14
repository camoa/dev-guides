---
description: Override config values per environment without modifying stored config or committing credentials to Git.
---

# Config Override System

## When to Use

When you need to override config values per environment (e.g., API keys, site name) without modifying stored config or committing credentials to Git.

## Override Layers

Drupal applies overrides in this order (later overrides win):
1. **Active storage** — Database config (base values)
2. **Module overrides** — Via `ConfigFactoryOverrideInterface` services
3. **Settings overrides** — `$config` array in settings.php

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Environment-specific values | settings.php overrides | Per-environment, not in Git (gitignored settings.local.php) |
| Dynamic overrides | Module overrides via service | Conditional logic, depend on runtime state |
| Language-specific config | Language module overrides | Automatic per-language config translation |
| Temporary testing | settings.php overrides | Quick, no code deployment |
| Complex conditional logic | Module override service | Full access to container, state, request |

## Example: Settings.php Overrides

```php
// settings.php or settings.local.php
$config['system.site']['name'] = 'Dev Site';
$config['system.site']['mail'] = 'dev@example.com';

// Override nested values
$config['mymodule.settings']['api']['key'] = 'dev-api-key-123';
$config['mymodule.settings']['api']['endpoint'] = 'https://dev-api.example.com';

// Override config entity (use full name with ID)
$config['node.type.article']['name'] = 'Dev Article';

// Per-environment example
if (getenv('ENVIRONMENT') === 'production') {
  $config['system.performance']['cache']['page']['max_age'] = 3600;
  $config['system.logging']['error_level'] = 'hide';
}
else {
  $config['system.performance']['cache']['page']['max_age'] = 0;
  $config['system.logging']['error_level'] = 'verbose';
}
```

**Reference:** `/core/lib/Drupal/Core/Config/Config.php` lines 144-163 (setOverriddenData)

## Example: Module Override Service

```php
// mymodule/src/Config/MyModuleConfigOverrides.php
namespace Drupal\mymodule\Config;

use Drupal\Core\Config\ConfigFactoryOverrideInterface;
use Drupal\Core\Config\StorageInterface;

class MyModuleConfigOverrides implements ConfigFactoryOverrideInterface {

  public function loadOverrides($names) {
    $overrides = [];

    if (in_array('system.site', $names)) {
      // Conditional override based on runtime state
      if ($this->isMaintenanceMode()) {
        $overrides['system.site']['name'] = 'Site Under Maintenance';
      }
    }

    return $overrides;
  }

  public function getCacheSuffix() {
    return 'MyModuleConfigOverride';
  }

  public function getCacheableMetadata($name) {
    return new CacheableMetadata();
  }

  public function createConfigObject($name, $collection = StorageInterface::DEFAULT_COLLECTION) {
    return NULL;
  }
}
```

**Service definition:**
```yaml
# mymodule.services.yml
services:
  mymodule.config_overrides:
    class: Drupal\mymodule\Config\MyModuleConfigOverrides
    tags:
      - { name: config.factory.override, priority: 5 }
```

**Reference:** `/core/lib/Drupal/Core/Config/ConfigFactoryOverrideInterface.php`, `/core/modules/language/src/Config/LanguageConfigOverride.php`

## Override Priority

**Lower priority values run first, higher values run last and win conflicts:**
- Priority -100: Low priority, runs early
- Priority 0: Default
- Priority 5: Module overrides (typical)
- Priority 100: settings.php overrides (highest, always wins)

## Checking for Overrides

```php
$config = \Drupal::config('system.site');

// Check if any overrides exist
if ($config->hasOverrides()) {
  // Get current value (with overrides)
  $name = $config->get('name');

  // Get original value (without overrides)
  $original_name = $config->getOriginal('name', FALSE);

  // Check specific key
  if ($config->hasOverrides('name')) {
    // 'name' key is overridden
  }
}

// Get editable config (no overrides)
$editable = \Drupal::service('config.factory')->getEditable('system.site');
$stored_name = $editable->get('name'); // Always returns stored value
```

## Common Mistakes

- Storing overrides in settings.php committed to Git — Use gitignored settings.local.php
- Overriding config entities without full name — Must include entity ID (e.g., `node.type.article`)
- Editing config that has overrides — Changes saved but overridden at runtime
- Not checking for overrides before comparing — Comparing overridden vs stored values
- Using overrides for permanent changes — Overrides are runtime-only, export/import uses stored values
- High-priority module overrides conflicting — Lower priority value, or use settings.php

## See Also

- [Config Factory & Reading Config](config-factory-and-reading-config.md) — reading config with overrides
- [Config Synchronization](config-synchronization.md) — syncing stored config
- [Config Split](config-split.md) — environment-specific config via Config Split
- Reference: [Configuration Override System](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-override-system)
