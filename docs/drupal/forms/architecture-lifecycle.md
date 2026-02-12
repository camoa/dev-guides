---
description: Form lifecycle — request flow, state management, caching
drupal_version: "11.x"
---

# Architecture: Form Lifecycle

## When to Use

> Use this reference when debugging form flow or implementing multi-step forms.

## Decision

| Situation | Storage Type | Method |
|-----------|--------------|--------|
| Multi-step data | Persistent | `$form_state->set()` / `get()` |
| UI state | Temporary | `setTemporaryValue()` |
| Form input values | Values | `getValue()` |
| Multi-step form | Caching | `setCached(TRUE)` REQUIRED |

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

Reference: `/web/core/lib/Drupal/Core/Form/FormBuilder.php` lines 249-300

## State Management

**FormState Object:**
- Persists data across rebuild cycles (AJAX, multi-step)
- Cached in database via `form_build_id` (when enabled)
- Methods: `set()`/`get()` for persistent storage, `setTemporaryValue()` for single request

**Storage Patterns:**
| Type | Persistence | Use Case |
|------|-------------|----------|
| Temporary | Single request | UI state, display mode |
| Persistent | Across rebuilds | Multi-step data, workflow state |
| Cached | Database cache | Multi-step forms, expensive builds |

## Form Caching Decision

```
Multi-step form? → setCached(TRUE) REQUIRED
Frequent AJAX rebuilds? → setCached(TRUE) recommended
Expensive #options generation? → setCached(TRUE) recommended
Simple single-step form? → No caching needed
```

## Common Mistakes

- **Wrong**: Using local variables instead of `$form_state->set()` in multi-step forms → **Right**: Store in FormState
- **Wrong**: Not calling `setCached(TRUE)` for multi-step forms → **Right**: Enable caching for persistence
- **Wrong**: Storing sensitive data in cached forms without encryption → **Right**: Be mindful of cache security

## See Also

- [Multi-Step Forms](multi-step-forms.md)
- [Form State Methods](form-state-methods.md)
- [AJAX Architecture](ajax-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Form/FormStateInterface.php`
