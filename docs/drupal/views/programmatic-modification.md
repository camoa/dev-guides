---
description: When config-based approach isn't sufficient: runtime view modification, dynamic filter injection, custom display logic.
drupal_version: "11.x"
---

## 18. Programmatic View Modification

### When to Use
When config-based approach isn't sufficient: runtime view modification, dynamic filter injection, custom display logic.

**Philosophy**: Config-first is preferred. Only use programmatic modification when config can't solve the problem.

### Loading Views

#### Load View Config Entity
```php
$view = \Drupal\views\Entity\View::load('my_view');
// Returns ViewEntityInterface (config entity)
// Use for: reading config, checking existence, deleting
```

#### Load Executable View
```php
$view = \Drupal::service('views.executable')->get('my_view');
// Returns ViewExecutable
// Use for: executing, altering, rendering
```

Reference: `core/modules/views/src/Entity/View.php` lines 123-130

### Executing Views Programmatically

#### Basic Execution
```php
$view = \Drupal\views\Views::getView('my_view');
$view->setDisplay('page_1');
$view->execute();
$results = $view->result;
```

#### Rendering View
```php
$view = \Drupal\views\Views::getView('my_view');
$view->setDisplay('block_1');
$view->setArguments([123]);  // Contextual filter values
$render_array = $view->render();
```

#### With Filters
```php
$view = \Drupal\views\Views::getView('my_view');
$view->setDisplay('default');
$view->setExposedInput(['type' => 'article']);
$view->execute();
```

### Altering Views with Hooks

#### hook_views_pre_view()
Runs before view execution.

```php
/**
 * Implements hook_views_pre_view().
 */
function mymodule_views_pre_view(\Drupal\views\ViewExecutable $view, $display_id, array &$args) {
  if ($view->id() == 'my_view' && $display_id == 'page_1') {
    // Modify view before execution
    $view->setItemsPerPage(20);
  }
}
```

#### hook_views_pre_render()
Runs after query execution, before rendering.

```php
/**
 * Implements hook_views_pre_render().
 */
function mymodule_views_pre_render(\Drupal\views\ViewExecutable $view) {
  if ($view->id() == 'my_view') {
    // Modify results before rendering
    foreach ($view->result as $row) {
      // Manipulate row data
    }
  }
}
```

#### hook_views_post_render()
Runs after rendering.

```php
/**
 * Implements hook_views_post_render().
 */
function mymodule_views_post_render(\Drupal\views\ViewExecutable $view, &$output, \Drupal\views\Plugin\views\cache\CachePluginBase $cache) {
  if ($view->id() == 'my_view') {
    // Modify render array
    $output['#suffix'] = '<div class="custom-footer">Footer text</div>';
  }
}
```

### Creating Views Programmatically

#### Create View Entity
```php
$view = \Drupal\views\Entity\View::create([
  'id' => 'my_custom_view',
  'label' => 'My Custom View',
  'module' => 'mymodule',
  'base_table' => 'node_field_data',
  'base_field' => 'nid',
  'display' => [
    'default' => [
      'display_plugin' => 'default',
      'id' => 'default',
      'display_title' => 'Default',
      'position' => 0,
      'display_options' => [],
    ],
  ],
]);
$view->save();
```

Reference: `core/modules/views/src/Entity/View.php` lines 374-390

### Pattern: Dynamic Contextual Filter
```php
function mymodule_views_pre_view(\Drupal\views\ViewExecutable $view, $display_id, array &$args) {
  if ($view->id() == 'related_content') {
    // Inject current node ID as argument
    $node = \Drupal::routeMatch()->getParameter('node');
    if ($node) {
      $args[0] = $node->id();
    }
  }
}
```

### Common Mistakes
- Creating views programmatically instead of using config → Config is exportable, versionable; code is not
- Not checking view existence before loading → `Views::getView()` returns NULL if view doesn't exist; always check
- Modifying view in wrong hook → `hook_views_pre_view()` for query changes, `hook_views_pre_render()` for result changes, `hook_views_post_render()` for output changes
- Forgetting to set display → `setDisplay()` required before `execute()` or `render()`
- Not calling `execute()` before accessing results → `$view->result` is empty until `execute()` runs

### See Also
- Section 17: Views Config Export & Recipes — config-first approach
- Section 10: Sort & Contextual Filters — argument configuration
- Reference: [ViewExecutable API](https://api.drupal.org/api/drupal/core!modules!views!src!ViewExecutable.php/11.x)
