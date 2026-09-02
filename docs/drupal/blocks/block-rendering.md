---
description: Customize block appearance through templates, preprocessing, and alter hooks
tldr: "Use block templates for markup changes, preprocessing for adding template variables, and alter hooks to modify render arrays across blocks. Keep logic out of templates."
drupal_version: "11.x"
---

# Block Rendering & Theming

## When to Use

> Customizing block appearance through templates, preprocessing, or altering render output.

## Steps

1. **Block render pipeline**
   - `BlockViewBuilder::viewMultiple()` called by region
   - `BlockAccessControlHandler` checks access
   - `BlockPluginInterface::build()` generates render array
   - `BlockViewBuilder::preRender()` adds wrapper
   - Theme system renders templates

2. **Using block templates**
   - Default: `block.html.twig`
   - Suggestions: `block--{plugin-id}.html.twig`, `block--{region}.html.twig`
   - Place in `{theme}/templates/block/`

3. **Preprocessing blocks**
   ```php
   function mytheme_preprocess_block(&$variables) {
     $block = $variables['elements']['#block'];
     $plugin_id = $block->getPluginId();
     $variables['custom_var'] = 'value';
   }
   ```

4. **Template variables available**
   - `{{ content }}` — Block content from `build()`
   - `{{ plugin_id }}` — Block plugin ID
   - `{{ label }}` — Block label
   - `{{ configuration }}` — Block configuration
   - `{{ attributes }}` — HTML attributes

5. **Altering block output**
   ```php
   function mymodule_block_view_alter(&$build, BlockPluginInterface $block) {
     if ($block->getPluginId() === 'system_branding_block') {
       $build['#attached']['library'][] = 'mymodule/branding-styles';
     }
   }
   ```

## Decision Points

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 2 (templates) | Styling specific plugin | Use `block--{plugin-id}.html.twig` |
| Step 2 (templates) | Styling region's blocks | Use `block--{region}.html.twig` |
| Step 3 (preprocess) | Adding data for template | Preprocess; keep logic out of templates |
| Step 5 (alter) | Changing all blocks | Use `hook_block_view_alter()` |
| Step 5 (alter) | Changing specific plugin | Check plugin ID in alter hook |

## Pattern

**Template suggestion (block--system-branding-block.html.twig):**
```twig
<div{{ attributes.addClass('site-branding') }}>
  {% if content.site_logo %}
    <a href="{{ path('<front>') }}">
      {{ content.site_logo }}
    </a>
  {% endif %}
  {% if content.site_name %}
    <h1>{{ content.site_name }}</h1>
  {% endif %}
</div>
```

**Preprocessing:**
```php
function mytheme_preprocess_block(&$variables) {
  $block = $variables['elements']['#block'];

  // Add custom class based on plugin
  $plugin_id = $block->getPluginId();
  $variables['attributes']['class'][] = 'block-plugin-' . str_replace('_', '-', $plugin_id);

  // Add region as variable
  $variables['region'] = $block->getRegion();
}
```

**Altering block build:**
```php
function mymodule_block_view_alter(&$build, BlockPluginInterface $block) {
  // Add cache tag to all blocks
  $build['#cache']['tags'][] = 'mymodule:blocks';

  // Modify specific block
  if ($block->getPluginId() === 'my_custom_block') {
    $build['#prefix'] = '<div class="custom-wrapper">';
    $build['#suffix'] = '</div>';
  }
}
```

**Reference:** `core/modules/block/templates/block.html.twig`, `core/modules/block/src/BlockViewBuilder.php`

## Common Mistakes

- Putting business logic in templates → Use preprocess or alter hooks; templates are for presentation only
- Not using `attributes` variable in custom templates → Loses important classes, IDs, ARIA attributes
- Overriding `block.html.twig` when specific suggestion is better → Use `block--{plugin-id}.html.twig` for targeted changes
- Forgetting to clear cache after template changes → Twig templates cached; must clear cache
- Altering `$build` without preserving cache metadata → Merge cache tags/contexts, don't replace

## See Also

- [Block Caching Strategies](block-caching.md)
- [Block Hooks & Events](block-events-hooks.md)
- Reference: https://www.drupal.org/docs/theming-drupal/twig-in-drupal
