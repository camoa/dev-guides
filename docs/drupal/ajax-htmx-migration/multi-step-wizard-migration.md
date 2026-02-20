---
description: Migrate multi-step wizard forms to HTMX — bookmarkable steps with browser back/forward support via route parameters
drupal_version: "11.x"
---

# Multi-Step Wizard Migration

## When to Use

> Use this when migrating multi-step wizard forms where each step is driven by AJAX navigation. HTMX enables bookmarkable steps with browser back/forward button support.

## Decision

| Step | Action |
|---|---|
| 1 | Add `{step}` parameter to route — each step becomes a distinct URL |
| 2 | Replace `#ajax` buttons with `html_tag` buttons + `Htmx` per step URL |
| 3 | Move step tracking to route parameter — remove `$form_state->get('step')` |
| 4 | Use `pushUrl()` on each button for browser history |
| 5 | Delete all submit handlers — navigation logic is gone |

## Pattern

**BEFORE:**
```php
$step = $form_state->get('step') ?: 1;
$form['next'] = [
  '#type' => 'submit',
  '#value' => t('Next'),
  '#submit' => ['::nextStep'],
  '#ajax' => ['callback' => '::stepCallback', 'wrapper' => 'form-wrapper'],
];
public function nextStep(&$form, $form_state) {
  $form_state->set('step', $form_state->get('step') + 1);
  $form_state->setRebuild();
}
```

**AFTER:**
```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

// Route: path: '/wizard/{step}'
public function buildForm(array $form, FormStateInterface $form_state, $step = 1) {
  $form['#attributes']['id'] = 'wizard-form';

  // ... render step fields ...

  if ($step > 1) {
    $prevUrl = Url::fromRoute('my_module.wizard', ['step' => $step - 1]);
    $form['prev'] = ['#type' => 'html_tag', '#tag' => 'button', '#value' => t('Previous'), '#attributes' => ['type' => 'button']];
    (new Htmx())->post($prevUrl)->onlyMainContent()->target('#wizard-form')->swap('outerHTML')->pushUrl($prevUrl)->applyTo($form['prev']);
  }

  if ($step < 3) {
    $nextUrl = Url::fromRoute('my_module.wizard', ['step' => $step + 1]);
    $form['next'] = ['#type' => 'html_tag', '#tag' => 'button', '#value' => t('Next'), '#attributes' => ['type' => 'button']];
    (new Htmx())->post($nextUrl)->onlyMainContent()->target('#wizard-form')->swap('outerHTML')->pushUrl($nextUrl)->applyTo($form['next']);
  }

  return $form;
}
// No callback or submit handler methods needed
```

**Routing:**
```yaml
my_module.wizard:
  path: '/wizard/{step}'
  defaults:
    _form: '\Drupal\my_module\Form\WizardForm'
    step: 1
  requirements:
    step: '\d+'
```

## Common Mistakes

- **Storing step in form state** → Use route parameters instead — makes steps bookmarkable and enables browser back/forward
- **Not using `pushUrl()`** → Without this, the URL stays the same and the back button does not work
- **Using submit handlers for navigation** → Delete them. HTMX buttons POST directly to the step URL
- **Forgetting form ID** → Set `'#attributes' => ['id' => 'wizard-form']` so HTMX can target the form for replacement
- **Not preserving form values between steps** → Store submitted values in temp storage or database; route parameters only handle navigation state

## See Also

- Previous: [Button-Triggered Content Load Migration](button-triggered-content-load-migration.md)
- Next: [Real-Time Validation Migration](real-time-validation-migration.md)
- Reference: `Htmx::pushUrl()` for browser history integration
