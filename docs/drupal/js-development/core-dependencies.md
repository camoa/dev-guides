---
description: Essential Drupal core JavaScript library dependencies and when to use them
drupal_version: "10.x/11.x"
---

# Core Dependencies

## When to Use

> Use when defining any JavaScript library. Dependencies ensure required code loads first.

## Decision

Core provides essential JavaScript libraries. Always declare exactly what your code needs - Drupal loads dependencies automatically and handles ordering.

## Pattern

**Common core dependencies**:

```yaml
dependencies:
  - core/drupal          # Required for Drupal.behaviors, Drupal.t()
  - core/once            # Required for once() API
  - core/jquery          # Only if using jQuery functionality
  - core/drupal.ajax     # Required for AJAX features
  - core/drupal.announce # Required for screen reader announcements
  - core/drupal.debounce # Required for debounce() performance pattern
  - core/drupalSettings  # Automatic when using drupalSettings
```

**Specialized dependencies**:

```yaml
dependencies:
  - core/drupal.dialog        # Modal dialogs
  - core/drupal.dialog.ajax   # AJAX-loaded dialogs
  - core/dropbutton           # Admin interface dropbuttons
  - core/drupal.progress      # Progress indicators
  - core/drupal.states        # Form state management
```

## Common Mistakes

- **Wrong**: Including jQuery when not needed → **Right**: Use vanilla JS instead
  - **Why**: Adds ~30KB weight unnecessarily
- **Wrong**: Missing drupal.ajax dependency → **Right**: Declare when using AJAX
  - **Why**: Drupal.ajax undefined, AJAX features break
- **Wrong**: Circular dependencies → **Right**: Review dependency chain
  - **Why**: Unpredictable load order, potential failures
- **Wrong**: Loading entire jQuery UI → **Right**: Only load specific components needed
  - **Why**: Massive weight, impacts performance

## See Also

- [DOM Manipulation](dom-manipulation.md) - When jQuery is actually needed
- [AJAX Integration](ajax-integration.md) - AJAX dependency patterns
- Reference: `/core/core.libraries.yml` - View all core libraries
