---
description: Configure the #ajax property on any form element — callbacks, wrappers, events, and progress indicators
drupal_version: "11.x"
---

# Form Element AJAX Configuration

## When to Use

> Use the `#ajax` property on any form element when you need server-driven content updates triggered by user interaction without a full page reload.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Simple content replacement | Return render array from callback | Drupal handles wrapping/replacement automatically |
| Multiple DOM updates | Return AjaxResponse with commands | Commands provide precise control over updates |
| Modal/dialog display | Return AjaxResponse with OpenModalDialogCommand | Built-in dialog system with proper focus management |
| Custom animations/effects | `effect` and `speed` in `#ajax` | Provides fade/slide effects without custom JavaScript |
| Disable validation on trigger | `#limit_validation_errors => []` | Allows AJAX without requiring valid form state |

## Pattern

```php
$form['element'] = [
  '#type' => 'select',
  '#title' => t('AJAX Trigger'),
  '#ajax' => [
    'callback' => '::callbackMethod',      // Required: PHP callback
    'wrapper' => 'target-id',              // Required: HTML ID to update
    'event' => 'change',                   // Default varies by element type
    'method' => 'replaceWith',             // replaceWith, html, append, prepend
    'effect' => 'fade',                    // fade, slide, none
    'speed' => 'slow',                     // slow, fast, milliseconds
    'progress' => [
      'type' => 'throbber',                // throbber, bar, fullscreen
      'message' => t('Loading...'),
    ],
    'disable-refocus' => FALSE,
  ],
];
```

Reference: `core/lib/Drupal/Core/Render/Element/RenderElement.php`

## Common Mistakes

- **Wrong**: Omitting `wrapper` property → **Right**: Without wrapper, AJAX fires but nothing updates (check browser console)
- **Wrong**: Using `#` in wrapper value → **Right**: Wrapper is the ID without the hash (`'wrapper' => 'my-id'` not `'#my-id'`)
- **Wrong**: Wrong event for element type → **Right**: `change` for select/checkbox; `focusout` for text inputs to avoid excessive requests
- **Wrong**: No `#limit_validation_errors` on non-submit buttons → **Right**: Add `'#limit_validation_errors' => []` to prevent validation on navigation buttons
- **Wrong**: No progress indicator for slow operations → **Right**: Always configure `progress` for operations >1 second

## See Also

- [Core Concepts](core-concepts.md)
- [Dependent Field Patterns](dependent-field-patterns.md)
- Reference: `core/modules/system/tests/modules/ajax_forms_test/src/Form/AjaxFormsTestSimpleForm.php`
