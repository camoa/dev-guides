---
description: "Run Drupal behaviors on HTMX-loaded content — custom events, lifecycle hooks, and double-processing prevention"
tldr: "Use this when you need to run JavaScript behaviors on content loaded via HTMX, or clean up when content is removed. Behaviors run after `htmx:drupal:load`, which fires only after settle AND asset loading complete."
drupal_version: "11.x"
---

# Drupal Behaviors Integration

## When to Use

> You need to run JavaScript behaviors on content loaded via HTMX, or clean up when content is removed.

Reference: `/core/misc/htmx/htmx-behaviors.js` — Behaviors integration and custom events

## Custom HTMX Events

Drupal adds two custom events to HTMX lifecycle:

| Event | When | Purpose |
|-------|------|---------|
| `htmx:drupal:load` | After settle AND asset loading complete | Attach behaviors to new content |
| `htmx:drupal:unload` | Before content removal | Detach behaviors from removed content |

Reference: Lines 14-22 of htmx-behaviors.js

## Pattern: Standard Drupal Behavior

Behaviors automatically work with HTMX content:

```javascript
Drupal.behaviors.myModuleBehavior = {
  attach(context, settings) {
    // context is the HTMX-loaded content
    // This runs after htmx:drupal:load fires
    console.log('Attached to:', context);
  },

  detach(context, settings, trigger) {
    // trigger is 'unload' for HTMX removals
    if (trigger === 'unload') {
      console.log('Cleaning up:', context);
    }
  }
};
```

Reference: Lines 14-16 of htmx-behaviors.js — `htmx:drupal:load` triggers `Drupal.attachBehaviors()`

## Pattern: HTMX Lifecycle Events

Listen to HTMX events directly:

```javascript
// Before request starts
htmx.on('htmx:beforeRequest', (event) => {
  console.log('Starting request to:', event.detail.path);
});

// After content swapped
htmx.on('htmx:afterSwap', (event) => {
  console.log('Content swapped:', event.detail.elt);
});

// After Drupal assets loaded and behaviors attached
htmx.on('htmx:drupal:load', (event) => {
  console.log('Drupal processing complete:', event.detail.elt);
});
```

Reference: [HTMX Events Documentation](https://htmx.org/events/)

## Pattern: Preventing Double-Processing

HTMX automatically processes elements added by traditional AJAX:

```javascript
Drupal.behaviors.htmx = {
  attach(context) {
    if (!attachFromHtmx && context !== document) {
      htmx.process(context);
    }
  }
};
```

Reference: Lines 34-40 of htmx-behaviors.js — Ensures AJAX-inserted HTMX attributes work

## Common Mistakes

- Not accounting for asset loading delay — Behaviors run AFTER `htmx:drupal:load`, not immediately after swap
- Forgetting to implement `detach()` method — Memory leaks when event handlers aren't cleaned up
- Expecting behaviors to run before assets load — `htmx:drupal:load` fires only after all CSS/JS loaded
- Not checking trigger type in `detach()` — `trigger === 'unload'` identifies HTMX removals

## See Also

- Previous: [Response Headers](response-headers.md)
- Next: [Asset Loading](asset-loading.md)
- Reference: [Drupal Behaviors Documentation](https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview)
