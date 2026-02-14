---
description: Identify and fix common config management mistakes — patterns that break deployment, cause data loss, or create security issues.
---

# Anti-Patterns & Common Mistakes

## When to Use

When you need to identify and fix common config management mistakes — patterns that break deployment, cause data loss, or create security issues.

## Critical Anti-Patterns

**Making config changes in production UI**

```
BAD WORKFLOW:
1. Edit view in production UI
2. Save changes
3. Changes live but not in Git
4. Next deploy: drush cim overwrites with Git version
5. Production changes lost
```

**WHY THIS IS WRONG:** Production changes aren't version-controlled, can't rollback, lost on next import from Git. Always develop locally, export, commit, import.

**FIX:** Develop locally -> Export -> Commit -> Import to production. Use `drush config:status` to detect drift.

---

**No config schema defined**

```php
// Config saved but no schema defined
$config = \Drupal::service('config.factory')->getEditable('mymodule.settings');
$config->set('api_key', 'value')->save();

// On import: "Missing schema for mymodule.settings"
// On validation: "Config cannot be validated"
```

**WHY THIS IS WRONG:** Without schema, Drupal can't validate, type-cast, or constrain config values. Leads to type coercion failures, validation errors, broken imports.

**FIX:** Define schema in `config/schema/mymodule.schema.yml` with proper types and constraints.

---

**Committing credentials to Git**

```yaml
# BAD — config/sync/mymodule.settings.yml committed to Git
api_key: 'secret-key-abc-123'
api_secret: 'super-secret-xyz'
```

**WHY THIS IS WRONG:** Git history is permanent and public (or accessible to unauthorized users). Credentials in repo are a security breach.

**FIX:** Use settings.php overrides (gitignored):
```php
// settings.local.php
$config['mymodule.settings']['api_key'] = getenv('API_KEY');
```

---

**Static Drupal calls in classes**

```php
// BAD
class MyService {
  public function doSomething() {
    $config = \Drupal::config('mymodule.settings');
  }
}
```

**WHY THIS IS WRONG:** Tight coupling, not testable, violates Drupal coding standards. Static calls can't be mocked in unit tests.

**FIX:** Inject ConfigFactoryInterface:
```php
// GOOD
class MyService {
  protected ConfigFactoryInterface $configFactory;

  public function __construct(ConfigFactoryInterface $config_factory) {
    $this->configFactory = $config_factory;
  }
}
```

---

**Modifying config with overrides active**

```php
// Production has override in settings.php:
// $config['system.site']['name'] = 'Production Site';

// Admin edits site name via UI, saves
$config = \Drupal::service('config.factory')->getEditable('system.site');
$config->set('name', 'New Name')->save();

// Override still active — 'New Name' never displayed
```

**WHY THIS IS WRONG:** Overrides applied at runtime after database read. Edits to database value are overridden immediately. User sees no effect of their change.

**FIX:** Remove override from settings.php if config should be editable. Use Config Split for environment-specific values instead.

---

**Not clearing cache after config import**

```bash
drush cim -y
# Config imported, but site still uses old cached config
```

**WHY THIS IS WRONG:** Config values are cached (render cache, dynamic page cache, etc.). Imported changes not reflected until cache cleared.

**FIX:** Always clear cache after import:
```bash
drush cim -y && drush cr
```

---

**Hardcoding config names**

```php
// BAD
$config = \Drupal::config('mymodule.settings');
$view = \Drupal::config('views.view.my_view');
```

**WHY THIS IS WRONG:** Fragile, breaks on renames, no IDE autocomplete, hard to refactor.

**FIX:** Use constants or entity type manager:
```php
// GOOD
const SETTINGS_CONFIG = 'mymodule.settings';
$config = $this->configFactory->get(self::SETTINGS_CONFIG);

// BETTER for entities
$view = $this->entityTypeManager->getStorage('view')->load('my_view');
```

---

**Importing without checking status first**

```bash
# BAD
drush cim -y

# GOOD
drush config:status
drush config:diff system.site
drush cim -y
```

**WHY THIS IS WRONG:** Blind import can overwrite production-only changes, delete unexpected config, break site. Always review what's changing.

**FIX:** Check `drush config:status` and `drush config:diff` before import. Create database backup before import.

---

**No FullyValidatable constraint**

```yaml
# BAD — Lenient validation
mymodule.settings:
  type: config_object
  mapping:
    api_key:
      type: string

# GOOD — Strict validation
mymodule.settings:
  type: config_object
  constraints:
    FullyValidatable: ~
  mapping:
    api_key:
      type: string
      constraints:
        NotBlank: {}
```

**WHY THIS IS WRONG:** Without FullyValidatable, Drupal allows missing keys, extra keys, invalid types. Validation is too lenient, invalid config slips through.

**FIX:** Add `FullyValidatable` constraint and proper field-level constraints.

---

**Using config for content**

```yaml
# BAD — User data in config
mymodule.users:
  users:
    - name: 'John'
      email: 'john@example.com'
    - name: 'Jane'
      email: 'jane@example.com'
```

**WHY THIS IS WRONG:** Config is for structure and settings, not user-generated content. Content belongs in nodes, users, custom entities. Config is deployed, content is site-specific.

**FIX:** Use content entities (nodes, custom entities) or State API for runtime data.

---

**Heavy processing in config events**

```php
// BAD — Long-running task in SAVE event
public function onConfigSave(ConfigCrudEvent $event) {
  // API call that takes 5 seconds
  $this->apiClient->syncData();
}
```

**WHY THIS IS WRONG:** Config save events block the config save operation. Heavy processing makes all config saves slow, affects admin UI, import, etc.

**FIX:** Queue heavy tasks:
```php
public function onConfigSave(ConfigCrudEvent $event) {
  $queue = \Drupal::queue('mymodule_sync');
  $queue->createItem(['config_name' => $event->getConfig()->getName()]);
}
```

## See Also

- [Best Practices & Patterns](best-practices-and-patterns.md) — correct patterns
- [Security & Performance](security-and-performance.md) — security and performance issues
- [Config Factory & Reading Config](config-factory-and-reading-config.md) — proper config access
