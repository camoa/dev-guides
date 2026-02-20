---
description: Debug HTMX issues in Drupal — attributes not working, content not swapping, missing JS behaviors, and request debugging
drupal_version: "11.x"
---

# Troubleshooting

## When to Use

> Use this when HTMX isn't working as expected — attributes not applying, content not swapping, behaviors not running, or history not updating.

## Decision

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| HTMX attributes not on element | Missing `applyTo()` call | Call `->applyTo($build['element'])` |
| Content not swapping | Target element not in DOM | Verify `document.querySelector('#target-id')` not null |
| Full page in response | Missing HtmxRenderer trigger | Add `_htmx_route: TRUE` or `onlyMainContent()` |
| `select()` not working | Selector not in response | Response must contain element matching `select` attribute |
| JS behaviors not running | Asset loading not complete | Use `htmx:drupal:load` event, not `htmx:afterSwap` |
| OOB swap not working | ID mismatch | Page and response must have matching IDs |
| History not updating | Missing `pushUrlHeader()` | Call `->pushUrlHeader($url)->applyTo($form)` |

## Pattern

**Verify HTMX renderer is invoked** (response should be minimal):

```html
<!doctype html><html><head><meta name="robots" content="noindex">...
```

NOT a full page with header, footer, sidebars.

**Debug HTMX requests in browser console:**

```javascript
htmx.logAll();  // Log all events

// Targeted debugging
htmx.on('htmx:beforeRequest', (e) => console.log('Request:', e.detail));
htmx.on('htmx:afterSwap', (e) => console.log('Swapped:', e.detail));
htmx.on('htmx:responseError', (e) => console.error('Error:', e.detail));
htmx.on('htmx:drupal:load', (e) => console.log('Drupal loaded:', e.detail));
```

**Server-side debugging:**

```php
if ($this->isHtmxRequest()) {
  \Drupal::logger('my_module')->notice('HTMX trigger: @trigger', [
    '@trigger' => $this->getHtmxTriggerName(),
  ]);
}
```

**Verify route option:**

```bash
drush route:debug | grep my_route
```

**Confirm `applyTo()` is called:**

```php
$htmx = new Htmx();
$htmx->get($url)->target('#content');
$htmx->applyTo($build['element']);  // REQUIRED — without this, nothing is applied
```

## Common Mistakes

- **Wrong**: Not checking browser console for JavaScript errors → **Right**: Errors break HTMX processing silently
- **Wrong**: Assuming HTMX request without checking → **Right**: Use `isHtmxRequest()` to verify
- **Wrong**: Not using `htmx.logAll()` → **Right**: Visibility into lifecycle is critical for debugging
- **Wrong**: Forgetting to clear cache after code changes → **Right**: Routing and render changes require cache rebuild
- **Wrong**: Debugging in production → **Right**: Use local/dev environment with debugging enabled

## See Also

- [Best Practices](best-practices.md)
- [AJAX Migration](ajax-migration.md)
- Reference: [HTMX Debugging Guide](https://htmx.org/docs/#debugging)
- Reference: [HTMX Events](https://htmx.org/events/)
