---
description: Customize block appearance through templates, preprocessing, and altering
drupal_version: "11.x"
---

# Block Rendering & Theming

## When to Use

Customizing block appearance through templates, preprocessing, or altering render output.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Step 2 (templates) | Styling specific plugin | Use `block--{plugin-id}.html.twig` |
| Step 2 (templates) | Styling region's blocks | Use `block--{region}.html.twig` |
| Step 3 (preprocess) | Adding data for template | Preprocess; keep logic out of templates |
| Step 5 (alter) | Changing all blocks | Use `hook_block_view_alter()` |
| Step 5 (alter) | Changing specific plugin | Check plugin ID in alter hook |

## Pattern

**Block render pipeline:**
1. `BlockViewBuilder::viewMultiple()` called by region
2. `BlockAccessControlHandler` checks access
3. `BlockPluginInterface::build()` generates render array
4. `BlockViewBuilder::preRender()` adds wrapper
5. Theme system renders templates

**Template (block--system-branding-block.html.twig):**
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

**Template variables:**
- `{{ content }}` — Block content from `build()`
- `{{ plugin_id }}` — Block plugin ID
- `{{ label }}` — Block label
- `{{ configuration }}` — Block configuration
- `{{ attributes }}` — HTML attributes

**Reference:** `core/modules/block/templates/block.html.twig`, `core/modules/block/src/BlockViewBuilder.php`

## Common Mistakes

- **Wrong**: Putting business logic in templates → **Right**: Use preprocess or alter hooks; templates are for presentation only
- **Wrong**: Not using `attributes` variable in custom templates → **Right**: Loses important classes, IDs, ARIA attributes
- **Wrong**: Overriding `block.html.twig` when specific suggestion is better → **Right**: Use `block--{plugin-id}.html.twig` for targeted changes
- **Wrong**: Forgetting to clear cache after template changes → **Right**: Twig templates cached; must clear cache
- **Wrong**: Altering `$build` without preserving cache metadata → **Right**: Merge cache tags/contexts, don't replace

## See Also

- [Block Caching Strategies](block-caching.md)
- [Block Hooks & Events](block-events-hooks.md)
- Reference: https://www.drupal.org/docs/theming-drupal/twig-in-drupal
