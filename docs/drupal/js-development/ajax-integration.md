---
description: "Choose between Drupal's legacy AJAX API and native HTMX for dynamic content loading"
tldr: "Understand the landscape of dynamic content loading in Drupal: HTMX (Drupal 11.3+) is the modern declarative path, the legacy AJAX API is imperative and required for Drupal 10.x or existing systems. Gotcha: both work automatically with Drupal.behaviors via context — no manual re-init needed."
drupal_version: "11.x"
---

# AJAX Integration

## When to Use

> Understanding the landscape of dynamic content loading in Drupal - choosing between legacy AJAX API and modern HTMX approach.

## Decision

**Critical context shift in Drupal 11.x**: the htmx library was vendored into Drupal core in 11.2, and the developer-facing `Drupal\Core\Htmx\Htmx` API plus the Ajax subsystem integration landed in 11.3.0. HTMX is a modern, declarative alternative to the traditional AJAX API. This section provides orientation - detailed coverage lives in dedicated guides.

**Choose your path**:
- **HTMX** (Drupal 11.3+) - Modern, declarative, HTML-first. Start here for new development.
- **AJAX API** (legacy) - Imperative, callback-based. Required for Drupal 10.x and existing systems, where HTMX is unavailable before 11.3.

**Key architectural difference**:
- **AJAX** = Imperative (JavaScript callbacks, command objects)
- **HTMX** = Declarative (HTML attributes, server responses interpreted by the htmx client library)

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

// Result: HTML attributes, no JavaScript callbacks needed
// <select data-hx-post="/form-url" data-hx-select="..." data-hx-target="..." data-hx-swap="outerHTML">
```

**AJAX API approach** (legacy, imperative):
```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\InvokeCommand;

// Callback function
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();
  $response->addCommand(new InvokeCommand('.selector', 'addClass', ['active']));
  return $response;
}

// Form element
$form['element'] = [
  '#ajax' => [
    'callback' => '::ajaxCallback',
    'event' => 'change',
    'wrapper' => 'result-wrapper',
  ],
];
```

**JavaScript integration with HTMX** (automatic via core):
```javascript
// From core/misc/htmx/htmx-behaviors.js
// Drupal.behaviors automatically run on HTMX-loaded content
htmx.on('htmx:drupal:load', ({ detail }) => {
  Drupal.attachBehaviors(detail.elt, drupalSettings);
});

htmx.on('htmx:drupal:unload', ({ detail }) => {
  Drupal.detachBehaviors(detail.elt, drupalSettings, 'unload');
});
```

**Behavior AJAX/HTMX compatibility** (works with both):
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

- **Not using context in behaviors** - WHY: AJAX/HTMX-loaded content doesn't initialize, mysterious bugs
- **Manually re-initializing after updates** - WHY: Drupal does this automatically via `Drupal.attachBehaviors()`/`Drupal.detachBehaviors()` on both systems
- **Missing detach() for destroyed content** - WHY: Event listeners remain, memory leaks accumulate
- **Choosing AJAX for new Drupal 11.3+ projects** - WHY: HTMX is simpler, more maintainable, and officially supported for new development

## See Also

**Within this guide**:
- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - AJAX/HTMX-compatible initialization
- [Once API](once-api.md) - Preventing duplicate processing

**Dedicated guides for deep coverage**:
- [Drupal AJAX Framework](../ajax/index.md) - Comprehensive AJAX API reference (callbacks, commands, forms)
- [Drupal HTMX](../htmx/index.md) - HTMX implementation patterns (the modern approach)
- [AJAX to HTMX Migration](../ajax-htmx-migration/index.md) - Converting AJAX to HTMX pattern-by-pattern

**Core references**:
- Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php` - HTMX utility class
- Reference: `/core/misc/htmx/htmx-behaviors.js` - Drupal.behaviors integration
- Reference: `/core/misc/ajax.js` - Legacy AJAX implementation
- Reference: [Official AJAX API Documentation](https://www.drupal.org/docs/drupal-apis/ajax-api)
- Reference: ["Ajax subsystem now includes HTMX" change record](https://www.drupal.org/node/3539472) (Drupal 11.3.0)
