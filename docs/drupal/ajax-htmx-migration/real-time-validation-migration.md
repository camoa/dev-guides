---
description: "Real-Time Validation Migration — migrate field-level validation that runs on blur without submitting the form"
tldr: "Migrate on-blur field validation (email availability, format checks). HTMX has no ->throttle() method — throttling and debouncing are trigger modifiers: trigger('focusout throttle:1s') or trigger('focusout delay:500ms')."
drupal_version: "11.x"
---

# Real-Time Validation Migration

## When to Use

> Migrate field-level validation that runs on blur (focusout) without submitting the form. Common for email availability checks, username validation, or format verification.

## Steps

1. **Replace `#ajax` with HTMX on field** — Configure `trigger('focusout')`
2. **Add validation result container** — Target for validation messages
3. **Check trigger in buildForm()** — Run validation when specific field triggered
4. **Return validation message** — Update the result container

## BEFORE: AJAX

```php
$form['email'] = [
  '#type' => 'email',
  '#title' => t('Email'),
  '#ajax' => [
    'callback' => '::validateEmailCallback',
    'wrapper' => 'email-validation',
    'event' => 'focusout',
    'progress' => ['type' => 'none'],
  ],
];

$form['email_validation'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'email-validation'],
];

public function validateEmailCallback(array &$form, FormStateInterface $form_state) {
  $email = $form_state->getValue('email');

  if ($this->emailExists($email)) {
    $form['email_validation']['#markup'] = '<span class="error">Email already taken</span>';
  }
  else {
    $form['email_validation']['#markup'] = '<span class="success">Available</span>';
  }

  return $form['email_validation'];
}
```

## AFTER: HTMX

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$form['email'] = [
  '#type' => 'email',
  '#title' => t('Email'),
];

// Configure HTMX to trigger on blur
(new Htmx())
  ->post(Url::fromRoute('<current>'))
  ->onlyMainContent()
  ->trigger('focusout')
  ->select('#email-validation')
  ->target('#email-validation')
  ->swap('outerHTML')
  ->applyTo($form['email']);

$form['email_validation'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'email-validation'],
];

// In buildForm, check if this is validation request
$trigger = $this->getHtmxTriggerName();
if ($trigger === 'email') {
  $email = $form_state->getValue('email');

  if ($email && $this->emailExists($email)) {
    $form['email_validation']['#markup'] = '<span class="error">Email already taken</span>';
  }
  elseif ($email) {
    $form['email_validation']['#markup'] = '<span class="success">Available</span>';
  }
}
```

Reference: HTMX trigger patterns in `/core/lib/Drupal/Core/Htmx/Htmx.php`

## Common Mistakes

- **Using `'event' => 'focusout'`** → HTMX uses `trigger('focusout')` method, not an array key
- **Not handling empty values** → Check if field has value before validating. Empty blur shouldn't show error
- **Creating separate callback** → Put validation logic in `buildForm()` checking `getHtmxTriggerName()`. No callback needed
- **Including progress indicator** → HTMX is fast enough without progress indicators. Omit unless validation is slow
- **Not throttling requests** → There is no `->throttle()` method. Throttle is a trigger modifier: use `->trigger('focusout throttle:1s')`. Debounce (delay) works similarly: `->trigger('focusout delay:500ms')`

## See Also

- Previous: [Multi-Step Wizard Migration](multi-step-wizard-migration.md)
- Next: [Infinite Scroll Migration](infinite-scroll-migration.md)
- Reference: HTMX trigger modifiers like `changed`, `delay`, `throttle` in HTMX documentation
