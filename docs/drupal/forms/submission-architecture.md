---
description: Submission architecture — handler priority, redirect patterns, state storage
drupal_version: "11.x"
---

# Submission Architecture

## When to Use

> Use button-specific handlers for different actions. Use setRedirect() for standard flow. Use setRebuild() for AJAX/multi-step.

## Decision

| Scenario | Method | Why |
|----------|--------|-----|
| Standard redirect | `setRedirect()` | Route-based navigation |
| AJAX submission | `disableRedirect()` | No page reload |
| Multi-step navigation | `setRebuild(TRUE)` | Rebuild form |
| Custom response | `setResponse()` | Non-HTML responses |

## Submission Handler Priority

**Execution Order:**
```
1. Button-specific #submit handlers (if that button clicked)
2. Form-level #submit handlers ($form['#submit'])
3. Form class submitForm() method

Only runs if validation passes
Skipped if $form_state->setRebuild(TRUE) called
```

Reference: `/web/core/lib/Drupal/Core/Form/FormSubmitter.php`

## Handler Patterns

**Class Method (Recommended):**
```php
public function submitForm(array &$form, FormStateInterface $form_state) {
  $value = $form_state->getValue('field_name');
  // Process submission
  $form_state->setRedirect('route.name');
}
```

**Button-Specific Handler:**
```php
$form['actions']['save_continue'] = [
  '#type' => 'submit',
  '#value' => $this->t('Save and Continue'),
  '#submit' => ['::saveContinue'],
];

public function saveContinue(array &$form, FormStateInterface $form_state) {
  // Custom handling
}
```

## Redirect Patterns

**Route-Based Redirect (Preferred):**
```php
$form_state->setRedirect('route.name', ['param' => $value]);
```

**URL Object Redirect:**
```php
$url = Url::fromRoute('entity.node.canonical', ['node' => 123]);
$form_state->setRedirectUrl($url);
```

**No Redirect (AJAX/Custom Response):**
```php
$form_state->disableRedirect();
```

**Custom Response:**
```php
use Symfony\Component\HttpFoundation\Response;
$response = new Response('Custom content');
$form_state->setResponse($response);
```

## Form State Storage

**Storage Types:**
| Type | Method | Persistence | Use Case |
|------|--------|-------------|----------|
| Temporary | `setTemporaryValue()` | Single request | UI state, display mode |
| Persistent | `set()`/`get()` | Across rebuilds | Multi-step data |
| Values | `getValue()` | Current submission | Form input values |

**Multi-Step Storage Pattern:**
```php
// Store step data
$form_state->set('step1_data', $data);
$form_state->set('current_step', 2);

// Retrieve later
$previous_data = $form_state->get('step1_data');
$step = $form_state->get('current_step');
```

## Rebuild vs Submit

**Rebuild Pattern:**
```php
$form_state->setRebuild(TRUE);
// Prevents submit handlers from running
// Form rebuilds with new values
// Common in AJAX forms
```

**Decision Matrix:**
```
User selecting value that changes form? → Rebuild
User completing final action? → Submit
AJAX interaction updating fields? → Rebuild
AJAX submitting final data? → Submit (disableRedirect)
```

## Common Mistakes

- **Wrong**: Not redirecting after successful submit → **Right**: Always redirect (prevents form resubmit on refresh)
- **Wrong**: Using string route name instead of Url object when needed → **Right**: Use proper method
- **Wrong**: Setting both redirect and custom response → **Right**: Response wins, be intentional
- **Wrong**: Forgetting to disable redirect in AJAX submit handlers → **Right**: Use disableRedirect()

## See Also

- [Multi-Step Forms](multi-step-forms.md)
- [AJAX Architecture](ajax-architecture.md)
- [Form State Methods](form-state-methods.md)
- [Redirect API](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Url.php)
- Reference: `/web/core/lib/Drupal/Core/Form/FormSubmitter.php`
