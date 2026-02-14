---
description: Using form elements outside forms as render-only elements -- textfield, select, checkboxes, radios, tableselect.
---

# Form Render Elements

## When to Use

Form elements can be used **outside of forms** as render-only elements when you need their HTML structure but not their input functionality. Inside forms, they become interactive with validation and submission handling.

## Decision: Form Element Context

| Context | Behavior | Example Use |
|---|---|---|
| Inside a form (via FormBuilderInterface) | Full form functionality: validation, submission, CSRF, states | User registration, node edit, admin config |
| Outside a form (in render array) | Renders HTML only, no interactivity | Display-only representation, documentation examples |
| Tableselect pattern | Special hybrid -- table + checkboxes with bulk operations | Views bulk operations, admin lists |

## Common Form Elements (Render-Only)

**Note:** These examples show render-only usage. For full form functionality, use Form API's `buildForm()`.

### textfield

```php
// Render-only (display purposes)
$build['name_display'] = [
  '#type' => 'textfield',
  '#title' => $this->t('Username'),
  '#value' => 'example_user',
  '#disabled' => TRUE,
  '#attributes' => ['readonly' => 'readonly'],
];
```

**Properties:** `#title`, `#default_value`, `#size`, `#maxlength`, `#placeholder`, `#required`, `#disabled`

---

### select

```php
// Render-only dropdown
$build['role_display'] = [
  '#type' => 'select',
  '#title' => $this->t('User Role'),
  '#options' => [
    'admin' => $this->t('Administrator'),
    'editor' => $this->t('Editor'),
    'viewer' => $this->t('Viewer'),
  ],
  '#value' => 'editor',
  '#disabled' => TRUE,
];
```

**Properties:** `#options` (required), `#empty_option`, `#empty_value`, `#multiple`

---

### checkbox / checkboxes

```php
// Single checkbox
$build['agree_display'] = [
  '#type' => 'checkbox',
  '#title' => $this->t('I agree'),
  '#return_value' => '1',
  '#disabled' => TRUE,
];

// Multiple checkboxes
$build['permissions'] = [
  '#type' => 'checkboxes',
  '#title' => $this->t('Permissions'),
  '#options' => [
    'create' => $this->t('Create content'),
    'edit' => $this->t('Edit content'),
    'delete' => $this->t('Delete content'),
  ],
  '#default_value' => ['create', 'edit'],
  '#disabled' => TRUE,
];
```

---

### radios

```php
$build['choice'] = [
  '#type' => 'radios',
  '#title' => $this->t('Select One'),
  '#options' => ['yes' => $this->t('Yes'), 'no' => $this->t('No')],
  '#default_value' => 'yes',
  '#disabled' => TRUE,
];
```

## Pattern: Table with Form Elements (Tableselect)

```php
// Inside a form
$form['users'] = [
  '#type' => 'tableselect',
  '#header' => [
    'name' => $this->t('Name'),
    'role' => $this->t('Role'),
  ],
  '#options' => [
    1 => ['name' => 'Alice', 'role' => 'Admin'],
    2 => ['name' => 'Bob', 'role' => 'Editor'],
  ],
  '#empty' => $this->t('No users found.'),
];
```

**Reference:** `core/lib/Drupal/Core/Render/Element/Tableselect.php`

## Common Mistakes

- **Using form elements outside forms and expecting them to work** -- They render HTML but won't process submissions
- **Forgetting `#disabled => TRUE` in render-only context** -- User might think they can interact with it
- **Not setting `#default_value` or `#value`** -- Elements render empty even in display mode
- **Mixing `#value` and `#default_value`** -- Use `#default_value` in forms, `#value` for render-only

## See Also

- [Core Render Elements](core-render-elements.md) for non-form elements
- Reference: Drupal Form API Guide (separate guide)
- Reference: [Form Render Elements](https://www.drupal.org/docs/drupal-apis/form-api/form-render-elements)
