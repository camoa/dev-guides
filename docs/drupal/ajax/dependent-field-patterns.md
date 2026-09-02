---
description: Build dependent form fields that update based on parent field value — category/subcategory, country/state patterns
tldr: "Use dependent fields when form options must change based on the value of another field (category/subcategory, country/state, product type/options)."
drupal_version: "11.x"
---

# Dependent Field Patterns

## When to Use

You need form fields that update based on the value of other fields (category/subcategory, country/state, product type/options).

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

- Not setting `#validated => TRUE` → Causes validation errors when parent value changes
- Populating options in callback instead of buildForm() → Options populate on rebuild, callback only returns element
- Not checking for NULL values → Triggers errors when parent field is cleared
- Returning wrong array key → Return the exact element that needs updating, not parent container
- Missing `#empty_option` on parent field → User can't deselect, dependent field stays populated with stale options

## See Also

- ← Previous: [Form Element AJAX Configuration](form-element-ajax-configuration.md) | Next: [Multi-Step Form Workflows](multi-step-form-workflows.md)
- Reference: [Use AJAX with Forms tutorial](https://drupalize.me/tutorial/use-ajax-forms)
