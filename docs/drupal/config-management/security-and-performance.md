---
description: Secure configuration data, prevent vulnerabilities, and optimize config access for performance.
---

# Security & Performance

## When to Use

When you need to secure configuration data, prevent vulnerabilities, and optimize config access for performance.

## Security Best Practices

**Never commit credentials to version control**

```php
// WRONG — Credentials in config YAML committed to Git
# config/sync/mymodule.settings.yml
api_key: 'secret-key-123'

// RIGHT — Credentials in gitignored settings file
// settings.local.php (gitignored)
$config['mymodule.settings']['api_key'] = getenv('API_KEY');
```

**WHY:** Git history is permanent. Credentials exposed in repo are compromised forever. Use environment variables or settings.php overrides.

**IMPACT:** Exposed credentials enable unauthorized API access, data breaches, account takeovers.

---

**Validate config before import**

```php
public function onConfigImportValidate(ConfigImporterEvent $event) {
  $importer = $event->getConfigImporter();
  $changes = $importer->getStorageComparer()->getChangelist('create');

  foreach ($changes as $config_name) {
    $data = $importer->getStorageComparer()->getSourceStorage()->read($config_name);

    // Validate config structure
    if (str_starts_with($config_name, 'mymodule.')) {
      if (empty($data['required_field'])) {
        $importer->logError('Missing required field in ' . $config_name);
      }

      // Sanitize values
      if (!empty($data['url']) && !UrlHelper::isValid($data['url'], TRUE)) {
        $importer->logError('Invalid URL in ' . $config_name);
      }
    }
  }
}
```

**WHY:** Prevents malicious or malformed config from being imported. Config can be manually edited in sync directory — validate before import.

**IMPACT:** Invalid config can break site, expose vulnerabilities (XSS, SQLi via config values used in queries/output).

---

**Sanitize config output**

```php
// WRONG — Direct output, XSS vulnerability
$site_name = \Drupal::config('system.site')->get('name');
echo $site_name;

// RIGHT — Sanitized output
use Drupal\Component\Utility\Html;
$site_name = \Drupal::config('system.site')->get('name');
echo Html::escape($site_name);

// BETTER — Render array with automatic sanitization
$build['site_name'] = [
  '#plain_text' => $site_name,
];
```

**WHY:** Config values can be edited by admins or imported from untrusted sources. Treat as user input, sanitize before output.

**IMPACT:** XSS attacks via malicious config values injected into output.

---

**Use config permissions correctly**

```php
// WRONG — Hardcoded permission check
if (\Drupal::currentUser()->hasPermission('administer site configuration')) {
  // Allow config edit
}

// RIGHT — Check entity-specific permission
$permission = $entity_type->getAdminPermission();
if (\Drupal::currentUser()->hasPermission($permission)) {
  // Allow config edit
}
```

**WHY:** Global config permission is too broad. Entity-specific permissions enable granular access control.

**IMPACT:** Unauthorized users can modify config, change site behavior, expose data.

---

**Protect config files on filesystem**

```bash
# File permissions for sync directory
chmod 750 config/sync/
chmod 640 config/sync/*.yml

# Webserver user can read, not write
chown www-data:www-data config/sync/
```

**WHY:** Config sync directory should be read-only for webserver. Write access enables attackers to inject malicious config.

**IMPACT:** Malicious config injected via filesystem access, imported on next `drush cim`.

## Performance Best Practices

**Cache frequently-accessed config**

```php
// WRONG — Config loaded on every call
public function getSetting($key) {
  return \Drupal::config('mymodule.settings')->get($key);
}

// RIGHT — Static cache
protected array $settings;

public function getSetting($key) {
  if (!isset($this->settings)) {
    $this->settings = $this->configFactory->get('mymodule.settings')->get();
  }
  return $this->settings[$key] ?? NULL;
}
```

**WHY:** Config loading involves database query or file read. Static caching prevents redundant loads.

**IMPACT:** Loading config in hot paths (node view, preprocess) compounds to seconds per page.

**THRESHOLD:** If config accessed >5 times per request, use static cache.

---

**Avoid config access in hot paths**

```php
// WRONG — Config loaded on every node view (hundreds per page)
function mymodule_preprocess_node(&$variables) {
  $config = \Drupal::config('mymodule.settings');
  $variables['setting'] = $config->get('display_mode');
}

// RIGHT — Cache config value with render element
function mymodule_preprocess_node(&$variables) {
  $variables['setting'] = 'default';  // Static default
  $variables['#cache']['tags'][] = 'config:mymodule.settings';
}
```

**WHY:** Hot paths (hooks firing frequently) amplify performance impact. Config loading in preprocess adds milliseconds per call.

**THRESHOLD:** If hook fires >10 times per request, avoid config access.

---

**Use loadMultiple for batch operations**

```php
// WRONG — Individual loads (N queries)
foreach ($config_names as $name) {
  $config = $this->configFactory->get($name);
  $this->process($config);
}

// RIGHT — Batch load (1 query)
$configs = $this->configFactory->loadMultiple($config_names);
foreach ($configs as $config) {
  $this->process($config);
}
```

**WHY:** Individual loads execute separate database queries. Batch loading uses single query with IN clause.

**IMPACT:** N+1 query problem — 100 configs = 100 queries vs 1 query.

---

**Minimize config in event subscribers**

```php
// WRONG — Config loaded for ALL config saves
public function onConfigSave(ConfigCrudEvent $event) {
  $other_config = $this->configFactory->get('other.settings');
  // ...
}

// RIGHT — Check config name first
public function onConfigSave(ConfigCrudEvent $event) {
  if ($event->getConfig()->getName() !== 'mymodule.settings') {
    return;  // Skip unrelated config
  }
  // Only load other config when needed
  $other_config = $this->configFactory->get('other.settings');
}
```

**WHY:** Config save events fire for ALL config saves. Loading unrelated config in every save is wasteful.

**IMPACT:** Admin UI slowdown, import takes longer.

---

**Don't export large data to config**

```php
// WRONG — Large array in config (megabytes)
$config = \Drupal::service('config.factory')->getEditable('mymodule.cache');
$config->set('cached_data', $large_array)->save();

// RIGHT — Use State API for runtime data
\Drupal::state()->set('mymodule.cached_data', $large_array);

// BETTER — Use cache API
\Drupal::cache('mymodule')->set('cached_data', $large_array);
```

**WHY:** Config is loaded entirely into memory, serialized/unserialized on every access. Large config slows all config operations.

**THRESHOLD:** Config >100KB should use State API or cache instead.

**IMPACT:** Memory exhaustion, slow config import/export, large Git diffs.

## Common Security Mistakes

- Credentials in config YAML — Use settings.php overrides with environment variables
- No validation on import — Malicious config imported unchecked
- Direct output without sanitization — XSS via config values
- Global config permission — Too broad access, use entity-specific permissions
- Writable sync directory — Attacker injects malicious config files

## Common Performance Mistakes

- Config loaded in hot paths — Use static cache or avoid config access
- Individual loads in loops — Use loadMultiple batch loading
- No static caching — Redundant database queries per request
- Large data in config — Use State API or cache instead
- Config access in all event subscribers — Check config name first

## See Also

- [Config Factory & Reading Config](config-factory-and-reading-config.md) — proper config access
- [Config Events](config-events.md) — event subscriber patterns
- [Best Practices & Patterns](best-practices-and-patterns.md) — DI and caching patterns
- Reference: [OWASP Configuration Management](https://owasp.org/www-project-top-ten/)
