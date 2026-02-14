---
description: Config management patterns, architecture decisions, and proven approaches for maintainable config workflows.
---

# Best Practices & Patterns

## When to Use

When you need guidance on config management patterns, architecture decisions, and proven approaches for maintainable config workflows.

## Development Workflow Best Practices

**Always develop locally, deploy via config management:**
- Make config changes on local/dev environment
- Export config with `drush cex`
- Commit to Git
- Import on staging/production with `drush cim`
- Never make config changes directly in production UI

**WHY:** Production UI changes aren't version-controlled, can't rollback, lost on next import. Config management ensures all environments stay in sync and changes are tracked.

## Code Standards

**Always use dependency injection for ConfigFactory:**
```php
// GOOD — Dependency injection
class MyService {
  protected ConfigFactoryInterface $configFactory;

  public function __construct(ConfigFactoryInterface $config_factory) {
    $this->configFactory = $config_factory;
  }

  public function doSomething() {
    $config = $this->configFactory->get('mymodule.settings');
  }
}
```

```php
// BAD — Static call
class MyService {
  public function doSomething() {
    $config = \Drupal::config('mymodule.settings');
  }
}
```

**WHY:** DI makes code testable, mockable, and follows Drupal coding standards. Static calls create tight coupling and can't be unit tested.

**Use immutable config for reading, editable for writing:**
```php
// GOOD — Read with immutable
$config = $this->configFactory->get('mymodule.settings');
$value = $config->get('key');

// GOOD — Write with editable
$config = $this->configFactory->getEditable('mymodule.settings');
$config->set('key', 'value')->save();
```

**WHY:** Immutable config prevents accidental modifications and clearly signals read-only intent. Editable config is override-free, ensuring you're modifying stored values.

## Schema Best Practices

**Always define config schema with FullyValidatable:**
```yaml
mymodule.settings:
  type: config_object
  label: 'My Module Settings'
  constraints:
    FullyValidatable: ~
  mapping:
    # ... keys here
```

**WHY:** Schema enables type validation, prevents invalid data, required for Recipes, JSON:API, GraphQL. FullyValidatable enforces strict validation, catches missing keys early.

**Use specialized types over generic strings:**
```yaml
# GOOD
notification_email:
  type: email
  constraints:
    Email: {}

# BAD
notification_email:
  type: string
```

**WHY:** Specialized types provide built-in validation, constraints, and better documentation. Generic strings allow invalid data.

## Dependency Management

**Use enforced dependencies for ownership:**
```yaml
# Config that should be deleted when module uninstalled
dependencies:
  enforced:
    module:
      - mymodule
```

**WHY:** Enforced dependencies ensure config is cleaned up on module uninstall. Without enforced dependency, config remains in database, orphaned.

**Let Drupal calculate dependencies automatically:**
- Extend ConfigEntityBase
- Use entity references, plugin collections
- Don't manually add dependencies unless enforced or non-calculable

**WHY:** Automatic calculation is more accurate, less error-prone. Manual dependencies easily get out of sync.

## Config Split Patterns

**Use complete split for dev modules:**
- Dev modules (Devel, Webprofiler) in dev split
- Split active only on local/staging via settings.local.php
- Prevents dev modules on production

**Use conditional split for environment-specific settings:**
- Cache settings, logging levels, API endpoints
- Prod split with production values
- Split active only on production via settings.php

**WHY:** Complete split prevents unwanted modules. Conditional split allows different values per environment while keeping config structure in sync.

## Security Best Practices

**Never commit credentials to Git:**
```php
// settings.local.php (gitignored)
$config['mymodule.settings']['api_key'] = 'secret-key-123';
```

**WHY:** Git history is permanent. Credentials in repo are a security breach. Use settings.php overrides or environment variables instead.

**Validate config in event subscribers:**
```php
public function onConfigImportValidate(ConfigImporterEvent $event) {
  $importer = $event->getConfigImporter();
  $changes = $importer->getStorageComparer()->getChangelist('create');
  foreach ($changes as $config_name) {
    if (str_starts_with($config_name, 'mymodule.')) {
      // Validate config before import
      $data = $importer->getStorageComparer()->getSourceStorage()->read($config_name);
      if (!$this->isValid($data)) {
        $importer->logError('Invalid config: ' . $config_name);
      }
    }
  }
}
```

**WHY:** Prevents invalid config from being imported, catches malicious or accidental data before it breaks the site.

## Performance Best Practices

**Use static caching for frequently-accessed config:**
```php
class MyService {
  protected ?array $settings = NULL;

  protected function getSettings(): array {
    if ($this->settings === NULL) {
      $config = $this->configFactory->get('mymodule.settings');
      $this->settings = $config->get();
    }
    return $this->settings;
  }
}
```

**WHY:** Config loading involves database query or file read. Static caching prevents redundant loads in same request.

**Don't load config in hot paths (hooks firing frequently):**
```php
// BAD — Config loaded on every node view
function mymodule_node_view(array &$build, NodeInterface $node, $display, $view_mode) {
  $config = \Drupal::config('mymodule.settings');
  // ...
}

// GOOD — Cache config value as render element
$build['#cache']['tags'][] = 'config:mymodule.settings';
```

**WHY:** Hot paths (node view, preprocess) fire hundreds of times per page. Config loading adds milliseconds per call, compounds to seconds.

## Common Mistakes

- Making config changes in production — Use local dev + export + import workflow
- No config schema — Validation failures, type coercion errors
- Static Drupal calls in classes — Use dependency injection
- Not clearing cache after import — Old cached config still active
- Committing credentials — Security breach, use settings.php overrides
- Heavy processing in config save events — Slows all config saves, use queue

## See Also

- [Config Factory & Reading Config](config-factory-and-reading-config.md) — reading config correctly
- [Writing Config Schema](writing-config-schema.md) — schema best practices
- [Deployment Workflows](deployment-workflows.md) — deployment patterns
- [Anti-Patterns & Common Mistakes](anti-patterns-and-common-mistakes.md) — what to avoid
