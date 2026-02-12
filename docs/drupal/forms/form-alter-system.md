---
description: Form alter system — hook order, alter patterns, cache contexts
drupal_version: "11.x"
---

# Form Alter System

## When to Use

> Use specific hook (FORM_ID) when possible. Add cache contexts when alter varies by context. Use #access instead of unset().

## Decision

| Situation | Hook | Why |
|-----------|------|-----|
| Specific form | `hook_form_FORM_ID_alter()` | Performance |
| Base form (e.g., node_form) | `hook_form_BASE_FORM_ID_alter()` | Shared forms |
| All forms | `hook_form_alter()` | Global changes |

## Hook Implementation Order

**Execution Sequence:**
```
1. hook_form_alter(&$form, $form_state, $form_id)
   - All modules, all forms

2. hook_form_BASE_FORM_ID_alter(&$form, $form_state, $form_id)
   - Shared base forms (e.g., node_form)

3. hook_form_FORM_ID_alter(&$form, $form_state, $form_id)
   - Specific form

4. Theme alter hooks (after all module hooks)
```

**Module Weight:**
```
Modules run by:
1. Module weight (system table)
2. Alphabetically by module name
Lower weight = runs first
```

Reference: `/web/core/lib/Drupal/Core/Form/form.api.php` lines 164-322

## Common Alter Patterns

**Add Validation Handler:**
```php
function mymodule_form_user_login_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  $form['#validate'][] = 'mymodule_user_login_validate';
}

function mymodule_user_login_validate(array &$form, FormStateInterface $form_state) {
  // Custom validation logic
}
```

**Add Submit Handler:**
```php
$form['actions']['submit']['#submit'][] = 'mymodule_custom_submit';

// OR add to form level
$form['#submit'][] = 'mymodule_custom_submit';
```

**Modify Element:**
```php
// Change required status
$form['field_name']['#required'] = TRUE;

// Update description
$form['field_name']['#description'] = t('Updated description');

// Change weight
$form['field_name']['#weight'] = 10;

// Hide field
$form['field_name']['#access'] = FALSE;

// Disable field
$form['field_name']['#disabled'] = TRUE;
```

## Advanced Alter Patterns

**Add Conditional Field (#states):**
```php
$form['field_name']['#states'] = [
  'visible' => [
    ':input[name="trigger"]' => ['checked' => TRUE],
  ],
  'required' => [
    ':input[name="trigger"]' => ['checked' => TRUE],
  ],
];
```

**Modify Button Submit Handlers:**
```php
// Replace handlers
$form['actions']['submit']['#submit'] = ['mymodule_custom_submit'];

// Prepend handler (run first)
array_unshift($form['#submit'], 'mymodule_first_submit');

// Append handler (run last)
$form['#submit'][] = 'mymodule_last_submit';
```

## Cache Context Considerations

**Add Cache Dependencies:**
```php
// When alter depends on user permissions
$form['#cache']['contexts'][] = 'user.permissions';

// When alter depends on config
$form['#cache']['tags'][] = 'config:mymodule.settings';

// When alter depends on current user
$form['#cache']['contexts'][] = 'user';

// When alter depends on URL
$form['#cache']['contexts'][] = 'url.path';
```

**Why Cache Contexts Matter:**
```
Forms are cached and reused
Without proper contexts: same form for all users
Add context when alter output varies by:
- User permissions
- User role
- Configuration
- URL parameters
```

## Best Practices

**DO:**
- Use specific hook (FORM_ID) when possible (performance)
- Add cache contexts when alter varies by context
- Preserve existing handlers unless replacing intentionally
- Use #access instead of unset() (allows other modules to override)

**DON'T:**
- Alter forms in .module file without hook
- Remove elements other modules might need
- Replace all submit handlers unless necessary
- Forget cache contexts for conditional alters

## Common Mistakes

- **Wrong**: Not checking if element exists before modifying → **Right**: Use `isset($form['field'])`
- **Wrong**: Using form_alter for all forms (performance) → **Right**: Use specific hook
- **Wrong**: Removing handlers other modules added → **Right**: Append/prepend, don't replace
- **Wrong**: Not testing alter execution order with multiple modules → **Right**: Test with dependencies

## See Also

- [Form States System](form-states-system.md)
- [Cache API](https://www.drupal.org/docs/drupal-apis/cache-api)
- Documentation: [Form API Hooks](https://www.drupal.org/docs/drupal-apis/form-api/introduction-to-form-api)
- Reference: `/web/core/lib/Drupal/Core/Form/form.api.php`
