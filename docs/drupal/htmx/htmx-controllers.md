---
description: Build HTMX-enabled Drupal controllers — conditional responses, route options, and render array patterns
drupal_version: "11.x"
---

# HTMX Controllers

## When to Use

> Use this when building controller routes that return dynamic content for HTMX requests.

## Decision

| Situation | Approach | Why |
|-----------|----------|-----|
| Route always serves minimal response | `_htmx_route: TRUE` in routing.yml | HtmxRenderer invoked automatically |
| Route serves both HTMX and full pages | Conditional logic with `isHtmxRequest()` | Same route handles both cases |
| Need HTMX attributes on elements | `Htmx` class + `applyTo()` | Applies attributes to render array |

## Pattern

**Basic HTMX controller:**

```php
use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

class MyController extends ControllerBase {
  public function htmxContent() {
    $build['button'] = [
      '#type' => 'html_tag',
      '#tag' => 'button',
      '#value' => 'Load More',
    ];
    (new Htmx())
      ->get(Url::fromRoute('my.route'))
      ->target('#content-wrapper')
      ->swap('innerHTML')
      ->applyTo($build['button']);

    return $build;
  }
}
```

**Conditional response** (same route for HTMX and full page):

```php
use Drupal\Core\Htmx\HtmxRequestInfoTrait;

class MyController extends ControllerBase {
  use HtmxRequestInfoTrait;

  protected function getRequest() {
    return \Drupal::request();
  }

  public function content() {
    if ($this->isHtmxRequest()) {
      return ['#markup' => '<div>Just the content</div>'];
    }
    $build['#theme'] = 'my_template';
    $build['content'] = ['#markup' => '<div>Just the content</div>'];
    return $build;
  }
}
```

**Route-level option** (always minimal response):

```yaml
my_module.htmx_only:
  path: '/my-module/htmx-only'
  defaults:
    _controller: '\Drupal\my_module\Controller\MyController::htmxOnly'
  options:
    _htmx_route: TRUE
```

## Common Mistakes

- **Wrong**: Returning full render arrays without `_htmx_route` or `onlyMainContent()` → **Right**: Results in full page HTML in HTMX response
- **Wrong**: Forgetting `getRequest()` when using HtmxRequestInfoTrait → **Right**: Methods will fail without it
- **Wrong**: Not testing both HTMX and non-HTMX requests → **Right**: Initial page load is never HTMX
- **Wrong**: Using `_htmx_route` for routes that serve both HTMX and full pages → **Right**: Use conditional logic instead

## See Also

- [Dynamic Forms](dynamic-forms.md)
- [HTMX Attributes Reference](htmx-attributes.md)
- [Request Detection](request-detection.md)
- [Response Headers](response-headers.md)
- Reference: `/core/modules/system/tests/modules/test_htmx/src/Controller/HtmxTestAttachmentsController.php`
- Reference: `/core/lib/Drupal/Core/EventSubscriber/HtmxContentViewSubscriber.php`
