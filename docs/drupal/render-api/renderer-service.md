---
description: Using the Renderer service to programmatically convert render arrays to HTML -- methods, patterns, and render context management.
---

# The Renderer Service

## When to Use

When you need to programmatically convert render arrays to HTML strings -- tokens, emails, feeds, AJAX responses, testing, or anywhere outside the normal page rendering flow.

## Steps: Using the Renderer Service

**1. Get the renderer service**

```php
$renderer = \Drupal::service('renderer');
```

**2. Choose the right rendering method**

| Method | Use When | Context |
|---|---|---|
| `renderRoot(&$elements)` | Final rendering for HTTP response | Cannot be nested; throws exception if called within another renderRoot() |
| `renderInIsolation(&$elements)` | Need HTML string inside another rendering process | Creates isolated render context; can be called within renderRoot() |
| `render(&$elements, $is_root_call)` | Internal/recursive rendering | Usually called by Drupal core, not directly by modules |

**3. Render the array**

```php
// Example: Render for email
$build = [
  '#theme' => 'mymodule_email_template',
  '#user' => $user,
  '#content' => $message,
];

$html = $renderer->renderInIsolation($build);
// Returns MarkupInterface object; cast to string or use directly
$email_body = (string) $html;
```

**Reference:** `core/lib/Drupal/Core/Render/RendererInterface.php` (lines 10-62) -- method documentation

## Pattern: Rendering in a Service

```php
namespace Drupal\mymodule\Service;

use Drupal\Core\Render\RendererInterface;

class EmailBuilder {

  protected $renderer;

  public function __construct(RendererInterface $renderer) {
    $this->renderer = $renderer;
  }

  public function buildWelcomeEmail($user) {
    $build = [
      '#theme' => 'mymodule_welcome_email',
      '#user' => $user,
    ];

    return $this->renderer->renderInIsolation($build);
  }

}
```

**Services YAML:**

```yaml
services:
  mymodule.email_builder:
    class: Drupal\mymodule\Service\EmailBuilder
    arguments: ['@renderer']
```

## Pattern: Capturing Bubbleable Metadata

```php
use Drupal\Core\Render\RenderContext;

$context = new RenderContext();

$output = $renderer->executeInRenderContext($context, function() use ($build, $renderer) {
  return $renderer->render($build);
});

// Check if metadata was collected
if (!$context->isEmpty()) {
  $metadata = $context->pop();  // BubbleableMetadata object
  $cache_tags = $metadata->getCacheTags();
  $attachments = $metadata->getAttachments();
}
```

**Reference:** `core/lib/Drupal/Core/Render/RendererInterface.php` (lines 358-386) -- `executeInRenderContext()` documentation

## Decision: When to Render Programmatically

| Scenario | Approach | Rationale |
|---|---|---|
| Controller return value | Return render array directly | Drupal's main content renderer handles it automatically |
| Block build method | Return render array | Block system handles rendering |
| AJAX callback | Return `AjaxResponse` with render arrays | AJAX system renders them client-side |
| Email body | Use `renderInIsolation()` | Need HTML string, no assets/attachments |
| Token replacement | Use `renderInIsolation()` | Tokens must resolve to strings |
| RSS/Atom feed | Use `renderInIsolation()` | Feed XML doesn't support CSS/JS attachments |
| Testing | Use `renderRoot()` or `renderInIsolation()` | Need actual HTML to assert against |

## Common Mistakes

- **Calling `renderRoot()` inside another `renderRoot()`** -- Fatal exception; use `renderInIsolation()` instead
- **Using `render()` directly instead of `renderRoot()`** -- Metadata doesn't bubble to response; use `renderRoot()` for final rendering
- **Rendering too early in preprocess functions** -- Pass render arrays to Twig instead; let Twig render them
- **Not capturing bubbleable metadata when needed** -- Assets/cache tags lost; use `executeInRenderContext()` if you need them
- **Rendering user-submitted content without proper context** -- XSS risk; ensure render arrays have proper `#markup` filtering

## See Also

- [Render API Overview](render-api-overview.md) for when NOT to render programmatically
- [Twig Integration](twig-integration.md) for automatic rendering in templates
- Reference: `core/lib/Drupal/Core/Render/Renderer.php` -- full implementation
