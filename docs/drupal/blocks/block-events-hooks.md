---
description: React to block operations and alter block behavior with hooks
drupal_version: "11.x"
---

# Block Hooks & Events

## When to Use

Reacting to block operations or altering block behavior across all blocks or specific plugins.

## Decision

| Hook | Use when... | Returns |
|------|-------------|---------|
| `hook_block_view_alter` | Modify render array for all blocks | void |
| `hook_block_access` | Control access to blocks | AccessResult |
| `hook_block_view_BASE_BLOCK_ID_alter` | Modify specific block plugin | void |
| `preprocess_block` | Add template variables | void |
| `hook_block_build_alter` | (Deprecated) Use `hook_block_view_alter` | — |

## Pattern

**hook_block_view_alter:**
```php
function mymodule_block_view_alter(&$build, BlockPluginInterface $block) {
  if ($block->getPluginId() === 'system_branding_block') {
    $build['#attached']['library'][] = 'mymodule/branding-enhancements';
    $build['#cache']['tags'][] = 'config:mymodule.branding';
  }
}
```

**hook_block_access:**
```php
function mymodule_block_access(Block $block, $operation, AccountInterface $account) {
  if ($operation === 'view' && $block->getPluginId() === 'my_block') {
    return AccessResult::forbiddenIf(!$account->hasPermission('view my block'))
      ->addCacheContexts(['user.permissions']);
  }
  return AccessResult::neutral();
}
```

**hook_block_view_BASE_BLOCK_ID_alter:**
```php
function mymodule_block_view_system_branding_block_alter(&$build, BlockPluginInterface $block) {
  // Only affects system_branding_block
  $build['#prefix'] = '<div class="custom-branding-wrapper">';
  $build['#suffix'] = '</div>';
}
```

**preprocess_block:**
```php
function mytheme_preprocess_block(&$variables) {
  $block = $variables['elements']['#block'];
  $plugin_id = $block->getPluginId();
  $variables['custom_class'] = 'block-' . str_replace('_', '-', $plugin_id);
  $variables['region'] = $block->getRegion();
}
```

**Reference:** https://api.drupal.org/api/drupal/core%21modules%21block%21block.api.php/group/block_api

## Common Mistakes

- **Wrong**: Using `hook_block_build_alter` → **Right**: Deprecated; use `hook_block_view_alter`
- **Wrong**: Returning wrong type from `hook_block_access` → **Right**: Must return `AccessResult`, not boolean or NULL
- **Wrong**: Replacing `$build` array in alter hooks → **Right**: Modify existing array; preserve cache metadata
- **Wrong**: Not adding cache contexts when access varies → **Right**: Leads to incorrect caching and wrong content shown
- **Wrong**: Using generic `hook_block_view_alter` when `hook_block_view_BASE_BLOCK_ID_alter` is more appropriate → **Right**: Specific hook is more efficient

## See Also

- [Block Access Control](block-access-control.md)
- [Block Rendering & Theming](block-rendering.md)
- Reference: https://api.drupal.org/api/drupal/core%21modules%21block%21block.api.php/group/block_api
