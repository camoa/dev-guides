---
description: Debug AJAX failures using browser DevTools, server-side logging, and a structured troubleshooting checklist
tldr: "Use these techniques when AJAX requests fail, return unexpected results, or produce errors. Start with the browser DevTools Network tab before adding server-side logging."
drupal_version: "11.x"
---

# Debugging Techniques

## When to Use

AJAX requests fail, return unexpected results, or produce errors.

## Pattern

```php
// Server-side debugging
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  // Log triggering element
  \Drupal::logger('my_module')->debug('Triggering element: @element', [
    '@element' => print_r($form_state->getTriggeringElement(), TRUE),
  ]);

  // Log form values
  \Drupal::logger('my_module')->debug('Form values: @values', [
    '@values' => print_r($form_state->getValues(), TRUE),
  ]);

  // Return error response for debugging
  if (!$valid_condition) {
    $response = new AjaxResponse();
    $response->addCommand(new AlertCommand('Debug: Invalid condition triggered'));
    return $response;
  }

  return $form['target'];
}
```

```javascript
// Client-side debugging (JavaScript console)
// Add to custom JavaScript file:
(function ($, Drupal) {
  // Log AJAX events
  $(document).ajaxStart(function() {
    console.log('AJAX request started');
  });

  $(document).ajaxComplete(function(event, xhr, settings) {
    console.log('AJAX request completed:', settings.url);
    console.log('Response:', xhr.responseJSON);
  });

  $(document).ajaxError(function(event, xhr, settings, error) {
    console.error('AJAX error:', error);
    console.error('URL:', settings.url);
    console.error('Response:', xhr.responseText);
  });

  // Debug specific AJAX command execution
  const originalPrototype = Drupal.AjaxCommands.prototype.insert;
  Drupal.AjaxCommands.prototype.insert = function (ajax, response, status) {
    console.log('InsertCommand executed:', response);
    originalPrototype.call(this, ajax, response, status);
  };
})(jQuery, Drupal);
```

Reference: `core/misc/ajax.js`

## Debugging Checklist

**Debugging Checklist:**

1. Open browser DevTools (F12)
2. Go to Network tab, filter XHR
3. Trigger AJAX action
4. Check request status (200 = success, 403 = access denied, 500 = server error)
5. Click request, view Response tab (should be JSON)
6. Check Console tab for JavaScript errors
7. Verify wrapper element exists: `$('#wrapper-id').length` in console
8. Check Drupal logs: Admin → Reports → Recent log messages

## Common Mistakes

- Not checking browser console → Most errors appear in console; always check Network and Console tabs
- Missing wrapper element → Command executes but nothing updates; verify wrapper ID exists in DOM
- Form validation errors → Check for red validation messages; add `'#limit_validation_errors' => []` to debug
- Returning wrong data type → Must return render array or AjaxResponse; strings/NULL cause failures
- Cacheable dependencies → AJAX uses cached form; clear cache and test again

## See Also

- ← Previous: [Screen Reader Support](screen-reader-support.md) | Next: [Testing AJAX](testing-ajax.md)
- Reference: `core/misc/ajax.js` (client-side AJAX implementation)
