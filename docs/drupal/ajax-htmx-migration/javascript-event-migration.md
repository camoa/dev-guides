---
description: Migrate custom JavaScript AJAX event hooks to HTMX events — beforeSend, success, error equivalents
drupal_version: "11.x"
---

# JavaScript Event Migration

## When to Use

> Use this when migrating custom JavaScript that hooks into AJAX events for preprocessing, validation, or post-processing.

## Decision

| AJAX Event Hook | HTMX Event | Timing |
|---|---|---|
| `beforeSerialize` | `htmx:configRequest` | Before request sent, modify request data |
| `beforeSubmit` | `htmx:beforeRequest` | Before request, can cancel |
| `beforeSend` | `htmx:beforeRequest` | Before request, can cancel |
| `success` | `htmx:afterSwap` | After DOM updated |
| `error` | `htmx:responseError` | Request failed |
| After behaviors attach | `htmx:drupal:load` | After `Drupal.attachBehaviors()` |
| Before element removal | `htmx:drupal:unload` | Before `Drupal.detachBehaviors()` |

## Pattern

**BEFORE — AJAX JavaScript:**
```javascript
(function ($, Drupal) {
  Drupal.behaviors.myAjax = {
    attach: function (context, settings) {
      var ajax = Drupal.ajax[$('#my-element', context).attr('id')];
      if (ajax) {
        ajax.beforeSend = function (xhr, settings) { console.log('starting'); };
        ajax.success = function (response, status) { console.log('done'); };
      }
    }
  };
})(jQuery, Drupal);
```

**AFTER — HTMX JavaScript:**
```javascript
(function (Drupal, htmx) {
  htmx.on('htmx:beforeRequest', function(event) {
    console.log('HTMX request starting', event.detail);
    // event.preventDefault() cancels the request
  });

  htmx.on('htmx:afterSwap', function(event) {
    console.log('HTMX swap completed', event.detail);
  });

  // Drupal-specific lifecycle events
  htmx.on('htmx:drupal:load', function(event) {
    console.log('Drupal behaviors attached', event.detail);
  });

  // Filter by element
  document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.target.matches('#my-htmx-element')) {
      console.log('Specific element updated');
    }
  });
})(Drupal, htmx);
```

**Or use `on()` in PHP for inline handlers:**
```php
(new Htmx())
  ->get(Url::fromRoute('my_module.content'))
  ->target('#content')
  ->on('::afterSwap', 'myHandler(event)')
  ->applyTo($build);
```

## Common Mistakes

- **Looking for `Drupal.ajax` object** → HTMX does not create JavaScript objects. Listen to events using `htmx.on()` or `addEventListener()`
- **Using jQuery event binding** → HTMX events are native DOM events. Use `htmx.on()` or `addEventListener()`, not jQuery `.on()`
- **Not checking `event.target`** → HTMX events bubble. Use `event.target.matches('#selector')` to handle only specific elements
- **Using jQuery context selectors** → Use `querySelector()` and `querySelectorAll()` with native DOM
- **Expecting `response` parameter** → HTMX events expose `event.detail` with request/response info, not direct parameters

## See Also

- Previous: [Dynamic Field Addition Migration](dynamic-field-addition-migration.md)
- Next: [Custom AJAX Command Migration](custom-ajax-command-migration.md)
- Reference: [HTMX event reference](https://htmx.org/reference/#events)
- Source: `/core/misc/htmx/htmx-behaviors.js`
