---
description: How Drupal loads CSS/JS for HTMX responses — differential loading, drupalSettings merge, and history cleanup
drupal_version: "11.x"
---

# Asset Loading

## When to Use

> Reference this when debugging missing assets in HTMX responses or understanding how differential loading works.

## Decision

| Step | Event | What happens |
|------|-------|-------------|
| 1. Request config | `htmx:configRequest` | Send `ajax_page_state` with current theme/libraries |
| 2. Server processing | (server) | Compare requested libraries to state; return only new ones |
| 3. Response parse | `htmx:beforeSwap` | Extract `link[rel="stylesheet"]` and `script[src]` from response |
| 4. Asset load | (loadjs) | Load new CSS/JS asynchronously; remove from response before swap |
| 5. Behavior trigger | `htmx:afterSettle` | After assets load, fire `htmx:drupal:load` |

## Pattern

**Request configuration** (automatic via htmx-assets.js):

```javascript
detail.parameters['ajax_page_state[theme]'] = pageState.theme;
detail.parameters['ajax_page_state[theme_token]'] = pageState.theme_token;
detail.parameters['ajax_page_state[libraries]'] = pageState.libraries;
```

**drupalSettings merge** (automatic):

```javascript
const settingsElement = responseHTML.querySelector(
  ':is(head, body) > script[type="application/json"][data-drupal-selector="drupal-settings-json"]'
);
if (settingsElement !== null) {
  Drupal.htmx.mergeSettings(drupalSettings, JSON.parse(settingsElement.textContent));
}
```

**History cleanup** — removes HTMX-specific params before saving to history:

```javascript
htmx.on('htmx:beforeHistoryUpdate', ({ detail }) => {
  const url = new URL(detail.history.path, window.location);
  ['_wrapper_format', 'ajax_page_state[theme]', '_triggering_element_name']
    .forEach((key) => url.searchParams.delete(key));
  detail.history.path = url.toString();
});
```

## Common Mistakes

- **Wrong**: Expecting all page assets in HTMX response → **Right**: Only new assets load (differential loading)
- **Wrong**: Not understanding timing → **Right**: Behaviors attach AFTER assets load, not immediately
- **Wrong**: Manually managing drupalSettings → **Right**: Automatic merge handles this
- **Wrong**: Assets missing from response → **Right**: Check that libraries are attached to render array `#attached['library']`

## See Also

- [Drupal Behaviors Integration](drupal-behaviors.md)
- [Library Dependencies](library-dependencies.md)
- [Production Patterns](production-patterns.md)
- Reference: `/core/misc/htmx/htmx-assets.js`
- Reference: `/core/misc/htmx/htmx-utils.js`
- Reference: [loadjs Documentation](https://github.com/muicss/loadjs)
