---
description: FormState methods reference — value access, storage, control flags, errors
drupal_version: "11.x"
---

# Form State: Methods Reference

## When to Use

> Use getValue() for sanitized form input. Use set()/get() for multi-step data persistence. Use control flags for form behavior.

## Decision

| Need | Method | Persistence |
|------|--------|-------------|
| Get submitted value | `getValue()` | Current submission |
| Multi-step data | `set()`/`get()` | Until form complete |
| UI state | `setTemporaryValue()` | Current request only |
| Set errors | `setErrorByName()` | Current request |
| Redirect | `setRedirect()` | Post-submit |
| Rebuild form | `setRebuild()` | Current request |

## Value Access Methods

**Retrieve Values:**
| Method | Returns | Use Case |
|--------|---------|----------|
| `getValues()` | All values (array) | Full form processing |
| `getValue($key)` | Single value | Specific field access |
| `getValue(['parent', 'child'])` | Nested value | Nested form elements |
| `hasValue($key)` | Boolean | Check before access |

**Sanitization:**
```
getValue() returns sanitized values (safe)
getUserInput() returns raw unsanitized input (UNSAFE - avoid)
Always use getValue() unless specific reason
```

**Modify Values:**
| Method | Purpose | When |
|--------|---------|------|
| `setValue($key, $value)` | Set single value | Programmatic changes |
| `setValues($array)` | Set all values | Programmatic submission |
| `unsetValue($key)` | Remove value | Conditional processing |

## Storage Methods (Persistent)

**Across Rebuilds:**
| Method | Purpose | Persistence |
|--------|---------|-------------|
| `set($property, $value)` | Store data | Until form complete |
| `get($property)` | Retrieve data | Until form complete |
| `has($property)` | Check existence | Until form complete |
| `setStorage($array)` | Set all storage | Until form complete |
| `getStorage()` | Get all storage | Until form complete |

**Common Storage Keys:**
```php
'step' - Current step number
'step1_data' - Step-specific data
'total_steps' - Total step count
'entity' - Working entity object
'original_values' - For comparison
```

## Temporary Storage (Single Request)

**Single Request Only:**
| Method | Purpose | Persistence |
|--------|---------|-------------|
| `setTemporaryValue($key, $value)` | Store temp data | Current request only |
| `getTemporaryValue($key)` | Get temp data | Current request only |
| `hasTemporaryValue($key)` | Check temp | Current request only |

## Control Flag Methods

**Form Behavior:**
| Method | Effect | When to Use |
|--------|--------|-------------|
| `setRebuild($bool)` | Prevent submission | AJAX updates, dynamic forms |
| `isRebuilding()` | Check rebuild state | Conditional logic |
| `setCached($bool)` | Enable caching | Multi-step forms (REQUIRED) |
| `isCached()` | Check cache state | Debugging |
| `disableRedirect()` | No redirect | AJAX submission |
| `setResponse($response)` | Custom response | Non-HTML responses |

**Redirect Methods:**
| Method | Purpose | Example |
|--------|---------|---------|
| `setRedirect($route, $params, $options)` | Route redirect | `setRedirect('node.add', ['node_type' => 'article'])` |
| `setRedirectUrl($url)` | URL object redirect | `setRedirectUrl(Url::fromRoute(...))` |

## Error Handling Methods

**Error Management:**
| Method | Purpose | Phase |
|--------|---------|-------|
| `setErrorByName($name, $msg)` | Set field error | Validation |
| `setError($element, $msg)` | Set element error | Validation |
| `getErrors()` | Get all errors | After validation |
| `getError($element)` | Get element error | After validation |
| `clearErrors()` | Reset errors | Error recovery |
| `hasAnyErrors()` | Check error state (static) | Conditional logic |

**Error Setting Best Practices:**
```php
// Preferred - by name
$form_state->setErrorByName('field_name', $this->t('Error'));

// When you have element reference
$form_state->setError($form['field'], $this->t('Error'));

// Check before setting
if (!$form_state->hasAnyErrors()) {
  // Conditional logic
}
```

## Complete Reference

Interface File: `/web/core/lib/Drupal/Core/Form/FormStateInterface.php` (1160+ lines)

## See Also

- [Multi-Step Forms](multi-step-forms.md)
- [AJAX Forms](ajax-architecture.md)
- [Validation](validation-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Form/FormState.php`
