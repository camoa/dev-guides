---
description: JavaScript integration with Drupal.behaviors, once(), and progressive enhancement
drupal_version: "11.x"
---

# JavaScript in SDCs

## When to Use

> Use this when adding interactive behavior to components, implementing Drupal.behaviors pattern, or integrating with `once()` or other Drupal JS APIs.

## Decision

| Pattern | Use Case | Why |
|---------|----------|-----|
| Drupal.behaviors | Component initialization | Supports AJAX, BigPipe, and dynamic content |
| `once()` | Prevent duplicate initialization | Behaviors can attach multiple times |
| `context` parameter | Scope queries to new content | Performance optimization |
| `detach` method | Cleanup on removal | Prevent memory leaks |

## Pattern

**Drupal.behaviors with once():**
```javascript
(function (Drupal, once) {
  'use strict';

  Drupal.behaviors.myComponent = {
    attach: function (context, settings) {
      once('my-component', '.my-component', context).forEach(function (element) {

        element.addEventListener('click', function (event) {
          // Handle event
        });

      });
    },

    detach: function (context, settings, trigger) {
      if (trigger === 'unload') {
        // Remove event listeners, destroy instances
      }
    }
  };

})(Drupal, once);
```

**Library Dependencies in YAML:**
```yaml
libraryOverrides:
  dependencies:
    - core/drupal
    - core/once
  js:
    my-component.js:
      attributes: { defer: true }
      preprocess: false
```

**Progressive Enhancement:**
```javascript
Drupal.behaviors.myComponent = {
  attach: function (context) {
    once('my-component-enhanced', '.my-component', context).forEach(function (element) {

      // Add enhancement marker
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

- **Wrong**: Not using `once()` → **Right**: Always use `once()` to prevent duplicate initialization (behaviors attach multiple times)
- **Wrong**: Querying entire document → **Right**: Use scoped `context` parameter (`context.querySelectorAll()`)
- **Wrong**: Missing `detach` method → **Right**: Implement cleanup to prevent memory leaks

## See Also

- Reference: `/core/misc/drupal.js` - Core Drupal JavaScript
- Reference: `/core/assets/vendor/once/once.js` - once() implementation
- Reference: `/themes/contrib/radix/` JavaScript patterns
- [Performance](performance.md)
- [Drupal JavaScript API](https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview)
