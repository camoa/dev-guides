---
description: "Build HTMX-enabled Drupal controllers — conditional responses, route options, and render array patterns"
tldr: "Use this when building controller routes that return dynamic content for HTMX requests. Return standard render arrays and either set `_htmx_route: TRUE` or check `isHtmxRequest()` to serve minimal responses."
drupal_version: "11.x"
---

# HTMX Controllers

## When to Use

> You're building controller routes that return dynamic content for HTMX requests.

## Pattern: Basic HTMX Controller

```php
use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

class MyController extends ControllerBase {
  public function htmxContent() {
    // Build content render array
    $build['content'] = [
      '#type' => 'markup',
      '#markup' => '<div>Dynamic content</div>',
    ];

    // Configure HTMX for a button
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

Reference: `/core/modules/system/tests/modules/test_htmx/src/Controller/HtmxTestAttachmentsController.php` lines 94-132

## Pattern: Conditional Responses

Return different content based on HTMX request:

```php
use Drupal\Core\Htmx\HtmxRequestInfoTrait;

class MyController extends ControllerBase {
  use HtmxRequestInfoTrait;

  protected function getRequest() {
    return \Drupal::request();
  }

  public function content() {
    if ($this->isHtmxRequest()) {
      // Minimal response for HTMX
      return ['#markup' => '<div>Just the content</div>'];
    }

    // Full page for initial request
    $build['#theme'] = 'my_template';
    $build['content'] = ['#markup' => '<div>Just the content</div>'];
    return $build;
  }
}
```

## Pattern: Using Route Option

Define route with `_htmx_route: TRUE` to automatically invoke HtmxRenderer:

```yaml
my_module.htmx_only:
  path: '/my-module/htmx-only'
  defaults:
    _controller: '\Drupal\my_module\Controller\MyController::htmxOnly'
  options:
    _htmx_route: TRUE
```

Controller returns standard render array — HtmxRenderer handles minimal response automatically.

Reference: `/core/lib/Drupal/Core/EventSubscriber/HtmxContentViewSubscriber.php` — Handles `_htmx_route` routes

## Common Mistakes

- Returning full render arrays without `_htmx_route` or `onlyMainContent()` — Results in full page HTML
- Forgetting to implement `getRequest()` when using HtmxRequestInfoTrait — Methods will fail
- Not testing both HTMX and non-HTMX requests — Initial page load isn't HTMX
- Using `_htmx_route` for routes that serve both HTMX and full pages — Use conditional logic instead

## See Also

- Previous: [Dynamic Forms](dynamic-forms.md)
- Next: [HTMX Attributes Reference](htmx-attributes.md)
- Reference: [Request Detection](request-detection.md)
- Reference: [Response Headers](response-headers.md)
