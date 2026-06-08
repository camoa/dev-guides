---
description: Complete HTMX attribute reference for Drupal — request, content, trigger, history, and OOB attributes via the Htmx class
tldr: "Reference this when configuring how HTMX elements make requests, where content goes, and how it swaps. The `Htmx` class provides 30+ attribute methods."
drupal_version: "11.x"
---

# HTMX Attributes Reference

## When to Use

> Reference this when configuring how HTMX elements make requests, where content goes, and how it swaps. The `Htmx` class provides 30+ attribute methods.

## Decision

**Request attributes:**

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `get(?Url)` | `data-hx-get` | Issue GET request |
| `post(?Url)` | `data-hx-post` | Issue POST request |
| `put(?Url)` | `data-hx-put` | Issue PUT request |
| `patch(?Url)` | `data-hx-patch` | Issue PATCH request |
| `delete(?Url)` | `data-hx-delete` | Issue DELETE request |

**Content control attributes:**

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `select(string)` | `data-hx-select` | CSS selector for content to swap from response |
| `selectOob(string\|array)` | `data-hx-select-oob` | Out-of-band selectors for additional swaps |
| `target(string)` | `data-hx-target` | CSS selector for swap target |
| `swap(string, string, bool)` | `data-hx-swap` | Swap strategy (innerHTML, outerHTML, beforeend, etc.) |
| `swapOob(true\|string)` | `data-hx-swap-oob` | Mark element for out-of-band swap |

**Trigger attributes:**

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `trigger(string\|array)` | `data-hx-trigger` | Event(s) that trigger request |
| `on(string, string)` | `data-hx-on-{event}` | Inline event handler |

**History attributes:**

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `pushUrl(bool\|Url)` | `data-hx-push-url` | Push URL to browser history |
| `replaceUrl(bool\|Url)` | `data-hx-replace-url` | Replace current URL in history |

**Special Drupal attribute:**

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `onlyMainContent(bool)` | `data-hx-drupal-only-main-content` | Triggers `_wrapper_format=drupal_htmx` parameter |

Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php` — complete API with 30+ methods

## Pattern

**Content extraction and swap:**

```php
(new Htmx())
  ->post($form_url)
  ->select('#main-content')        // Extract this from response
  ->target('#content-wrapper')     // Put it here
  ->swap('outerHTML')              // Replace entire target
  ->applyTo($build['element']);
```

**Trigger variations:**

```php
(new Htmx())->trigger('click');
(new Htmx())->trigger(['click', 'keyup changed']);
(new Htmx())->trigger('revealed');       // Infinite scroll
(new Htmx())->trigger('every 5s');       // Polling
(new Htmx())->trigger('keyup changed delay:500ms');  // Debounced
```

**Swap with modifier** — Drupal defaults `ignoreTitle` to TRUE:

```php
$htmx->swap('outerHTML');                    // "outerHTML ignoreTitle:true"
$htmx->swap('outerHTML', '', FALSE);         // Allow title changes
$htmx->swap('beforeend', 'scroll:bottom');  // With modifier
```

**Out-of-band swap:**

```php
(new Htmx())
  ->swapOob('outerHTML:#status')
  ->applyTo($form['status'], '#wrapper_attributes');
```

**Additional control:**

```php
(new Htmx())
  ->vals(['extra' => 'value'])
  ->confirm('Are you sure?')
  ->indicator('#spinner')
  ->include('[name="search"]')
  ->applyTo($build['button']);
```

## Common Mistakes

- **Wrong**: Forgetting `onlyMainContent()` when route doesn't have `_htmx_route` → **Right**: Results in full page responses
- **Wrong**: Using `swap('none')` without OOB swaps → **Right**: Nothing updates
- **Wrong**: Not understanding ignoreTitle default → **Right**: Pass `FALSE` as third param to `swap()` to allow title changes
- **Wrong**: Hardcoding URLs instead of using Url objects → **Right**: Breaks multilingual sites and alias changes
- **Wrong**: Chaining attributes without calling `applyTo()` → **Right**: Configuration isn't applied to render array

## See Also

- [HTMX Controllers](htmx-controllers.md)
- [Response Headers](response-headers.md)
- [Dynamic Forms](dynamic-forms.md)
- Reference: [HTMX Official Attribute Reference](https://htmx.org/reference/#attributes)
- Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php`
