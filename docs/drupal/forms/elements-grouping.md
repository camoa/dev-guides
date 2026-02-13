---
description: Grouping and action elements - containers, fieldsets, buttons for form organization
drupal_version: "11.x"
---

# Form Elements: Grouping and Action Elements

## When to Use

> Use grouping elements to organize form structure and improve UX. Choose containers for AJAX wrappers, fieldsets for visual grouping, details for collapsible sections.

## Decision

| Situation | Element | Why |
|-----------|---------|-----|
| AJAX wrapper target | container | Invisible, structural |
| Related fields grouping | fieldset | Visual border, legend |
| Optional/advanced settings | details | Collapsible, saves space |
| Multiple setting groups | vertical_tabs | Tabbed interface |
| Form action buttons | actions | Standard wrapper, styling |

## Grouping Pattern

```php
// Container (invisible wrapper)
$form['ajax_wrapper'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'ajax-wrapper'], // For AJAX targeting
];

// Fieldset (visible grouping)
$form['contact_info'] = [
  '#type' => 'fieldset',
  '#title' => $this->t('Contact Information'),
];

// Details (collapsible)
$form['advanced'] = [
  '#type' => 'details',
  '#title' => $this->t('Advanced Settings'),
  '#open' => FALSE, // Collapsed by default
];

// Actions container (for buttons)
$form['actions'] = [
  '#type' => 'actions',
];
```

## Button Pattern

```php
// Submit button (primary action)
$form['actions']['submit'] = [
  '#type' => 'submit',
  '#value' => $this->t('Save'),
];

// Custom submit handler
$form['actions']['save_continue'] = [
  '#type' => 'submit',
  '#value' => $this->t('Save and Continue'),
  '#submit' => ['::saveContinue'], // Custom handler
];

// Button with validation control
$form['actions']['previous'] = [
  '#type' => 'submit',
  '#value' => $this->t('Previous'),
  '#limit_validation_errors' => [], // No validation
  '#submit' => ['::previousStep'],
];
```

## Button Handler Priority

```
1. Button #submit handlers (if that button clicked)
2. Form-level #submit handlers
3. Class submitForm() method
```

## Common Mistakes

- **Wrong**: Using button instead of submit → **Right**: Use submit (submits by default)
- **Wrong**: No #limit_validation_errors on "Previous" → **Right**: Skip validation when going back
- **Wrong**: Complex forms without grouping → **Right**: Use fieldset/details for clarity
- **Wrong**: Creating custom buttons for simple submits → **Right**: Use #submit property

## See Also

- [Submission Architecture](submission-architecture.md)
- [Multi-Step Forms](multi-step-forms.md)
- [AJAX Architecture](ajax-architecture.md)
- Reference: `/web/core/lib/Drupal/Core/Render/Element/Actions.php`
