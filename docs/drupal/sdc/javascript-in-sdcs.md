---
description: Adding interactive behavior with Drupal.behaviors, once(), and progressive enhancement
drupal_version: "11.x"
---

# JavaScript in SDCs

## When to Use

> Use this when adding interactive behavior to components, using Drupal.behaviors pattern, or integrating with `once()` or other Drupal JS APIs.

## Decision: JavaScript Integration Pattern

| Pattern | Purpose | Why |
|---------|---------|-----|
| `Drupal.behaviors` | Standard Drupal JS attachment | Works with AJAX, BigPipe, dynamic content |
| `once()` | Prevent duplicate initialization | Behaviors can attach multiple times |
| `context` parameter | Scope to new content only | Performance, avoid re-processing |
| `detach` method | Cleanup when removed | Prevent memory leaks |

## Pattern

Drupal.behaviors with once():

```javascript
/**
 * @file
 * Component behavior for my-component.
 */

(function (Drupal, once) {
  'use strict';

  /**
   * Attaches component behavior.
   */
  Drupal.behaviors.myComponent = {
    attach: function (context, settings) {
      // Use once() to prevent multiple initialization
      once('my-component', '.my-component', context).forEach(function (element) {

        // Component initialization logic here
        element.addEventListener('click', function (event) {
          // Handle event
        });

      });
    },

    detach: function (context, settings, trigger) {
      // Cleanup when behavior is detached
      if (trigger === 'unload') {
        // Remove event listeners, destroy instances
      }
    }
  };

})(Drupal, once);
```

Library dependencies in component YAML:

```yaml
libraryOverrides:
  dependencies:
    - core/drupal
    - core/once
    - core/drupal.ajax
  js:
    my-component.js:
      attributes: { defer: true }
      preprocess: false
```

Progressive enhancement (works without JavaScript):

```javascript
Drupal.behaviors.myComponent = {
  attach: function (context) {
    once('my-component-enhanced', '.my-component', context).forEach(function (element) {

      // Add enhanced functionality marker
      element.classList.add('my-component--js-enhanced');

      // Initialize interactive features
      const toggle = element.querySelector('.my-component__toggle');
      if (toggle) {
        toggle.addEventListener('click', function (event) {
          event.preventDefault();
          element.classList.toggle('my-component--expanded');
        });
      }

    });
  }
};
```

## Common Mistakes

- **Wrong**: Not using `once()` to prevent duplicate initialization → **Right**: Drupal.behaviors can attach multiple times (AJAX, BigPipe). Without `once()`, event listeners get added multiple times, causing bugs.
- **Wrong**: Querying entire document instead of scoped `context` → **Right**: Drupal passes `context` to limit behavior to new content. Ignoring it causes performance issues and processes elements multiple times.
- **Wrong**: Not implementing `detach` method → **Right**: Without cleanup, event listeners and instances persist after elements removed, causing memory leaks.

## See Also

- Reference: `/core/misc/drupal.js` - Core Drupal JavaScript
- Reference: `/core/assets/vendor/once/once.js` - once() implementation
- Reference: `/themes/contrib/radix/` JavaScript patterns
- [Performance](performance.md)
- [Drupal JavaScript API](https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview)
