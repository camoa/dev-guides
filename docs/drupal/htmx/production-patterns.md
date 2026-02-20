---
description: Proven HTMX patterns for Drupal — load more, infinite scroll, modals, real-time polling, and live search
drupal_version: "11.x"
---

# Production Patterns

## When to Use

> Reference this for proven HTMX implementations of common UI patterns: load more, infinite scroll, modals, real-time updates, and live search.

## Decision

| Pattern | Key attributes | Notes |
|---------|---------------|-------|
| Load more | `swap('beforeend')`, `select()` | `select()` prevents button from being appended |
| Infinite scroll | `trigger('revealed')` | Fires when element scrolls into view |
| Modal content | `target('#modal')`, `swap('innerHTML')` | Modal container must already exist on page |
| Real-time polling | `trigger('every 5s')` | Combine with caching to reduce server load |
| Live search | `trigger('keyup changed delay:500ms')` | Debounce prevents requests on every keystroke |

## Pattern

**Load more / pagination:**

```php
(new Htmx())
  ->get(Url::fromRoute('my.load_more', ['page' => $page + 1]))
  ->target('#items-container')
  ->swap('beforeend')
  ->select('#items-container > *')
  ->applyTo($build['load_more']);
```

**Infinite scroll:**

```php
$build['sentinel'] = ['#type' => 'html_tag', '#tag' => 'div'];
(new Htmx())
  ->get(Url::fromRoute('my.load_more', ['page' => $page + 1]))
  ->trigger('revealed')
  ->target('#items-container')
  ->swap('beforeend')
  ->select('#items-container > *')
  ->applyTo($build['sentinel']);
```

**Modal content on demand:**

```php
(new Htmx())
  ->get(Url::fromRoute('my.modal_content', ['id' => $entity_id]))
  ->target('#modal-content')
  ->swap('innerHTML')
  ->onlyMainContent()
  ->applyTo($build['open_modal']);
```

**Real-time polling:**

```php
(new Htmx())
  ->get(Url::fromRoute('my.status'))
  ->trigger('every 5s')
  ->target('#status-display')
  ->swap('outerHTML')
  ->onlyMainContent()
  ->applyTo($build['status']);
```

**Live search with debounce:**

```php
(new Htmx())
  ->get(Url::fromRoute('my.search'))
  ->trigger('keyup changed delay:500ms')
  ->target('#search-results')
  ->swap('innerHTML')
  ->include('[name="search"]')
  ->indicator('#spinner')
  ->onlyMainContent()
  ->applyTo($form['search']);
```

## Common Mistakes

- **Wrong**: Not using `swap('beforeend')` for append operations → **Right**: `innerHTML` replaces instead of appending
- **Wrong**: Forgetting `select()` for load more → **Right**: Entire response (including the button) gets appended
- **Wrong**: Not debouncing live search → **Right**: Creates too many requests while typing
- **Wrong**: Using polling without considering server load → **Right**: Combine with cache strategy
- **Wrong**: Not providing loading indicators → **Right**: Users don't know request is in progress

## See Also

- [Asset Loading](asset-loading.md)
- [Production Example: ConfigSingleExportForm](production-example-config-export.md)
- Reference: [HTMX Examples](https://htmx.org/examples/)
