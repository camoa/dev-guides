---
description: Validation architecture — three-tier system, execution order, error methods
drupal_version: "11.x"
---

# Validation Architecture

### Validation Levels

**Three-Tier Validation System:**
```
1. Element-level (#element_validate)
   - Per-element basis
   - Format, range, pattern validation
   - Runs first

2. Form-level (validateForm(), #validate)
   - Cross-field validation
   - Business logic
   - Runs second

3. Typed config (ConfigFormBase only)
   - Schema constraint validation
   - Runs automatically from config schema
   - Runs third
```

**Reference Implementation:**
- File: `/web/core/lib/Drupal/Core/Form/FormValidator.php`
- Method: `validateForm()` lines 94-126 shows execution order
- Method: `doValidateForm()` lines 122+ recursive validation

### Validation Execution Order

**Complete Chain:**
```
1. CSRF token validation (failure stops all processing)
2. Element validators (depth-first tree traversal)
   - #element_validate callbacks
   - Built-in element type validation
3. Form validators (#validate array)
   - In order added (via hook_form_alter or buildForm)
4. Form class validateForm() method
5. Typed config validators (ConfigFormBase only)
   - Constraint validators from schema
6. If any errors: redisplay form, no submit handlers run
```

**Reference:** `/web/core/lib/Drupal/Core/Form/form.api.php` lines 180-237

### Error Setting Methods

**By Element Name (Preferred):**
```php
$form_state->setErrorByName('field_name', $this->t('Error message'));
```

**By Element Reference:**
```php
$form_state->setError($form['field_name'], $this->t('Error message'));
```

**Error Checking:**
```php
if ($form_state->hasAnyErrors()) { /* ... */ }
$errors = $form_state->getErrors(); // Associative array
$form_state->clearErrors(); // Reset all
```

### Validation Patterns

**Element Validation:**
```
When: Single field format/range check
Where: #element_validate property
Example: Email format, number range, string length
Pattern: Return NULL, errors via setErrorByName()
```

**Form Validation:**
```
When: Cross-field validation, business logic
Where: validateForm() method or #validate array
Example: End date > start date, unique constraint
Pattern: Access multiple fields via getValue()
```

**Typed Config Validation (Drupal 10.2+):**
```
When: ConfigFormBase with schema constraints
Where: Automatic from mymodule.schema.yml
Example: Min/max values, required fields, data types
Pattern: Define constraints in schema, validation automatic
```

**Reference:** [Config Validation](https://www.drupal.org/project/drupal/issues/2971727)

**Common Mistakes:**
- Setting errors in buildForm() (wrong phase)
- Using element validation for cross-field checks (no access to other fields)
- Not translating error messages (use $this->t())
- Forgetting to check for existing errors before setting new ones

**See Also:**
- Form State Methods (dedicated section)
- Typed Data Constraints Guide
- Error Display Theming
