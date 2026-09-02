---
description: "Add interactive behavior to Single Directory Components with automatic library discovery"
tldr: "Place a JavaScript file in the component directory following naming convention, and Drupal creates the library and attaches it automatically when the component renders. Gotcha: the auto-generated library name is core/components.THEME_OR_MODULE--COMPONENT, not sdc/..."
drupal_version: "11.x"
---

# JavaScript in SDC Components

## When to Use

> Adding interactive behavior to Single Directory Components.

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

**Library auto-generated**: Drupal creates library as `core/components.THEME_OR_MODULE--COMPONENT` and attaches automatically (`Component::getLibraryName()`).

**Reference**:
- https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components - Official SDC docs
- https://drupalize.me/tutorial/anatomy-drupal-single-directory-component-sdc - Component anatomy

## Common Mistakes

- **Manually creating library for SDC JS** - WHY: Drupal does this automatically, creates duplication
- **Not using data attributes for targeting** - WHY: Class-based selectors conflict with styling, break encapsulation
- **Global selectors in component JS** - WHY: Breaks component reusability, affects other instances
- **Forgetting context parameter** - WHY: Breaks when multiple component instances on page

## See Also

- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - Component initialization
- Reference: [SDC in Core](https://www.lullabot.com/articles/getting-single-directory-components-drupal-core)
