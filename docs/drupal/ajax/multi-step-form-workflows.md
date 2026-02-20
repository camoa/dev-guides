---
description: Build wizard-style multi-step forms with AJAX navigation using form_state step tracking
drupal_version: "11.x"
---

# Multi-Step Form Workflows

## When to Use

> Use multi-step AJAX forms for wizard-style workflows where users navigate sequential steps without page reloads. Use standard forms for simple one-page submissions.

## Decision

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Navigation | First step | Hide "Previous" button |
| Navigation | Last step | Show "Submit" instead of "Next" |
| Data persistence | Moving between steps | Store values in `$form_state->set('data', $values)` |
| Validation | Step requires validation | Use separate submit handler with validation |
| Progress indication | Multiple steps | Add progress bar showing current step |

## Pattern

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $step = $form_state->get('step') ?: 1;
  $form_state->set('step', $step);

  $form['#prefix'] = '<div id="form-wrapper">';
  $form['#suffix'] = '</div>';

  switch ($step) {
    case 1: $form['step1'] = $this->buildStep1($form_state); break;
    case 2: $form['step2'] = $this->buildStep2($form_state); break;
  }

  $form['actions']['next'] = [
    '#type' => 'submit',
    '#value' => t('Next'),
    '#submit' => ['::nextStep'],
    '#limit_validation_errors' => [],
    '#ajax' => ['callback' => '::stepCallback', 'wrapper' => 'form-wrapper'],
  ];
  return $form;
}

public function nextStep(array &$form, FormStateInterface $form_state) {
  $step = $form_state->get('step');
  $form_state->set('step', $step + 1);
  $form_state->setRebuild();  // CRITICAL: rebuilds form
}

public function stepCallback(array &$form, FormStateInterface $form_state) {
  return $form;  // Return whole form to update all content
}
```

Reference: `core/modules/system/tests/modules/ajax_forms_test/src/Form/AjaxFormsTestLazyLoadForm.php`

## Common Mistakes

- **Wrong**: Forgetting `$form_state->setRebuild()` → **Right**: Without it, form submits instead of rebuilding
- **Wrong**: Not wrapping entire form → **Right**: Without a wrapper around the whole form, navigation buttons don't update
- **Wrong**: Validating on navigation buttons → **Right**: Add `#limit_validation_errors => []` to Previous/Next buttons
- **Wrong**: Storing data in private properties → **Right**: Store in `$form_state` — properties are lost on rebuild
- **Wrong**: Not conditionally showing Previous/Submit buttons → **Right**: No Previous on step 1, show Submit only on final step

## See Also

- [Dependent Field Patterns](dependent-field-patterns.md)
- [Live Field Validation](live-field-validation.md)
- Reference: [Drupal AJAX API documentation](https://www.drupal.org/docs/drupal-apis/ajax-api)
