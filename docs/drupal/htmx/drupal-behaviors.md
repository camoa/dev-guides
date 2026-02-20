---
description: Run Drupal behaviors on HTMX-loaded content — custom events, lifecycle hooks, and double-processing prevention
drupal_version: "11.x"
---

# Drupal Behaviors Integration

## When to Use

> Use this when you need to run JavaScript behaviors on content loaded via HTMX, or clean up when content is removed.

## Decision

| Event | When fires | Purpose |
|-------|-----------|---------|
| `htmx:drupal:load` | After settle AND asset loading complete | Attach behaviors to new content |
| `htmx:drupal:unload` | Before content removal | Detach behaviors from removed content |

Behaviors automatically work with HTMX content — `htmx:drupal:load` triggers `Drupal.attachBehaviors()`.

## Pattern

**Standard Drupal behavior** (works automatically with HTMX):

```javascript
Drupal.behaviors.myModuleBehavior = {
  attach(context, settings) {
    // context is the HTMX-loaded content
    // Runs after htmx:drupal:load fires
    console.log('Attached to:', context);
  },
  detach(context, settings, trigger) {
    if (trigger === 'unload') {
      console.log('Cleaning up:', context);
    }
  }
};
```

**Listening to HTMX lifecycle events:**

```javascript
htmx.on('htmx:beforeRequest', (event) => {
  console.log('Starting request to:', event.detail.path);
});
htmx.on('htmx:afterSwap', (event) => {
  console.log('Content swapped:', event.detail.elt);
});
htmx.on('htmx:drupal:load', (event) => {
  console.log('Drupal processing complete:', event.detail.elt);
});
```

**Preventing double-processing** (HTMX processes elements inserted by traditional AJAX):

```javascript
Drupal.behaviors.htmx = {
  attach(context) {
    if (!attachFromHtmx && context !== document) {
      htmx.process(context);
    }
  }
};
```

## Common Mistakes

- **Wrong**: Expecting behaviors to run immediately after swap → **Right**: Behaviors run AFTER `htmx:drupal:load`, which fires only after all assets load
- **Wrong**: Forgetting to implement `detach()` → **Right**: Memory leaks when event handlers aren't cleaned up
- **Wrong**: Not checking trigger type in `detach()` → **Right**: Use `trigger === 'unload'` to identify HTMX removals

## See Also

- [Response Headers](response-headers.md)
- [Asset Loading](asset-loading.md)
- Reference: `/core/misc/htmx/htmx-behaviors.js`
- Reference: [Drupal JavaScript API Overview](https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview)
- Reference: [HTMX Events Documentation](https://htmx.org/events/)
