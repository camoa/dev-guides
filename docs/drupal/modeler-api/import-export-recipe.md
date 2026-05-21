---
description: Modeler API import, archive export, and Recipe export — mechanisms, Drush command, and exportability control
tldr: "Three distribution mechanisms exist: archive export (.tar.gz), Recipe export (full Drupal Recipe directory via ExportRecipe service or drush modeler_api:model:export), and import. Recipe export requires Drush 13+ and populates recipe.yml from the model's metadata — fill in the documentation field before exporting."
drupal_version: "11.x"
---

# Import, Export, and Recipe Export

## When to Use

> Use this when shipping models with your module (Recipe export), when debugging export/import workflows, or when implementing `isExportable()` on your Model Owner.

## Decision

| Mechanism | UI entry | Drush command | What it produces |
|---|---|---|---|
| **Archive export** | `/{basePath}/{id}/export` | — | `.tar.gz` with all config YAML + `dependencies.yml` |
| **Recipe export** | `/{basePath}/{id}/recipe` form | `modeler_api:model:export` | Full Drupal Recipe directory (`recipe.yml`, `composer.json`, `config/`, `README.md`) |
| **Import** | `/{basePath}/import` form | — | Reads an archive `.tar.gz` and imports via config import |

## Pattern

**Recipe export via Drush (recommended for CI pipelines):**

```bash
# Basic export (to temporary://recipe):
drush modeler_api:model:export eca my_automation_id

# With custom namespace and destination:
drush modeler_api:model:export eca my_automation_id \
  --namespace=my-vendor \
  --destination=../recipes/my_automation
```

The `ExportRecipe` service (`modeler_api.export.recipe`) produces:
- `recipe.yml` — Recipe type `Workflow`, lists required modules and config actions/imports
- `composer.json` — `drupal-recipe` type, declares `drupal/core >=11.2` and contrib dependencies
- `config/` — YAML for all config entities that cannot be re-imported from a module
- `README.md` — Installation instructions with `drush recipe` command

**Controlling exportability:**

```php
// Prevent specific models from appearing in the export UI:
public function isExportable(ConfigEntityInterface $model): bool {
  return !$model->getThirdPartySetting('my_module', 'system_model', FALSE);
}
```

**Dependency resolution:** `Api::exportArchive()` recursively resolves all config dependencies so the archive is self-contained. With `STORAGE_OPTION_SEPARATE`, the corresponding `modeler_api.data_model.*` entity is automatically included.

User roles referenced by model config are exported as `ensure_exists` + `grantPermissions` config actions (additive-safe for Recipe application).

## Common Mistakes

- **Wrong**: Using `drush recipe` with Drush < 13 → **Right**: The `drush recipe` command requires Drush 13. Earlier versions need `php core/scripts/drupal recipe`.
- **Wrong**: Changing `config.strict: false` in the exported recipe → **Right**: The export sets this intentionally to allow partial config imports. Do not change it.
- **Wrong**: Exporting before filling in the `documentation` field → **Right**: The `documentation` metadata value becomes the `description` in `recipe.yml` and `README.md`. Fill it in before exporting.

## See Also

- [DataModel Entity and Storage](data-model-entity-storage.md)
- [Drush Commands](drush-commands.md)
- Reference: `src/ExportRecipe.php`, `src/Form/ExportRecipe.php`, `src/Drush/Commands/ModelerApiCommands.php`
