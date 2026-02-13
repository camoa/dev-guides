---
description: Form request lifecycle and state management - build, validate, submit flow
drupal_version: "11.x"
---

# Architecture: Form Lifecycle

## When to Use

> Understand the lifecycle to know when to cache forms (multi-step, AJAX) and where to place logic (buildForm vs submitForm).

## Decision

| Situation | Action | Why |
|-----------|--------|-----|
| Multi-step form | `setCached(TRUE)` REQUIRED | Persist state across requests |
| Frequent AJAX rebuilds | `setCached(TRUE)` recommended | Reduce database queries |
| Expensive #options | `setCached(TRUE)` recommended | Cache generated options |
| Simple single-step | No caching needed | Unnecessary overhead |

## Pattern

Standard form request flow:

```
1. Route → FormBuilder receives form class
2. Instantiate via DI container (create() method)
3. buildForm() constructs render array
4. Add security: CSRF token, form_id, form_build_id
5. Process elements: #process, #after_build
6. Render to HTML

Submission:
1. Validate CSRF token (fail → stop)
2. Run validation handlers
3. If valid: Run submit handlers
4. Redirect or custom response
```

## State Management

| Type | Method | Persistence | Use Case |
|------|--------|-------------|----------|
| Temporary | `setTemporaryValue()` | Single request | UI state, display mode |
| Persistent | `set()`/`get()` | Across rebuilds | Multi-step data, workflow state |
| Cached | `setCached(TRUE)` | Database cache | Multi-step forms, expensive builds |

```php
// Multi-step form caching
$form_state->setCached(TRUE); // REQUIRED
$form_state->set('step1_data', $data); // Persists across rebuilds

// Temporary value (single request)
$form_state->setTemporaryValue('display_mode', 'compact');
```

## Common Mistakes

- **Wrong**: Local variables for multi-step data → **Right**: Use `$form_state->set()` (persists)
- **Wrong**: No `setCached(TRUE)` for multi-step → **Right**: Required for state persistence
- **Wrong**: Storing sensitive data in cached forms → **Right**: Encrypt or don't cache sensitive data

## See Also

- [Multi-Step Forms](multi-step-forms.md)
- [Form State Methods](form-state-methods.md)
- [AJAX Architecture](ajax-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Form/FormBuilder.php` lines 249-300
