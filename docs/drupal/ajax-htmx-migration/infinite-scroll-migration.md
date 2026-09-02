---
description: "Infinite Scroll Migration — migrate Load More buttons and scroll-triggered pagination that append content to a list"
tldr: "Migrate Load More / infinite-scroll patterns. Button-triggered loading uses swap('beforeend') on click; scroll-triggered loading adds a sentinel element with trigger('revealed') that fires when it enters the viewport."
drupal_version: "11.x"
---

# Infinite Scroll Migration

## When to Use

> Migrate "Load More" buttons or infinite scroll patterns that append new content to a list. Common in content listings, search results, and feeds.

## Steps

1. **Use route parameter for page number** — Track pagination state
2. **Replace `#ajax` button with HTMX button** — Configure to append content
3. **Use `swap('beforeend')` for appending** — Add new items to list
4. **For scroll-triggered loading** — Use sentinel element with `trigger('revealed')`
5. **Update button to point to next page** — Increment page parameter

## BEFORE: AJAX

```php
$form['load_more'] = [
  '#type' => 'button',
  '#value' => t('Load More'),
  '#ajax' => [
    'callback' => '::loadMoreCallback',
    'wrapper' => 'content-list',
    'method' => 'append',
  ],
];

$form['content_list'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'content-list'],
];

public function loadMoreCallback(array &$form, FormStateInterface $form_state) {
  $page = $form_state->get('page') + 1;
  $form_state->set('page', $page);

  $items = $this->loadItems($page);

  return [
    '#theme' => 'item_list',
    '#items' => $items,
  ];
}
```

## AFTER: HTMX (Button-Triggered)

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$page = $form_state->getValue('page', 0);
$nextPage = $page + 1;

$form['load_more'] = [
  '#type' => 'html_tag',
  '#tag' => 'button',
  '#value' => t('Load More'),
  '#attributes' => ['type' => 'button'],
];

(new Htmx())
  ->get(Url::fromRoute('my_module.load_items', ['page' => $nextPage]))
  ->onlyMainContent()
  ->select('.item-list')
  ->target('#content-list')
  ->swap('beforeend')  // Append to end of container
  ->applyTo($form['load_more']);

$form['content_list'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'content-list'],
  'items' => [
    '#theme' => 'item_list',
    '#items' => $this->loadItems($page),
    '#attributes' => ['class' => ['item-list']],
  ],
];
```

## AFTER: HTMX (Scroll-Triggered)

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$page = $form_state->getValue('page', 0);
$nextPage = $page + 1;

$form['content_list'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'content-list'],
  'items' => [
    '#theme' => 'item_list',
    '#items' => $this->loadItems($page),
    '#attributes' => ['class' => ['item-list']],
  ],
];

// Sentinel element at bottom of list triggers load when visible
$form['sentinel'] = [
  '#type' => 'html_tag',
  '#tag' => 'div',
  '#attributes' => ['id' => 'load-sentinel'],
  '#value' => '', // Can add loading indicator
];

(new Htmx())
  ->get(Url::fromRoute('my_module.load_items', ['page' => $nextPage]))
  ->trigger('revealed')  // Trigger when element enters viewport
  ->onlyMainContent()
  ->select('.item-list')
  ->target('#content-list')
  ->swap('beforeend')
  ->applyTo($form['sentinel']);
```

Reference: HTMX `revealed` trigger and swap strategies

## Common Mistakes

- **Using `'method' => 'append'`** → HTMX uses `swap('beforeend')` to append content inside an element
- **Storing page in form state** → Use route parameter for the load endpoint: `Url::fromRoute('my_module.load', ['page' => $page])`
- **Not using `revealed` trigger for infinite scroll** → The `trigger('revealed')` fires when element enters viewport, perfect for scroll-triggered loading
- **Updating the wrong element** → `target()` should point to the list container, `select()` should extract just the new items from response
- **Not hiding sentinel after last page** → Check if more items exist and conditionally include the sentinel element

## See Also

- Previous: [Real-Time Validation Migration](real-time-validation-migration.md)
- Next: [Dynamic Field Addition Migration](dynamic-field-addition-migration.md)
- Reference: HTMX `revealed` trigger in HTMX documentation
