---
description: Migrate AJAX button or link that loads dynamic content into a container — replace AjaxResponse with render arrays
drupal_version: "11.x"
---

# Button-Triggered Content Load Migration

## When to Use

> Use this when migrating a button or link that loads dynamic content into a container on click — "Load More", "Refresh", or content panel patterns.

## Decision

| Step | Action |
|---|---|
| 1 | Convert controller to return render array — remove `AjaxResponse` |
| 2 | Replace `#ajax` button with `html_tag` button + `Htmx` configuration |
| 3 | Configure HTMX `target()` for where content should load |
| 4 | Add `_htmx_route: TRUE` to routing or use `onlyMainContent()` |
| 5 | Remove all `addCommand()` calls — messages are included automatically |

## Pattern

**BEFORE:**
```php
public function loadContent(Request $request) {
  $response = new AjaxResponse();
  $response->addCommand(new ReplaceCommand('#content-wrapper', $content));
  $response->addCommand(new MessageCommand('Content loaded!'));
  return $response;
}

$form['load_button'] = [
  '#type' => 'button',
  '#value' => t('Load Content'),
  '#ajax' => ['callback' => '::loadCallback', 'wrapper' => 'content-wrapper'],
];
```

**AFTER:**
```php
// Controller — just return render array
public function loadContent() {
  return [
    '#theme' => 'my_content',
    '#data' => $this->getData(),
  ];
}

// Form button with HTMX
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

**Routing:**
```yaml
# Option 1: always returns minimal HTML
my_module.load_content:
  path: '/my-module/load-content'
  defaults:
    _controller: '\Drupal\my_module\Controller\MyController::loadContent'
  options:
    _htmx_route: TRUE
```

## Common Mistakes

- **Still using `AjaxResponse`** → HTMX controllers return render arrays. Delete all `AjaxResponse` objects and `addCommand()` calls
- **Not using `onlyMainContent()` or `_htmx_route`** → HTMX will receive the full HTML page without one of these
- **Confusing `select()` and `target()`** → `select()` extracts from the response, `target()` specifies where on the current page to insert it
- **Using form `#type` button** → Form API buttons submit the form. Use `'#type' => 'html_tag', '#tag' => 'button'` for non-submitting buttons
- **Manually adding messages** → Status messages are automatically included via `HtmxRenderer`. Do not add them manually

## See Also

- Previous: [Cascading Selects with URL Migration](cascading-selects-with-url-migration.md)
- Next: [Multi-Step Wizard Migration](multi-step-wizard-migration.md)
- Source: `/core/modules/system/tests/modules/test_htmx/` test module
- Reference: `HtmxRenderer` at `/core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php`
