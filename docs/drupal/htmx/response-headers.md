---
description: "HTMX response headers in Drupal — redirect, trigger events, retarget, reswap, and history management"
tldr: "Use this when you need to control client-side behavior after response — redirect, trigger events, change swap strategy, or update browser history — via the Htmx class's 11 response header methods."
drupal_version: "11.x"
---

# HTMX Response Headers

## When to Use

> You need to control client-side behavior after response (redirect, trigger events, change swap strategy, etc.).

Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php` — 11 response header methods (lines 335-522)

## Header Methods

| Method | Header | Purpose |
|--------|--------|---------|
| `locationHeader(Url\|HtmxLocationResponseData)` | `HX-Location` | Client-side redirect with optional context |
| `pushUrlHeader(Url\|false)` | `HX-Push-Url` | Push URL to history after swap |
| `replaceUrlHeader(Url\|false)` | `HX-Replace-Url` | Replace current URL after swap |
| `redirectHeader(Url)` | `HX-Redirect` | Full page client-side redirect |
| `refreshHeader(bool)` | `HX-Refresh` | Force full page refresh |
| `reswapHeader(string)` | `HX-Reswap` | Change swap strategy for this response |
| `retargetHeader(string)` | `HX-Retarget` | Change target selector for this response |
| `reselectHeader(string)` | `HX-Reselect` | Change content selector for this response |
| `triggerHeader(string\|array)` | `HX-Trigger` | Trigger client-side events after swap |
| `triggerAfterSettleHeader(string\|array)` | `HX-Trigger-After-Settle` | Trigger events after settle |
| `triggerAfterSwapHeader(string\|array)` | `HX-Trigger-After-Swap` | Trigger events after swap |

## Pattern: Push URL to History

```php
$push_url = Url::fromRoute('my.route', ['type' => $type, 'name' => $name]);

(new Htmx())
  ->pushUrlHeader($push_url)
  ->applyTo($form);
```

Reference: `/core/modules/config/src/Form/ConfigSingleExportForm.php` lines 157-161

## Pattern: Complex Location Redirect

For redirects with additional context:

```php
use Drupal\Core\Htmx\HtmxLocationResponseData;

$location_data = new HtmxLocationResponseData(
  path: Url::fromRoute('my.destination'),
  target: '#modal-content',
  swap: 'innerHTML',
  values: ['key' => 'value'],
  headers: ['X-Custom' => 'header']
);

(new Htmx())
  ->locationHeader($location_data)
  ->applyTo($build);
```

Reference: `/core/lib/Drupal/Core/Htmx/HtmxLocationResponseData.php` — Constructor parameters at lines 42-52

**Constructor Parameters:**
- `path` (Url) — URL for GET request
- `source` (string) — Source element of request
- `event` (string) — Event that triggered request
- `handler` (string) — JavaScript callback for response
- `target` (string) — Swap target
- `swap` (string) — Swap strategy
- `values` (array) — Additional values to submit
- `headers` (array) — Additional headers
- `select` (string) — Content selector

## Pattern: Trigger Client Events

```php
// Trigger single event
(new Htmx())
  ->triggerHeader('myEvent')
  ->applyTo($build);

// Trigger multiple events with data
(new Htmx())
  ->triggerHeader([
    'showMessage' => ['text' => 'Saved successfully'],
    'updateCount' => ['count' => 5],
  ])
  ->applyTo($build);
```

Reference: Lines 480-522 of Htmx.php

## Pattern: Dynamic Retarget/Reswap

Override target or swap strategy in response:

```php
// Change where content goes
(new Htmx())
  ->retargetHeader('#different-target')
  ->applyTo($build);

// Change how content swaps
(new Htmx())
  ->reswapHeader('beforeend')
  ->applyTo($build);
```

Reference: Lines 430-462 of Htmx.php

## Common Mistakes

- Using `locationHeader()` for simple URL push — Use `pushUrlHeader()` instead
- Not applying headers to render array — Call `applyTo()` to add headers to `#attached['http_header']`
- Triggering events before swap completes — Use `triggerAfterSwapHeader()` or `triggerAfterSettleHeader()` for timing control
- Expecting headers to work on non-HTMX requests — Headers only affect HTMX client behavior

## See Also

- Previous: [HTMX Attributes Reference](htmx-attributes.md)
- Next: [Drupal Behaviors Integration](drupal-behaviors.md)
- Reference: [HTMX Official Response Headers](https://htmx.org/reference/#response_headers)
