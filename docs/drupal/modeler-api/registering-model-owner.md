---
description: Register a config entity as a Modeler API Model Owner — plugin class, identity methods, save-cycle contract, lazy injection, palette, and constraints
tldr: "Implement ModelOwnerBase with #[ModelOwner], declare identity methods (configEntityTypeId, configEntityBasePath) for auto-generated routes, then implement the 7-step contract: class + component-type map, identity methods, lazy getter injection, save-cycle methods (usedComponents/resetComponents/addComponent/ownerComponent), palette methods, and buildConfigurationForm(). Constructors are final — use lazy getters. ECA's Eca plugin is the canonical reference."
drupal_version: "11.x"
---

# Registering a Model Owner

## When to Use

> Use this when you want your module's config entity type to appear in the Modeler API ecosystem — with its own admin UI, permissions, routes, and visual editing.

## Decision

The following 7-step walkthrough uses **ECA's own `Eca` plugin** (`Drupal\eca_ui\Plugin\ModelerApiModelOwner\Eca`) as the canonical reference. Swap ECA's event/condition/action services for your own domain's plugin managers.

| Step | What to implement | Key rule |
|------|------------------|----------|
| 1 | Add `modeler_api:modeler_api` to `.info.yml` | Required |
| 2 | Plugin class + `SUPPORTED_COMPONENT_TYPES` map | Maps Api type constants → your domain type strings |
| 3 | Identity methods | `configEntityBasePath()` drives all CRUD route generation |
| 4 | Lazy getter injection | `__construct()` and `create()` are `final` — no override |
| 5 | Save-cycle methods | `usedComponents`, `resetComponents`, `addComponent`, `ownerComponent` |
| 6 | Palette methods | `availableOwnerComponents`, `ownerComponentId`, `ownerComponentDefaultConfig` |
| 7 | `buildConfigurationForm()` | Renders the component settings form inside the modeler |

## Pattern

**Step 2 — Plugin class and component-type map:**

```php
namespace Drupal\eca_ui\Plugin\ModelerApiModelOwner;

use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\modeler_api\Api;
use Drupal\modeler_api\Attribute\ModelOwner;
use Drupal\modeler_api\Plugin\ModelerApiModelOwner\ModelOwnerBase;

#[ModelOwner(
  id: 'eca',
  label: new TranslatableMarkup('ECA'),
  description: new TranslatableMarkup('Configure ECA - Events, Conditions, Actions.'),
)]
class Eca extends ModelOwnerBase {

  // Maps each Modeler API component type to the owner's own type string.
  public const array SUPPORTED_COMPONENT_TYPES = [
    Api::COMPONENT_TYPE_START   => 'event',
    Api::COMPONENT_TYPE_LINK    => 'condition',
    Api::COMPONENT_TYPE_ELEMENT => 'action',
    Api::COMPONENT_TYPE_GATEWAY => 'gateway',
  ];
}
```

**Step 3 — Identity methods:**

```php
public function configEntityProviderId(): string { return 'eca'; }
public function configEntityTypeId(): string { return 'eca'; }
public function configEntityBasePath(): string { return 'admin/config/workflow/eca'; }

public function modelIdExistsCallback(): array {
  return [EcaModel::class, 'load'];
}
public function supportedOwnerComponentTypes(): array {
  return self::SUPPORTED_COMPONENT_TYPES;
}
public function componentLabels(): array {
  return ['start' => 'Event', 'element' => 'Action', 'link' => 'Condition', 'gateway' => 'Gateway'];
}
public function componentLabelsPlural(): array {
  return ['start' => 'Events', 'element' => 'Actions', 'link' => 'Conditions', 'gateway' => 'Gateways'];
}
```

**Step 4 — Lazy getter injection:**

```php
protected ?ContainerInterface $container;
protected Events $eventsService;

protected function getContainer(): ContainerInterface {
  if (!isset($this->container)) {
    $this->container = \Drupal::getContainer();
  }
  return $this->container;
}

protected function eventsService(): Events {
  if (!isset($this->eventsService)) {
    $this->eventsService = $this->getContainer()->get('eca.service.event');
  }
  return $this->eventsService;
}
// Repeat for conditionsService() and actionsService().
```

**Step 5 — Save-cycle methods:**

