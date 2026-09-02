---
description: React to block operations and alter block behavior with hooks
tldr: "Use alter hooks to modify block render arrays or access across all blocks or specific plugins. Use preprocess for adding template variables."
drupal_version: "11.x"
---

# Block Hooks & Events

## When to Use

> Reacting to block operations or altering block behavior across all blocks or specific plugins.

## Items

#### hook_block_view_alter
**Description:** Modify block render array after `build()` but before rendering
**Signature:**
```php
function hook_block_view_alter(
  array &$build,
  \Drupal\Core\Block\BlockPluginInterface $block
) {}
```
**Usage Example:**
```php
function mymodule_block_view_alter(&$build, BlockPluginInterface $block) {
  if ($block->getPluginId() === 'system_branding_block') {
    $build['#attached']['library'][] = 'mymodule/branding-enhancements';
    $build['#cache']['tags'][] = 'config:mymodule.branding';
  }
}
```
**Gotchas:** `$build` is the render array from `build()`; don't replace, modify; preserve cache metadata

#### hook_block_access
**Description:** Control access to block viewing for all blocks
**Signature:**
```php
function hook_block_access(
  \Drupal\block\Entity\Block $block,
  $operation,
  \Drupal\Core\Session\AccountInterface $account
) {}
```
**Usage Example:**
```php
function mymodule_block_access(Block $block, $operation, AccountInterface $account) {
  if ($operation === 'view' && $block->getPluginId() === 'my_block') {
    return AccessResult::forbiddenIf(!$account->hasPermission('view my block'))
      ->addCacheContexts(['user.permissions']);
  }
  return AccessResult::neutral();
}
```
**Gotchas:** Return `AccessResult`, not boolean; use `neutral()` when not making a decision

#### hook_block_view_BASE_BLOCK_ID_alter
**Description:** Alter specific block plugin by ID
**Signature:**
```php
function hook_block_view_BASE_BLOCK_ID_alter(
  array &$build,
  \Drupal\Core\Block\BlockPluginInterface $block
) {}
```
**Usage Example:**
```php
function mymodule_block_view_system_branding_block_alter(&$build, BlockPluginInterface $block) {
  // Only affects system_branding_block
  $build['#prefix'] = '<div class="custom-branding-wrapper">';
  $build['#suffix'] = '</div>';
}
```
**Gotchas:** Replace `BASE_BLOCK_ID` with plugin ID, underscores only (replace hyphens/colons)

#### hook_block_build_alter
**Description:** Legacy hook, deprecated in favor of `hook_block_view_alter`
**Status:** Deprecated
**Gotchas:** Don't use; use `hook_block_view_alter` instead

#### hook_entity_view_alter (for Block config entity)
**Description:** Alter Block config entity rendering (rare use case)
**Signature:**
```php
function hook_entity_view_alter(
  array &$build,
  \Drupal\Core\Entity\EntityInterface $entity,
  \Drupal\Core\Entity\Display\EntityViewDisplayInterface $display
) {}
```
**Usage Example:**
```php
function mymodule_entity_view_alter(&$build, EntityInterface $entity, $display) {
  if ($entity->getEntityTypeId() === 'block') {
    // Rarely needed; blocks rendered via BlockViewBuilder, not entity view
  }
}
```
**Gotchas:** Blocks don't typically use entity view pipeline; use `hook_block_view_alter` instead

#### preprocess_block
**Description:** Theme preprocess for block template variables
**Signature:**
```php
function hook_preprocess_block(&$variables) {}
```
**Usage Example:**
```php
function mytheme_preprocess_block(&$variables) {
  $block = $variables['elements']['#block'];
  $plugin_id = $block->getPluginId();
  $variables['custom_class'] = 'block-' . str_replace('_', '-', $plugin_id);
  $variables['region'] = $block->getRegion();
}
```
**Gotchas:** Access block via `$variables['elements']['#block']`; don't modify `$variables['content']` structure

## Common Mistakes

- Using `hook_block_build_alter` → Deprecated; use `hook_block_view_alter`
- Returning wrong type from `hook_block_access` → Must return `AccessResult`, not boolean or NULL
- Replacing `$build` array in alter hooks → Modify existing array; preserve cache metadata
- Not adding cache contexts when access varies → Leads to incorrect caching and wrong content shown
- Using generic `hook_block_view_alter` when `hook_block_view_BASE_BLOCK_ID_alter` is more appropriate → Specific hook is more efficient

## See Also

- [Block Access Control](block-access-control.md)
- [Block Rendering & Theming](block-rendering.md)
- Reference: https://api.drupal.org/api/drupal/core%21modules%21block%21block.api.php/group/block_api
