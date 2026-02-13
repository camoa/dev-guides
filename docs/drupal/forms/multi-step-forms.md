---
description: Multi-step form pattern with state persistence and navigation
drupal_version: "11.x"
---

# Multi-Step Form Pattern

## When to Use

> Use multi-step forms for complex workflows requiring user input across multiple pages. Always enable caching with setCached(TRUE).

## Decision

| Requirement | Implementation | Why |
|-------------|----------------|-----|
| Multi-step wizard | FormBase + setCached(TRUE) | State persistence required |
| Progressive data collection | Multi-step pattern | Better UX than long single form |
| Conditional step branching | Custom step logic | Skip irrelevant steps |
| Simple single form | Standard FormBase | No caching needed |

## Pattern

```php
use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;

class MultiStepForm extends FormBase {
  public function getFormId() {
    return 'multistep_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    // REQUIRED: Enable caching
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
    $form['step1'] = [
      '#type' => 'container',
      '#tree' => TRUE,
    ];

    $form['step1']['name'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Name'),
      '#required' => TRUE,
    ];

    $form['actions']['next'] = [
      '#type' => 'submit',
      '#value' => $this->t('Next'),
      '#submit' => ['::nextSubmit'],
      '#limit_validation_errors' => [['step1']], // Validate step1 only
    ];

    return $form;
  }

  public function nextSubmit(array &$form, FormStateInterface $form_state) {
    // Save current step data
    $step = $form_state->get('step');
    $step_data = $form_state->getValue('step' . $step);
    $form_state->set('step' . $step . '_data', $step_data);

    // Advance step
    $form_state->set('step', $step + 1);

    // Rebuild form
    $form_state->setRebuild(TRUE);
  }

  public function previousSubmit(array &$form, FormStateInterface $form_state) {
    // Go back one step
    $step = $form_state->get('step');
    $form_state->set('step', $step - 1);

    // Rebuild form
    $form_state->setRebuild(TRUE);
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Collect all step data
    $step1_data = $form_state->get('step1_data');
    $step2_data = $form_state->get('step2_data');
    $step3_data = $form_state->getValue('step3');

    // Process complete submission
    $this->processData($step1_data, $step2_data, $step3_data);

    // Redirect
    $form_state->setRedirect('route.success');
  }
}
```

## Navigation Patterns

**Next Button:**
- Save current step data via `set()`
- Increment step counter
- Call `setRebuild(TRUE)`
- Use `#limit_validation_errors` to validate current step only

**Previous Button:**
- Decrement step counter
- Call `setRebuild(TRUE)`
- Use `#limit_validation_errors => []` (no validation)

**Final Submit:**
- Collect data from all steps
- Process complete submission
- Redirect to success page

## Data Persistence

```php
// Store step data (persists across rebuilds)
$form_state->set('step1_data', $data);
$form_state->set('current_step', 2);

// Retrieve later
$previous_data = $form_state->get('step1_data');
$step = $form_state->get('current_step');

// Pre-populate from previous steps
$previous_data = $form_state->get('step1_data');
$form['field']['#default_value'] = $previous_data['field'] ?? '';
```

## Progress Indicator

```php
// Simple counter
$step = $form_state->get('step');
$total = 3;

$form['progress'] = [
  '#markup' => $this->t('Step @current of @total', [
    '@current' => $step,
    '@total' => $total,
  ]),
];
```

## Common Mistakes

- **Wrong**: No setCached(TRUE) → **Right**: REQUIRED for multi-step (data lost otherwise)
- **Wrong**: No #limit_validation_errors on Next/Previous → **Right**: Validate only current step
- **Wrong**: No setRebuild(TRUE) in navigation → **Right**: Required to rebuild form
- **Wrong**: Local variables for step data → **Right**: Use FormState storage
- **Wrong**: No pre-population on back → **Right**: Restore previous values

## See Also

- [Form State Methods](form-state-methods.md)
- [Partial Validation](validation-partial.md)
- [Form Lifecycle](architecture-lifecycle.md)
- Tutorial: [SitePoint: Multi-step Forms](https://www.sitepoint.com/how-to-build-multi-step-forms-in-drupal-8/)
