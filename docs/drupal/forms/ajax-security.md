---
description: AJAX security and advanced patterns — validation, XSS prevention, modals
drupal_version: "11.x"
---

# AJAX: Security and Advanced Patterns

## When to Use

> Always return render arrays for XSS safety. Use AjaxResponse for multiple updates. Validate input in callbacks.

## Decision

| Pattern | When | Why |
|---------|------|-----|
| Return render array | Single update | Auto-escaped, safe |
| Return AjaxResponse | Multiple updates | Granular control |
| Dependent fields | Container wrapper | Update multiple fields |
| Modal dialog | OpenModalDialogCommand | Dialog UI |

## AJAX Security

**Built-in Protections:**
```
AJAX requests validate:
- form_build_id (cache key)
- form_token (CSRF protection)
Same security as regular form submission
```

**Value Callback Security:**
```
FormBuilder whitelist (lines 133-156)
Only safe callbacks execute before token validation
File uploads, dates blocked until token validated
Prevents state changes from invalid requests
```

Reference: `/web/core/lib/Drupal/Core/Form/FormBuilder.php` lines 133-156

## Safe AJAX Patterns

**DO:**
- Return render arrays (automatically escaped)
- Use t() for translated strings (auto-escaped)
- Validate input in callback before processing
- Use AJAX commands from core library

**DON'T:**
- Return raw HTML strings without sanitization
- Use $_POST directly in callbacks (use $form_state)
- Skip form validation in AJAX rebuilds
- Trust client-provided data

## XSS Prevention

```php
// SAFE - render array
return $form['container'];

// SAFE - escaped markup
return ['#markup' => $this->t('Text: @text', ['@text' => $value])];

// UNSAFE - raw HTML
return ['#markup' => '<div>' . $value . '</div>'];
```

## Advanced AJAX Patterns

**Dependent Field Updates:**
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

## AJAX with Form States

Combine for best UX:
- #states for client-side show/hide
- AJAX for dynamic options/content

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
    ['width' => '50%', 'dialogClass' => 'custom-class']
  ));

  return $response;
}
```

## Progress Indicator Types

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

## Common Mistakes

- **Wrong**: Not rebuilding form in AJAX callback → **Right**: Return updated form elements
- **Wrong**: Returning HTML instead of render array → **Right**: Return render arrays for XSS safety
- **Wrong**: Missing AJAX library attachment → **Right**: Library auto-attached by #ajax
- **Wrong**: Using AJAX when #states would suffice → **Right**: Prefer #states for simple logic

## See Also

- [AJAX Architecture](ajax-architecture.md)
- [Form States System](form-states-system.md)
- [Security Best Practices](security-best-practices.md)
- Documentation: [AJAX API Basic Concepts](https://www.drupal.org/docs/drupal-apis/ajax-api/basic-concepts)
- Reference: `/web/core/lib/Drupal/Core/Ajax/`
