---
description: Validate form fields on focusout to provide immediate feedback without form submission
tldr: "Use live validation when user experience benefits from immediate field-level feedback (email availability checks, username format, real-time constraints). Avoid for simple required-field checks."
drupal_version: "11.x"
---

# Live Field Validation

## When to Use

You need to validate form fields as users type or when they leave a field, providing immediate feedback without form submission.

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

- Using `keyup` event → Excessive server requests; use `focusout` or debounced `keyup`
- Not handling empty values → Returns errors for unfilled required fields before user finishes
- Validating before minimum input length → Check username availability only after >=3 characters typed
- Not clearing previous validation messages → Old errors persist when field becomes valid
- Using throbber progress indicator → Distracting for fast validation; use `'type' => 'none'`

## See Also

- ← Previous: [Multi-Step Form Workflows](multi-step-form-workflows.md) | Next: [Content Manipulation Commands](content-manipulation-commands.md)
- Reference: [AJAX API Basic Concepts](https://www.drupal.org/docs/drupal-apis/ajax-api/basic-concepts)
