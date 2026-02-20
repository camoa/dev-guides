---
description: Migrate a parent select that updates child select options — the most common Drupal AJAX pattern
drupal_version: "11.x"
---

# Dependent Dropdown Migration

## When to Use

> Use this when migrating a parent select element that dynamically updates a child select element's options based on the parent's value.

## Decision

| Step | Action |
|---|---|
| 1 | Remove `#ajax` property from parent select |
| 2 | Configure `Htmx` targeting the child wrapper via CSS selector |
| 3 | Move callback logic into `buildForm()`, check `getHtmxTriggerName()` |
| 4 | Delete the callback method — it is no longer needed |

## Pattern

**BEFORE:**
```php
$form['category'] = [
  '#type' => 'select',
  '#ajax' => [
    'callback' => '::categoryCallback',
    'wrapper' => 'subcategory-wrapper',
    'event' => 'change',
  ],
];
$form['subcategory'] = [
  '#type' => 'select',
  '#prefix' => '<div id="subcategory-wrapper">',
  '#suffix' => '</div>',
];
public function categoryCallback(array &$form, FormStateInterface $form_state) {
  return $form['subcategory'];
}
```

**AFTER:**
```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$form['category'] = ['#type' => 'select', '#options' => $this->getCategoryOptions()];

(new Htmx())
  ->post(Url::fromRoute('<current>'))
  ->onlyMainContent()
  ->select('#edit-subcategory--wrapper')
  ->target('#edit-subcategory--wrapper')
  ->swap('outerHTML')
  ->applyTo($form['category']);

$form['subcategory'] = ['#type' => 'select', '#options' => []];

$trigger = $this->getHtmxTriggerName();
if ($trigger === 'category' || $form_state->getValue('category')) {
  $selected = $form_state->getValue('category');
  $form['subcategory']['#options'] = $this->getSubcategoryOptions($selected);
}
// No callback method needed
```

## Common Mistakes

- **Keeping the callback method** → Delete it. HTMX rebuilds the form directly in `buildForm()`, no callback executes
- **Using `$form_state->isRebuilding()`** → Use `$this->getHtmxTriggerName()` instead — it identifies which element triggered the request
- **Forgetting wrapper element** → Use `'#wrapper_attributes' => ['id' => 'subcategory-wrapper']` instead of `#prefix`/`#suffix`
- **Not using `onlyMainContent()`** → Without this, HTMX receives the full HTML page
- **Wrong selector syntax** → Use `'#edit-subcategory--wrapper'` (double dash) for Drupal auto-generated form element wrappers

## See Also

- Previous: [AJAX Command to HTMX Equivalents](ajax-command-to-htmx-equivalents.md)
- Next: [Cascading Selects with URL Migration](cascading-selects-with-url-migration.md)
- Source: `/core/modules/config/src/Form/ConfigSingleExportForm.php` lines 100–120
- Reference: `HtmxRequestInfoTrait::getHtmxTriggerName()` at `/core/lib/Drupal/Core/Htmx/HtmxRequestInfoTrait.php`
