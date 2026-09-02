---
description: "Button-Triggered Content Load Migration — migrate a button or link that loads dynamic content into a container on click"
tldr: "Migrate a Load More/Refresh button that loads content into a container. Controllers return render arrays, not AjaxResponse — and select() extracts from the response while target() says where on the page it lands."
drupal_version: "11.x"
---

# Button-Triggered Content Load Migration

## When to Use

> Migrate a button or link that loads dynamic content into a container when clicked. Common for "Load More", "Refresh", or modal content patterns.

## Steps

1. **Convert controller to return render array** — Remove `AjaxResponse`, return build array
2. **Replace `#ajax` button with HTMX button** — Use `html_tag` button with HTMX attributes
3. **Configure HTMX target** — Specify where content should be loaded
4. **Add route option for minimal response** — Use `_htmx_route: TRUE` or `onlyMainContent()`
5. **Remove AJAX command logic** — Messages and settings included automatically

## BEFORE: AJAX

```php
// Controller returning AJAX response
public function loadContent(Request $request) {
  $response = new AjaxResponse();

  $content = [
    '#theme' => 'my_content',
    '#data' => $this->getData(),
  ];

  $response->addCommand(new ReplaceCommand('#content-wrapper', $content));
  $response->addCommand(new MessageCommand('Content loaded!'));

  return $response;
}

// Form with AJAX button
$form['load_button'] = [
  '#type' => 'button',
  '#value' => t('Load Content'),
  '#ajax' => [
    'callback' => '::loadCallback',
    'wrapper' => 'content-wrapper',
  ],
];

$form['content'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'content-wrapper'],
];

public function loadCallback(array &$form, FormStateInterface $form_state) {
  return $form['content'];
}
```

## AFTER: HTMX

```php
// Controller returns render array (not AjaxResponse)
public function loadContent() {
  // Just return the content - HtmxRenderer handles the rest
  return [
    '#theme' => 'my_content',
    '#data' => $this->getData(),
    '#attached' => [
      'library' => ['my_module/my_library'],
    ],
  ];
}

// Form with HTMX button
$form['load_button'] = [
  '#type' => 'html_tag',
  '#tag' => 'button',
  '#value' => t('Load Content'),
  '#attributes' => ['type' => 'button'],
];

(new Htmx())
  ->get(Url::fromRoute('my_module.load_content'))
  ->onlyMainContent()
  ->select('.content-class')
  ->target('#content-wrapper')
  ->swap('innerHTML')
  ->applyTo($form['load_button']);

$form['content'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'content-wrapper'],
];
```

**Routing options:**
```yaml
# Option 1: Use _htmx_route option (always returns minimal HTML)
my_module.load_content:
  path: '/my-module/load-content'
  defaults:
    _controller: '\Drupal\my_module\Controller\MyController::loadContent'
  options:
    _htmx_route: TRUE

# Option 2: Standard route (onlyMainContent() adds ?_wrapper_format query param)
my_module.load_content:
  path: '/my-module/load-content'
  defaults:
    _controller: '\Drupal\my_module\Controller\MyController::loadContent'
```

Reference: `/core/modules/system/tests/modules/test_htmx/` test module

## Common Mistakes

- **Still using `AjaxResponse`** → HTMX controllers return render arrays. Delete all `AjaxResponse` objects and `addCommand()` calls
- **Not using `onlyMainContent()` or `_htmx_route`** → HTMX will receive the full HTML page unless you specify minimal response. Use one of these
- **Confusing `select()` and `target()`** → `select()` extracts content from response (like jQuery selector on response HTML), `target()` says where to put it (selector on current page)
- **Using form `#type` button instead of `html_tag`** → Form API buttons submit the form. Use `'#type' => 'html_tag', '#tag' => 'button'` for non-submitting buttons
- **Manually adding messages** → Status messages are automatically included in HTMX responses via `HtmxRenderer`. Don't add them manually

## See Also

- Previous: [Cascading Selects with URL Migration](cascading-selects-with-url-migration.md)
- Next: [Multi-Step Wizard Migration](multi-step-wizard-migration.md)
- Reference: `HtmxRenderer` at `/core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php`
