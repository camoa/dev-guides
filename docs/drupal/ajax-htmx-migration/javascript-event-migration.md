---
description: "JavaScript Event Migration — migrate custom JS that hooks into AJAX events to the equivalent HTMX events"
tldr: "Migrate custom JS that hooks preprocessing, validation, or post-processing into AJAX events. HTMX has no Drupal.ajax object — replace jQuery hook overrides with htmx.on('htmx:beforeRequest'/'htmx:afterSwap', ...)."
drupal_version: "11.x"
---

# JavaScript Event Migration

## When to Use

> Migrate custom JavaScript that hooks into AJAX events for preprocessing, validation, or post-processing. HTMX uses different events but follows similar patterns.

## Decision

| AJAX Event Hook | HTMX Event | Timing |
|---|---|---|
| `beforeSerialize` | `htmx:configRequest` | Before request sent, modify request data |
| `beforeSubmit` | `htmx:beforeRequest` | Before request, can cancel |
| `beforeSend` | `htmx:beforeRequest` | Before request, can cancel |
| `success` | `htmx:afterSwap` | After DOM updated |
| `error` | `htmx:responseError` | Request failed |
| After behaviors attach | `htmx:drupal:load` | After Drupal.attachBehaviors() |
| Before element removal | `htmx:drupal:unload` | Before Drupal.detachBehaviors() |

## Pattern

**BEFORE: AJAX JavaScript**
```javascript
(function ($, Drupal) {
  Drupal.behaviors.myAjax = {
    attach: function (context, settings) {
      var $element = $('#my-ajax-element', context);

      if ($element.length && Drupal.ajax[$element.attr('id')]) {
        var ajax = Drupal.ajax[$element.attr('id')];

        // Hook before send
        var originalBeforeSend = ajax.beforeSend;
        ajax.beforeSend = function (xhr, settings) {
          console.log('AJAX request starting');
          return originalBeforeSend.call(this, xhr, settings);
        };

        // Hook success
        var originalSuccess = ajax.success;
        ajax.success = function (response, status) {
          console.log('AJAX completed');
          originalSuccess.call(this, response, status);
        };
      }
    }
  };
})(jQuery, Drupal);
```

**AFTER: HTMX JavaScript**
```javascript
(function (Drupal, htmx) {
  // Listen for HTMX events globally
  htmx.on('htmx:beforeRequest', function(event) {
    console.log('HTMX request starting', event.detail);
    // Can call event.preventDefault() to cancel
  });

  htmx.on('htmx:afterSwap', function(event) {
    console.log('HTMX swap completed', event.detail);
  });

  // Custom Drupal events for behavior lifecycle
  htmx.on('htmx:drupal:load', function(event) {
    console.log('Drupal behaviors attached', event.detail);
  });

  htmx.on('htmx:drupal:unload', function(event) {
    console.log('Content being removed', event.detail);
  });

  // Listen on specific element via CSS selector
  document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.target.matches('#my-htmx-element')) {
      console.log('Specific element updated');
    }
  });
})(Drupal, htmx);
```

**Or use `on()` attribute in PHP:**
```php
(new Htmx())
  ->get(Url::fromRoute('my_module.content'))
  ->target('#content')
  ->on('::afterSwap', 'myHandler(event)')  // Inline handler
  ->applyTo($build);
```

Reference: `/core/misc/htmx/htmx-behaviors.js` for Drupal-specific HTMX events

## Common Mistakes

- **Looking for `Drupal.ajax` object** → HTMX doesn't create JavaScript objects. Listen to events instead using `htmx.on()` or `addEventListener()`
- **Using jQuery event binding** → HTMX events are native DOM events. Use `htmx.on()` or `addEventListener()`, not jQuery `.on()`
- **Not checking event.target** → HTMX events bubble. Check `event.target.matches('#selector')` if you only want to handle specific elements
- **Using old jQuery selectors for context** → HTMX works with native DOM. Use `querySelector()`, `querySelectorAll()`, or `matches()`
- **Expecting `response` parameter** → HTMX events have `event.detail` object with request/response info, not direct parameters

## See Also

- Previous: [Dynamic Field Addition Migration](dynamic-field-addition-migration.md)
- Next: [Custom AJAX Command Migration](custom-ajax-command-migration.md)
- Reference: [HTMX event reference](https://htmx.org/reference/#events)
