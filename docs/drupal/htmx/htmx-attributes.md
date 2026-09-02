---
description: "Complete HTMX attribute reference for Drupal — request, content, trigger, history, and OOB attributes via the Htmx class"
tldr: "Reference this when configuring how HTMX elements make requests, where content goes, and how it swaps. The `Htmx` class provides 30+ attribute methods; chaining without calling `applyTo()` never applies the configuration."
drupal_version: "11.x"
---

# HTMX Attributes Reference

## When to Use

> You need to configure how HTMX elements make requests, where content goes, and how it swaps.

Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php` — Complete API with 30+ attribute methods

## Request Attributes

Configure HTTP request details:

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `get(?Url)` | `data-hx-get` | Issue GET request |
| `post(?Url)` | `data-hx-post` | Issue POST request |
| `put(?Url)` | `data-hx-put` | Issue PUT request |
| `patch(?Url)` | `data-hx-patch` | Issue PATCH request |
| `delete(?Url)` | `data-hx-delete` | Issue DELETE request |

**Usage:**
```php
(new Htmx())->get(Url::fromRoute('my.route'));
(new Htmx())->post(Url::fromRoute('my.form'));
```

Reference: Lines 547-632 of Htmx.php

## Content Control Attributes

Control what content to extract and where to put it:

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `select(string)` | `data-hx-select` | CSS selector for content to swap from response |
| `selectOob(string\|array)` | `data-hx-select-oob` | Out-of-band selectors for additional swaps |
| `target(string)` | `data-hx-target` | CSS selector for swap target |
| `swap(string, string, bool)` | `data-hx-swap` | Swap strategy (innerHTML, outerHTML, beforeend, etc.) |
| `swapOob(true\|string)` | `data-hx-swap-oob` | Mark element for out-of-band swap |

**Usage:**
```php
(new Htmx())
  ->select('#main-content')         // Extract this from response
  ->target('#content-wrapper')      // Put it here
  ->swap('outerHTML');               // Replace entire target

// Out-of-band swap for multiple updates
(new Htmx())
  ->swapOob('outerHTML:#status')    // Also update status region
  ->applyTo($form['status'], '#wrapper_attributes');
```

Reference: Lines 712-794 of Htmx.php

**Swap Strategy with ignoreTitle:**

Drupal defaults `ignoreTitle` to TRUE, preventing title changes:

```php
$htmx->swap('outerHTML');                    // Adds "outerHTML ignoreTitle:true"
$htmx->swap('outerHTML', '', FALSE);         // Allow title changes
$htmx->swap('beforeend', 'scroll:bottom');   // Adds modifiers: "beforeend scroll:bottom ignoreTitle:true"
```

Reference: Lines 759-770 of Htmx.php

## Trigger Attributes

Control when requests fire:

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `trigger(string\|array)` | `data-hx-trigger` | Event(s) that trigger request |
| `on(string, string)` | `data-hx-on-{event}` | Inline event handler |

**Usage:**
```php
(new Htmx())->trigger('click');                      // Single event
(new Htmx())->trigger(['click', 'keyup changed']);   // Multiple events
(new Htmx())->trigger('revealed');                   // For infinite scroll
(new Htmx())->trigger('every 5s');                   // Polling

// Event handler shorthand (:: prefix for HTMX events)
(new Htmx())->on('click', 'alert("clicked")');
(new Htmx())->on('::beforeRequest', 'console.log("starting")');
```

Reference: Lines 835-859 (trigger), 656-664 (on) of Htmx.php

## Additional Control Attributes

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `vals(array)` | `data-hx-vals` | Additional values as JSON |
| `headers(array)` | `data-hx-headers` | Additional request headers |
| `confirm(string)` | `data-hx-confirm` | Confirmation dialog before request |
| `disable()` | `data-hx-disable` | Disable HTMX processing on element |
| `disabledElt(string)` | `data-hx-disabled-elt` | Elements to disable during request |
| `include(string)` | `data-hx-include` | Include additional element values |
| `indicator(string)` | `data-hx-indicator` | Loading indicator element |
| `params(string\|array)` | `data-hx-params` | Filter submitted parameters |
| `validate(bool)` | `data-hx-validate` | Validate before submit |

**Usage:**
```php
(new Htmx())
  ->vals(['extra' => 'value'])
  ->confirm('Are you sure?')
  ->indicator('#spinner');
```

Reference: Lines 860-1278 of Htmx.php

## History Attributes

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `pushUrl(bool\|Url)` | `data-hx-push-url` | Push URL to browser history |
| `replaceUrl(bool\|Url)` | `data-hx-replace-url` | Replace current URL in history |
| `history()` | `data-hx-history` | Prevent localStorage history |
| `historyElt()` | `data-hx-history-elt` | Element for history snapshot |

**Usage:**
```php
(new Htmx())->pushUrl(Url::fromRoute('my.route', ['id' => 123]));
(new Htmx())->pushUrl(TRUE);   // Use request URL
(new Htmx())->pushUrl(FALSE);  // Don't push
```

Reference: Lines 687-1209 of Htmx.php

## Special Drupal Attribute

| Method | Attribute | Purpose |
|--------|-----------|---------|
| `onlyMainContent(bool)` | `data-hx-drupal-only-main-content` | Triggers `_wrapper_format=drupal_htmx` parameter |

**Usage:**
```php
(new Htmx())
  ->post($url)
  ->onlyMainContent()   // Triggers HtmxRenderer
  ->target('#content');
```

Reference: Lines 231-242 of Htmx.php, lines 41-48 of htmx-assets.js

## Common Mistakes

- Forgetting `onlyMainContent()` when route doesn't have `_htmx_route` — Results in full page responses
- Using `swap('none')` without OOB swaps — Nothing updates
- Not understanding ignoreTitle default — Page title won't change unless you set third parameter to FALSE
- Hardcoding URLs instead of using Url objects — Breaks multilingual sites and alias changes
- Chaining attributes without calling `applyTo()` — Configuration isn't applied to render array

## See Also

- Previous: [HTMX Controllers](htmx-controllers.md)
- Next: [Response Headers](response-headers.md)
- Reference: [HTMX Official Attribute Reference](https://htmx.org/reference/#attributes)
- Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php`
