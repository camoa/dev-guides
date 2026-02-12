---
description: Element lifecycle callbacks — #process, #after_build, #pre_render
drupal_version: "11.x"
---

# Form Elements: Lifecycle Callbacks

## When to Use

> Use #process to add children. Use #after_build for complete tree access. Use #pre_render for final display changes.

## Decision

| Phase | Callback | Can Modify | Use For |
|-------|----------|------------|---------|
| Build | #process | Structure | Add child elements, AJAX wrappers |
| Build | #after_build | Anything | Access complete tree, dependencies |
| Render | #pre_render | Display | Final HTML modifications, libraries |

## Element Processing Callbacks

**Callback Execution Order:**
```
1. #process - During form building (can add children)
2. #after_build - After complete form tree built
3. #pre_render - Final modifications before rendering
```

**#process Pattern:**
```php
'#process' => [
  '::processElement',
  'callback_function_name',
]
```

- Runs during form building
- Can add child elements dynamically
- Core example: password_confirm adds two password fields

**#after_build Pattern:**
```php
'#after_build' => ['::afterBuildCallback']
```

- Runs after entire form tree exists
- Can access parent/sibling elements
- Common use: Add form-wide dependencies

**#pre_render Pattern:**
```php
'#pre_render' => ['::preRenderCallback']
```

- Runs just before rendering to HTML
- Final chance to modify display
- Common use: Attach libraries, alter markup

Reference: `/web/core/lib/Drupal/Core/Render/Element/FormElement.php`

## Value and Validation Callbacks

**#value_callback:**
```php
'#value_callback' => 'callback_function_name'
```

- Purpose: Custom value extraction from form input
- When: Element has complex value structure
- Example: Date elements combine multiple inputs

**#element_validate:**
```php
'#element_validate' => [
  '::validateElement',
  'callback_function_name',
]
```

- Purpose: Element-specific validation
- Runs: Before form-level validation
- Common: Format validation, range checks

## Callback Security

```
FormBuilder maintains callback whitelist
Only approved callbacks run without token validation
Custom callbacks validated after token check
Never use user input as callback names
```

Reference: `/web/core/lib/Drupal/Core/Form/FormBuilder.php` lines 133-156

## Common Mistakes

- **Wrong**: Using #process when #pre_render appropriate (inefficient) → **Right**: Use correct phase
- **Wrong**: Modifying values in #pre_render (too late) → **Right**: Use #process for value changes
- **Wrong**: Not understanding callback execution order → **Right**: Study the flow
- **Wrong**: Adding element validators that need form-level context → **Right**: Use form validation

## See Also

- [Validation Architecture](validation-architecture.md)
- [Form Builder Service](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Form!FormBuilder.php)
- Reference: `/web/core/lib/Drupal/Core/Render/Element/`
