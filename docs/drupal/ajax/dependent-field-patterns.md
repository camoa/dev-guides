---
description: Build dependent form fields that update based on parent field value — category/subcategory, country/state patterns
drupal_version: "11.x"
---

# Dependent Field Patterns

## When to Use

> Use dependent fields when form options must change based on the value of another field (category/subcategory, country/state, product type/options).

## Pattern

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['category'] = [
    '#type' => 'select',
    '#title' => t('Category'),
    '#options' => $this->getCategoryOptions(),
    '#empty_option' => t('- Select -'),
    '#ajax' => [
      'callback' => '::updateSubcategory',
      'wrapper' => 'subcategory-wrapper',
    ],
  ];

  $form['subcategory'] = [
    '#type' => 'select',
    '#title' => t('Subcategory'),
    '#prefix' => '<div id="subcategory-wrapper">',
    '#suffix' => '</div>',
    '#options' => [],
    '#validated' => TRUE,  // Prevent validation errors on rebuild
  ];

  // Populate dependent field if parent selected
  $selected_category = $form_state->getValue('category');
  if ($selected_category) {
    $form['subcategory']['#options'] =
      $this->getSubcategoryOptions($selected_category);
  }

  return $form;
}

public function updateSubcategory(array &$form, FormStateInterface $form_state) {
  return $form['subcategory'];
}
```

Reference: `core/modules/system/tests/modules/ajax_forms_test/src/Form/AjaxFormsTestSimpleForm.php`

## Common Mistakes

- **Wrong**: Not setting `#validated => TRUE` → **Right**: Required to prevent validation errors when parent value changes
- **Wrong**: Populating options in callback instead of buildForm → **Right**: Populate options during rebuild in buildForm; callback only returns the element
- **Wrong**: Not checking for NULL values → **Right**: Triggers errors when parent field is cleared; always guard with `if ($selected)`
- **Wrong**: Returning wrong array key → **Right**: Return the exact element that needs updating, not a parent container
- **Wrong**: Missing `#empty_option` on parent → **Right**: Without it, user can't deselect, leaving dependent field with stale options

## See Also

- [Form Element AJAX Configuration](form-element-ajax-configuration.md)
- [Multi-Step Form Workflows](multi-step-form-workflows.md)
- Reference: [Use AJAX with Forms tutorial](https://drupalize.me/tutorial/use-ajax-forms)
