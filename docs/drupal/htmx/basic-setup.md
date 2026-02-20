---
description: Enable HTMX in a custom Drupal module — route definition, controller, and library attachment
drupal_version: "11.x"
---

# Basic Setup

## When to Use

> Use this when creating a custom module and adding HTMX functionality for the first time.

## Decision

| At this step | If | Then |
|---|---|---|
| Route definition | All requests should use HtmxRenderer | Add `_htmx_route: TRUE` option |
| Route definition | Only some requests need minimal response | Omit `_htmx_route` and use `onlyMainContent()` on elements |
| Library attachment | Using `Htmx` class with `applyTo()` | Library attaches automatically |
| Library attachment | Building manual HTMX attributes | Add `core/drupal.htmx` to `#attached['library']` |

## Pattern

**Step 1: Route** (`my_module.routing.yml`):

```yaml
my_module.htmx_content:
  path: '/my-module/htmx-content'
  defaults:
    _controller: '\Drupal\my_module\Controller\MyController::htmxContent'
    _title: 'HTMX Content'
  requirements:
    _permission: 'access content'
  options:
    _htmx_route: TRUE
```

**Step 2: Controller** (`src/Controller/MyController.php`):

```php
use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

class MyController extends ControllerBase {
  public function htmxContent() {
    $build['content'] = ['#markup' => '<div>Dynamic content</div>'];

    (new Htmx())
      ->get(Url::fromRoute('my_module.htmx_content'))
      ->target('#content-wrapper')
      ->swap('innerHTML')
      ->applyTo($build['trigger']);

    return $build;
  }
}
```

Library attaches automatically via `applyTo()`. Manual attachment only needed if not using the `Htmx` class:

```php
$build['#attached']['library'][] = 'core/drupal.htmx';
```

## Common Mistakes

- **Wrong**: Forgetting `_htmx_route` when all route responses should be minimal → **Right**: Without it, routes return full page renders
- **Wrong**: Manually attaching library when using `applyTo()` → **Right**: Redundant; already automatic
- **Wrong**: Not clearing cache after routing changes → **Right**: Routes won't update until cache rebuild

## See Also

- [Request/Response Lifecycle](request-response-lifecycle.md)
- [Library Dependencies](library-dependencies.md)
- [Request Detection](request-detection.md)
- Reference: `/core/modules/system/tests/modules/test_htmx/test_htmx.routing.yml`
- Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php`
