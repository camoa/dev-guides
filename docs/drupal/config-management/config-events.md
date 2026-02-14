---
description: React to config changes via event subscribers — save, delete, import, rename events.
---

# Config Events

## When to Use

When you need to react to config changes — save, delete, import, rename — via event subscribers.

## Config Events

| Event | When Fired | Use For |
|-------|------------|---------|
| `ConfigEvents::SAVE` | After config saved | Cache invalidation, logging, notifications |
| `ConfigEvents::DELETE` | After config deleted | Cleanup, logging |
| `ConfigEvents::RENAME` | After config renamed | Update references |
| `ConfigEvents::IMPORT` | After full import | Post-import tasks, cache rebuild |
| `ConfigEvents::IMPORT_VALIDATE` | Before import | Validate config, prevent invalid imports |
| `ConfigCollectionEvents::SAVE_IN_COLLECTION` | Save in non-default collection | Language config changes |
| `ConfigCollectionEvents::DELETE_IN_COLLECTION` | Delete in non-default collection | Collection-specific cleanup |

**Reference:** `/core/lib/Drupal/Core/Config/ConfigEvents.php`, `/core/lib/Drupal/Core/Config/ConfigCrudEvent.php`

## Pattern: Event Subscriber

```php
// mymodule/src/EventSubscriber/ConfigSubscriber.php
namespace Drupal\mymodule\EventSubscriber;

use Drupal\Core\Config\ConfigCrudEvent;
use Drupal\Core\Config\ConfigEvents;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

class ConfigSubscriber implements EventSubscriberInterface {

  public static function getSubscribedEvents() {
    return [
      ConfigEvents::SAVE => 'onConfigSave',
      ConfigEvents::DELETE => 'onConfigDelete',
      ConfigEvents::IMPORT_VALIDATE => 'onConfigImportValidate',
    ];
  }

  public function onConfigSave(ConfigCrudEvent $event) {
    $config = $event->getConfig();
    $config_name = $config->getName();

    // React to specific config changes
    if ($config_name === 'system.site') {
      $site_name = $config->get('name');
      \Drupal::logger('mymodule')->notice('Site name changed to @name', ['@name' => $site_name]);
    }

    // Invalidate custom cache
    if (str_starts_with($config_name, 'mymodule.')) {
      \Drupal::cache('mymodule')->invalidateAll();
    }
  }

  public function onConfigDelete(ConfigCrudEvent $event) {
    $config = $event->getConfig();
    $config_name = $config->getName();

    // Cleanup when config deleted
    if (str_starts_with($config_name, 'mymodule.example.')) {
      // Delete related data
    }
  }

  public function onConfigImportValidate(ConfigImporterEvent $event) {
    $importer = $event->getConfigImporter();

    // Prevent invalid imports
    if ($importer->hasUnprocessedConfigurationChanges()) {
      $changes = $importer->getStorageComparer()->getChangelist('create');
      foreach ($changes as $config_name) {
        if (str_starts_with($config_name, 'mymodule.')) {
          // Validate config before import
          $data = $importer->getStorageComparer()->getSourceStorage()->read($config_name);
          if (empty($data['required_field'])) {
            $importer->logError('Required field missing in ' . $config_name);
          }
        }
      }
    }
  }
}
```

**Service definition:**
```yaml
# mymodule.services.yml
services:
  mymodule.config_subscriber:
    class: Drupal\mymodule\EventSubscriber\ConfigSubscriber
    tags:
      - { name: event_subscriber }
```

## Config Import Events

**Import Lifecycle:**
1. `ConfigEvents::IMPORT_VALIDATE` — Before import starts, validate changes
2. `ConfigEvents::IMPORT` — After full import succeeds
3. Individual `ConfigEvents::SAVE` for each created/updated config
4. Individual `ConfigEvents::DELETE` for each deleted config

## Getting Event Data

```php
public function onConfigSave(ConfigCrudEvent $event) {
  $config = $event->getConfig();

  // Config name
  $name = $config->getName();

  // Current data
  $data = $config->get();

  // Original data (before save)
  $original_data = $config->getOriginal();

  // Check if new config
  if ($config->isNew()) {
    // First save
  }

  // Check specific changes
  if ($config->get('enabled') !== $config->getOriginal('enabled')) {
    // 'enabled' key changed
  }
}
```

## Common Mistakes

- Heavy processing in event subscriber — Slows config save/import, use queue instead
- Not checking config name — Subscriber runs for ALL config changes
- Modifying config in SAVE event — Triggers another SAVE event, infinite loop
- Throwing exceptions in non-validate events — Config already saved, site broken
- Not clearing cache in subscriber — Old cached config still used
- Forgetting to tag service — Subscriber not registered, events not fired

## See Also

- [Config Factory & Reading Config](config-factory-and-reading-config.md) — reading config in subscribers
- [Config Synchronization](config-synchronization.md) — import events
- [Best Practices & Patterns](best-practices-and-patterns.md) — event subscriber patterns
- Reference: [ConfigEvents API](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Config!ConfigEvents.php)
