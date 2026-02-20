---
description: Load, create, modify, and place blocks programmatically via code
drupal_version: "11.x"
---

# Programmatic Block Operations

## When to Use

> Use in update hooks, migrations, or automated tasks when you need to load, create, modify, or place blocks via code rather than the UI.

## Decision

| Operation | Code | Gotcha |
|-----------|------|--------|
| Load block plugin | `$plugin_manager->createInstance('plugin_id')` | Temporary; config not persisted |
| Load Block entity | `Block::load('entity_id')` | Load by Block ID, not plugin ID |
| Place block | `Block::create(['plugin' => '...'])->save()` | ID must be unique per theme |
| List all plugins | `$plugin_manager->getDefinitions()` | Returns all including derivatives |
| List placed blocks | `loadByProperties(['theme' => '...'])` | Returns disabled blocks too |
| Render block | `$plugin->build()` + wrapper | Bypasses access checks |
| Disable block | `$block->disable()->save()` | Sets status FALSE |
| Delete placement | `$block->delete()` | Only deletes placement, not plugin |

## Pattern

**Loading and rendering block plugin:**
```php
$plugin_manager = \Drupal::service('plugin.manager.block');
$plugin = $plugin_manager->createInstance('system_branding_block', [
  'label' => 'My Branding',
]);
$build = $plugin->build();
```

**Placing a block:**
```php
$block = Block::create([
  'id' => 'my_placed_block',
  'plugin' => 'system_powered_by_block',
  'theme' => 'olivero',
  'region' => 'footer',
  'weight' => 10,
  'settings' => ['label' => 'Powered by Drupal'],
]);
$block->save();
```

**Creating and placing content block:**
```php
use Drupal\block_content\Entity\BlockContent;

$block_content = BlockContent::create([
  'type' => 'basic',
  'info' => 'My Content Block',
  'reusable' => TRUE,
  'body' => [
    'value' => '<p>Block content</p>',
    'format' => 'basic_html',
  ],
]);
$block_content->save();

$block = Block::create([
  'id' => 'olivero_my_content',
  'plugin' => 'block_content:' . $block_content->uuid(),
  'theme' => 'olivero',
  'region' => 'sidebar_first',
]);
$block->save();
```

**Loading placed blocks by region:**
```php
$blocks = \Drupal::entityTypeManager()
  ->getStorage('block')
  ->loadByProperties([
    'theme' => 'olivero',
    'region' => 'header',
  ]);
```

**Rendering block with wrapper:**
```php
$plugin_manager = \Drupal::service('plugin.manager.block');
$plugin = $plugin_manager->createInstance('system_branding_block');
$build = $plugin->build();
$build = [
  '#theme' => 'block',
  '#configuration' => $plugin->getConfiguration(),
  '#plugin_id' => $plugin->getPluginId(),
  'content' => $build,
];
```

## Common Mistakes

- **Wrong**: Confusing block plugin instances with Block config entities → **Right**: Plugins define behavior; entities define placement
- **Wrong**: Not handling exceptions when loading blocks → **Right**: `Block::load()` returns NULL if not found; check before using
- **Wrong**: Hardcoding entity IDs → **Right**: Use UUIDs for portability across environments
- **Wrong**: Creating Block entities without checking if they exist → **Right**: Duplicate ID causes error; check first
- **Wrong**: Rendering blocks without access checks → **Right**: Programmatic rendering bypasses `blockAccess()`; call manually if needed

## See Also

- [Creating Block Plugins](creating-block-plugins.md)
- [Block Placement & Configuration](block-placement.md)
- [Content Block Entities](content-blocks.md)
- Reference: https://www.drupal.org/docs/drupal-apis/entity-api
