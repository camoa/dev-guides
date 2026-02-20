---
description: Migrate Add Another button patterns — use vals() to pass incremented count instead of form state storage
drupal_version: "11.x"
---

# Dynamic Field Addition Migration

## When to Use

> Use this when migrating "Add Another" patterns where clicking a button adds a new form field to the form — multi-value fields and repeating field groups.

## Decision

| Step | Action |
|---|---|
| 1 | Replace form state count storage with a hidden field |
| 2 | Replace `#ajax` button with `html_tag` button + `Htmx` |
| 3 | Use `vals()` to send the incremented count with the HTMX request |
| 4 | Target the items container wrapper |
| 5 | Delete the submit handler — increment is in `vals()` |

## Pattern

**BEFORE:**
```php
$item_count = $form_state->get('item_count') ?: 1;
$form['add_item'] = [
  '#type' => 'submit',
  '#value' => t('Add Item'),
  '#submit' => ['::addItem'],
  '#ajax' => ['callback' => '::itemsCallback', 'wrapper' => 'items-wrapper'],
];
public function addItem(&$form, $form_state) {
  $form_state->set('item_count', $form_state->get('item_count') + 1);
  $form_state->setRebuild();
}
```

**AFTER:**
```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$item_count = $form_state->getValue('item_count', 1);

$form['item_count'] = ['#type' => 'hidden', '#value' => $item_count];
$form['items'] = ['#type' => 'container', '#tree' => TRUE, '#attributes' => ['id' => 'items-wrapper']];

for ($i = 0; $i < $item_count; $i++) {
  $form['items'][$i] = ['#type' => 'textfield', '#title' => t('Item @num', ['@num' => $i + 1])];
}

$form['add_item'] = ['#type' => 'html_tag', '#tag' => 'button', '#value' => t('Add Item'), '#attributes' => ['type' => 'button']];

(new Htmx())
  ->post(Url::fromRoute('<current>'))
  ->onlyMainContent()
  ->vals(['item_count' => $item_count + 1])
  ->select('#items-wrapper')
  ->target('#items-wrapper')
  ->swap('outerHTML')
  ->applyTo($form['add_item']);
```

## Common Mistakes

- **Storing count in form state** → Use hidden field instead. HTMX submissions do not preserve form state like AJAX callbacks do
- **Not using `vals()`** → You must send the incremented count with the HTMX request using `vals(['field' => 'value'])`
- **Adding `setRebuild()`** → Not needed with HTMX. The form rebuilds automatically when it processes the new hidden field value
- **Using submit handler** → Delete it. The increment logic is in the `vals()` call and `buildForm()` reads the hidden field
- **Not handling removal** → For "Remove" buttons, use the same `vals()` pattern passing the item index to remove

## See Also

- Previous: [Infinite Scroll Migration](infinite-scroll-migration.md)
- Next: [JavaScript Event Migration](javascript-event-migration.md)
- Reference: `Htmx::vals()` for sending additional request data at `/core/lib/Drupal/Core/Htmx/Htmx.php`
