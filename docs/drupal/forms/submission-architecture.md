---
description: Submission architecture — handler priority, redirect patterns, state storage
drupal_version: "11.x"
---

# Submission Architecture

### Submission Handler Priority

**Execution Order:**
```
1. Button-specific #submit handlers (if that button clicked)
2. Form-level #submit handlers ($form['#submit'])
3. Form class submitForm() method

Only runs if validation passes
Skipped if $form_state->setRebuild(TRUE) called
```

**Core Submitter Service:**
- File: `/web/core/lib/Drupal/Core/Form/FormSubmitter.php`
- Handles: Redirect logic, batch operations, response setting
- Reference: `submitForm()` method shows complete flow

### Handler Patterns

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
  '#submit' => ['::saveContinue'], // Method name or callable
];

public function saveContinue(array &$form, FormStateInterface $form_state) {
  // Custom handling
}
```

**Multiple Handlers:**
```php
$form['#submit'][] = 'mymodule_form_submit';
$form['actions']['submit']['#submit'][] = '::customSubmit';
```

### Redirect Patterns

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

**External URL (Rare):**
```php
use Drupal\Core\Url;
$url = Url::fromUri('https://example.com');
$form_state->setRedirectUrl($url);
```

### Form State Storage

**Storage Types:**
| Type | Method | Persistence | Use Case |
|------|--------|-------------|----------|
| Temporary | `setTemporaryValue()` | Single request | Display mode, UI state |
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

### Rebuild vs Submit

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

**Common Mistakes:**
- Not redirecting after successful submit (form resubmit on refresh)
  - **WHY BAD:** Browser refresh resubmits form (POST data), creates duplicate nodes/entities, processes payment twice, users see "resubmit form?" dialog
- Using string route name instead of Url object when needed
  - **WHY BAD:** Can't add route parameters, multilingual prefix breaks, access checking bypassed, route generation fails
- Setting both redirect and custom response (response wins)
  - **WHY BAD:** Redirect silently ignored, confusing behavior, developer expects redirect but custom response takes precedence
- Forgetting to disable redirect in AJAX submit handlers
  - **WHY BAD:** AJAX response hijacked by redirect, JavaScript receives HTML redirect page instead of JSON, AJAX fails

**See Also:**
- Redirect API Guide
- Multi-Step Forms (dedicated section)
- AJAX Submission (AJAX section)
