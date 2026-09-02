---
description: "Enable HTMX in a custom Drupal module — route definition, controller, and library attachment"
tldr: "Use this when creating a custom module and adding HTMX functionality: define a route with `_htmx_route: TRUE`, build a controller that applies `Htmx` attributes, and rely on `applyTo()` for automatic library attachment."
drupal_version: "11.x"
---

# Basic Setup

## When to Use

> You're creating a custom module and want to add HTMX functionality.

## Steps

1. **Define Route with HTMX Option** — File: `my_module.routing.yml`
   ```yaml
   my_module.htmx_content:
     path: '/my-module/htmx-content'
     defaults:
       _title: 'HTMX Content'
       _controller: '\Drupal\my_module\Controller\MyController::htmxContent'
     requirements:
       _permission: 'access content'
     options:
       _htmx_route: TRUE
   ```

   The `_htmx_route: TRUE` option automatically invokes HtmxRenderer for this route.

   Reference: `/core/modules/system/tests/modules/test_htmx/test_htmx.routing.yml` lines 41-49

2. **Create Controller** — File: `src/Controller/MyController.php`
   ```php
   use Drupal\Core\Controller\ControllerBase;
   use Drupal\Core\Htmx\Htmx;
   use Drupal\Core\Url;

   class MyController extends ControllerBase {
     public function htmxContent() {
       $build['content'] = ['#markup' => '<div>Dynamic content</div>'];

       // Configure HTMX attributes
       (new Htmx())
         ->get(Url::fromRoute('my_module.htmx_content'))
         ->target('#content-wrapper')
         ->swap('innerHTML')
         ->applyTo($build['trigger']);

       return $build;
     }
   }
   ```

   Reference: `/core/modules/system/tests/modules/test_htmx/src/Controller/HtmxTestAttachmentsController.php`

3. **Attach Library (Optional)** — Library attaches automatically when using `Htmx::applyTo()`:
   ```php
   // Automatic via applyTo() - preferred
   (new Htmx())->get('/path')->applyTo($build);

   // Manual if needed
   $build['#attached']['library'][] = 'core/drupal.htmx';
   ```

   Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php` lines 1291-1295

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Route definition | All requests to this route should use HtmxRenderer | Add `_htmx_route: TRUE` option |
| Route definition | Only some requests need minimal response | Omit `_htmx_route` and use `onlyMainContent()` on elements |
| Library attachment | Using `Htmx` class | Library attaches automatically via `applyTo()` |
| Library attachment | Building manual HTMX attributes | Add `core/drupal.htmx` to `#attached['library']` |

## Common Mistakes

- Using `/modules/custom/` in examples — Use your actual module name and namespace
- Forgetting `_htmx_route` when all route responses should be minimal — Results in full page renders
- Manually attaching library when using `applyTo()` — Redundant, already automatic
- Not clearing cache after routing changes — Routes won't update until cache rebuild

## See Also

- Previous: [Request/Response Lifecycle](request-response-lifecycle.md)
- Next: [Request Detection](request-detection.md)
- Reference: [Library Dependencies](library-dependencies.md)
