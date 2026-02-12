---
description: Multi-step forms — caching, navigation, data persistence patterns
drupal_version: "11.x"
---

# Multi-Step Form Pattern

### Architecture Overview

**Multi-Step Requirements:**
```
1. Enable caching: $form_state->setCached(TRUE) [REQUIRED]
2. Store current step: $form_state->set('step', $step_number)
3. Conditional buildForm() based on step
4. Navigation buttons: Next, Previous, Submit
5. Final step processes all collected data
```

**Why Caching Required:**
```
Form must persist across page requests
form_build_id links requests to cached form
Without cache: FormState storage lost between steps
Cache location: database cache_form table
```

### Implementation Pattern

**buildForm() Structure:**
```php
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
```

**Step Builder Methods:**
```php
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
    '#limit_validation_errors' => [['step1']], // Only validate step1
  ];

  return $form;
}
```

### Navigation Handlers

**Next Button:**
```php
public function nextSubmit(array &$form, FormStateInterface $form_state) {
  // Save step data
  $step = $form_state->get('step');
  $step_data = $form_state->getValue('step' . $step);
  $form_state->set('step' . $step . '_data', $step_data);

  // Advance step
  $form_state->set('step', $step + 1);

  // Rebuild form for next step
  $form_state->setRebuild(TRUE);
}
```

**Previous Button:**
```php
public function previousSubmit(array &$form, FormStateInterface $form_state) {
  // Go back one step
  $step = $form_state->get('step');
  $form_state->set('step', $step - 1);

  // Rebuild form
  $form_state->setRebuild(TRUE);
}

// In buildForm, add previous button:
$form['actions']['previous'] = [
  '#type' => 'submit',
  '#value' => $this->t('Previous'),
  '#submit' => ['::previousSubmit'],
  '#limit_validation_errors' => [], // No validation for going back
];
```

**Final Submit:**
```php
public function submitForm(array &$form, FormStateInterface $form_state) {
  // Collect all step data
  $step1_data = $form_state->get('step1_data');
  $step2_data = $form_state->get('step2_data');
  $step3_data = $form_state->getValue('step3');

  // Process complete submission
  // ... save to database, create entities, etc.

  // Redirect
  $form_state->setRedirect('route.success');
}
```

### Data Persistence Patterns

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

### Progress Indicators

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

**Progress Bar (Render Array):**
```php
$form['progress'] = [
  '#theme' => 'progress_bar',
  '#percent' => ($step / $total) * 100,
  '#message' => $this->t('Step @current of @total', [
    '@current' => $step,
    '@total' => $total,
  ]),
];
```

### Common Patterns

**Conditional Steps:**
```php
// In nextSubmit:
if ($form_state->getValue(['step1', 'skip_step2'])) {
  $form_state->set('step', 3); // Skip to step 3
}
else {
  $form_state->set('step', 2);
}
```

**Step Validation:**
```php
public function validateForm(array &$form, FormStateInterface $form_state) {
  $step = $form_state->get('step');

  // Step-specific validation
  switch ($step) {
    case 1:
      $this->validateStep1($form, $form_state);
      break;
    case 2:
      $this->validateStep2($form, $form_state);
      break;
  }
}
```

**Common Mistakes:**
- Forgetting `setCached(TRUE)` (data loss between steps)
- Not using `#limit_validation_errors` on Next/Previous
- Not calling `setRebuild(TRUE)` in navigation handlers
- Storing data in local variables instead of FormState
- Not pre-populating fields when returning to previous step

**See Also:**
- Form State Methods (dedicated section)
- Partial Validation (dedicated section)
- Form Caching Strategy
- Tutorial: [SitePoint: Multi-step Forms](https://www.sitepoint.com/how-to-build-multi-step-forms-in-drupal-8/)