```php
// READ — entity config → Component[] for the canvas.
public function usedComponents(ConfigEntityInterface $model): array {
  $components = [];
  foreach (self::SUPPORTED_COMPONENT_TYPES as $type => $typeString) {
    foreach ($model->get($typeString . 's') ?? [] as $id => $item) {
      $successors = [];
      foreach ($item['successors'] ?? [] as $successor) {
        $successors[] = new ComponentSuccessor($successor['id'], $successor['condition'] ?? '');
      }
      $components[] = new Component(
        $this, $id, $type,
        $item['plugin'] ?? '', $item['label'] ?? '',
        $item['configuration'] ?? [], $successors,
      );
    }
  }
  return $components;
}

// SAVE step 1 — clear stored components before the API re-adds them.
public function resetComponents(ConfigEntityInterface $model): ModelOwnerInterface {
  $model->resetComponents();
  return $this;
}

// SAVE step 2 — persist one canvas node into entity config.
public function addComponent(ConfigEntityInterface $model, Component $component): bool {
  $id = $component->getId();
  $successors = array_map(
    fn($s) => ['id' => $s->getId(), 'condition' => $s->getConditionId()],
    $component->getSuccessors(),
  );
  return match ($component->getType()) {
    Api::COMPONENT_TYPE_START   => $model->addEvent($id, $component->getPluginId(), $component->getLabel(), $component->getConfiguration(), $successors),
    Api::COMPONENT_TYPE_LINK    => $model->addCondition($id, $component->getPluginId(), $component->getLabel(), $component->getConfiguration()),
    Api::COMPONENT_TYPE_ELEMENT => $model->addAction($id, $component->getPluginId(), $component->getLabel(), $component->getConfiguration(), $successors),
    Api::COMPONENT_TYPE_GATEWAY => $model->addGateway($id, 0, $successors, $component->getLabel()),
    default => FALSE,
  };
}

// Instantiate a domain plugin — the API uses this to validate components.
public function ownerComponent(int $type, string $id, array $config = []): ?PluginInspectionInterface {
  return match ($type) {
    Api::COMPONENT_TYPE_START   => $this->eventsService()->createInstance($id, $config),
    Api::COMPONENT_TYPE_LINK    => $this->conditionsService()->createInstance($id, $config),
    Api::COMPONENT_TYPE_ELEMENT => $this->actionsService()->createInstance($id, $config),
    default => NULL,
  };
}
```

**Step 6 — Palette methods:**

```php
public function availableOwnerComponents(int $type): array {
  return match ($type) {
    Api::COMPONENT_TYPE_START   => $this->eventsService()->events(),
    Api::COMPONENT_TYPE_LINK    => $this->conditionsService()->conditions(),
    Api::COMPONENT_TYPE_ELEMENT => $this->actionsService()->actions(),
    default => [],
  };
}
public function ownerComponentId(int $type): string {
  return self::SUPPORTED_COMPONENT_TYPES[$type] ?? 'unsupported';
}
public function ownerComponentDefaultConfig(int $type, string $id): array {
  $plugin = $this->ownerComponent($type, $id);
  return $plugin instanceof ConfigurableInterface ? $plugin->defaultConfiguration() : [];
}
```

**Step 7 — `buildConfigurationForm()`:**

```php
public function buildConfigurationForm(PluginInspectionInterface $plugin, ?string $modelId = NULL, bool $modelIsNew = TRUE): array {
  $form_state = new FormState();
  try {
    if ($plugin instanceof PluginFormInterface) {
      return $plugin->buildConfigurationForm([], $form_state);
    }
    return [];
  }
  catch (\Throwable $ex) {
    return ['error_message' => [
      '#type' => 'markup',
      '#markup' => '<strong>' . $this->t('Error in configuration form.') . '</strong><br>' . $ex->getMessage(),
    ]];
  }
}
```

**Model constraints (optional but recommended):**

ECA keeps constraints minimal — only requiring a condition when parallel edges exist:

```php
public function modelConstraints(): array {
  return [
    Api::COMPONENT_TYPE_START   => ['successors' => ['requireConditionWhenParallel' => TRUE]],
    Api::COMPONENT_TYPE_ELEMENT => ['successors' => ['requireConditionWhenParallel' => TRUE]],
    Api::COMPONENT_TYPE_GATEWAY => ['successors' => ['requireConditionWhenParallel' => TRUE]],
  ];
}
```

Each per-type entry also accepts `min` / `max` (component count) and nested `successors.min` / `successors.max` (out-degree). Violation messages use `componentLabels()` / `componentLabelsPlural()` strings from step 3.

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
- Reference: `src/Plugin/ModelerApiModelOwner/ModelOwnerBase.php`, `src/Plugin/ModelerApiModelOwner/ModelOwnerInterface.php`, `eca/modules/ui/src/Plugin/ModelerApiModelOwner/Eca.php`
