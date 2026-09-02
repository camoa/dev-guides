---
description: "Multi-Step Wizard Migration — migrate AJAX-driven wizard steps to bookmarkable HTMX steps with back/forward support"
tldr: "Migrate a multi-step wizard so each step is a distinct URL instead of form-state. Store the step as a route parameter, not $form_state->get('step') — that is what makes pushUrl() and the browser back button work."
drupal_version: "11.x"
---

# Multi-Step Wizard Migration

## When to Use

> Migrate multi-step wizard forms where each step is an AJAX-driven navigation. HTMX enables bookmarkable steps with browser back/forward button support.

## Steps

1. **Add step parameter to route** — Make each step a distinct URL
2. **Replace `#ajax` buttons with HTMX buttons** — Configure each to load its step URL
3. **Move form state to route parameters** — Use `$step` argument instead of `$form_state->get('step')`
4. **Use `pushUrl()` for browser history** — Enable back button navigation
5. **Remove submit handlers** — No longer needed for navigation

## BEFORE: AJAX

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $step = $form_state->get('step') ?: 1;

  $form['#prefix'] = '<div id="form-wrapper">';
  $form['#suffix'] = '</div>';

  switch ($step) {
    case 1:
      $form['step1_field'] = [
        '#type' => 'textfield',
        '#title' => t('Step 1 Field'),
      ];
      break;
    case 2:
      $form['step2_field'] = [
        '#type' => 'textfield',
        '#title' => t('Step 2 Field'),
      ];
      break;
  }

  if ($step > 1) {
    $form['prev'] = [
      '#type' => 'submit',
      '#value' => t('Previous'),
      '#submit' => ['::previousStep'],
      '#ajax' => [
        'callback' => '::stepCallback',
        'wrapper' => 'form-wrapper',
      ],
    ];
  }

  if ($step < 3) {
    $form['next'] = [
      '#type' => 'submit',
      '#value' => t('Next'),
      '#submit' => ['::nextStep'],
      '#ajax' => [
        'callback' => '::stepCallback',
        'wrapper' => 'form-wrapper',
      ],
    ];
  }

  return $form;
}

public function stepCallback(array &$form, FormStateInterface $form_state) {
  return $form;
}

public function nextStep(array &$form, FormStateInterface $form_state) {
  $step = $form_state->get('step') + 1;
  $form_state->set('step', $step);
  $form_state->setRebuild();
}
```

## AFTER: HTMX

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

// Route parameter: path: '/wizard/{step}'
public function buildForm(array $form, FormStateInterface $form_state, $step = 1) {
  $form['#attributes']['id'] = 'wizard-form';

  switch ($step) {
    case 1:
      $form['step1_field'] = [
        '#type' => 'textfield',
        '#title' => t('Step 1 Field'),
      ];
      break;
    case 2:
      $form['step2_field'] = [
        '#type' => 'textfield',
        '#title' => t('Step 2 Field'),
      ];
      break;
  }

  if ($step > 1) {
    $prevUrl = Url::fromRoute('my_module.wizard', ['step' => $step - 1]);

    $form['prev'] = [
      '#type' => 'html_tag',
      '#tag' => 'button',
      '#value' => t('Previous'),
      '#attributes' => ['type' => 'button'],
    ];

    (new Htmx())
      ->post($prevUrl)
      ->onlyMainContent()
      ->target('#wizard-form')
      ->swap('outerHTML')
      ->pushUrl($prevUrl)
      ->applyTo($form['prev']);
  }

  if ($step < 3) {
    $nextUrl = Url::fromRoute('my_module.wizard', ['step' => $step + 1]);

    $form['next'] = [
      '#type' => 'html_tag',
      '#tag' => 'button',
      '#value' => t('Next'),
      '#attributes' => ['type' => 'button'],
    ];

    (new Htmx())
      ->post($nextUrl)
      ->onlyMainContent()
      ->target('#wizard-form')
      ->swap('outerHTML')
      ->pushUrl($nextUrl)
      ->applyTo($form['next']);
  }

  return $form;
}

// No callback or submit handler methods needed!
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

Reference: Multi-step pattern similar to `/core/modules/config/src/Form/ConfigSingleExportForm.php`

## Common Mistakes

- **Storing step in form state** → Use route parameters instead. This makes steps bookmarkable and enables browser back/forward buttons
- **Not using `pushUrl()`** → Without this, the URL stays the same and back button doesn't work. Always push URL for navigation steps
- **Using submit handlers for navigation** → Delete them. HTMX buttons are simple `html_tag` buttons that POST to the step URL
- **Forgetting form ID** → Use `'#attributes' => ['id' => 'wizard-form']` so HTMX can target the form for replacement
- **Not preserving form values between steps** → Store submitted values in temp storage or database. Route parameters only handle navigation state, not form data

## See Also

- Previous: [Button-Triggered Content Load Migration](button-triggered-content-load-migration.md)
- Next: [Real-Time Validation Migration](real-time-validation-migration.md)
- Reference: `Htmx::pushUrl()` for browser history integration
