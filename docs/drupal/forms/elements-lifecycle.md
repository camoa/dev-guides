---
description: Element lifecycle callbacks — #process, #after_build, #pre_render
drupal_version: "11.x"
---

# Form Elements: Lifecycle Callbacks

### Element Processing Callbacks

**Callback Execution Order:**
```
1. #process - During form building (can add children)
2. #after_build - After complete form tree built
3. #pre_render - Final modifications before rendering
```

**When to Use Each:**
| Callback | Phase | Common Use | Can Modify |
|----------|-------|------------|------------|
| #process | Build | Add child elements, AJAX wrappers | Structure |
| #after_build | Build | Access complete tree, add dependencies | Anything |
| #pre_render | Render | Final HTML modifications, libraries | Display |

**#process Pattern:**
```
Runs during form building
Can add child elements dynamically
Core example: password_confirm adds two password fields
Common use: Container elements, composite fields
```

**#after_build Pattern:**
```
Runs after entire form tree exists
Can access parent/sibling elements
Common use: Add form-wide dependencies
```

**#pre_render Pattern:**
```
Runs just before rendering to HTML
Final chance to modify display
Common use: Attach libraries, alter markup
```

### Value and Validation Callbacks

**#value_callback:**
```
Purpose: Custom value extraction from form input
When: Element has complex value structure
Example: Date elements combine multiple inputs
Reference: /web/core/lib/Drupal/Core/Render/Element/FormElement.php
```

**#element_validate:**
```
Purpose: Element-specific validation
Type: Array of callback functions
Runs: Before form-level validation
Common: Format validation, range checks
```

**Element Validation Pattern:**
```php
'#element_validate' => [
  '::validateElement',
  'callback_function_name',
]
```

**Callback Security:**
```
FormBuilder maintains callback whitelist
Only approved callbacks run without token validation
Custom callbacks validated after token check
Never use user input as callback names
```

**Common Mistakes:**
- Using #process when #pre_render appropriate (inefficient)
- Modifying values in #pre_render (too late, use #process)
- Not understanding callback execution order
- Adding element validators that need form-level context

**See Also:**
- Validation Architecture (dedicated section)
- Form Builder Service
- Security: Value Callback Whitelist
