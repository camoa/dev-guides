---
description: "How Drupal loads CSS/JS for HTMX responses — differential loading, drupalSettings merge, and history cleanup"
tldr: "Reference this when debugging missing assets in HTMX responses. Drupal only loads assets not already on the page, comparing requested libraries against ajax_page_state via loadjs; behaviors attach only after assets finish loading."
drupal_version: "11.x"
---

# Asset Loading

## When to Use

> You need to understand how Drupal loads CSS/JS for HTMX responses, or you're debugging missing assets.

Reference: `/core/misc/htmx/htmx-assets.js` — Complete asset loading implementation
Reference: `/core/misc/htmx/htmx-utils.js` — `Drupal.htmx.mergeSettings()` and `Drupal.htmx.addAssets()`

## Differential Loading Process

Drupal only loads assets not already on the page:

1. **Request Configuration** (`htmx:configRequest`) — Send current page state
   ```javascript
   detail.parameters['ajax_page_state[theme]'] = pageState.theme;
   detail.parameters['ajax_page_state[theme_token]'] = pageState.theme_token;
   detail.parameters['ajax_page_state[libraries]'] = pageState.libraries;
   ```

   Reference: Lines 55-58 of htmx-assets.js

2. **Server Processing** — Drupal compares requested libraries to `ajax_page_state`, returns only new ones

   Reference: System module integration at `/core/modules/system/src/Hook/SystemHooks.php` line 279

3. **Response Parsing** (`htmx:beforeSwap`) — Extract assets from response
   ```javascript
   const assetsElements = responseHTML.querySelectorAll(
     'link[rel="stylesheet"][href], script[src]'
   );
   ```

   Reference: Lines 122-125 of htmx-assets.js

4. **Asset Loading** — Load new CSS/JS with loadjs, remove from serverResponse

   Reference: Lines 141 of htmx-assets.js calls `Drupal.htmx.addAssets()`

5. **Behavior Trigger** (`htmx:afterSettle`) — After assets load, fire `htmx:drupal:load`

   Reference: Lines 138-145 of htmx-assets.js

## Pattern: drupalSettings Merge

Settings automatically merge from response:

```javascript
// Extract settings from response
const settingsElement = responseHTML.querySelector(
  ':is(head, body) > script[type="application/json"][data-drupal-selector="drupal-settings-json"]'
);

if (settingsElement !== null) {
  Drupal.htmx.mergeSettings(
    drupalSettings,
    JSON.parse(settingsElement.textContent)
  );
}
```

Reference: Lines 106-116 of htmx-assets.js

## Pattern: Loading Assets with loadjs

```javascript
Drupal.htmx.addAssets(data);  // data is array of {href, src, type, ...attributes}

// loadjs handles:
// - CSS files (prefix 'css!')
// - JS modules (prefix 'module!')
// - Regular JS (no prefix)
// - Copying attributes (defer, async, crossorigin)
// - Async loading (CSS and modules), ordered loading (JS)
```

Reference: Lines 60-103 of htmx-utils.js

## History Cleanup

Before saving to history, remove HTMX-specific parameters:

```javascript
htmx.on('htmx:beforeHistoryUpdate', ({ detail }) => {
  const url = new URL(detail.history.path, window.location);
  [
    '_wrapper_format',
    'ajax_page_state[theme]',
    'ajax_page_state[theme_token]',
    'ajax_page_state[libraries]',
    '_triggering_element_name',
    '_triggering_element_value',
  ].forEach((key) => url.searchParams.delete(key));

  detail.history.path = url.toString();
});
```

Reference: Lines 68-81 of htmx-assets.js

## Common Mistakes

- Expecting all page assets in HTMX response — Only new assets load (differential loading)
- Not understanding timing — Behaviors attach AFTER assets load, not immediately
- Forgetting loadjs is async for CSS — CSS loads in parallel, JS loads in order
- Manually managing drupalSettings — Automatic merge handles this
- Assets missing from response — Check that libraries are attached to render array `#attached['library']`

## See Also

- Previous: [Drupal Behaviors Integration](drupal-behaviors.md)
- Next: [Production Patterns](production-patterns.md)
- Reference: [loadjs Documentation](https://github.com/muicss/loadjs)
