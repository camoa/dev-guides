---
description: Migrate field-level validation on blur — email availability checks and format verification without form submission
drupal_version: "11.x"
---

# Real-Time Validation Migration

## When to Use

> Use this when migrating field-level validation that runs on blur (focusout) without submitting the form — email availability checks, username validation, format verification.

## Decision

| Step | Action |
|---|---|
| 1 | Replace `#ajax` with `Htmx` on the field, configure `trigger('focusout')` |
| 2 | Add a validation result container as HTMX target |
| 3 | In `buildForm()`, check `getHtmxTriggerName()` to detect the triggering field |
| 4 | Set validation message markup on the container element |

## Pattern

**BEFORE:**
```php
$form['email'] = [
  '#type' => 'email',
  '#ajax' => [
    'callback' => '::validateEmailCallback',
    'wrapper' => 'email-validation',
    'event' => 'focusout',
  ],
];
$form['email_validation'] = ['#type' => 'container', '#attributes' => ['id' => 'email-validation']];

public function validateEmailCallback(array &$form, FormStateInterface $form_state) {
  $email = $form_state->getValue('email');
  $form['email_validation']['#markup'] = $this->emailExists($email) ? '<span class="error">Email already taken</span>' : '<span class="success">Available</span>';
  return $form['email_validation'];
}
```

**AFTER:**
```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$form['email'] = ['#type' => 'email', '#title' => t('Email')];

(new Htmx())
  ->post(Url::fromRoute('<current>'))
  ->onlyMainContent()
  ->trigger('focusout')
  ->select('#email-validation')
  ->target('#email-validation')
  ->swap('outerHTML')
  ->applyTo($form['email']);

$form['email_validation'] = ['#type' => 'container', '#attributes' => ['id' => 'email-validation']];

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

## Common Mistakes

- **Using `'event' => 'focusout'`** → HTMX uses the `trigger('focusout')` method, not an array key
- **Not handling empty values** → Check if the field has a value before validating — empty blur should not show an error
- **Creating a separate callback** → Put validation logic in `buildForm()` checking `getHtmxTriggerName()`. No callback needed
- **Including a progress indicator** → HTMX is fast enough without progress indicators. Omit unless validation is slow
- **Not throttling requests** → For expensive validation, add `->throttle('1s')` to prevent rapid-fire requests on every keystroke + blur

## See Also

- Previous: [Multi-Step Wizard Migration](multi-step-wizard-migration.md)
- Next: [Infinite Scroll Migration](infinite-scroll-migration.md)
- Reference: HTMX trigger modifiers (`changed`, `delay`, `throttle`) in HTMX documentation
- Source: `/core/lib/Drupal/Core/Htmx/Htmx.php`
