---
description: AJAX security and advanced patterns — validation, XSS prevention, modals
drupal_version: "11.x"
---

# AJAX: Security and Advanced Patterns

### AJAX Security

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

**Reference:** `/web/core/lib/Drupal/Core/Form/FormBuilder.php` lines 133-156

### Safe AJAX Patterns

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

**XSS Prevention:**
```php
// SAFE - render array
return $form['container'];

// SAFE - escaped markup
return ['#markup' => $this->t('Text: @text', ['@text' => $value])];

// UNSAFE - raw HTML
return ['#markup' => '<div>' . $value . '</div>'];
```

### Advanced AJAX Patterns

**Dependent Field Updates:**
```
Pattern: One field changes, others update
Implementation:
1. Primary field has #ajax callback
2. Callback returns container with dependent fields
3. Container has wrapper ID matching #ajax wrapper
```

**Example Structure:**
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

**AJAX with Form States (#states):**
```
Combine for best UX:
#states for client-side show/hide
AJAX for dynamic options/content
```

**Modal Dialog Pattern:**
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

**Progress Indicator Types:**
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

**Common Mistakes:**
- Not rebuilding form in AJAX callback (stale state)
- Returning HTML instead of render array (XSS risk)
- Missing AJAX library attachment
- Using AJAX when #states would suffice (overcomplicated)

**See Also:**
- Modal Dialog Guide
- Form States System (dedicated section)
- JavaScript API Guide
- Official: [AJAX API Basic Concepts](https://www.drupal.org/docs/drupal-apis/ajax-api/basic-concepts)
