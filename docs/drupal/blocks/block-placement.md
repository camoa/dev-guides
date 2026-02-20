---
description: Control where blocks appear via regions, themes, and Block config entities
drupal_version: "11.x"
---

# Block Placement & Configuration

## When to Use

> Use when controlling where blocks appear (regions, themes) and their configuration (weight, visibility, settings). Block config entities are the placement layer — distinct from the block plugin itself.

## Decision

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

**Modifying placement:**

```php
$block = Block::load('my_block_instance');
$block->setRegion('sidebar_first');
$block->setWeight(5);
$block->save();
```

**Block config entity structure:**
- References a block plugin (via `plugin` property)
- Stores instance-specific settings
- Tied to specific theme and region
- Contains visibility conditions

**Reference:** `core/modules/block/src/Entity/Block.php`, `core/modules/block/src/BlockRepository.php`

## Common Mistakes

- **Wrong**: Using same block ID across themes → **Right**: Each Block config entity must have unique ID
- **Wrong**: Deleting Block entity thinking it deletes the plugin → **Right**: Only removes placement; plugin still exists
- **Wrong**: Not setting `theme` property → **Right**: Required; block won't render
- **Wrong**: Hardcoding region names → **Right**: Check theme regions; they vary per theme
- **Wrong**: Placing disabled blocks without checking status → **Right**: Set `status => TRUE` for active blocks

## See Also

- [Visibility Conditions](visibility-conditions.md)
- [Config Management & Recipes](config-recipes.md)
- [Programmatic Block Operations](programmatic-operations.md)
- Reference: https://www.drupal.org/docs/core-modules-and-themes/core-modules/block-module/managing-blocks
