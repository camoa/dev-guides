---
description: Use config overrides to change configuration values without modifying stored config
drupal_version: "11.x"
---

# Config Overrides - Open for Extension (OCP)

## When to Use

Config overrides let you change configuration values without modifying stored config. Use for environment-specific settings (dev/staging/prod).

## Decision

| Override location | Use case | Priority |
|---|---|---|
| settings.php | Environment-specific (DB creds, API keys) | Highest |
| settings.local.php | Local development overrides | High |
| Module config override service | Dynamic/conditional overrides | Medium |
| Drush config:set | One-off changes | Avoid (not version-controlled) |

## Pattern

**GOOD: settings.php override (OCP)**

```php
// settings.php - override without modifying config files
$config['system.site']['name'] = 'Dev Site';
$config['system.performance']['css']['preprocess'] = FALSE;
```

**GOOD: Config override service (OCP)**

```php
// src/MyConfigOverrides.php
class MyConfigOverrides implements ConfigFactoryOverrideInterface {
  public function loadOverrides($names) {
    $overrides = [];
    if (in_array('system.site', $names)) {
      // Dynamic override based on condition
      if ($this->isTestEnvironment()) {
        $overrides['system.site']['name'] = 'Test Site';
      }
    }
    return $overrides;
  }
}
```

Reference: `/core/lib/Drupal/Core/Config/ConfigFactoryOverrideInterface.php`

## Common Mistakes

- Editing config YAML files directly in sites/default/files/config -- use config management. **WHY:** Config export overwrites manual edits; not version-controlled; unpredictable
- Hardcoding environment differences in config files -- use settings.php overrides. **WHY:** Different config per environment = deploy conflicts; can't promote code safely
- Using `\Drupal::config()->set()->save()` for overrides -- use override service. **WHY:** Permanently changes config; not reversible; breaks config sync
- Not understanding override priority -- test override application. **WHY:** Module overrides can be overridden by settings.php; unexpected behavior

## See Also

- [Plugin System](plugin-system-ocp.md) for extension patterns
- Reference: [Altering existing services and config](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/altering-existing-services-providing-dynamic-services)
