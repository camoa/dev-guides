---
description: Multi-step forms — caching, navigation, data persistence patterns
drupal_version: "11.x"
---

# Multi-Step Form Pattern

## When to Use

> Use multi-step forms for complex workflows. Always enable caching with setCached(TRUE). Use partial validation for navigation.

## Decision

| Requirement | Implementation | Why |
|-------------|----------------|-----|
| Step persistence | `setCached(TRUE)` | REQUIRED for state |
| Store step data | `$form_state->set()` | Persist across rebuilds |
| Navigation | `setRebuild(TRUE)` | Rebuild form |
| Previous button | `#limit_validation_errors => []` | Skip validation |
| Next button | `#limit_validation_errors => [['step']]` | Validate current step only |

## Architecture Overview

**Multi-Step Requirements:**
1. Enable caching: `$form_state->setCached(TRUE)` [REQUIRED]
2. Store current step: `$form_state->set('step', $step_number)`
3. Conditional buildForm() based on step
4. Navigation buttons: Next, Previous, Submit
5. Final step processes all collected data

**Why Caching Required:**
```
Form must persist across page requests
form_build_id links requests to cached form
Without cache: FormState storage lost between steps
Cache location: database cache_form table
```

## Pattern

```php
<?php

namespace Drupal\mymodule\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;

class MultiStepForm extends FormBase {

  public function getFormId() {
    return 'mymodule_multistep_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    // Enable caching (REQUIRED for multi-step)
    $form_state->setCached(TRUE);

    // Get or initialize step
    $step = $form_state->get('step') ?? 1;
    $form_state->set('step', $step);

    // Build step-specific form
    switch ($step) {
      case 1:
        return $this->buildStep1($form, $form_state);
      case 2:
        return $this->buildStep2($form, $form_state);
      case 3:
        return $this->buildStep3($form, $form_state);
    }
  }

  protected function buildStep1(array $form, FormStateInterface $form_state) {
    $form['step1']['name'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Name'),
      '#required' => TRUE,
    ];

    $form['actions']['next'] = [
      '#type' => 'submit',
      '#value' => $this->t('Next'),
      '#submit' => ['::nextSubmit'],
      '#limit_validation_errors' => [['step1']],
    ];

    return $form;
  }

  public function nextSubmit(array &$form, FormStateInterface $form_state) {
    // Save step data
    $step = $form_state->get('step');
    $step_data = $form_state->getValue('step' . $step);
    $form_state->set('step' . $step . '_data', $step_data);

    // Advance step
    $form_state->set('step', $step + 1);

    // Rebuild form
    $form_state->setRebuild(TRUE);
  }

  public function previousSubmit(array &$form, FormStateInterface $form_state) {
    $step = $form_state->get('step');
    $form_state->set('step', $step - 1);
    $form_state->setRebuild(TRUE);
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Collect all step data
    $step1_data = $form_state->get('step1_data');
    $step2_data = $form_state->get('step2_data');

    // Process complete submission
    $form_state->setRedirect('route.success');
  }
}
```

## Navigation Handlers

**Previous Button:**
```php
$form['actions']['previous'] = [
  '#type' => 'submit',
  '#value' => $this->t('Previous'),
  '#submit' => ['::previousSubmit'],
  '#limit_validation_errors' => [], // No validation
];
```

## Data Persistence

**Store Step Data:**
```php
$form_state->set('step1_data', $data);      // Persist across steps
$form_state->set('total_steps', 3);         // Configuration
$form_state->set('entity', $entity);        // Working entity
```

**Pre-populate from Previous Steps:**
```php
$previous_data = $form_state->get('step1_data');
$form['field']['#default_value'] = $previous_data['field'] ?? '';
```

## Progress Indicators

**Simple Counter:**
```php
$step = $form_state->get('step');
$total = $form_state->get('total_steps') ?? 3;

$form['progress'] = [
  '#markup' => $this->t('Step @current of @total', [
    '@current' => $step,
    '@total' => $total,
  ]),
];
```

## Common Mistakes

- **Wrong**: Forgetting `setCached(TRUE)` → **Right**: Always enable for multi-step (data loss)
- **Wrong**: Not using `#limit_validation_errors` on Next/Previous → **Right**: Use partial validation
- **Wrong**: Not calling `setRebuild(TRUE)` in navigation handlers → **Right**: Rebuild required
- **Wrong**: Storing data in local variables → **Right**: Use FormState storage
- **Wrong**: Not pre-populating fields when returning to previous step → **Right**: Set defaults from stored data

## See Also

- [Form State Methods](form-state-methods.md)
- [Partial Validation](validation-partial.md)
- Tutorial: [Multi-step Forms](https://www.sitepoint.com/how-to-build-multi-step-forms-in-drupal-8/)
- Reference: `/web/core/lib/Drupal/Core/Form/FormState.php`
