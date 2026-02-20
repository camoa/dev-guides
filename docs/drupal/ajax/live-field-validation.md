---
description: Validate form fields on focusout to provide immediate feedback without form submission
drupal_version: "11.x"
---

# Live Field Validation

## When to Use

> Use live validation when user experience benefits from immediate field-level feedback (email availability checks, username format, real-time constraints). Avoid for simple required-field checks.

## Pattern

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['email'] = [
    '#type' => 'email',
    '#title' => t('Email Address'),
    '#required' => TRUE,
    '#ajax' => [
      'callback' => '::validateEmailCallback',
      'wrapper' => 'email-validation',
      'event' => 'focusout',  // Validate when user leaves field
      'progress' => ['type' => 'none'],  // No spinner for validation
    ],
  ];

  $form['email_validation'] = [
    '#type' => 'container',
    '#attributes' => ['id' => 'email-validation'],
  ];

  return $form;
}

public function validateEmailCallback(array &$form, FormStateInterface $form_state) {
  $email = $form_state->getValue('email');

  if (empty($email)) {
    return $form['email_validation'];
  }

  $response = new AjaxResponse();

  if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $message = '<div class="messages messages--error">Invalid email format.</div>';
  }
  elseif ($this->emailExists($email)) {
    $message = '<div class="messages messages--error">Email already registered.</div>';
  }
  else {
    $message = '<div class="messages messages--status">Email available.</div>';
  }

  $response->addCommand(new HtmlCommand('#email-validation', $message));
  return $response;
}
```

Reference: `core/lib/Drupal/Core/Ajax/HtmlCommand.php`

## Common Mistakes

- **Wrong**: Using `keyup` event → **Right**: Causes excessive server requests; use `focusout` or debounced `keyup`
- **Wrong**: Not handling empty values → **Right**: Returns errors for unfilled fields before user finishes; guard with `empty()` check
- **Wrong**: Validating before minimum input length → **Right**: Check availability only after >=3 characters typed
- **Wrong**: Not clearing previous validation messages → **Right**: Old errors persist when field becomes valid; always replace the container
- **Wrong**: Using throbber progress → **Right**: Distracting for fast validation; use `'type' => 'none'`

## See Also

- [Multi-Step Form Workflows](multi-step-form-workflows.md)
- [Content Manipulation Commands](content-manipulation-commands.md)
- Reference: [AJAX API Basic Concepts](https://www.drupal.org/docs/drupal-apis/ajax-api/basic-concepts)
