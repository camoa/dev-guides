---
description: Load, create, modify, and place blocks programmatically via code
tldr: "Use in update hooks, migrations, or automated tasks when you need to load, create, modify, or place blocks via code rather than the UI."
drupal_version: "11.x"
---

# Programmatic Block Operations

## When to Use

> Loading, creating, modifying, or placing blocks via code (update hooks, migrations, automated tasks).

## Items

#### Loading block plugins
**Description:** Get a block plugin instance to call its methods
**Code:**
```php
$plugin_manager = \Drupal::service('plugin.manager.block');
$plugin = $plugin_manager->createInstance('system_branding_block', [
  'label' => 'My Branding',
]);
$build = $plugin->build();
```
**Gotchas:** Plugin instance is temporary; configuration not persisted unless you create a Block config entity

#### Loading Block config entities
**Description:** Get placed block configuration
**Code:**
```php
$block = Block::load('olivero_branding');
$plugin_id = $block->getPluginId();
$region = $block->getRegion();
$settings = $block->get('settings');
```
**Gotchas:** Load by Block entity ID (unique), not plugin ID (reusable)

#### Creating Block config entity (placement)
**Description:** Programmatically place a block in a region
**Code:**
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
**Gotchas:** ID must be unique per theme; region must exist in theme

#### Listing all block plugins
**Description:** Get all available block plugins
**Code:**
```php
$plugin_manager = \Drupal::service('plugin.manager.block');
$definitions = $plugin_manager->getDefinitions();
foreach ($definitions as $plugin_id => $definition) {
  $label = $definition['admin_label'];
}
```
**Gotchas:** Returns all plugins, including derivatives; filter as needed

#### Listing placed blocks by theme/region
**Description:** Get Block config entities by criteria
**Code:**
```php
$blocks = \Drupal::entityTypeManager()
  ->getStorage('block')
  ->loadByProperties([
    'theme' => 'olivero',
    'region' => 'header',
  ]);
```
**Gotchas:** Returns disabled blocks too; check `$block->status()` if needed

#### Rendering a block programmatically
**Description:** Get render array for a block without placement
**Code:**
```php
$plugin_manager = \Drupal::service('plugin.manager.block');
$plugin = $plugin_manager->createInstance('system_branding_block');
$build = $plugin->build();
// Add wrapper like BlockViewBuilder does
$build = [
  '#theme' => 'block',
  '#configuration' => $plugin->getConfiguration(),
  '#plugin_id' => $plugin->getPluginId(),
  'content' => $build,
];
```
**Gotchas:** Bypasses access checks and visibility conditions; handle manually if needed

#### Disabling/enabling blocks
**Description:** Toggle block visibility without deleting
**Code:**
```php
$block = Block::load('olivero_search');
$block->disable();
$block->save();

$block->enable();
$block->save();
```
**Gotchas:** `disable()` sets status to FALSE; block still exists but doesn't render

#### Deleting block placement
**Description:** Remove Block config entity
**Code:**
```php
$block = Block::load('olivero_search');
$block->delete();
```
**Gotchas:** Only deletes placement config, not the plugin or content entity it references

#### Creating BlockContent entity
**Description:** Programmatically create content block
**Code:**
```php
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
$uuid = $block_content->uuid();
```
**Gotchas:** Use UUID for referencing across environments, not entity ID

#### Placing a BlockContent entity
**Description:** Place a content block in a region
**Code:**
```php
$block_content = BlockContent::load(1);
$block = Block::create([
  'id' => 'olivero_my_content',
  'plugin' => 'block_content:' . $block_content->uuid(),
  'theme' => 'olivero',
  'region' => 'sidebar_first',
]);
$block->save();
```
**Gotchas:** Plugin ID format is `block_content:{uuid}`; must use UUID, not entity ID

## Common Mistakes

- Confusing block plugin instances with Block config entities → Plugins define behavior; entities define placement
- Not handling exceptions when loading blocks → `Block::load()` returns NULL if not found; check before using
- Hardcoding entity IDs → Use UUIDs for portability across environments
- Creating Block entities without checking if they exist → Duplicate ID causes error; check first or use `loadOrCreate()`
- Rendering blocks without access checks → Programmatic rendering bypasses `blockAccess()`; call manually if needed

## See Also

- [Creating Block Plugins](creating-block-plugins.md)
- [Block Placement & Configuration](block-placement.md)
- [Content Block Entities](content-blocks.md)
- Reference: https://www.drupal.org/docs/drupal-apis/entity-api
