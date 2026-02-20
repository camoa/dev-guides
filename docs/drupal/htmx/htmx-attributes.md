---
description: Complete HTMX attribute reference for Drupal — request, content, trigger, history, and OOB attributes via the Htmx class
drupal_version: "11.x"
---

# HTMX Attributes Reference

## When to Use

> Reference this when configuring how HTMX elements make requests, where content goes, and how it swaps. The `Htmx` class provides 30+ attribute methods.

## Decision

| Category | Method | Attribute | Purpose |
|----------|--------|-----------|---------|
| Request | `get(?Url)` | `data-hx-get` | Issue GET request |
| Request | `post(?Url)` | `data-hx-post` | Issue POST request |
| Content | `select(string)` | `data-hx-select` | CSS selector for content to extract from response |
| Content | `target(string)` | `data-hx-target` | CSS selector for swap target |
| Content | `swap(string)` | `data-hx-swap` | Swap strategy (innerHTML, outerHTML, beforeend, etc.) |
| Content | `swapOob(true\|string)` | `data-hx-swap-oob` | Out-of-band swap |
| Trigger | `trigger(string\|array)` | `data-hx-trigger` | Event(s) that trigger request |
| History | `pushUrl(bool\|Url)` | `data-hx-push-url` | Push URL to browser history |
| History | `replaceUrl(bool\|Url)` | `data-hx-replace-url` | Replace current URL |
| Drupal | `onlyMainContent(bool)` | `data-hx-drupal-only-main-content` | Triggers `_wrapper_format=drupal_htmx` |

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
(new Htmx())->trigger('revealed');      // For infinite scroll
(new Htmx())->trigger('every 5s');      // Polling
```

**Swap with modifier** — Drupal defaults `ignoreTitle` to TRUE:

```php
$htmx->swap('outerHTML');                   // "outerHTML ignoreTitle:true"
$htmx->swap('outerHTML', '', FALSE);        // Allow title changes
$htmx->swap('beforeend', 'scroll:bottom'); // With modifier
```

**Out-of-band swap:**

```php
(new Htmx())
  ->swapOob('outerHTML:#status')
  ->applyTo($form['status'], '#wrapper_attributes');
```

**Additional control attributes:**

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
- **Wrong**: Not understanding ignoreTitle default → **Right**: Pass `FALSE` as third param to allow title changes
- **Wrong**: Hardcoding URLs instead of using Url objects → **Right**: Breaks multilingual sites and alias changes
- **Wrong**: Chaining attributes without calling `applyTo()` → **Right**: Configuration isn't applied to render array

## See Also

- [HTMX Controllers](htmx-controllers.md)
- [Response Headers](response-headers.md)
- [Dynamic Forms](dynamic-forms.md)
- Reference: [HTMX Official Attribute Reference](https://htmx.org/reference/#attributes)
- Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php`
