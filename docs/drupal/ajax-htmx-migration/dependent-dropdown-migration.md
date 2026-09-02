---
description: "Dependent Dropdown Migration — migrate a parent select that dynamically updates a child select's options"
tldr: "Migrate a parent select that updates a child select's options on change. Delete the AJAX callback method entirely — HTMX rebuilds the form in buildForm() and getHtmxTriggerName() replaces isRebuilding()."
drupal_version: "11.x"
---

# Dependent Dropdown Migration

## When to Use

> Migrate a parent select element that dynamically updates a child select element's options based on the parent's value. The most common AJAX pattern in Drupal forms.

## Steps

1. **Remove `#ajax` property from parent select** — Replace with `Htmx` configuration
2. **Configure HTMX targeting** — Point to child wrapper using CSS selector
3. **Move callback logic into buildForm()** — Check `getHtmxTriggerName()` to detect trigger
4. **Remove callback method** — No longer needed with HTMX

## BEFORE: AJAX

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['category'] = [
    '#type' => 'select',
    '#title' => t('Category'),
    '#options' => $this->getCategoryOptions(),
    '#empty_option' => t('- Select -'),
    '#ajax' => [
      'callback' => '::categoryCallback',
      'wrapper' => 'subcategory-wrapper',
      'event' => 'change',
    ],
  ];

  $form['subcategory'] = [
    '#type' => 'select',
    '#title' => t('Subcategory'),
    '#options' => [],
    '#prefix' => '<div id="subcategory-wrapper">',
    '#suffix' => '</div>',
  ];

  $selected = $form_state->getValue('category');
  if ($selected) {
    $form['subcategory']['#options'] = $this->getSubcategoryOptions($selected);
  }

  return $form;
}

public function categoryCallback(array &$form, FormStateInterface $form_state) {
  return $form['subcategory'];
}
```

## AFTER: HTMX

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

public function buildForm(array $form, FormStateInterface $form_state) {
  $form_url = Url::fromRoute('<current>');

  $form['category'] = [
    '#type' => 'select',
    '#title' => t('Category'),
    '#options' => $this->getCategoryOptions(),
    '#empty_option' => t('- Select -'),
  ];

  // Configure HTMX on the category element
  (new Htmx())
    ->post($form_url)
    ->onlyMainContent()
    ->select('#edit-subcategory--wrapper')
    ->target('#edit-subcategory--wrapper')
    ->swap('outerHTML')
    ->applyTo($form['category']);

  $form['subcategory'] = [
    '#type' => 'select',
    '#title' => t('Subcategory'),
    '#options' => [],
  ];

  // Check for HTMX trigger or existing value
  $trigger = $this->getHtmxTriggerName();
  if ($trigger === 'category' || $form_state->getValue('category')) {
    $selected = $form_state->getValue('category');
    $form['subcategory']['#options'] = $this->getSubcategoryOptions($selected);
  }

  return $form;
}

// No callback method needed!
```

Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php` lines 100-120

## Common Mistakes

- **Keeping the callback method** → Delete it. HTMX rebuilds the form directly in `buildForm()`, there's no callback execution
- **Using `$form_state->isRebuilding()`** → Use `$this->getHtmxTriggerName()` instead. It tells you which specific element triggered the HTMX request
- **Forgetting wrapper element** → The child select needs a wrapper element with an ID. Use `'#wrapper_attributes' => ['id' => 'subcategory-wrapper']` instead of prefix/suffix
- **Not using `onlyMainContent()`** → Without this, HTMX receives the full HTML page. Use `onlyMainContent()` to get just the form content
- **Wrong selector syntax** → Use `'#edit-subcategory--wrapper'` (double dash) for form element wrappers. Drupal auto-generates these IDs

## See Also

- Previous: [AJAX Command to HTMX Equivalents](ajax-command-to-htmx-equivalents.md)
- Next: [Cascading Selects with URL Migration](cascading-selects-with-url-migration.md) — Multiple dependent selects
- Reference: `HtmxRequestInfoTrait::getHtmxTriggerName()` at `/core/lib/Drupal/Core/Htmx/HtmxRequestInfoTrait.php`
