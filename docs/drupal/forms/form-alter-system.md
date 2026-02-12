---
description: Form alter system — hook order, alter patterns, cache contexts
drupal_version: "11.x"
---

# Form Alter System

### Hook Implementation Order

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

**Reference:** `/web/core/lib/Drupal/Core/Form/form.api.php` lines 164-322

### Common Alter Patterns

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

**Remove Element:**
```php
unset($form['field_name']);

// OR hide it
$form['field_name']['#access'] = FALSE;
```

### Advanced Alter Patterns

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

**Change Button Text:**
```php
$form['actions']['submit']['#value'] = t('Custom Text');
$form['actions']['delete']['#value'] = t('Remove');
```

**Add Custom Button:**
```php
$form['actions']['custom'] = [
  '#type' => 'submit',
  '#value' => t('Custom Action'),
  '#submit' => ['mymodule_custom_action_submit'],
  '#weight' => 10,
];
```

### Cache Context Considerations

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

### Debugging Form Alters

**Display Form ID:**
```php
function mymodule_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  \Drupal::messenger()->addMessage('Form ID: ' . $form_id);
}
```

**Log Form Structure:**
```php
\Drupal::logger('mymodule')->debug('<pre>@form</pre>', [
  '@form' => print_r($form, TRUE),
]);
```

**Check Execution Order:**
```php
\Drupal::logger('mymodule')->debug('Form alter running for: @id', [
  '@id' => $form_id,
]);
```

### Best Practices

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

**Common Mistakes:**
- Not checking if element exists before modifying
- Using form_alter for all forms (performance)
- Removing handlers other modules added
- Not testing alter execution order with multiple modules

**See Also:**
- Hook System Guide
- Cache API Guide
- Form States System (next section)
- Official: [Form API Hooks](https://www.drupal.org/docs/drupal-apis/form-api/introduction-to-form-api)
