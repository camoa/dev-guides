---
description: Control where blocks appear via regions, themes, and Block config entities
tldr: "Use when controlling where blocks appear (regions, themes) and their configuration (weight, visibility, settings). Block config entities are the placement layer — distinct from the block plugin itself."
drupal_version: "11.x"
---

# Block Placement & Configuration

## When to Use

> Controlling where blocks appear (regions, themes) and their configuration (weight, visibility, settings).

## Steps

1. **Understanding Block config entity**
   - References a block plugin (via `plugin` property)
   - Stores instance-specific settings
   - Tied to specific theme and region
   - Contains visibility conditions

2. **Placing blocks via UI**
   - Navigate to `/admin/structure/block`
   - Select theme
   - Click "Place block" in desired region
   - Configure and save

3. **Placing blocks programmatically**
   ```php
   $block = Block::create([
     'id' => 'my_block_instance',
     'plugin' => 'system_branding_block',
     'region' => 'header',
     'theme' => 'bartik',
     'weight' => -10,
     'settings' => [
       'label' => 'Site branding',
       'label_display' => 0,
     ],
   ]);
   $block->save();
   ```

4. **Modifying placement**
   ```php
   $block = Block::load('my_block_instance');
   $block->setRegion('sidebar_first');
   $block->setWeight(5);
   $block->save();
   ```

5. **Removing placement**
   ```php
   $block = Block::load('my_block_instance');
   $block->delete(); // Only deletes placement, not the plugin
   ```

## Decision Points

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 2 (UI placement) | Same block in multiple regions/themes | Create separate Block config entities |
| Step 3 (programmatic) | Deploying across environments | Export config or use recipes |
| Step 3 (programmatic) | Settings come from block plugin | Don't override unless necessary |
| Step 4 (modify) | Changing multiple blocks | Use batch operations or update hooks |
| Step 5 (remove) | Temporarily hiding block | Set `status => FALSE` instead of deleting |

## Pattern

**Complete block placement:**

```php
use Drupal\block\Entity\Block;

$block = Block::create([
  'id' => 'olivero_search',
  'plugin' => 'search_form_block',
  'region' => 'header',
  'theme' => 'olivero',
  'weight' => -5,
  'status' => TRUE,
  'settings' => [
    'label' => 'Search',
    'label_display' => '0',
    'provider' => 'search',
  ],
  'visibility' => [
    'request_path' => [
      'id' => 'request_path',
      'negate' => FALSE,
      'pages' => '/admin/*',
    ],
  ],
]);
$block->save();
```

**Loading blocks by region:**

```php
$blocks = \Drupal::entityTypeManager()
  ->getStorage('block')
  ->loadByProperties([
    'theme' => 'olivero',
    'region' => 'sidebar_first',
  ]);
```

**Reference:** `core/modules/block/src/Entity/Block.php`, `core/modules/block/src/BlockRepository.php`

## Common Mistakes

- Using same block ID across themes → Each Block config entity must have unique ID
- Deleting Block entity thinking it deletes the plugin → Only removes placement; plugin still exists
- Not setting `theme` property → Required; block won't render
- Hardcoding region names → Check theme regions; they vary per theme
- Placing disabled blocks without checking status → Set `status => TRUE` for active blocks

## See Also

- [Visibility Conditions](visibility-conditions.md)
- [Config Management & Recipes](config-recipes.md)
- [Programmatic Block Operations](programmatic-operations.md)
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/block-module/managing-blocks
