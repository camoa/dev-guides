---
description: Understand how Drupal stores configuration data — active storage (database), sync storage (filesystem), and custom backends.
---

# Config Storage

## When to Use

When you need to understand how Drupal stores configuration data — active storage (database), sync storage (filesystem), and custom storage backends.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Runtime config access | Active storage (database) | Fast, always available, overrides applied |
| Version control | Sync storage (files) | Git-friendly YAML, deployable |
| Export config to files | `drush cex` | Writes active config to sync directory |
| Import config from files | `drush cim` | Reads sync files, writes to active storage |
| Custom storage backend | Implement `StorageInterface` | S3, remote API, custom database |
| Config collections | `createCollection($name)` | Language-specific config, custom partitions |

## Architecture

**Active Storage (Database)**
- Location: `config` table in database
- Format: Serialized PHP arrays (via `serialize()`)
- Purpose: Runtime config with overrides applied
- Access: `\Drupal::service('config.storage')`

**Sync Storage (Filesystem)**
- Location: `../config/sync/` (configurable in settings.php)
- Format: YAML files
- Purpose: Version-controlled config for deployment
- Access: `\Drupal::service('config.storage.sync')`

## Pattern

```php
// Access active storage
$active_storage = \Drupal::service('config.storage');
$data = $active_storage->read('system.site');

// Access sync storage
$sync_storage = \Drupal::service('config.storage.sync');
$sync_data = $sync_storage->read('system.site');

// List all config names
$names = $active_storage->listAll('mymodule.');

// Check if config exists
if ($active_storage->exists('mymodule.settings')) {
  // Config exists
}

// Write directly to storage (not recommended, use Config objects)
$active_storage->write('mymodule.settings', $data);
```

**Reference:** `/core/lib/Drupal/Core/Config/StorageInterface.php`, `/core/lib/Drupal/Core/Config/FileStorage.php`, `/core/lib/Drupal/Core/Config/DatabaseStorage.php`

## Storage Implementations

**DatabaseStorage** — Default active storage, uses `config` table
- Fast database queries
- Transactions supported
- No filesystem dependencies

**FileStorage** — Default sync storage, uses YAML files
- Git-friendly format
- Human-readable
- Direct filesystem access required

**CachedStorage** — Wraps another storage with static cache
- Reduces database/filesystem hits
- Invalidated on config save

**NullStorage** — No-op storage for testing
- All operations succeed, no data persisted

## Common Mistakes

- Writing directly to storage — Use Config objects via ConfigFactory instead
- Hardcoding sync directory path — Read from `Settings::get('config_sync_directory')`
- Not using StorageInterface — Breaks compatibility with custom storage backends
- Accessing storage without DI — Inject `config.storage` service
- Assuming sync directory is writable — Check permissions before export
- Modifying active storage files — Database is source of truth, files are export only

## See Also

- [Config Synchronization](config-synchronization.md) — syncing active vs sync storage
- [Config Import/Export](config-import-export.md) — Drush commands for export/import
- [Deployment Workflows](deployment-workflows.md) — using sync storage for deployment
- Reference: [Storage Interface](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Config!StorageInterface.php)
