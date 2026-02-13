---
description: AJAX security, XSS prevention, and advanced patterns like modals
drupal_version: "11.x"
---

# AJAX: Security and Advanced Patterns

## When to Use

> Always use render arrays in AJAX callbacks (auto-escaped). Use AJAX commands for multiple element updates.

## Security

**Built-in Protections:**
- AJAX requests validate form_build_id (cache key)
- AJAX requests validate form_token (CSRF protection)
- Same security as regular form submission

**Value Callback Security:**
- FormBuilder whitelist controls pre-token execution
- File uploads, dates blocked until token validated
- Prevents state changes from invalid requests

## Safe AJAX Patterns

```php
// SAFE - render array (auto-escaped)
public function ajaxCallback(array &$form, FormStateInterface $form_state) {
  return $form['container'];
}

// SAFE - escaped markup with t()
return ['#markup' => $this->t('Text: @text', ['@text' => $value])];

// SAFE - plain text
return ['#plain_text' => $user_input];

// UNSAFE - raw HTML concatenation
return ['#markup' => '<div>' . $value . '</div>']; // XSS vulnerability
```

## Advanced Pattern: Dependent Fields

```php
$form['trigger'] = [
  '#type' => 'select',
  '#ajax' => [
    'callback' => '::updateDependents',
    'wrapper' => 'dependents-wrapper',
  ],
];

$form['dependents'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'dependents-wrapper'],
];

$form['dependents']['field1'] = [...]; // Updated by AJAX

public function updateDependents(array &$form, FormStateInterface $form_state) {
  return $form['dependents'];
}
```

## Modal Dialog Pattern

```php
use Drupal\Core\Ajax\AjaxResponse;
use Drupal\Core\Ajax\OpenModalDialogCommand;

public function openModal(array &$form, FormStateInterface $form_state) {
  $response = new AjaxResponse();

  $modal_form = \Drupal::formBuilder()->getForm('Drupal\mymodule\Form\ModalForm');

  $response->addCommand(new OpenModalDialogCommand(
    'Modal Title',
    $modal_form,
    ['width' => '50%']
  ));

  return $response;
}
```

## Progress Indicators

```php
// Throbber (default)
'progress' => ['type' => 'throbber']

// Fullscreen
'progress' => ['type' => 'fullscreen']

// Custom message
'progress' => [
  'type' => 'throbber',
  'message' => $this->t('Calculating...'),
]

// None
'progress' => ['type' => 'none']
```

## AJAX with #states

Combine for best UX:
- #states for instant client-side show/hide
- AJAX for dynamic options/content loading

## Common Mistakes

- **Wrong**: Not rebuilding form in AJAX callback → **Right**: Return updated element
- **Wrong**: Returning HTML instead of render array → **Right**: Use render arrays (XSS safe)
- **Wrong**: Missing AJAX library attachment → **Right**: Auto-attached by Form API
- **Wrong**: Using AJAX when #states sufficient → **Right**: #states is faster

## See Also

- [Form States System](form-states-system.md)
- [AJAX Architecture](ajax-architecture.md)
- [Modal Dialog Guide](https://www.drupal.org/docs/drupal-apis/ajax-api/basic-concepts)
- Reference: `/web/core/modules/system/tests/modules/ajax_forms_test/`
