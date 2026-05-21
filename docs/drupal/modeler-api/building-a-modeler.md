---
description: Build a custom Modeler plugin — required methods, JS integration points, and dependency injection
tldr: "Build a Modeler plugin only when Workflow Modeler and BPMN.iO genuinely don't fit. Extend ModelerBase with #[Modeler] attribute, implement parseData/readComponents/getRawData/edit, and use drupalSettings.modeler_api URLs for all JS endpoints — never hardcode them."
drupal_version: "11.x"
---

# Building a Modeler Plugin

## When to Use

> Use this when you are building a new visual editing experience from scratch — a new canvas technology, format, or specialized editor — and want to plug it into the Modeler API ecosystem. If you are only connecting an existing config entity to an existing visual editor, implement a Model Owner instead.

## Decision

| Method | Required? | Purpose |
|--------|----------|---------|
| `isEditable()` | Yes | Return `TRUE` to offer editing (default: `FALSE`) |
| `parseData()` | Yes | Ingest raw data, populate internal state |
| `readComponents()` | Yes | Convert internal state to `Component[]` |
| `getRawData()` | Yes | Serialize current state back to raw string |
| `edit()` | Yes (if editable) | Render array for the editing canvas |
| `configForm()` | Yes (if editable) | `JsonResponse` for component config forms |
| `prepareEmptyModelData()` | Yes | Raw data for a brand-new empty model |
| `convert()` | Recommended | Cross-modeler conversion via `getUsedComponents()` |
| `enable()`, `disable()`, `clone()` | Recommended | Lifecycle mutations on raw data |

## Pattern

```php
use Drupal\modeler_api\Attribute\Modeler;
use Drupal\modeler_api\Plugin\ModelerApiModeler\ModelerBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

#[Modeler(
  id: 'my_modeler',
  label: new TranslatableMarkup('My Modeler'),
  description: new TranslatableMarkup('Canvas built with My Technology.'),
)]
class MyModeler extends ModelerBase {

  protected array $parsedData = [];

  public function isEditable(): bool { return TRUE; }
  public function getRawFileExtension(): ?string { return 'json'; }

  public function parseData(ModelOwnerInterface $owner, string $data): void {
    $this->parsedData = json_decode($data, TRUE) ?? [];
  }

  public function readComponents(): array { /* build Component[] from parsedData */ }

  public function getRawData(): string {
    return json_encode($this->parsedData, JSON_PRETTY_PRINT);
  }

  public function edit(ModelOwnerInterface $owner, string $id, string $data,
    bool $isNew = FALSE, bool $readOnly = FALSE): array {
    return [
      '#type' => 'container',
      '#attached' => [
        'library' => ['my_modeler/editor'],
        'drupalSettings' => ['myModeler' => ['modelId' => $id, 'modelData' => $data]],
      ],
    ];
  }
}
```

**Lazy service injection** (`__construct()` and `create()` are `final`):

```php
protected function getMyService(): MyService {
  if (!isset($this->myService)) {
    $this->myService = $this->getContainer()->get('my_module.service');
  }
  return $this->myService;
}
```

**JavaScript integration** — use URLs from `drupalSettings.modeler_api`:

| Setting key | Route | Purpose |
|---|---|---|
| `save_url` | `entity.{type}.save` | `POST` raw data on save |
| `config_url` | `entity.{type}.config` | `POST` component config form (JSON) |
| `replay_url` | `entity.{type}.replay` | `GET` replay data |
| `test_url` | `entity.{type}.test` | Testing endpoints |
| `export_url` | `entity.{type}.export` | Export archive |
| `export_recipe_url` | `entity.{type}.export_recipe` | Recipe export form |

Model metadata is available at `drupalSettings.modeler_api.metadata` (version, label, documentation, storage, executable, template, tags, changelog).

## Common Mistakes

- **Wrong**: Building a Modeler when you just need a Model Owner → **Right**: If connecting an existing config entity to an existing visual editor, only implement a Model Owner.
- **Wrong**: Calling `owner->addComponent()` from the Modeler → **Right**: The Modeler only calls `parseData()` and `readComponents()`. The Api service handles `addComponent()`.
- **Wrong**: Hardcoding save endpoint URLs → **Right**: Always use the URL from `drupalSettings.modeler_api.save_url`; it includes the CSRF token and correct parameters.

## See Also

- [Architecture: Owners vs Modelers](architecture-owners-vs-modelers.md)
- [The Modeler Landscape](modeler-landscape.md)
- Reference: `src/Plugin/ModelerApiModeler/ModelerBase.php`, `modeler-src/src/Plugin/ModelerApiModeler/WorkflowModeler.php`
