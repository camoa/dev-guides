---
description: Quick reference to key recipe system classes and their locations in Drupal core
drupal_version: "11.x"
---

# Code Reference Map

## When to Use

> Use this reference when you need to locate core recipe classes for debugging, extending, or understanding recipe internals.

## Decision

### Recipe Core

| Class | Path | Purpose |
|-------|------|---------|
| Recipe | `core/lib/Drupal/Core/Recipe/Recipe.php` | Main recipe class, YAML parsing, validation |
| RecipeRunner | `core/lib/Drupal/Core/Recipe/RecipeRunner.php` | Applies recipes, batch operations |
| RecipeConfigurator | `core/lib/Drupal/Core/Recipe/RecipeConfigurator.php` | Manages recipe dependencies |
| InstallConfigurator | `core/lib/Drupal/Core/Recipe/InstallConfigurator.php` | Manages extension installation |
| ConfigConfigurator | `core/lib/Drupal/Core/Recipe/ConfigConfigurator.php` | Manages config import and strict mode |
| InputConfigurator | `core/lib/Drupal/Core/Recipe/InputConfigurator.php` | Collects and validates input values |

### Config Actions

| Class | Path | Purpose |
|-------|------|---------|
| ConfigActionManager | `core/lib/Drupal/Core/Config/Action/ConfigActionManager.php` | Plugin manager for config actions |
| SimpleConfigUpdate | `core/lib/Drupal/Core/Config/Action/Plugin/ConfigAction/SimpleConfigUpdate.php` | Updates simple config |
| EntityMethod | `core/lib/Drupal/Core/Config/Action/Plugin/ConfigAction/EntityMethod.php` | Derives actions from entity methods |
| EntityCreate | `core/lib/Drupal/Core/Config/Action/Plugin/ConfigAction/EntityCreate.php` | Creates config entities |
| SetProperties | `core/lib/Drupal/Core/Config/Action/Plugin/ConfigAction/SetProperties.php` | Sets entity properties |

### Default Content

| Class | Path | Purpose |
|-------|------|---------|
| Finder | `core/lib/Drupal/Core/DefaultContent/Finder.php` | Finds and sorts content by dependencies |
| Exporter | `core/lib/Drupal/Core/DefaultContent/Exporter.php` | Exports content entities to YAML |
| Importer | `core/lib/Drupal/Core/DefaultContent/Importer.php` | Imports content from YAML |
| AdminAccountSwitcher | `core/lib/Drupal/Core/DefaultContent/AdminAccountSwitcher.php` | Switches to admin user for import |

### Config Checkpoint

| Class | Path | Purpose |
|-------|------|---------|
| Checkpoint | `core/lib/Drupal/Core/Config/Checkpoint/Checkpoint.php` | Represents a configuration snapshot |
| LinearHistory | `core/lib/Drupal/Core/Config/Checkpoint/LinearHistory.php` | Tracks checkpoint history for rollback |

### Supporting Classes

| Class | Path | Purpose |
|-------|------|---------|
| RecipeFileException | `core/lib/Drupal/Core/Recipe/RecipeFileException.php` | Recipe validation errors |
| RecipePreExistingConfigException | `core/lib/Drupal/Core/Recipe/RecipePreExistingConfigException.php` | Strict mode violations |
| InputCollectorInterface | `core/lib/Drupal/Core/Recipe/InputCollectorInterface.php` | Interface for collecting inputs |
| RecipeInputFormTrait | `core/lib/Drupal/Core/Recipe/RecipeInputFormTrait.php` | Form API integration for inputs |

## Common Mistakes

- **Wrong**: Looking for recipe classes in modules → **Right**: All recipe code is in core `lib/Drupal/Core/`
- **Wrong**: Extending Recipe class → **Right**: Recipe is final; compose via `recipes:` key instead
- **Wrong**: Implementing config actions outside plugin system → **Right**: Use ConfigActionPluginInterface and attributes
- **Wrong**: Not understanding default content is core → **Right**: Default content API is not contrib; shipped in core 10.3+
- **Wrong**: Assuming recipe classes are services → **Right**: Most are static or value objects; RecipeRunner uses static methods

## See Also

- [Security & Performance](security-performance.md)
- Reference: `core/recipes/` directory in Drupal core
