---
description: Debug AJAX failures using browser DevTools, server-side logging, and a structured troubleshooting checklist
drupal_version: "11.x"
---

# Debugging Techniques

## When to Use

> Use these techniques when AJAX requests fail, return unexpected results, or produce errors. Start with the browser DevTools Network tab before adding server-side logging.

## Pattern

**Server-side logging:**

```php
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  \Drupal::logger('my_module')->debug('Triggering element: @element', [
    '@element' => print_r($form_state->getTriggeringElement(), TRUE),
  ]);
  \Drupal::logger('my_module')->debug('Form values: @values', [
    '@values' => print_r($form_state->getValues(), TRUE),
  ]);

  if (!$valid_condition) {
    $response = new AjaxResponse();
    $response->addCommand(new AlertCommand('Debug: Invalid condition triggered'));
    return $response;
  }

  return $form['target'];
}
```

**Client-side logging:**

```javascript
(function ($, Drupal) {
  $(document).ajaxStart(function() { console.log('AJAX request started'); });

  $(document).ajaxComplete(function(event, xhr, settings) {
    console.log('AJAX completed:', settings.url, xhr.responseJSON);
  });

  $(document).ajaxError(function(event, xhr, settings, error) {
    console.error('AJAX error:', error, 'URL:', settings.url);
  });
})(jQuery, Drupal);
```

**Debugging checklist:**

1. Open browser DevTools (F12)
2. Go to Network tab, filter XHR
3. Trigger AJAX action
4. Check request status (200=success, 403=access denied, 500=server error)
5. Click request, view Response tab (should be JSON)
6. Check Console tab for JavaScript errors
7. Verify wrapper element exists: `$('#wrapper-id').length` in console
8. Check Drupal logs: Admin → Reports → Recent log messages

Reference: `core/misc/ajax.js`

## Common Mistakes

- **Wrong**: Not checking browser console → **Right**: Most errors appear in console; always check Network and Console tabs first
- **Wrong**: Missing wrapper element → **Right**: Command executes but nothing updates; verify wrapper ID exists in DOM
- **Wrong**: Form validation errors blocking AJAX → **Right**: Add `#limit_validation_errors => []` to the triggering element to debug
- **Wrong**: Returning wrong data type → **Right**: Must return render array or AjaxResponse; strings/NULL cause failures
- **Wrong**: Not clearing cache between tests → **Right**: AJAX uses cached form; clear cache and test again

## See Also

- [Screen Reader Support](screen-reader-support.md)
- [Testing AJAX](testing-ajax.md)
- Reference: `core/misc/ajax.js` (client-side AJAX implementation)
