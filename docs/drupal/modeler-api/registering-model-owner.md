---
description: Register a config entity as a Modeler API Model Owner — plugin class, component management, constraints, and optional features
tldr: "Implement ModelOwnerBase in src/Plugin/ModelerApiModelOwner/ with the #[ModelOwner] attribute, declare configEntityBasePath() for auto-generated routes, and implement usedComponents/resetComponents/addComponent as the save-cycle contract. Constructors are final — use lazy getter injection."
drupal_version: "11.x"
---

# Registering a Model Owner

## When to Use

> Use this when you want your module's config entity type to appear in the Modeler API ecosystem — with its own admin UI, permissions, routes, and visual editing.

## Decision

| Step | What to do | Notes |
|------|-----------|-------|
| 1. Dependency | Add `modeler_api:modeler_api` to `.info.yml` dependencies | Required |
| 2. Plugin class | Extend `ModelOwnerBase` in `src/Plugin/ModelerApiModelOwner/` | Use `#[ModelOwner]` attribute |
| 3. Identity methods | Implement `modelIdExistsCallback()`, `configEntityProviderId()`, `configEntityTypeId()`, `configEntityBasePath()` | Required |
| 4. Component contract | Implement `usedComponents()`, `resetComponents()`, `addComponent()`, `ownerComponent()` | Core save cycle |
| 5. Service injection | Use lazy getter methods | `__construct()` and `create()` are `final` |

## Pattern

**Minimal plugin class:**

```php
namespace Drupal\my_module\Plugin\ModelerApiModelOwner;

use Drupal\modeler_api\Api;
use Drupal\modeler_api\Attribute\ModelOwner;
use Drupal\modeler_api\Component;
use Drupal\modeler_api\Plugin\ModelerApiModelOwner\ModelOwnerBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[ModelOwner(
  id: 'my_workflow',
  label: new TranslatableMarkup('My Workflow'),
  description: new TranslatableMarkup('Visual modeler for My Module workflows.'),
)]
class MyWorkflow extends ModelOwnerBase {
  public function modelIdExistsCallback(): array {
    return [\Drupal\my_module\Entity\Workflow::class, 'load'];
  }
  public function configEntityProviderId(): string { return 'my_module'; }
  public function configEntityTypeId(): string { return 'my_module_workflow'; }
  public function configEntityBasePath(): ?string {
    return 'admin/config/workflow/my-workflows';
  }
  public function supportedOwnerComponentTypes(): array {
    return [
      Api::COMPONENT_TYPE_START   => 'trigger',
      Api::COMPONENT_TYPE_ELEMENT => 'action',
      Api::COMPONENT_TYPE_LINK    => 'condition',
    ];
  }
}
```

**Component management methods (save-cycle contract):**

```php
public function usedComponents(ConfigEntityInterface $model): array {
  $components = [];
  foreach ($model->get('events') ?? [] as $eventId => $event) {
    $successors = array_map(
      fn($s) => new ComponentSuccessor($s['target'], $s['condition'] ?? ''),
      $event['successors'] ?? [],
    );
    $components[] = new Component($this, $eventId, Api::COMPONENT_TYPE_START,
      $event['plugin'], $event['label'] ?? '', $event['configuration'] ?? [], $successors);
  }
  return $components;
}

public function resetComponents(ConfigEntityInterface $model): ModelOwnerInterface {
  $model->set('events', [])->set('actions', [])->set('conditions', []);
  return $this;
}

public function addComponent(ConfigEntityInterface $model, Component $component): bool {
  $id = $component->getId();
  match ($component->getType()) {
    Api::COMPONENT_TYPE_START => $model->set('events',
      ($model->get('events') ?? []) + [$id => [
        'plugin' => $component->getPluginId(),
        'label' => $component->getLabel(),
        'configuration' => $component->getConfiguration(),
      ]]),
    default => NULL,
  };
  return TRUE;
}
```

**Lazy getter injection (instead of constructor DI):**

```php
protected ?MyEventPluginManager $eventManager = NULL;

protected function getEventManager(): MyEventPluginManager {
  if (!isset($this->eventManager)) {
    $this->eventManager = \Drupal::service('plugin.manager.my_event');
  }
  return $this->eventManager;
}
```

**Model constraints (optional but recommended):**

```php
public function modelConstraints(): array {
  return [
    Api::COMPONENT_TYPE_START => ['min' => 1, 'max' => 1,
      'successors' => ['min' => 1, 'max' => 1]],
    Api::COMPONENT_TYPE_ELEMENT => ['min' => 1],
    Api::COMPONENT_TYPE_LINK => ['successors' => [
      'max' => 1, 'requireConditionWhenParallel' => TRUE]],
  ];
}
```

**Optional features:**

| Feature | Enable via | What it does |
|---------|-----------|-------------|
| Replay data | `supportsReplayData(): bool = TRUE` | Shows execution trace overlay in modeler |
| In-modeler testing | `supportsTesting(): bool = TRUE` | Start/poll/cancel async test jobs |
| Templates | Entity type key `template` | Mark models as reusable templates |
| Settings form | `settingsForm(): string` | Returns form class for owner-specific settings |
| Documentation links | `docBaseUrl()` + `pluginDocUrl()` | Per-plugin external docs links |

## Common Mistakes

- **Wrong**: Overriding `__construct()` or `create()` → **Right**: Both are `final` in `ModelOwnerBase`. Use lazy getters instead.
- **Wrong**: Returning `NULL` from `configEntityBasePath()` when you want routing → **Right**: `NULL` means the module manages its own routes; only internal API routes (save, config, replay, test) are still generated.
- **Wrong**: Not clearing storage in `resetComponents()` → **Right**: Forgetting to clear causes deleted canvas components to persist in entity config after save.
- **Wrong**: Mismatched `configEntityProviderId()` → **Right**: Must match the module name that provides the config entity type (used in export archive filenames).

## See Also

- [The Component Model](component-model.md)
- [DataModel Entity and Storage](data-model-entity-storage.md)
- [YAML Plugin Definitions](yaml-plugin-definitions.md)
- Reference: `src/Plugin/ModelerApiModelOwner/ModelOwnerBase.php`, `src/Plugin/ModelerApiModelOwner/ModelOwnerInterface.php`, `eca-src/modules/ui/src/Plugin/ModelerApiModelOwner/Eca.php`
