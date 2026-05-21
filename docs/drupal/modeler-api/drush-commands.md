---
description: Modeler API Drush commands — update, enable, disable, and model export
tldr: "Four Drush commands: modeler_api:update (migrate all models after plugin ID changes), modeler_api:disable / modeler_api:enable (bulk status toggle per owner), modeler_api:model:export (generate a Drupal Recipe directory). Run update on dev first — it permanently modifies stored raw data."
drupal_version: "11.x"
---

# Drush Commands

## When to Use

> Use this for maintenance tasks: bulk enable/disable after plugin ID changes, updating model raw data after plugin schema changes, and exporting models to Recipes in CI pipelines.

## Decision

| Command | Purpose | When to run |
|---|---|---|
| `modeler_api:update` | Migrate all models when plugin definitions changed | After major module upgrades that change plugin IDs or schema |
| `modeler_api:disable {owner_id}` | Disable all models for a given owner | Before a major migration or taking automation offline site-wide |
| `modeler_api:enable {owner_id}` | Re-enable all models for a given owner | After maintenance is complete |
| `modeler_api:model:export {owner_id} {id}` | Export a single model to a Drupal Recipe directory | CI pipelines, model distribution |

## Pattern

```bash
# Update all models after plugin changes (run on dev first):
drush modeler_api:update

# Disable all ECA models:
drush modeler_api:disable eca

# Re-enable:
drush modeler_api:enable eca

# Export to Drupal Recipe (basic):
drush modeler_api:model:export eca my_automation_id

# Export with custom namespace and destination:
drush modeler_api:model:export eca my_automation_id \
  --namespace=my-vendor \
  --destination=../recipes/my_automation
```

**`modeler_api:model:export` arguments and options:**

| Argument/Option | Description | Default |
|---|---|---|
| `owner_id` | Model Owner plugin ID (e.g., `eca`, `my_workflow`) | Required |
| `id` | The model's machine name | Required |
| `--namespace` | Composer package namespace prefix | `drupal` |
| `--destination` | Output directory relative to Drupal root | `temporary://recipe` |

`modeler_api:update` output: count of models not requiring updates, models updated, and errors reported. The `ModelerInterface::updateComponents()` method is called for each model; modelers detect and migrate outdated component data.

## Common Mistakes

- **Wrong**: Running `modeler_api:update` on production without testing → **Right**: Run on a dev environment first. The command permanently modifies stored raw data.
- **Wrong**: Passing owner IDs with wrong casing → **Right**: Owner IDs are lowercased internally. Pass them in lowercase (`eca`, not `ECA`).
- **Wrong**: Expecting `modeler_api:model:export` to apply the recipe → **Right**: The command only generates the recipe directory. Apply with `drush recipe` (Drush 13+) separately.

## See Also

- [Import, Export, and Recipe Export](import-export-recipe.md)
- Reference: `src/Drush/Commands/ModelerApiCommands.php`, `src/Update.php`, `src/ExportRecipe.php`
