---
description: "Choose between Drupal's legacy AJAX API and native HTMX for dynamic content loading"
tldr: "Use HTMX (Drupal 11.3+) for new declarative dynamic-content work; use the legacy AJAX API for Drupal 10.x or existing systems. Drupal.behaviors work automatically with both via context — no manual re-init needed."
drupal_version: "11.x"
---

# AJAX Integration

## When to Use

> Use to decide between Drupal's legacy AJAX API and native HTMX when loading content dynamically without a full page refresh. This guide is orientation only — detailed coverage lives in the dedicated guides linked below.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| New development on Drupal 11.3+ | HTMX | Declarative, HTML-first, officially supported by core |
| Drupal 10.x or an existing AJAX codebase | AJAX API | HTMX is unavailable before 11.3; legacy imperative system still required |
| Need fine-grained JavaScript command control | AJAX API | Callback/command objects give explicit imperative control |
| Simple element interactivity (swap, toggle) | HTMX | HTML attributes only, no JavaScript callback needed |

**Key architectural difference**: AJAX is imperative (JavaScript callbacks, command objects). HTMX is declarative (HTML attributes, server responses interpreted by the htmx client library).

## Pattern

**HTMX approach** (Drupal 11.3+, declarative):

```php
use Drupal\Core\Htmx\Htmx;

// Make a select element interactive
$htmx = new Htmx();
$htmx->post()
  ->select('*:has(>select[name="config_name"])')
  ->target('*:has(>select[name="config_name"])')
  ->swap('outerHTML');
$htmx->applyTo($form['config_type']);

// Result: HTML attributes, no JavaScript callback needed
// <select data-hx-post="/form-url" data-hx-select="..." data-hx-target="..." data-hx-swap="outerHTML">
```

**AJAX API approach** (legacy, imperative):

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\InvokeCommand;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();
  $response->addCommand(new InvokeCommand('.selector', 'addClass', ['active']));
  return $response;
}

$form['element'] = [
  '#ajax' => [
    'callback' => '::ajaxCallback',
    'event' => 'change',
    'wrapper' => 'result-wrapper',
  ],
];
```

**Behavior compatibility** (works automatically with both):

```javascript
Drupal.behaviors.dynamicContent = {
  attach(context, settings) {
    // Works on initial load AND after AJAX/HTMX updates
    // No special handling needed if using context
    once('dynamic', '.content', context).forEach(function (element) {
      element.addEventListener('click', handleClick);
    });
  }
};
```

## Common Mistakes

- **Wrong**: Not using context in behaviors → **Right**: Always query within context
  - **Why**: AJAX/HTMX-loaded content doesn't initialize, mysterious bugs
- **Wrong**: Manually re-initializing after updates → **Right**: Let Drupal behaviors handle it
  - **Why**: Drupal does this automatically via `Drupal.attachBehaviors()`/`Drupal.detachBehaviors()` on both systems
- **Wrong**: Missing detach() for destroyed content → **Right**: Clean up in detach()
  - **Why**: Event listeners remain, memory leaks accumulate
- **Wrong**: Choosing AJAX for new Drupal 11.3+ projects → **Right**: Start with HTMX
  - **Why**: HTMX is simpler, more maintainable, and officially supported for new development

## See Also

- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - AJAX/HTMX-compatible initialization
- [Once API](once-api.md) - Preventing duplicate processing
- [Drupal AJAX Framework](../ajax/index.md) - Comprehensive AJAX API reference (callbacks, commands, forms)
- [Drupal HTMX](../htmx/index.md) - HTMX implementation patterns (the modern approach)
- [AJAX to HTMX Migration](../ajax-htmx-migration/index.md) - Converting AJAX to HTMX pattern-by-pattern
- Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php` - HTMX utility class
- Reference: `/core/misc/htmx/htmx-behaviors.js` - Drupal.behaviors integration with HTMX
- Reference: `/core/misc/ajax.js` - Legacy AJAX implementation
- Reference: [Official AJAX API Documentation](https://www.drupal.org/docs/drupal-apis/ajax-api)
