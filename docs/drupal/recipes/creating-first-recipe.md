---
description: Follow this workflow to create a minimal working recipe from scratch
tldr: "Follow this workflow to create a minimal working recipe from scratch."
drupal_version: "11.x"
---

# Creating Your First Recipe

## When to Use

> Follow this workflow to create a minimal working recipe from scratch.

## Steps: Create and Apply a Minimal Recipe

1. **Create recipe directory** — Recipes live in discoverable locations
   ```bash
   mkdir -p recipes/my_recipe
   ```
   Recipes can be in `/recipes/`, module subdirectories, or Composer packages.

2. **Write recipe.yml** — Minimum viable recipe
   ```yaml
   name: 'My Recipe'
   description: 'Example recipe.'
   type: 'Feature'
   install:
     - node
   config:
     strict: false
   ```

3. **Add configuration (optional)** — Create `config/` directory for config files
   ```bash
   mkdir -p recipes/my_recipe/config
   # Export config from active site
   drush config:export --destination=recipes/my_recipe/config
   ```

4. **Apply the recipe** — Using Drush or core script
   ```bash
   # Drush (recommended)
   drush recipe recipes/my_recipe

   # Core script (no Drush)
   php core/scripts/drupal recipe recipes/my_recipe
   ```

## Decision Points: Config Layout and Strict Mode

| At this step... | If... | Then... |
|---|---|---|
| Adding configuration | Config is simple and static | Use `config/` directory for config files |
| Adding configuration | Config needs dynamic updates | Use `config.actions` for config actions |
| Choosing strict mode | Recipe sets up new functionality | Use `strict: false` to allow existing config |
| Choosing strict mode | Recipe enforces specific config state | Use `strict: true` or array of config names to validate |

## Common Mistakes

- Applying recipe before installing required modules → Use `install:` key to declare dependencies
- Putting recipe.yml in wrong location → Must be in recipe root directory, not subdirectory
- Using `config:` key without understanding strict mode → Defaults to `strict: true` in current core (may change)
- Not testing recipe on clean install → Recipes should be idempotent but are designed for apply-once
- Forgetting composer.json for published recipes → Recipes distributed via Composer need `type: drupal-recipe`

## See Also

- Previous: ← [Recipe YAML Schema](recipe-yaml-schema.md)
- Next: [Recipe Composition & Dependencies](recipe-composition.md) →
- Reference: https://project.pages.drupalcode.org/distributions_recipes/recipe.html
