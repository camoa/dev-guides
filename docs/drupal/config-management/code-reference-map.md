---
description: Locate core config classes, interfaces, and files for deeper understanding or extending config functionality.
---

# Code Reference Map

## When to Use

When you need to locate core config classes, interfaces, and files for deeper understanding or extending config functionality.

## Core Config Classes

| Class | Path | Purpose |
|-------|------|---------|
| ConfigFactoryInterface | `core/lib/Drupal/Core/Config/ConfigFactoryInterface.php` | Service interface for loading config |
| ConfigFactory | `core/lib/Drupal/Core/Config/ConfigFactory.php` | Default config factory implementation |
| Config | `core/lib/Drupal/Core/Config/Config.php` | Mutable config object with overrides |
| ImmutableConfig | `core/lib/Drupal/Core/Config/ImmutableConfig.php` | Read-only config object |
| ConfigBase | `core/lib/Drupal/Core/Config/ConfigBase.php` | Base class for all config objects |
| StorableConfigBase | `core/lib/Drupal/Core/Config/StorableConfigBase.php` | Base for config with storage |

## Config Entity Classes

| Class | Path | Purpose |
|-------|------|---------|
| ConfigEntityInterface | `core/lib/Drupal/Core/Config/Entity/ConfigEntityInterface.php` | Config entity interface |
| ConfigEntityBase | `core/lib/Drupal/Core/Config/Entity/ConfigEntityBase.php` | Base class for config entities |
| ConfigEntityStorage | `core/lib/Drupal/Core/Config/Entity/ConfigEntityStorage.php` | Storage handler for config entities |
| ConfigEntityTypeInterface | `core/lib/Drupal/Core/Config/Entity/ConfigEntityTypeInterface.php` | Entity type definition interface |
| ConfigDependencyManager | `core/lib/Drupal/Core/Config/Entity/ConfigDependencyManager.php` | Manages config dependencies |

## Config Storage Classes

| Class | Path | Purpose |
|-------|------|---------|
| StorageInterface | `core/lib/Drupal/Core/Config/StorageInterface.php` | Storage backend interface |
| FileStorage | `core/lib/Drupal/Core/Config/FileStorage.php` | YAML file storage implementation |
| DatabaseStorage | `core/lib/Drupal/Core/Config/DatabaseStorage.php` | Database storage implementation |
| CachedStorage | `core/lib/Drupal/Core/Config/CachedStorage.php` | Cached storage wrapper |
| StorageComparer | `core/lib/Drupal/Core/Config/StorageComparer.php` | Compares active vs sync storage |

## Config Management Classes

| Class | Path | Purpose |
|-------|------|---------|
| ConfigImporter | `core/lib/Drupal/Core/Config/ConfigImporter.php` | Imports config from sync to active |
| ConfigInstaller | `core/lib/Drupal/Core/Config/ConfigInstaller.php` | Installs config on module enable |
| ConfigManager | `core/lib/Drupal/Core/Config/ConfigManager.php` | Helper functions for config system |
| ConfigManagerInterface | `core/lib/Drupal/Core/Config/ConfigManagerInterface.php` | Config manager interface |

## Config Schema Classes

| Class | Path | Purpose |
|-------|------|---------|
| TypedConfigManagerInterface | `core/lib/Drupal/Core/Config/TypedConfigManagerInterface.php` | Schema manager interface |
| TypedConfigManager | `core/lib/Drupal/Core/Config/TypedConfigManager.php` | Schema manager implementation |
| Mapping | `core/lib/Drupal/Core/Config/Schema/Mapping.php` | Schema mapping type |
| Sequence | `core/lib/Drupal/Core/Config/Schema/Sequence.php` | Schema sequence type |

## Config Events

| Class/Constant | Path | Purpose |
|----------------|------|---------|
| ConfigEvents | `core/lib/Drupal/Core/Config/ConfigEvents.php` | Config event constants |
| ConfigCrudEvent | `core/lib/Drupal/Core/Config/ConfigCrudEvent.php` | Save/delete event object |
| ConfigImporterEvent | `core/lib/Drupal/Core/Config/ConfigImporterEvent.php` | Import event object |
| ConfigCollectionEvents | `core/lib/Drupal/Core/Config/ConfigCollectionEvents.php` | Collection event constants |

## Config Override Classes

| Class | Path | Purpose |
|-------|------|---------|
| ConfigFactoryOverrideInterface | `core/lib/Drupal/Core/Config/ConfigFactoryOverrideInterface.php` | Override service interface |
| ConfigFactoryOverrideBase | `core/lib/Drupal/Core/Config/ConfigFactoryOverrideBase.php` | Base class for overrides |
| LanguageConfigOverride | `core/modules/language/src/Config/LanguageConfigOverride.php` | Language-specific overrides |

## Config Schema Files

| File | Path | Purpose |
|------|------|---------|
| core.data_types.schema.yml | `core/config/schema/core.data_types.schema.yml` | Core data type definitions |
| system.schema.yml | `core/modules/system/config/schema/system.schema.yml` | System module schema examples |
| field.schema.yml | `core/modules/field/config/schema/field.schema.yml` | Field module schema |
| views.view.schema.yml | `core/modules/views/config/schema/views.view.schema.yml` | Complex entity schema example |

## Config Module Files

| Path | Purpose |
|------|---------|
| `core/modules/config/` | Config module (UI for config management) |
| `core/modules/config/src/Controller/ConfigController.php` | Config diff/import UI |
| `core/modules/config/src/Form/ConfigSync.php` | Config sync form |

## Useful Drush Commands

| Command | Implementation | Purpose |
|---------|----------------|---------|
| `drush cex` | ConfigCommands::export() | Export active config to sync |
| `drush cim` | ConfigCommands::import() | Import sync config to active |
| `drush config:status` | ConfigCommands::status() | Show differences |
| `drush config:diff` | ConfigCommands::diff() | Show config diff |

**Reference:** Drush commands in `core/modules/config/src/Commands/ConfigCommands.php`

## Key Constants

```php
// Config name max length
ConfigBase::MAX_NAME_LENGTH = 250;

// Default collection name
StorageInterface::DEFAULT_COLLECTION = '';

// Config events
ConfigEvents::SAVE = 'config.save';
ConfigEvents::DELETE = 'config.delete';
ConfigEvents::RENAME = 'config.rename';
ConfigEvents::IMPORT = 'config.importer.import';
ConfigEvents::IMPORT_VALIDATE = 'config.importer.validate';
```

## See Also

- [Config System Overview](config-system-overview.md) — architecture overview
- [Config Factory & Reading Config](config-factory-and-reading-config.md) — using ConfigFactory
- [Config Entities](config-entities.md) — creating config entities
- Reference: [Configuration API Documentation](https://api.drupal.org/api/drupal/core!core.api.php/group/config_api)
