---
description: Build wizard-style multi-step forms with AJAX navigation using form_state step tracking
tldr: "Use multi-step AJAX forms for wizard-style workflows where users navigate sequential steps without page reloads. Use standard forms for simple one-page submissions."
drupal_version: "11.x"
---

# Multi-Step Form Workflows

## When to Use

You need wizard-style forms with sequential steps, where users navigate forward/backward without page reloads.

## Steps

1. **Initialize step tracking**

   ```php
   public function buildForm(array $form, FormStateInterface $form_state) {
     $step = $form_state->get('step') ?: 1;
     $form_state->set('step', $step);
   }
   ```

2. **Build step-specific form elements**

   ```php
   switch ($step) {
     case 1:
       $form['step1'] = $this->buildStep1($form_state);
       break;
     case 2:
       $form['step2'] = $this->buildStep2($form_state);
       break;
   }
   ```

3. **Add navigation buttons with AJAX**

   ```php
   $form['actions']['next'] = [
     '#type' => 'submit',
     '#value' => t('Next'),
     '#submit' => ['::nextStep'],
     '#ajax' => [
       'callback' => '::stepCallback',
       'wrapper' => 'form-wrapper',
     ],
   ];
   ```

4. **Implement step transitions**

   ```php
   public function nextStep(array &$form, FormStateInterface $form_state) {
     $step = $form_state->get('step');
     $form_state->set('step', $step + 1);
     $form_state->setRebuild();  // CRITICAL: rebuilds form
   }
   ```

5. **Return entire form from callback**

   ```php
   public function stepCallback(array &$form, FormStateInterface $form_state) {
     return $form;  // Return whole form to update all content
   }
   ```

The form itself must carry the wrapper the navigation buttons target:

```php
$form['#prefix'] = '<div id="form-wrapper">';
$form['#suffix'] = '</div>';
```

## Decision Points

| At this step... | If... | Then... |
|-----------------|-------|---------|
| Navigation | First step | Hide "Previous" button |
| Navigation | Last step | Show "Submit" instead of "Next" |
| Data persistence | Moving between steps | Store values in `$form_state->set('data', $values)` |
| Validation | Step requires validation | Use separate submit handler with validation |
| Progress indication | Multiple steps | Add progress bar showing current step |

## Common Mistakes

- Forgetting `$form_state->setRebuild()` → Form submits instead of rebuilding, workflow breaks
- Not wrapping entire form → Update misses navigation buttons; wrap form with `#prefix`/`#suffix` containing wrapper ID
- Validating on navigation buttons → Add `#limit_validation_errors => []` to Previous/Next buttons
- Losing form data between steps → Store in `$form_state`, not private properties (form rebuilds from scratch)
- Not conditionally showing buttons → Previous button on step 1, Next button on final step creates poor UX

## See Also

- ← Previous: [Dependent Field Patterns](dependent-field-patterns.md) | Next: [Live Field Validation](live-field-validation.md)
- Reference: `core/modules/system/tests/modules/ajax_forms_test/src/Form/AjaxFormsTestLazyLoadForm.php`
