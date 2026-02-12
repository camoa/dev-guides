---
description: Form lifecycle — request flow, state management, caching
drupal_version: "11.x"
---

# Architecture: Form Lifecycle

## When to Use

> Use this reference to understand form request flow, state persistence, and caching decisions.

## Request Flow

**Standard Form Request:**
1. FormBuilder receives form class/ID from route/controller
2. Instantiates form object via class resolver (DI container)
3. Calls `buildForm()` to construct render array
4. Adds security elements: CSRF token, form_id, form_build_id
5. Processes elements: runs #process, #after_build callbacks
6. Renders form to HTML

**Form Submission Request:**
1. Validates CSRF token (fails → stops processing)
2. Executes validation handlers (element → form → typed config)
3. If validation passes: runs submit handlers
4. Redirects or returns custom response

## State Management

**FormState Object:**
- Persists data across rebuild cycles (AJAX, multi-step)
- Cached in database via `form_build_id` (when enabled)
- Methods: `set()`/`get()` for persistent storage, `setTemporaryValue()` for single request

## Decision

| Type | Method | Persistence | Use Case |
|------|--------|-------------|----------|
| Temporary | `setTemporaryValue()` | Single request | UI state, display mode |
| Persistent | `set()`/`get()` | Across rebuilds | Multi-step data, workflow state |
| Cached | `setCached(TRUE)` | Database cache | Multi-step forms, expensive builds |

**Form Caching Decision:**
```
Multi-step form? → setCached(TRUE) REQUIRED
Frequent AJAX rebuilds? → setCached(TRUE) recommended
Expensive #options generation? → setCached(TRUE) recommended
Simple single-step form? → No caching needed
```

## Pattern

```php
// Multi-step form caching
public function buildForm(array $form, FormStateInterface $form_state) {
  $form_state->setCached(TRUE);

  // Persistent storage across steps
  $form_state->set('user_data', $data);

  // Temporary (single request)
  $form_state->setTemporaryValue('display_mode', 'advanced');

  return $form;
}
```

## Common Mistakes

- **Wrong**: Using local variables instead of `$form_state->set()` in multi-step forms → **Right**: Store all step data in FormState
  - WHY BAD: Local variables lost between page requests, form resets to step 1 on every submit
- **Wrong**: Not calling `setCached(TRUE)` for multi-step forms → **Right**: Always enable caching for multi-step
  - WHY BAD: FormState not persisted across requests, form_build_id link broken, multi-step navigation impossible
- **Wrong**: Storing sensitive data in cached forms without encryption → **Right**: Use TempStore or encrypt cached data
  - WHY BAD: cache_form table not encrypted, database dumps leak data, session hijacking exposes info

## See Also

- [Multi-Step Form Pattern](multi-step-forms.md)
- [Form State Methods Reference](form-state-methods.md)
- [AJAX Form Architecture](ajax-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Form/FormBuilder.php` lines 249-300
