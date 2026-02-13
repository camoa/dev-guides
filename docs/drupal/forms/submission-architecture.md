---
description: Form submission architecture - handler priority, redirect patterns, and state storage
drupal_version: "11.x"
---

# Submission Architecture

## When to Use

> Understand submission handler priority to control execution order. Always redirect after successful submit to prevent form resubmission.

## Decision

| Situation | Pattern | Why |
|-----------|---------|-----|
| Standard submission | setRedirect() | Prevents resubmission on refresh |
| AJAX submission | disableRedirect() | Custom response, no page reload |
| External URL | setRedirectUrl(Url::fromUri()) | Rare, only for external sites |
| Custom response | setResponse($response) | Non-HTML responses |

## Submission Handler Priority

```
Execution Order (if validation passes):
1. Button-specific #submit handlers (if that button clicked)
2. Form-level #submit handlers ($form['#submit'])
3. Form class submitForm() method

Skipped if $form_state->setRebuild(TRUE) called
```

## Pattern

```php
// Standard submit
public function submitForm(array &$form, FormStateInterface $form_state) {
  $value = $form_state->getValue('field_name');

  // Process data
  $this->doSomething($value);

  // Always redirect (prevents resubmission)
  $form_state->setRedirect('route.name', ['param' => $id]);
}

// Button-specific handler
$form['actions']['save_continue'] = [
  '#type' => 'submit',
  '#value' => $this->t('Save and Continue'),
  '#submit' => ['::saveContinue'],
];

public function saveContinue(array &$form, FormStateInterface $form_state) {
  // Custom handling
  $this->save($form_state->getValues());
  $form_state->setRedirect('mymodule.next_step');
}

// AJAX submission
public function ajaxSubmit(array &$form, FormStateInterface $form_state) {
  $form_state->disableRedirect(); // No page reload
  // Return AjaxResponse
}
```

## Redirect Patterns

```php
// Route-based (preferred)
$form_state->setRedirect('route.name', ['param' => $value]);

// URL object
$url = Url::fromRoute('entity.node.canonical', ['node' => 123]);
$form_state->setRedirectUrl($url);

// External URL (rare)
$url = Url::fromUri('https://example.com');
$form_state->setRedirectUrl($url);

// Custom response
$response = new Response('Custom content');
$form_state->setResponse($response);
```

## Form State Storage

| Type | Method | Persistence | Use Case |
|------|--------|-------------|----------|
| Temporary | `setTemporaryValue()` | Single request | UI state |
| Persistent | `set()`/`get()` | Across rebuilds | Multi-step data |
| Values | `getValue()` | Current submission | Form input |

## Rebuild vs Submit

```php
// Rebuild (prevents submit handlers from running)
$form_state->setRebuild(TRUE); // Form rebuilds with new values

// Use rebuild when:
// - User selecting value that changes form
// - AJAX interaction updating fields

// Use submit when:
// - User completing final action
// - AJAX submitting final data (use disableRedirect)
```

## Common Mistakes

- **Wrong**: Not redirecting after submit → **Right**: Always redirect (prevents resubmission)
- **Wrong**: Using string route name when Url object needed → **Right**: Use Url::fromRoute()
- **Wrong**: Setting both redirect and custom response → **Right**: Response wins, choose one
- **Wrong**: No disableRedirect() in AJAX submit → **Right**: AJAX response hijacked by redirect

## See Also

- [Redirect API Guide](https://www.drupal.org/docs/drupal-apis/routing-system)
- [Multi-Step Forms](multi-step-forms.md)
- [AJAX Architecture](ajax-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Form/FormSubmitter.php`
