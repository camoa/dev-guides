---
description: Build custom AJAX endpoints outside Form API with nojs/ajax route parameters and graceful degradation
drupal_version: "11.x"
---

# Custom Route Implementation

## When to Use

> Use custom AJAX routes when you need AJAX endpoints outside Form API: autocomplete, search, content loading, or API-style endpoints. Always implement the `nojs` fallback for JavaScript-disabled environments.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Route definition | Needs graceful degradation | Use `{ajax}` parameter with 'nojs' default |
| Access control | Complex permissions | Use `_custom_access` callback instead of `_permission` |
| Response type | Multiple commands needed | Use AjaxResponse with multiple addCommand() calls |
| Response type | Single element update | Return render array directly from callback |

## Pattern

**Route definition:**

```yaml
# my_module.routing.yml
my_module.ajax_content:
  path: '/my-module/ajax/content/{type}/{ajax}'
  defaults:
    _controller: '\Drupal\my_module\Controller\AjaxController::getContent'
    ajax: 'nojs'
  requirements:
    _permission: 'access content'
    type: '[a-z]+'
    ajax: 'nojs|ajax'
```

**Controller:**

```php
class AjaxController extends ControllerBase {
  public function getContent($type, $ajax = 'nojs') {
    $content = $this->buildContent($type);

    if ($ajax === 'ajax') {
      $response = new AjaxResponse();
      $response->addCommand(new ReplaceCommand('#content-wrapper', $content));
      return $response;
    }

    // Non-AJAX fallback
    return ['#theme' => 'my_template', '#content' => $content];
  }
}
```

**Frontend link:**

```php
$build['link'] = [
  '#type' => 'link',
  '#title' => t('Load Content'),
  '#url' => Url::fromRoute('my_module.ajax_content', ['type' => 'example', 'ajax' => 'nojs']),
  '#attributes' => ['class' => ['use-ajax']],  // Drupal auto-handles AJAX
  '#attached' => ['library' => ['core/drupal.ajax']],
];
```

Reference: `core/modules/system/tests/modules/ajax_test/ajax_test.routing.yml`

## Common Mistakes

- **Wrong**: Not providing non-AJAX fallback → **Right**: Breaks for users without JavaScript; always handle `nojs` path
- **Wrong**: Wrong route parameter pattern → **Right**: `{ajax}` requirement must be `nojs|ajax` exactly
- **Wrong**: Forgetting to replace `/nojs/` with `/ajax/` in custom JavaScript → **Right**: AJAX never triggers; use `use-ajax` class to let Drupal handle it
- **Wrong**: Not using ControllerBase → **Right**: Missing helper methods like `t()`, `entityTypeManager()`, etc.
- **Wrong**: Missing access control → **Right**: Security vulnerability; always define `_permission` or `_custom_access`

## See Also

- [Custom AJAX Commands](custom-ajax-commands.md)
- [File Upload Patterns](file-upload-patterns.md)
- [Access Control Patterns](access-control-patterns.md)
