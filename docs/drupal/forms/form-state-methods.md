---
description: FormState methods reference - value access, storage, control flags, and error handling
drupal_version: "11.x"
---

# Form State: Methods Reference

## When to Use

> Use getValue() for submitted values (sanitized), set()/get() for persistent storage across rebuilds, setTemporaryValue() for single-request data.

## Decision

| Data Type | Method | Persistence | Use Case |
|-----------|--------|-------------|----------|
| Submitted values | `getValue()` | Current submission | Form input |
| Multi-step data | `set()`/`get()` | Until form complete | Workflow state |
| UI state | `setTemporaryValue()` | Single request only | Display mode |

## Value Access Methods

```php
// Retrieve values (ALWAYS use these, not $_POST)
$all_values = $form_state->getValues(); // All values
$single = $form_state->getValue('field_name'); // Single field
$nested = $form_state->getValue(['parent', 'child']); // Nested
$exists = $form_state->hasValue('field'); // Check before access

// Modify values
$form_state->setValue('field', $new_value); // Set single
$form_state->setValues($array); // Set all
$form_state->unsetValue('field'); // Remove
```

**CRITICAL:** getValue() returns sanitized values. getUserInput() returns raw unsanitized (UNSAFE - avoid).

## Storage Methods (Persistent)

```php
// Persist across rebuilds (multi-step forms)
$form_state->set('step', 2);
$form_state->set('step1_data', $data);
$step = $form_state->get('step');
$exists = $form_state->has('step1_data');

// Common storage keys
'step' - Current step number
'step1_data' - Step-specific data
'entity_id' - Working entity ID
'original_values' - For comparison
```

## Temporary Storage (Single Request)

```php
// Single request only - lost after page reload
$form_state->setTemporaryValue('display_mode', 'compact');
$mode = $form_state->getTemporaryValue('display_mode');
$exists = $form_state->hasTemporaryValue('display_mode');

// Use cases: UI state, calculation intermediates, conditional display
```

## Control Flag Methods

```php
// Form behavior
$form_state->setRebuild(TRUE); // Prevent submission, rebuild form
$form_state->isRebuilding(); // Check rebuild state
$form_state->setCached(TRUE); // Enable caching (REQUIRED for multi-step)
$form_state->disableRedirect(); // No redirect (AJAX submission)
$form_state->setResponse($response); // Custom response

// Redirect methods
$form_state->setRedirect('route.name', ['param' => $value]);
$form_state->setRedirectUrl(Url::fromRoute('...'));
```

## Error Handling Methods

```php
// Set errors (validation phase only)
$form_state->setErrorByName('field_name', $this->t('Error message')); // Preferred
$form_state->setError($form['field'], $this->t('Error')); // With element reference

// Check and retrieve errors
FormStateInterface::hasAnyErrors(); // Static method
$errors = $form_state->getErrors(); // All errors (array)
$error = $form_state->getError($form['field']); // Single field
$form_state->clearErrors(); // Reset all
```

## Common Mistakes

- **Wrong**: Using getUserInput() → **Right**: Use getValue() (sanitized)
- **Wrong**: Local variables for multi-step → **Right**: Use set()/get()
- **Wrong**: Not calling setCached(TRUE) for multi-step → **Right**: Required for persistence
- **Wrong**: Using $_POST directly → **Right**: Always use FormState methods

## See Also

- [Multi-Step Forms](multi-step-forms.md)
- [AJAX Forms](ajax-architecture.md)
- [Validation Architecture](validation-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Form/FormStateInterface.php` (1160+ lines)
