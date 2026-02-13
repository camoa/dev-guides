---
description: Form alter hook system - execution order, alter patterns, and cache contexts
drupal_version: "11.x"
---

# Form Alter System

## When to Use

> Use specific form alter hooks (hook_form_FORM_ID_alter) for performance. Use generic hook_form_alter only when altering multiple forms.

## Decision

| Situation | Hook | Why |
|-----------|------|-----|
| Alter specific form | hook_form_FORM_ID_alter | Performance - runs only for that form |
| Alter base form type | hook_form_BASE_FORM_ID_alter | Shared base (e.g., node_form) |
| Alter multiple forms | hook_form_alter | Generic, runs on every form |
| Alter depends on permissions | Add cache contexts | Vary cache properly |

## Hook Execution Order

```
1. hook_form_alter(&$form, $form_state, $form_id)
   - All modules, all forms

2. hook_form_BASE_FORM_ID_alter(&$form, $form_state, $form_id)
   - Shared base forms (e.g., node_form)

3. hook_form_FORM_ID_alter(&$form, $form_state, $form_id)
   - Specific form

4. Theme alter hooks (after all module hooks)

Module weight controls order within each hook level.
```

## Common Alter Patterns

```php
// Add validation handler
function mymodule_form_user_login_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  $form['#validate'][] = 'mymodule_user_login_validate';
}

// Add submit handler
function mymodule_form_FORM_ID_alter(&$form, FormStateInterface $form_state, $form_id) {
  $form['actions']['submit']['#submit'][] = 'mymodule_custom_submit';
  // OR add to form level
  $form['#submit'][] = 'mymodule_custom_submit';
}

// Modify element
$form['field_name']['#required'] = TRUE;
$form['field_name']['#description'] = t('Updated description');
$form['field_name']['#weight'] = 10;
$form['field_name']['#access'] = FALSE; // Hide field
$form['field_name']['#disabled'] = TRUE; // Disable field

// Remove element
unset($form['field_name']);
// OR hide it
$form['field_name']['#access'] = FALSE;
```

## Add Conditional Field (#states)

```php
$form['custom_value']['#states'] = [
  'visible' => [
    ':input[name="use_custom"]' => ['checked' => TRUE],
  ],
  'required' => [
    ':input[name="use_custom"]' => ['checked' => TRUE],
  ],
];
```

## Cache Context Considerations

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
Forms are cached and reused. Without proper contexts, same form shown to all users even when output should differ by permission/role.

## Debugging

```php
// Display form ID
function mymodule_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  \Drupal::messenger()->addMessage('Form ID: ' . $form_id);
}

// Log form structure
\Drupal::logger('mymodule')->debug('<pre>@form</pre>', [
  '@form' => print_r($form, TRUE),
]);
```

## Best Practices

**DO:**
- Use specific hook (FORM_ID) when possible (performance)
- Add cache contexts when alter varies by context
- Preserve existing handlers unless replacing intentionally
- Use #access instead of unset() (allows other modules to override)

**DON'T:**
- Use generic form_alter for single form (performance hit)
- Remove elements other modules might need
- Replace all submit handlers unless necessary
- Forget cache contexts for conditional alters

## Common Mistakes

- **Wrong**: Not checking element exists before modifying → **Right**: Check with isset()
- **Wrong**: hook_form_alter for single form → **Right**: Use hook_form_FORM_ID_alter
- **Wrong**: Removing handlers other modules added → **Right**: Append/prepend instead
- **Wrong**: No cache contexts for conditional alters → **Right**: Add appropriate contexts

## See Also

- [Form States System](form-states-system.md)
- [Cache API Guide](https://www.drupal.org/docs/drupal-apis/cache-api)
- [Hook System Guide](https://www.drupal.org/docs/drupal-apis/hooks)
- Reference: `/web/core/lib/Drupal/Core/Form/form.api.php` lines 164-322
