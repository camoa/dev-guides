---
description: Load JavaScript conditionally based on content type, route, user role, or other conditions
drupal_version: "10.x/11.x"
---

# Conditional Loading

## When to Use

> Use when optimizing performance by loading JavaScript only when needed based on content type, route, user role, or other conditions.

## Decision

Evaluate conditions in PHP (preprocess, hooks, controllers) before attaching libraries. Use Drupal's caching system with cache contexts to ensure conditional libraries work with page caching.

## Pattern

**Content type condition**:

```php
function theme_preprocess_node(&$variables) {
  if ($variables['node']->bundle() === 'article') {
    $variables['#attached']['library'][] = 'theme/article-enhancements';
  }
}
```

**Route-based condition**:

```php
function theme_preprocess_page(&$variables) {
  $route_name = \Drupal::routeMatch()->getRouteName();
  if (strpos($route_name, 'admin') === 0) {
    $variables['#attached']['library'][] = 'module/admin';
  }
}
```

**User permission condition** (with cache context):

```php
$build['#cache']['contexts'][] = 'user.permissions';
if (\Drupal::currentUser()->hasPermission('access administration pages')) {
  $build['#attached']['library'][] = 'module/admin-tools';
}
```

**Field-based condition**:

```php
if (!$variables['content']['field_enable_feature']['#items']->isEmpty()) {
  $variables['#attached']['library'][] = 'module/conditional-feature';
}
```

## Common Mistakes

- **Wrong**: Checking conditions in JavaScript instead of PHP → **Right**: Evaluate in PHP before attachment
  - **Why**: JS already loaded and parsed, defeats optimization purpose
- **Wrong**: Not declaring cache contexts → **Right**: Add appropriate `#cache['contexts']`
  - **Why**: Wrong library served from cache, broken functionality
- **Wrong**: Overly specific conditions → **Right**: Balance specificity with cache efficiency
  - **Why**: Cache fragmentation, performance degradation
- **Wrong**: Conditional loading without testing cached pages → **Right**: Test with caching enabled
  - **Why**: Works uncached, fails with caching enabled

## See Also

- [Performance Optimization](performance-optimization.md) - When conditional loading matters
- Reference: [Drupal Cache API](https://www.drupal.org/docs/drupal-apis/cache-api) - Cache context patterns
