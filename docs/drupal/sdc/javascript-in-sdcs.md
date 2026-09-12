---
description: "Drupal.behaviors with once(), declaring JS library dependencies, and progressive enhancement in SDCs"
tldr: "Attach behavior with Drupal.behaviors + once() scoped to context, never document.querySelectorAll, and implement detach for cleanup. Declare JS dependencies via libraryOverrides: dependencies: — there is no libraryDependencies key."
drupal_version: "11.x"
---

# JavaScript in SDCs

## When to Use

> - You're adding interactive behavior to components
> - You need to use Drupal.behaviors pattern
> - You're integrating with `once()` or other Drupal JS APIs

## Decision

Attach behavior with `Drupal.behaviors` and scope every query to the passed `context`, guarded with `once()` to prevent duplicate initialization across AJAX/BigPipe attaches. Implement `detach` to clean up.

## Pattern

**Pattern: Drupal.behaviors with once()**

Reference: `/themes/contrib/radix/` JavaScript patterns

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

**Pattern: Library Dependencies**

Declare JS dependencies in component YAML. There is no `libraryDependencies` key — see [Component YAML Schema](component-yaml-schema.md).

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

**Pattern: Progressive Enhancement**

Assume component works without JavaScript, enhance with JS.

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

**Common Mistake:** Not using `once()` to prevent duplicate initialization.
**WHY:** Drupal.behaviors can attach multiple times (AJAX, BigPipe). Without `once()`, event listeners get added multiple times, causing bugs.

**Common Mistake:** Querying entire document instead of scoped `context`.
**WHY:** Drupal passes `context` to limit behavior to new content. Ignoring it causes performance issues and processes elements multiple times.

**Common Mistake:** Not implementing `detach` method.
**WHY:** Without cleanup, event listeners and instances persist after elements removed, causing memory leaks.

## See Also

- Reference: `/core/misc/drupal.js` — Core Drupal JavaScript
- Reference: `/core/assets/vendor/once/once.js` — `once()` implementation
- [Performance](performance.md)
- [Drupal JavaScript API](https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview)
