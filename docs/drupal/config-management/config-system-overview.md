---
description: Understand Drupal's configuration management architecture — how config data is structured, stored, validated, synchronized, and overridden.
---

# Config System Overview

## When to Use

When you need to understand Drupal's configuration management architecture — how config data is structured, stored, validated, synchronized, and overridden.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Read-only config access | `\Drupal::config('name')` | Returns ImmutableConfig, prevents accidental modification |
| Write/modify config | `\Drupal::service('config.factory')->getEditable('name')` | Returns mutable Config object |
| Multiple config objects | `ConfigFactory::loadMultiple(['name1', 'name2'])` | Batch loads, more efficient than individual loads |
| Config with overrides applied | Default `get()` method | Includes module and settings.php overrides |
| Config without overrides | `getEditable()` or `getOriginal()` | Override-free for editing or debugging |

## Pattern

```php
// Read config (immutable)
$config = \Drupal::config('system.site');
$site_name = $config->get('name');

// Edit config (mutable)
$config = \Drupal::service('config.factory')->getEditable('mymodule.settings');
$config->set('api_key', 'new_value')->save();

// Check for overrides
if ($config->hasOverrides('api_key')) {
  $original = $config->getOriginal('api_key', FALSE);
}
```

**Reference:** `/core/lib/Drupal/Core/Config/ConfigFactoryInterface.php`, `/core/lib/Drupal/Core/Config/Config.php`

## Architecture Layers

1. **Storage Layer** — Reads/writes config data to filesystem (YAML) or database
2. **Schema Layer** — Validates config data types and structure via typed config
3. **Override Layer** — Merges module and settings.php overrides into runtime data
4. **Entity Layer** — Config entities provide CRUD, dependencies, and UI
5. **Sync Layer** — Compares active vs sync storage, imports/exports changes
6. **Event Layer** — Dispatches events for save, delete, import, validate

## Common Mistakes

- Using `\Drupal::config()->get()` for write operations — Use `getEditable()` instead
- Modifying config in production UI — Changes aren't tracked in Git, won't deploy to other environments
- Ignoring config schema — Causes validation failures, type coercion issues, deployment errors
- Storing content in config — Content belongs in nodes/terms, config is for structure/settings
- Hardcoding config names — Use constants or derive from entity type machine names

## See Also

- [Simple Config vs Config Entities](simple-config-vs-config-entities.md) — choosing the right config type
- [Config Factory & Reading Config](config-factory-and-reading-config.md) — reading config in code
- [Config Synchronization](config-synchronization.md) — syncing between environments
- Reference: [Configuration API Overview](https://www.drupal.org/docs/drupal-apis/configuration-api)
