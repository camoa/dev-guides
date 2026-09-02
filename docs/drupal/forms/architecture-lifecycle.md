---
description: "Form request lifecycle and state management - build, validate, submit flow"
tldr: "Understand the lifecycle to know when to cache forms (multi-step, AJAX) and where to place logic (buildForm vs submitForm)."
drupal_version: "11.x"
---

# Architecture: Form Lifecycle

## When to Use

> Understand the lifecycle to know when to cache forms (multi-step, AJAX) and where to place logic (buildForm vs submitForm).

## Reference: Request Flow

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

**Reference Implementation:**

- FormBuilder main flow: `/web/core/lib/Drupal/Core/Form/FormBuilder.php` lines 249-300
- Complete lifecycle: Study `buildForm()`, `validateForm()`, `submitForm()` methods

## Reference: State Management

**FormState Object:**

- Persists data across rebuild cycles (AJAX, multi-step)
- Cached in database via `form_build_id` (when enabled)
- Methods: `set()`/`get()` for persistent storage, `setTemporaryValue()` for single request

## Decision: Storage Patterns

| Type | Method | Persistence | Use Case |
|------|--------|-------------|----------|
| Temporary | `setTemporaryValue()` | Single request | UI state, display mode |
| Persistent | `set()`/`get()` | Across rebuilds | Multi-step data, workflow state |
| Cached | `setCached(TRUE)` | Database cache | Multi-step forms, expensive builds |

## Decision: Form Caching

```
Multi-step form? → setCached(TRUE) REQUIRED
Frequent AJAX rebuilds? → setCached(TRUE) recommended
Expensive #options generation? → setCached(TRUE) recommended
Simple single-step form? → No caching needed
```

## Common Mistakes

- Using local variables instead of `$form_state->set()` in multi-step forms
    - **WHY BAD:** Local variables lost between page requests, form resets to step 1 on every submit, user data disappears
- Not calling `setCached(TRUE)` for multi-step forms
    - **WHY BAD:** FormState not persisted across requests, form_build_id link broken, multi-step navigation impossible
- Storing sensitive data in cached forms without encryption
    - **WHY BAD:** cache_form table not encrypted, database dumps leak data, session hijacking exposes sensitive info

## See Also

- [Multi-Step Form Pattern](multi-step-forms.md) (dedicated section)
- [Form State Methods Reference](form-state-methods.md) (dedicated section)
- [AJAX Form Architecture](ajax-architecture.md) (dedicated section)
- Reference: [Form API Workflow](https://www.drupal.org/docs/drupal-apis/form-api/form-api-workflow)
