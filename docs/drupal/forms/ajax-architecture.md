---
description: AJAX form architecture - core system, element properties, callbacks, and commands
drupal_version: "11.x"
---

# AJAX Form Architecture

## When to Use

> Use AJAX when you need server-side logic or dynamic options. Use #states for simple show/hide (faster, client-side only).

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Dynamic options based on input | AJAX | Need server data |
| Dependent dropdowns | AJAX | Options must change |
| Load entities/data | AJAX | Server-side processing |
| Simple show/hide fields | #states | Faster, no server call |
| Field enable/disable | #states | Client-side only |

## Pattern

```php
// Trigger element with AJAX
$form['country'] = [
  '#type' => 'select',
  '#title' => $this->t('Country'),
  '#options' => $countries,
  '#ajax' => [
    'callback' => '::updateStates',
    'wrapper' => 'states-wrapper',
    'event' => 'change', // Default for select
  ],
];

// Target container
$form['states_wrapper'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'states-wrapper'],
];

$form['states_wrapper']['state'] = [
  '#type' => 'select',
  '#title' => $this->t('State'),
  '#options' => $this->getStates($form_state),
];

// Callback returns element
public function updateStates(array &$form, FormStateInterface $form_state) {
  return $form['states_wrapper'];
}
```

## AJAX Property Configuration

```php
'#ajax' => [
  'callback' => '::ajaxCallback',    // Required
  'wrapper' => 'element-id',         // Target container ID
  'event' => 'change',               // Trigger event
  'method' => 'replace',             // Command method
  'effect' => 'fade',                // Visual effect
  'progress' => [
    'type' => 'throbber',            // or 'fullscreen'
    'message' => $this->t('Loading...'),
  ],
],
```

## Common Events

| Element Type | Default Event | Alternative |
|--------------|---------------|-------------|
| Select, radio, checkbox | change | - |
| Button, link | click | - |
| Textfield | change | keyup (use debounce) |
| Any | blur | custom |

## Advanced Pattern: AjaxResponse

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\ReplaceCommand;
use Drupal\Core\Ajax\MessageCommand;

public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();
  $response->addCommand(new ReplaceCommand('#wrapper', $form['element']));
  $response->addCommand(new MessageCommand('Updated'));
  return $response;
}
```

## Core AJAX Commands

| Command | Purpose | Parameters |
|---------|---------|------------|
| ReplaceCommand | Replace element | selector, content |
| AppendCommand | Add after | selector, content |
| PrependCommand | Add before | selector, content |
| RemoveCommand | Delete element | selector |
| MessageCommand | Show status | message, type |
| RedirectCommand | Navigate | url |
| InvokeCommand | Call JS method | selector, method, args |
| OpenModalDialogCommand | Open modal | title, content, options |

## Common Mistakes

- **Wrong**: Missing wrapper ID in #ajax → **Right**: Always specify wrapper
- **Wrong**: Wrapper ID doesn't exist → **Right**: Check HTML output
- **Wrong**: Not returning render array or AjaxResponse → **Right**: Return one or the other
- **Wrong**: Using non-unique wrapper IDs → **Right**: Unique IDs prevent wrong replacements

## See Also

- [AJAX Security](ajax-security.md)
- [Form States System](form-states-system.md)
- [JavaScript API Guide](https://www.drupal.org/docs/develop/drupal-apis/javascript-api)
- Reference: `/web/core/lib/Drupal/Core/Form/FormAjaxResponseBuilder.php`
