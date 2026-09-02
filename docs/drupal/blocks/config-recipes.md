---
description: Export block configuration and deploy via config sync or Drupal recipes
tldr: "Use when exporting block configuration for deployment, syncing between environments, or using `placeBlock` recipe actions (Drupal 11.1+). Block plugins have no exportable config — only Block config entities do."
drupal_version: "11.x"
---

# Config Management & Recipes

## When to Use

> Exporting block configuration for deployment, syncing between environments, or using in recipes.

## Steps

1. **Understanding block config structure**
   - Block plugins → No exportable config (they're code)
   - Block config entities → Exportable YAML (`block.block.*.yml`)
   - Visibility conditions → Stored in `visibility` key
   - Plugin settings → Stored in `settings` key

2. **Exporting block config**
   - Single config: `/admin/config/development/configuration/single/export`
   - Full config export: `drush config:export`
   - File location: `config/sync/block.block.{id}.yml`

3. **Config file structure**
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

4. **Importing block config**
   - UI: `/admin/config/development/configuration/single/import`
   - Drush: `drush config:import`
   - Programmatic: `\Drupal::service('config.installer')->installOptionalConfig()`

5. **Using PlaceBlock recipe action** (Drupal 11.1+)
   ```yaml
   name: 'Place custom blocks'
   config:
     actions:
       block.block.olivero_myblock:
         placeBlock:
           plugin: my_custom_block
           region: sidebar_first
           theme: olivero
           settings:
             label: 'My Block'
   ```

## Decision Points

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 2 (export) | Deploying to production | Export full config, review diffs before deploy |
| Step 3 (structure) | Referencing content blocks | Use UUID in plugin ID (`block_content:{uuid}`) |
| Step 4 (import) | Config already exists | Import will update existing; check for conflicts |
| Step 5 (recipes) | Drupal 11.1+ | Use PlaceBlock action for cleaner recipe syntax |

## Pattern

**Exporting block config via Drush:**
```bash
drush config:export --destination=/tmp/config
# Review block.block.*.yml files
cp /tmp/config/block.block.* config/sync/
drush config:import
```

**Programmatic config creation:**
```php
use Drupal\block\Entity\Block;

// Create from array
$config = [
  'id' => 'olivero_search',
  'plugin' => 'search_form_block',
  'region' => 'header',
  'theme' => 'olivero',
  'settings' => ['label' => 'Search'],
];

$block = Block::create($config);
$block->save();

// Or load config and modify
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

- Exporting UUID when not needed → UUIDs change per environment; remove for reusable config
- Not checking dependencies → Block config requires theme and module dependencies; verify they exist
- Hardcoding entity IDs in visibility conditions → Use UUIDs or labels for portability
- Importing config without reviewing diffs → Can overwrite production customizations
- Not updating config after code changes → Block plugin changes don't auto-update placed block settings

## See Also

- [Block Placement & Configuration](block-placement.md)
- [Programmatic Block Operations](programmatic-operations.md)
- Reference: https://www.drupal.org/docs/configuration-management
