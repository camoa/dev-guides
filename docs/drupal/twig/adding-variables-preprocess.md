---
topic: drupal/twig
guide: adding-variables-preprocess
---

## Adding Variables in Preprocess

### When to Use
When you need to pass data from PHP to a Twig template that is not available through the default variable set.

### Decision
| What to pass | How | Notes |
|---|---|---|
| Simple string/bool/int | Direct assignment: `$variables['my_var'] = 'value'` | Available as `{{ my_var }}` |
| Translated string | `$variables['label'] = t('My Label')` | Use `t()`, not string literal |
| Render array | `$variables['block'] = ['#theme' => '...']` | Prints via `{{ block }}` |
| Entity view | Use ViewBuilder: see pattern below | Preferred over raw render arrays |
| URL string | `Url::fromRoute(...)->toString()` | Already a string |
| URL object | `Url::fromRoute(...)` | Available as `{{ url(route) }}` context |
| Config value | `\Drupal::config('system.site')->get('name')` | Cache metadata needed |
| Attribute object | `new Attribute(['class' => ['my-class']])` | Prints via `{{ attrs }}` |

### Pattern

**Passing rendered entity:**
```php
function mytheme_preprocess_node(&$variables) {
  $node = $variables['node'];

  // Load and render a related entity
  if ($node->hasField('field_author_profile') && !$node->field_author_profile->isEmpty()) {
    $profile = $node->field_author_profile->entity;
    if ($profile && $profile->access('view')) {
      $view_builder = \Drupal::entityTypeManager()->getViewBuilder('node');
      $variables['author_card'] = $view_builder->view($profile, 'card');
    }
  }

  // Pass a simple computed value
  $variables['word_count'] = str_word_count(strip_tags($node->body->value ?? ''));

  // Pass an Attribute object for a custom element
  $variables['card_attributes'] = new Attribute([
    'class' => ['card', 'card--' . $node->bundle()],
    'data-nid' => $node->id(),
  ]);
}
```

**Cache metadata for custom variables (critical):**
```php
// If you add data from an entity or config, bubble its cache metadata
use Drupal\Core\Cache\CacheableMetadata;

function mytheme_preprocess_node(&$variables) {
  $config = \Drupal::config('mymodule.settings');
  $variables['show_badge'] = $config->get('show_badge');

  // Bubble config cache metadata so page cache invalidates correctly
  CacheableMetadata::createFromRenderArray($variables)
    ->addCacheableDependency($config)
    ->applyTo($variables);
}
```

### Common Mistakes
- Adding data from external sources (config, entities) without bubbling cache metadata → stale cache issues
- Passing a raw entity object as a variable and then trying to render it directly → pass a render array, not the entity
- Using `\Drupal::service()` in preprocess for services that should be injected → fine in `.theme` files, avoid in modules
- Passing large arrays or fully loaded entity lists → load lazily or only what's needed for the current view mode
- Forgetting that default variables (`attributes`, `title_attributes`, etc.) are set by `ThemeManager::getDefaultTemplateVariables()` and can be modified in preprocess

### See Also
- Preprocess layers → [Preprocess Functions](preprocess-functions.md)
- Render arrays reference → `drupal-render-api.md`
- Cache metadata → `drupal-render-api.md`
