---
description: "Proven HTMX patterns for Drupal — load more, infinite scroll, modals, real-time polling, and live search"
tldr: "Reference this for proven HTMX implementations of common UI patterns: load more (swap beforeend + select), infinite scroll (trigger revealed), modals, polling (trigger every Ns), and debounced live search."
drupal_version: "11.x"
---

# Production Patterns

## When to Use

> You need proven patterns for common HTMX use cases: load more, modals, infinite scroll, real-time updates.

## Pattern: Load More / Pagination

Append new content to existing list:

```php
// Controller
public function loadMore(int $page = 0) {
  $items = $this->getItems($page);

  $build['items'] = [
    '#theme' => 'item_list',
    '#items' => $items,
  ];

  if ($this->hasMoreItems($page)) {
    $build['load_more'] = [
      '#type' => 'html_tag',
      '#tag' => 'button',
      '#value' => 'Load More',
    ];

    (new Htmx())
      ->get(Url::fromRoute('my.load_more', ['page' => $page + 1]))
      ->target('#items-container')
      ->swap('beforeend')              // Append to container
      ->select('#items-container > *') // Extract only new items
      ->applyTo($build['load_more']);
  }

  return $build;
}
```

## Pattern: Infinite Scroll

Trigger on scroll reveal:

```php
$build['sentinel'] = [
  '#type' => 'html_tag',
  '#tag' => 'div',
  '#attributes' => ['id' => 'scroll-sentinel'],
];

(new Htmx())
  ->get(Url::fromRoute('my.load_more', ['page' => $page + 1]))
  ->trigger('revealed')              // Fire when scrolled into view
  ->target('#items-container')
  ->swap('beforeend')
  ->select('#items-container > *')
  ->applyTo($build['sentinel']);
```

## Pattern: Modal/Dialog Content

Load content into dialog on demand:

```php
// Button that opens modal
$build['open_modal'] = [
  '#type' => 'html_tag',
  '#tag' => 'button',
  '#value' => 'Open Details',
];

(new Htmx())
  ->get(Url::fromRoute('my.modal_content', ['id' => $entity_id]))
  ->target('#modal-content')
  ->swap('innerHTML')
  ->onlyMainContent()
  ->applyTo($build['open_modal']);

// Modal container (already on page)
$build['modal'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'modal-content', 'class' => ['modal']],
];
```

## Pattern: Real-Time Updates (Polling)

Poll for updates at intervals:

```php
$build['status'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'status-display'],
  '#markup' => $this->getCurrentStatus(),
];

(new Htmx())
  ->get(Url::fromRoute('my.status'))
  ->trigger('every 5s')              // Poll every 5 seconds
  ->target('#status-display')
  ->swap('outerHTML')
  ->onlyMainContent()
  ->applyTo($build['status']);
```

## Pattern: Form with Live Search

Update results as user types:

```php
$form['search'] = [
  '#type' => 'textfield',
  '#title' => 'Search',
];

(new Htmx())
  ->get(Url::fromRoute('my.search'))
  ->trigger('keyup changed delay:500ms')  // Debounce typing
  ->target('#search-results')
  ->swap('innerHTML')
  ->include('[name="search"]')            // Include search field value
  ->indicator('#spinner')                 // Show loading indicator
  ->onlyMainContent()
  ->applyTo($form['search']);

$form['results'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'search-results'],
  '#markup' => $this->getSearchResults($search_term),
];
```

## Common Mistakes

- Not using `swap('beforeend')` for append operations — `innerHTML` replaces instead of appending
- Forgetting `select()` for load more — Entire response (including button) gets appended
- Not debouncing live search — Creates too many requests while typing
- Using polling without considering server load — Combine with cache strategy
- Not providing loading indicators — Users don't know request is in progress

## See Also

- Previous: [Asset Loading](asset-loading.md)
- Next: [Complete Production Example](production-example-config-export.md)
- Reference: [HTMX Examples](https://htmx.org/examples/)
