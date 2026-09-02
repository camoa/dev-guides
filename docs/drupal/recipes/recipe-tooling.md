---
description: Tools for applying, testing, and developing recipes including Drush commands and core scripts
tldr: "Use recipe tooling when you need to apply recipes, export content, or integrate recipes into custom workflows."
drupal_version: "11.x"
---

# Recipe Tooling

## When to Use

> Use recipe tooling when you need to apply recipes, export content, or integrate recipes into custom workflows.

Tools for applying, testing, and developing recipes.

## Items: Recipe Commands and APIs

### drush recipe

**Description:** Apply recipe via Drush
**Usage:**
```bash
drush recipe recipes/my_recipe
drush recipe /path/to/recipe
drush recipe myorg/my-recipe  # Composer package
```
**Gotchas:** Drush 12+ required; prompts for inputs; shows batch progress

### core/scripts/drupal recipe

**Description:** Apply recipe via core PHP script (no Drush)
**Usage:**
```bash
php core/scripts/drupal recipe recipes/my_recipe
php core/scripts/drupal recipe core/recipes/standard -v
```
**Gotchas:** No Drush dependency; `-v` flag outputs step-by-step progress; useful for CI/automated installs; prompts via Symfony Console

### core/scripts/drupal quick-start

**Description:** Install Drupal from scratch using a recipe (no install profile required)
**Usage:**
```bash
php core/scripts/drupal quick-start core/recipes/article_content_type
```
**Gotchas:** New in Drupal 10.3; skips install profile entirely; installs minimal Drupal + applies recipe; useful for development and testing

### drush content:export

**Description:** Export content entities to YAML
**Usage:**
```bash
drush content:export node 123 recipes/my_recipe/content --dependencies
drush content:export media 456 recipes/my_recipe/content
```
**Gotchas:** Added in Drupal 11.1; requires Drush; auto-handles dependencies and files

### RecipeRunner::processRecipe()

**Description:** Programmatically apply recipe
**Usage:**
```php
use Drupal\Core\Recipe\Recipe;
use Drupal\Core\Recipe\RecipeRunner;

$recipe = Recipe::createFromDirectory('/path/to/recipe');
RecipeRunner::processRecipe($recipe);
```
**Gotchas:** Static method; uses service container; no batch; runs synchronously

### RecipeRunner::toBatchOperations()

**Description:** Convert recipe to batch operations
**Usage:**
```php
$recipe = Recipe::createFromDirectory('/path/to/recipe');
$operations = RecipeRunner::toBatchOperations($recipe);
$batch = [
  'operations' => $operations,
  'finished' => 'recipe_batch_finished',
];
batch_set($batch);
```
**Gotchas:** Breaks recipe into steps; useful for web-based application; handles timeouts

## Common Mistakes

- Using old Drush versions → Recipe support requires Drush 12+; earlier versions don't have recipe command
- Not handling batch callbacks → toBatchOperations requires custom finished callback; see core examples
- Applying recipes in wrong environment → Recipes modify active config; test in safe environment first
- Assuming Drush is only option → Core script works without Drush; good for Docker/CI
- Forgetting to clear cache after manual application → Config changes may not take effect until cache clear

## See Also

- Previous: ← [Composer Integration & Publishing](composer-integration.md)
- Next: [Core Recipes Catalog](core-recipes-catalog.md) →
- Reference: `core/lib/Drupal/Core/Recipe/RecipeRunner.php`
