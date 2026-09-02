---
description: "Dynamic Field Addition Migration — migrate Add Another patterns that add a new form field on click"
tldr: "Migrate Add Another patterns for repeating fields. HTMX submissions don't preserve form state like AJAX callbacks — track the count in a hidden field and send the incremented value with vals()."
drupal_version: "11.x"
---

# Dynamic Field Addition Migration

## When to Use

> Migrate "Add Another" patterns where clicking a button adds a new form field (textfield, fieldset, etc.) to the form. Common in multi-value fields and repeating field groups.

## Steps

1. **Track count in hidden field** — Replace form state storage with hidden field
2. **Replace `#ajax` button with HTMX button** — Configure to reload field container
3. **Use `vals()` to send incremented count** — Pass new count with HTMX request
4. **Update container wrapper** — Target the container holding all fields
5. **Remove submit handler** — Logic moves to buildForm()

## BEFORE: AJAX

```php
$form['items'] = [
  '#type' => 'container',
  '#tree' => TRUE,
  '#prefix' => '<div id="items-wrapper">',
  '#suffix' => '</div>',
];

$item_count = $form_state->get('item_count') ?: 1;

for ($i = 0; $i < $item_count; $i++) {
  $form['items'][$i] = [
    '#type' => 'textfield',
    '#title' => t('Item @num', ['@num' => $i + 1]),
  ];
}

$form['add_item'] = [
  '#type' => 'submit',
  '#value' => t('Add Item'),
  '#submit' => ['::addItem'],
  '#ajax' => [
    'callback' => '::itemsCallback',
    'wrapper' => 'items-wrapper',
  ],
];

public function addItem(array &$form, FormStateInterface $form_state) {
  $count = $form_state->get('item_count') ?: 1;
  $form_state->set('item_count', $count + 1);
  $form_state->setRebuild();
}

public function itemsCallback(array &$form, FormStateInterface $form_state) {
  return $form['items'];
}
```

## AFTER: HTMX

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$form['items'] = [
  '#type' => 'container',
  '#tree' => TRUE,
  '#attributes' => ['id' => 'items-wrapper'],
];

// Get item count from form state or input
$item_count = $form_state->getValue('item_count', 1);

$form['item_count'] = [
  '#type' => 'hidden',
  '#value' => $item_count,
];

for ($i = 0; $i < $item_count; $i++) {
  $form['items'][$i] = [
    '#type' => 'textfield',
    '#title' => t('Item @num', ['@num' => $i + 1]),
  ];
}

$form['add_item'] = [
  '#type' => 'html_tag',
  '#tag' => 'button',
  '#value' => t('Add Item'),
  '#attributes' => ['type' => 'button'],
];

// Send incremented count with request
(new Htmx())
  ->post(Url::fromRoute('<current>'))
  ->onlyMainContent()
  ->vals(['item_count' => $item_count + 1])
  ->select('#items-wrapper')
  ->target('#items-wrapper')
  ->swap('outerHTML')
  ->applyTo($form['add_item']);
```

Reference: `Htmx::vals()` method for sending additional values

## Common Mistakes

- **Storing count in form state** → Use hidden field instead. HTMX submissions don't preserve form state like AJAX callbacks do
- **Not using `vals()`** → You need to send the incremented count with the HTMX request using `vals(['field' => 'value'])`
- **Forgetting to rebuild** → Actually not needed with HTMX. The form rebuilds automatically when it processes the new hidden field value
- **Using submit handler** → Delete it. The increment logic is in the `vals()` call, and buildForm() uses that value
- **Not handling removal** → For "Remove" buttons, use similar pattern with `vals()` passing which item index to remove

## See Also

- Previous: [Infinite Scroll Migration](infinite-scroll-migration.md)
- Next: [JavaScript Event Migration](javascript-event-migration.md)
- Reference: `Htmx::vals()` for sending additional request data
