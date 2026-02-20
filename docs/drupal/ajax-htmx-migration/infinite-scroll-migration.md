---
description: Migrate Load More buttons and infinite scroll patterns — append content using swap beforeend and the revealed trigger
drupal_version: "11.x"
---

# Infinite Scroll Migration

## When to Use

> Use this when migrating "Load More" buttons or infinite scroll patterns that append new content to a list — content listings, search results, and feeds.

## Decision

| Trigger type | HTMX approach | Use when |
|---|---|---|
| Button click | `swap('beforeend')` on button | User controls when to load more |
| Scroll-triggered | `trigger('revealed')` on sentinel element | Automatic infinite scroll |

## Pattern

**BEFORE:**
```php
$form['load_more'] = [
  '#type' => 'button',
  '#value' => t('Load More'),
  '#ajax' => ['callback' => '::loadMoreCallback', 'wrapper' => 'content-list', 'method' => 'append'],
];
```

**AFTER — Button-triggered:**
```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$nextPage = $form_state->getValue('page', 0) + 1;

$form['load_more'] = ['#type' => 'html_tag', '#tag' => 'button', '#value' => t('Load More'), '#attributes' => ['type' => 'button']];

(new Htmx())
  ->get(Url::fromRoute('my_module.load_items', ['page' => $nextPage]))
  ->onlyMainContent()
  ->select('.item-list')
  ->target('#content-list')
  ->swap('beforeend')
  ->applyTo($form['load_more']);

$form['content_list'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'content-list'],
  'items' => ['#theme' => 'item_list', '#items' => $this->loadItems(0), '#attributes' => ['class' => ['item-list']]],
];
```

**AFTER — Scroll-triggered:**
```php
// Sentinel element at bottom fires when it enters viewport
$form['sentinel'] = ['#type' => 'html_tag', '#tag' => 'div', '#attributes' => ['id' => 'load-sentinel'], '#value' => ''];

(new Htmx())
  ->get(Url::fromRoute('my_module.load_items', ['page' => $nextPage]))
  ->trigger('revealed')
  ->onlyMainContent()
  ->select('.item-list')
  ->target('#content-list')
  ->swap('beforeend')
  ->applyTo($form['sentinel']);
```

## Common Mistakes

- **Using `'method' => 'append'`** → HTMX uses `swap('beforeend')` to append content inside an element
- **Storing page in form state** → Use route parameter for the load endpoint: `Url::fromRoute('my_module.load', ['page' => $page])`
- **Not using `revealed` trigger for infinite scroll** → `trigger('revealed')` fires when element enters viewport — the correct approach for scroll-triggered loading
- **Updating the wrong element** → `target()` points to the list container; `select()` extracts just the new items from the response
- **Not hiding sentinel after last page** → Check if more items exist and conditionally include the sentinel element

## See Also

- Previous: [Real-Time Validation Migration](real-time-validation-migration.md)
- Next: [Dynamic Field Addition Migration](dynamic-field-addition-migration.md)
- Reference: HTMX `revealed` trigger in [HTMX documentation](https://htmx.org/docs/#special-events)
