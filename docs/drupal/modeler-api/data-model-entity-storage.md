---
description: Modeler API raw data storage — third-party settings, separate DataModel entity, or none
tldr: "Raw model data (JSON/XML) is stored separately from the structured config entity. Default is third-party settings (portable, good for small models); use STORAGE_OPTION_SEPARATE for large models to avoid config blob limits; STORAGE_OPTION_NONE requires implementing convert() so the modeler can reconstruct from entity config."
drupal_version: "11.x"
---

# DataModel Entity and Storage

## When to Use

> Use this when deciding where to store raw model data, when troubleshooting large model sizes hitting config blob limits, or when implementing `defaultStorageMethod()`.

## Decision

| Constant | Value | How stored | When to use |
|---|---|---|---|
| `Settings::STORAGE_OPTION_THIRD_PARTY` | `'third-party'` | Embedded in the config entity's third-party settings under `modeler_api.data` | Default. Good for small models. Portable in config export. |
| `Settings::STORAGE_OPTION_SEPARATE` | `'separate'` | In a dedicated `modeler_api_data_model` config entity, linked by MD5 hash | Recommended for large models (BPMN XML can be tens of KB). Avoids config size limits. |
| `Settings::STORAGE_OPTION_NONE` | `'none'` | Not stored. Modeler reconstructs from entity config via `convert()`. | When the owner fully captures state in its own config (e.g., `ai_agents`). |

Storage method resolution priority: per-model override → global settings → `defaultStorageMethod()`.

## Pattern

```php
// In your ModelOwnerBase subclass:
public function defaultStorageMethod(): string {
  return \Drupal\modeler_api\Form\Settings::STORAGE_OPTION_SEPARATE;
}

// Prevent users from changing it in the UI:
public function enforceDefaultStorageMethod(): bool {
  return FALSE; // TRUE to lock the setting
}
```

**DataModel config entity** — machine name `modeler_api_data_model`, config prefix `modeler_api.data_model`.

- ID format: `{entity_type_id}_{modeler_plugin_id}_{model_id}` (e.g., `eca_workflow_modeler_my_eca`)
- Only two fields: `id` and `data` (raw string)
- When using separate storage, the hash `hash:{md5}` is stored in third-party settings; `ModelOwnerBase::getModelData()` retrieves the data model entity and verifies the hash before returning data

For new (unsaved) models, separate storage falls back to third-party automatically. The permanent `modeler_api_data_model` entity is created on first save.

## Common Mistakes

- **Wrong**: Using `STORAGE_OPTION_NONE` without implementing `convert()` → **Right**: Without `convert()`, the modeler opens blank for existing models. `convert()` must call `owner->getUsedComponents()` to reconstruct canvas data.
- **Wrong**: Assuming config export includes separate DataModel entities automatically → **Right**: They are separate config entities and must be explicitly exported. Recipe export and archive export both handle this automatically.

## See Also

- [Registering a Model Owner](registering-model-owner.md)
- [Import, Export, and Recipe Export](import-export-recipe.md)
- Reference: `src/Entity/DataModel.php`, `src/Plugin/ModelerApiModelOwner/ModelOwnerBase.php`, `src/Form/Settings.php`
