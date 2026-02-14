---
description: Tools for applying, testing, and developing recipes including Drush commands and core scripts
drupal_version: "11.x"
---

# Recipe Tooling

## When to Use

> Use recipe tooling when you need to apply recipes, export content, or integrate recipes into custom workflows.

## Decision

| Tool | Use For | Requirements |
|------|---------|--------------|
| drush recipe | Apply recipe via CLI | Drush 12+ |
| core/scripts/drupal recipe | Apply recipe without Drush | Core PHP, no Drush |
| core/scripts/drupal quick-start | Install Drupal from scratch using recipe | Drupal 10.3+ |
| drush content:export | Export content entities to YAML | Drupal 11.1+, Drush |
| RecipeRunner::processRecipe() | Programmatic recipe application | PHP code |
| RecipeRunner::toBatchOperations() | Convert recipe to batch for web | PHP code, batch API |

## Pattern

Apply recipe via Drush:

```bash
drush recipe recipes/my_recipe
drush recipe /path/to/recipe
drush recipe myorg/my-recipe  # Composer package
```

Apply recipe via core script (no Drush):

```bash
php core/scripts/drupal recipe recipes/my_recipe
php core/scripts/drupal recipe core/recipes/standard -v
```

Install Drupal from scratch using recipe:

```bash
php core/scripts/drupal quick-start core/recipes/article_content_type
```

Export content entities:

```bash
drush content:export node 123 recipes/my_recipe/content --dependencies
drush content:export media 456 recipes/my_recipe/content
```

Programmatic application:

```php
use Drupal\Core\Recipe\Recipe;
use Drupal\Core\Recipe\RecipeRunner;

$recipe = Recipe::createFromDirectory('/path/to/recipe');
RecipeRunner::processRecipe($recipe);
```

Batch operations for web-based application:

```php
$recipe = Recipe::createFromDirectory('/path/to/recipe');
$operations = RecipeRunner::toBatchOperations($recipe);
$batch = [
  'operations' => $operations,
  'finished' => 'recipe_batch_finished',
];
batch_set($batch);
```

## Common Mistakes

- **Wrong**: Using old Drush versions → **Right**: Recipe support requires Drush 12+; earlier versions don't have recipe command
- **Wrong**: Not handling batch callbacks → **Right**: toBatchOperations requires custom finished callback; see core examples
- **Wrong**: Applying recipes in wrong environment → **Right**: Recipes modify active config; test in safe environment first
- **Wrong**: Assuming Drush is only option → **Right**: Core script works without Drush; good for Docker/CI
- **Wrong**: Forgetting to clear cache after manual application → **Right**: Config changes may not take effect until cache clear

## See Also

- [Composer Integration & Publishing](composer-integration.md)
- [Core Recipes Catalog](core-recipes-catalog.md)
- Reference: `core/lib/Drupal/Core/Recipe/RecipeRunner.php`
