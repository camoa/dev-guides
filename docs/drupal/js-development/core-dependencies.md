---
description: "Essential Drupal core JavaScript library dependencies and when to use them"
tldr: "When defining any JavaScript library, declare exactly what your code needs so Drupal loads dependencies automatically. Gotcha: including jQuery when not needed adds ~30KB unnecessarily."
drupal_version: "11.x"
---

# Core Dependencies

## When to Use

> When defining any JavaScript library - dependencies ensure required code loads first.

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
  - core/drupal.dropbutton    # Admin interface dropbuttons
  - core/drupal.progress      # Progress indicators
  - core/drupal.states        # Form state management
```

**Reference**: View all core libraries at `/core/core.libraries.yml`

## Common Mistakes

- **Including jQuery when not needed** - WHY: Adds ~30KB weight, use vanilla JS instead
- **Missing drupal.ajax dependency** - WHY: Drupal.ajax undefined, AJAX features break
- **Circular dependencies** - WHY: Unpredictable load order, potential failures
- **Loading entire jQuery UI** - WHY: Massive weight, only load specific components needed

## See Also

- [DOM Manipulation](dom-manipulation.md) - When jQuery is actually needed
- [AJAX Integration](ajax-integration.md) - AJAX dependency patterns
