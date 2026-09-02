---
description: "Debug HTMX issues in Drupal — attributes not working, content not swapping, missing JS behaviors, and request debugging"
tldr: "Use this when HTMX isn't working as expected — attributes not applying, content not swapping, behaviors not running, or history not updating. Confirm `applyTo()` was called and use `htmx.logAll()` for lifecycle visibility."
drupal_version: "11.x"
---

# Troubleshooting

## When to Use

> You're experiencing HTMX issues and need to diagnose and fix them.

## Common Issues and Solutions

**Issue: HTMX attributes not working**

- **Check library attachment:**
  ```bash
  # View page source, search for htmx
  # Should see: <script src="/core/assets/vendor/htmx/htmx.min.js">
  ```

- **Verify attributes rendered:**
  ```bash
  # Inspect element in browser DevTools
  # Should see: data-hx-get="/path" data-hx-target="#id"
  ```

- **Confirm Htmx::applyTo() called:**
  ```php
  $htmx = new Htmx();
  $htmx->get($url)->target('#content');
  $htmx->applyTo($build['element']);  // REQUIRED
  ```

**Issue: Content not swapping**

- **Verify target exists:**
  ```javascript
  // Browser console
  document.querySelector('#target-id');  // Should not be null
  ```

- **Check select selector matches response:**
  ```php
  // Response must contain element matching select attribute
  (new Htmx())
    ->select('#main-content')  // This must exist in response
    ->target('#wrapper')
    ->applyTo($build);
  ```

- **Inspect Network tab:**
  ```bash
  # DevTools Network tab → Click request
  # Preview tab → Verify content present
  # Headers tab → Verify HX-Request: true
  ```

- **Verify HtmxRenderer invoked:**
  ```bash
  # Response should be minimal HTML structure, not full page
  # Look for: <!doctype html><html><head><meta name="robots" content="noindex">
  ```

**Issue: JavaScript not executing on swapped content**

- **Check behavior implementation:**
  ```javascript
  Drupal.behaviors.myBehavior = {
    attach(context, settings) {
      // Use context, not document
      $(context).find('.my-element').once('myBehavior').each(function() {
        // Your code
      });
    }
  };
  ```

- **Verify htmx:drupal:load fires:**
  ```javascript
  // Browser console
  htmx.on('htmx:drupal:load', (e) => console.log('Load event', e.detail));
  ```

- **Check asset loading:**
  ```javascript
  // Browser console
  htmx.on('htmx:beforeSwap', (e) => console.log('Assets:', e.detail));
  ```

**Issue: Form not submitting**

- **Verify form method:**
  ```php
  (new Htmx())
    ->post($url)  // Must match form method
    ->applyTo($form['submit']);
  ```

- **Check CSRF token present:**
  ```bash
  # View form source
  # Should have: <input type="hidden" name="form_token">
  # Drupal forms include this automatically
  ```

- **Validate route exists:**
  ```bash
  drush route:debug | grep my_route
  ```

**Issue: Multiple swaps not working**

- **Use swapOob:**
  ```php
  // Response element needs OOB attribute
  (new Htmx())
    ->swapOob('true')
    ->applyTo($form['status'], '#wrapper_attributes');
  ```

- **Verify IDs match:**
  ```php
  // Page has: <div id="status">
  // Response must have: <div id="status" data-hx-swap-oob="true">
  ```

**Issue: Browser history not updating**

- **Use pushUrlHeader:**
  ```php
  (new Htmx())
    ->pushUrlHeader(Url::fromRoute('my.route', ['id' => $id]))
    ->applyTo($form);
  ```

- **Check history cleanup:**
  ```javascript
  // Browser console → Network tab
  // Click request → check if _wrapper_format in URL
  // Should be removed before history save
  ```

## Debugging HTMX Requests

**Browser DevTools Network Tab:**

1. Filter by XHR
2. Click HTMX request
3. **Headers tab:**
   - Request Headers: `HX-Request: true`, `HX-Target: #id`, `HX-Trigger: element-id`
   - Response Headers: `HX-Push-Url`, `HX-Trigger`, etc.
4. **Preview tab:** See rendered HTML
5. **Response tab:** See raw HTML

**HTMX Event Logging:**

```javascript
// Add to browser console for debugging
htmx.logAll();

// Or specific events
htmx.on('htmx:beforeRequest', (e) => console.log('Request:', e.detail));
htmx.on('htmx:afterSwap', (e) => console.log('Swapped:', e.detail));
htmx.on('htmx:responseError', (e) => console.error('Error:', e.detail));
htmx.on('htmx:drupal:load', (e) => console.log('Drupal loaded:', e.detail));
```

Reference: [HTMX Events](https://htmx.org/events/)

**Server-Side Debugging:**

```php
// Check if request is HTMX
if ($this->isHtmxRequest()) {
  \Drupal::logger('my_module')->notice('HTMX request detected');
  \Drupal::logger('my_module')->notice('Trigger: @trigger', [
    '@trigger' => $this->getHtmxTriggerName(),
  ]);
}

// Dump render array before returning
\Drupal::logger('my_module')->debug('Build: @build', [
  '@build' => print_r($build, TRUE),
]);

// Verify route option
$route = \Drupal::routeMatch()->getRouteObject();
$htmx_route = $route->getOption('_htmx_route') ?? FALSE;
\Drupal::logger('my_module')->notice('HTMX route: @option', [
  '@option' => $htmx_route ? 'TRUE' : 'FALSE',
]);
```

**Check HtmxRenderer Invocation:**

```bash
# View response HTML source
# Should see minimal structure:
<!doctype html>
<html>
<head>
<meta name="robots" content="noindex">
<title>...</title>
...
</head>
<body>
<!-- Status messages -->
<!-- Main content -->
</body>
</html>

# NOT full page with header, footer, sidebars, etc.
```

## Common Mistakes

- Not checking browser console for JavaScript errors — Errors break HTMX processing
- Assuming HTMX request without checking — Use `isHtmxRequest()` to verify
- Not using `htmx.logAll()` for debugging — Visibility into lifecycle is critical
- Forgetting to clear cache after code changes — Routing and render changes require cache rebuild
- Not testing in multiple browsers — Some behaviors vary by browser
- Debugging in production — Use local/dev environment with debugging enabled

## See Also

- Previous: [Best Practices](best-practices.md)
- Next: [AJAX Migration](ajax-migration.md)
- Reference: [HTMX Debugging Guide](https://htmx.org/docs/#debugging)
