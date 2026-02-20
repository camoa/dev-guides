---
description: HTMX response headers in Drupal — redirect, trigger events, retarget, reswap, and history management
drupal_version: "11.x"
---

# Response Headers

## When to Use

> Use this when you need to control client-side behavior after a response — redirect, trigger events, change swap strategy, or update browser history.

## Decision

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

## Pattern

**Push URL to history:**

```php
(new Htmx())
  ->pushUrlHeader(Url::fromRoute('my.route', ['type' => $type, 'name' => $name]))
  ->applyTo($form);
```

**Trigger client-side events:**

```php
(new Htmx())
  ->triggerHeader([
    'showMessage' => ['text' => 'Saved successfully'],
    'updateCount' => ['count' => 5],
  ])
  ->applyTo($build);
```

**Complex location redirect:**

```php
use Drupal\Core\Htmx\HtmxLocationResponseData;

$location_data = new HtmxLocationResponseData(
  path: Url::fromRoute('my.destination'),
  target: '#modal-content',
  swap: 'innerHTML',
);
(new Htmx())->locationHeader($location_data)->applyTo($build);
```

**Dynamic retarget/reswap:**

```php
(new Htmx())->retargetHeader('#different-target')->applyTo($build);
(new Htmx())->reswapHeader('beforeend')->applyTo($build);
```

## Common Mistakes

- **Wrong**: Using `locationHeader()` for simple URL push → **Right**: Use `pushUrlHeader()` instead
- **Wrong**: Not calling `applyTo()` → **Right**: Headers won't be added to `#attached['http_header']`
- **Wrong**: Triggering events before swap with `triggerHeader()` when timing matters → **Right**: Use `triggerAfterSwapHeader()` or `triggerAfterSettleHeader()`
- **Wrong**: Expecting headers to affect non-HTMX requests → **Right**: Headers only affect HTMX client behavior

## See Also

- [HTMX Attributes Reference](htmx-attributes.md)
- [Drupal Behaviors Integration](drupal-behaviors.md)
- [Production Example: ConfigSingleExportForm](production-example-config-export.md)
- Reference: [HTMX Official Response Headers](https://htmx.org/reference/#response_headers)
- Reference: `/core/lib/Drupal/Core/Htmx/Htmx.php` lines 335-522
- Reference: `/core/lib/Drupal/Core/Htmx/HtmxLocationResponseData.php`
