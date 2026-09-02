---
description: Configure the #ajax property on any form element — callbacks, wrappers, events, and progress indicators
tldr: "Use the `#ajax` property on any form element when you need server-driven content updates triggered by user interaction without a full page reload."
drupal_version: "11.x"
---

# Form Element AJAX Configuration

## When to Use

You need to add AJAX behavior to any form element (select, textfield, checkbox, button, etc.).

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Simple content replacement | Return render array from callback | Drupal handles wrapping/replacement automatically |
| Multiple DOM updates | Return AjaxResponse with commands | Commands provide precise control over updates |
| Modal/dialog display | Return AjaxResponse with OpenModalDialogCommand | Built-in dialog system with proper focus management |
| Custom animations/effects | `effect` and `speed` settings in `#ajax` | Provides fade/slide effects without custom JavaScript |
| Disable validation on trigger | `#limit_validation_errors => []` | Allows AJAX without requiring valid form state |

## Pattern

```php
// Complete #ajax configuration
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
    'disable-refocus' => FALSE,            // Prevent refocus after update
  ],
];
```

Reference: `core/lib/Drupal/Core/Render/Element/RenderElement.php`

## Common Mistakes

- Omitting `wrapper` property → AJAX fires but nothing updates (check browser console for errors)
- Using `#` in wrapper value → Wrapper is the ID without the hash (`'wrapper' => 'my-id'` not `'#my-id'`)
- Wrong event for element type → `change` works for select/checkbox, use `focusout` for text inputs to avoid excessive requests
- Not disabling validation for non-submit buttons → Add `#limit_validation_errors => []` to buttons that shouldn't trigger validation
- Missing progress indicator for slow operations → Users don't know request is processing; always configure `progress` for operations >1 second

## See Also

- ← Previous: [Core Concepts](core-concepts.md) | Next: [Dependent Field Patterns](dependent-field-patterns.md)
- Reference: `core/modules/system/tests/modules/ajax_forms_test/src/Form/AjaxFormsTestSimpleForm.php`
