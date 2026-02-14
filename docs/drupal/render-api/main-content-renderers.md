---
description: How Drupal renders different response types -- HTML pages, AJAX, modal dialogs -- and choosing the right response format.
---

# Main Content Renderers

## When to Use

Understanding how Drupal renders different response types -- HTML pages, AJAX, modal dialogs, iframes. Rarely need to interact with these directly, but helpful for advanced use cases.

## Main Content Renderer Types

Drupal uses different renderers based on the request wrapper format.

| Format | Renderer | Use Case | How Requested |
|---|---|---|---|
| `html` | `HtmlRenderer` | Standard page responses | Default, normal page loads |
| `ajax` | `AjaxRenderer` | AJAX commands | `?_wrapper_format=drupal_ajax` |
| `dialog` | `DialogRenderer` | Modal/dialog content | `?_wrapper_format=drupal_dialog` |
| `modal` | `ModalRenderer` | Modal dialogs | `?_wrapper_format=drupal_modal` |

**Reference:** `core/lib/Drupal/Core/Render/MainContent/` -- renderer implementations

## Decision: Choosing Response Type

| If you're building... | Return from controller... | Renderer handles... |
|---|---|---|
| Normal page | Render array | Wrapping in page template, adding regions, blocks |
| AJAX callback | `AjaxResponse` with commands | Sending AJAX commands as JSON |
| Modal dialog link | Render array (link uses ajax wrapper) | Opening content in modal |
| REST/JSON API | `JsonResponse` or `ResourceResponse` | Serializing data |
| Feed (RSS/Atom) | Render array, set `Content-Type` header | Rendering as XML |

## Pattern: Controller Returning Render Array

```php
namespace Drupal\mymodule\Controller;

use Drupal\Core\Controller\ControllerBase;

class MyPageController extends ControllerBase {

  public function content() {
    // Just return a render array
    return [
      '#theme' => 'mymodule_page',
      '#data' => $this->getData(),
      '#cache' => [
        'contexts' => ['user'],
        'max-age' => 3600,
      ],
    ];
  }

  // HtmlRenderer wraps this in page.html.twig with regions/blocks
}
```

## Pattern: AJAX Response

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\ReplaceCommand;
use Drupal\Core\Ajax\InvokeCommand;

public function ajaxUpdate() {
  $build = [
    '#theme' => 'mymodule_widget',
    '#data' => $this->getData(),
  ];

  $response = new AjaxResponse();

  // Replace content
  $response->addCommand(new ReplaceCommand('#widget', $build));

  // Call JavaScript function
  $response->addCommand(new InvokeCommand('.widget', 'updateAnimation'));

  return $response;
}
```

**Available AJAX commands:**

- `ReplaceCommand` -- Replace HTML
- `AppendCommand` / `PrependCommand` -- Add HTML
- `RemoveCommand` -- Remove elements
- `InvokeCommand` -- Call JS method
- `RedirectCommand` -- Redirect browser
- `OpenModalDialogCommand` -- Open modal

**Reference:** `core/lib/Drupal/Core/Ajax/` -- AJAX command plugins

## Pattern: Modal Dialog

**Link that opens modal:**

```php
$build['modal_link'] = [
  '#type' => 'link',
  '#title' => t('Open Modal'),
  '#url' => Url::fromRoute('mymodule.modal_content'),
  '#attributes' => [
    'class' => ['use-ajax'],
    'data-dialog-type' => 'modal',
    'data-dialog-options' => Json::encode(['width' => 700]),
  ],
  '#attached' => ['library' => ['core/drupal.dialog.ajax']],
];
```

**Controller for modal content:**

```php
public function modalContent() {
  return [
    '#theme' => 'mymodule_modal',
    '#title' => t('Modal Title'),
    '#content' => $this->getModalContent(),
  ];
}
```

**Drupal automatically:**

1. Detects `data-dialog-type="modal"` on link
2. Loads content via AJAX with `_wrapper_format=drupal_modal`
3. Renders in modal dialog

## Pattern: Setting Main Content Render Array Properties

```php
public function build() {
  $build = [
    '#type' => 'container',
    'content' => ['#markup' => 'Page content'],
  ];

  // Add title (used by page template)
  $build['#title'] = t('My Custom Page');

  // Disable default cache contexts (advanced)
  $build['#cache']['contexts'] = [];

  // Prevent page from being cached at all
  $build['#cache']['max-age'] = 0;

  return $build;
}
```

## Common Mistakes

- **Returning HTML string from controller instead of render array** -- Bypasses theme system, caching, and security
- **Not attaching `core/drupal.dialog.ajax` library for modal links** -- Modals don't work
- **Assuming `#title` always works** -- Only works for main content render arrays, not arbitrary nested ones
- **Manually implementing AJAX that Drupal provides** -- Use built-in AJAX framework instead

## See Also

- [Render Array Patterns](render-array-patterns.md) for AJAX response patterns
- Reference: `core/lib/Drupal/Core/Render/MainContent/HtmlRenderer.php`
