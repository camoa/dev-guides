---
description: Add interactive behavior to Single Directory Components with automatic library discovery
drupal_version: "10.3+"
---

# JavaScript in SDC Components

## When to Use

> Use when adding interactive behavior to Single Directory Components (Drupal core feature since 10.3).

## Decision

Place JavaScript file in component directory following naming convention. Drupal automatically creates library and attaches JS when component renders. Use standard Drupal.behaviors pattern for initialization.

## Pattern

**File structure**:

```
components/button/
├── button.component.yml
├── button.twig
├── button.css
└── button.js           # Automatically discovered
```

**Component JavaScript** (button.js):

```javascript
(function (Drupal, once) {
  'use strict';

  Drupal.behaviors.buttonComponent = {
    attach(context) {
      // Target component specifically
      once('button-component', '[data-component="button"]', context).forEach(function (element) {
        // Component initialization
        element.addEventListener('click', function(e) {
          element.classList.toggle('is-active');
        });
      });
    },

    detach(context, settings, trigger) {
      if (trigger === 'unload') {
        // Component cleanup
      }
    }
  };
})(Drupal, once);
```

**Accessing component via data attribute** (button.twig):

```twig
<button{{ attributes.addClass('button').setAttribute('data-component', 'button') }}>
  {{ label }}
</button>
```

**Library auto-generated**: Drupal creates library as `sdc/THEME_OR_MODULE--COMPONENT` and attaches automatically.

## Common Mistakes

- **Wrong**: Manually creating library for SDC JS → **Right**: Let Drupal auto-discover
  - **Why**: Drupal does this automatically, creates duplication
- **Wrong**: Class-based selectors for targeting → **Right**: Use data attributes
  - **Why**: Class-based selectors conflict with styling, break encapsulation
- **Wrong**: Global selectors in component JS → **Right**: Target specific component instances
  - **Why**: Breaks component reusability, affects other instances
- **Wrong**: Forgetting context parameter → **Right**: Always use context
  - **Why**: Breaks when multiple component instances on page

## See Also

- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - Component initialization
- Reference: [Using Single Directory Components](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components)
- Reference: [SDC in Core](https://www.lullabot.com/articles/getting-single-directory-components-drupal-core)
- Reference: [Anatomy of SDC](https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc)
