---
description: "Core Drupal JavaScript pattern for AJAX-compatible DOM manipulation and initialization"
tldr: "Always use Drupal.behaviors for DOM manipulation, since $(document).ready() only runs once and breaks with AJAX and BigPipe. Gotcha: skip the once() wrapper or context parameter and behaviors re-scan the whole DOM or double-bind on every AJAX update."
drupal_version: "11.x"
---

# Drupal.behaviors Pattern

## When to Use

> **Always** for DOM manipulation in Drupal. Behaviors are the foundation of Drupal JavaScript - they work with AJAX, BigPipe, and dynamic content loading.

## Decision

Drupal.behaviors is an object where each property is a behavior. Behaviors have `attach()` (required) and `detach()` (optional) methods. Drupal automatically executes all behaviors on page load and whenever AJAX updates the DOM.

**WHY behaviors exist**: jQuery's `$(document).ready()` only runs once on initial page load. Drupal's AJAX, BigPipe, and dynamic content require JavaScript to initialize new content after page load. Behaviors solve this by re-running whenever the DOM changes.

## Pattern

**Standard behavior structure**:
```javascript
(function (Drupal, once) {
  'use strict';

  Drupal.behaviors.moduleBehavior = {
    attach(context, settings) {
      once('unique-id', '.selector', context).forEach(function (element) {
        // Initialize element
        element.addEventListener('click', function() {
          // Event handling
        });
      });
    },

    detach(context, settings, trigger) {
      if (trigger === 'unload') {
        // Cleanup: remove event listeners, clear intervals
        // Prevents memory leaks
      }
    }
  };
})(Drupal, once);
```

**Global operation pattern** (runs once per page):
```javascript
once('global-init', 'html').forEach(function () {
  // Page-level initialization
  // Equivalent to $(document).ready()
});
```

**Reference examples**:
- `/core/misc/details-aria.js` - ARIA pattern
- `/core/misc/progress.js` - Complex behavior with classes

**Documentation**: https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview

## Common Mistakes

- **Using $(document).ready()** - WHY: Only runs once, breaks with AJAX/BigPipe
- **Not using context parameter** - WHY: Scans entire DOM every time, severe performance penalty
- **Missing once() wrapper** - WHY: Code runs multiple times on same element, duplicate event bindings, memory leaks
- **No detach() implementation** - WHY: Memory leaks from event listeners and intervals that never clean up
- **jQuery dependency in IIFE without declaring it** - WHY: Code breaks if jQuery loads after your script

## See Also

- [Once API](once-api.md) - Preventing duplicate processing
- [Event Handling](event-handling.md) - Event delegation patterns
- Reference: [Official Behaviors Documentation](https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview)
