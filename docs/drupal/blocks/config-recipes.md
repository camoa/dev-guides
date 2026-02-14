---
description: Export block configuration and use in recipes for deployment
drupal_version: "11.x"
---

# Config Management & Recipes

## When to Use

Exporting block configuration for deployment, syncing between environments, or using in recipes.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 2 (export) | Deploying to production | Export full config, review diffs before deploy |
| Step 3 (structure) | Referencing content blocks | Use UUID in plugin ID (`block_content:{uuid}`) |
| Step 4 (import) | Config already exists | Import will update existing; check for conflicts |
| Step 5 (recipes) | Drupal 11.1+ | Use PlaceBlock action for cleaner recipe syntax |

## Pattern

**Block config structure:**
- Block plugins → No exportable config (they're code)
- Block config entities → Exportable YAML (`block.block.*.yml`)
- Visibility conditions → Stored in `visibility` key
- Plugin settings → Stored in `settings` key

**Config file structure (block.block.olivero_branding.yml):**
```yaml
uuid: abc-123
langcode: en
status: true
dependencies:
  module: [system]
  theme: [olivero]
id: olivero_branding
theme: olivero
region: header
weight: -10
provider: null
plugin: system_branding_block
settings:
  id: system_branding_block
  label: 'Site branding'
  label_display: '0'
  use_site_logo: true
  use_site_name: true
  use_site_slogan: false
visibility: {}
```

**Exporting via Drush:**
```bash
drush config:export --destination=/tmp/config
# Review block.block.*.yml files
cp /tmp/config/block.block.* config/sync/
drush config:import
```

**Programmatic config:**
```php
use Drupal\block\Entity\Block;

// Create from array
$block = Block::create([
  'id' => 'olivero_search',
  'plugin' => 'search_form_block',
  'region' => 'header',
  'theme' => 'olivero',
  'settings' => ['label' => 'Search'],
]);
$block->save();

// Or modify existing config
$config = \Drupal::configFactory()->getEditable('block.block.olivero_search');
$config->set('region', 'sidebar_first');
$config->save();
```

**Recipe example (recipes/myrecipe/recipe.yml):**
```yaml
name: 'Site blocks'
description: 'Configures standard site blocks'
type: 'Site building'
config:
  actions:
    block.block.olivero_branding:
      placeBlock:
        plugin: system_branding_block
        region: header
        theme: olivero
        weight: -10
        settings:
          use_site_logo: true
          use_site_name: true
          use_site_slogan: false
    block.block.olivero_search:
      placeBlock:
        plugin: search_form_block
        region: header
        theme: olivero
        weight: -5
```

**Reference:** `core/modules/block/src/Plugin/ConfigAction/PlaceBlock.php`, https://www.drupal.org/docs/distributions-modules-and-themes/creating-distributions/how-to-write-a-recipe

## Common Mistakes

- **Wrong**: Exporting UUID when not needed → **Right**: UUIDs change per environment; remove for reusable config
- **Wrong**: Not checking dependencies → **Right**: Block config requires theme and module dependencies; verify they exist
- **Wrong**: Hardcoding entity IDs in visibility conditions → **Right**: Use UUIDs or labels for portability
- **Wrong**: Importing config without reviewing diffs → **Right**: Can overwrite production customizations
- **Wrong**: Not updating config after code changes → **Right**: Block plugin changes don't auto-update placed block settings

## See Also

- [Block Placement & Configuration](block-placement.md)
- [Programmatic Block Operations](programmatic-operations.md)
- Reference: https://www.drupal.org/docs/configuration-management
