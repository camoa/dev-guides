---
description: Drupal's library-based JavaScript architecture with behaviors, drupalSettings, and AJAX system
drupal_version: "10.x/11.x"
---

# JavaScript Architecture

## When to Use

> Use this understanding before implementing any JavaScript functionality in Drupal. This is foundational knowledge for all Drupal JS work.

## Decision

Drupal uses a library-based asset management system where all JavaScript is defined in `*.libraries.yml` files and attached via PHP render arrays. This architecture enables dependency management, aggregation, conditional loading, and AJAX compatibility.

**Key architectural concepts**:

| Concept | Purpose |
|---------|---------|
| Libraries | Define collections of JS/CSS assets with dependencies |
| Behaviors | Provide AJAX-compatible initialization pattern |
| drupalSettings | Pass server-side data to JavaScript |
| Once API | Prevent duplicate initialization |
| AJAX system | Automatically re-run behaviors on dynamic content |

## Pattern

**Core JavaScript system location**:
- `/core/misc/drupal.js` - Core Drupal object and behaviors system
- `/core/misc/ajax.js` - AJAX framework and commands
- `/core/misc/once.js` - Once API for preventing duplicate processing

**Library system workflow**:

1. Define library in `MODULE.libraries.yml`
2. Declare dependencies (core/drupal, core/once, etc.)
3. Attach library via `#attached` in render array
4. Drupal loads dependencies, aggregates, and injects into page
5. Behaviors automatically execute on page load and AJAX updates

## Common Mistakes

- **Wrong**: Inline JavaScript in templates → **Right**: Define in library and attach via render array
  - **Why**: Inline bypasses aggregation, breaks caching, creates CSP violations
- **Wrong**: Direct `<script>` tags in templates → **Right**: Use library system
  - **Why**: No dependency management, no aggregation, defeats asset system
- **Wrong**: Global DOM operations without context → **Right**: Use context parameter in behaviors
  - **Why**: Performance penalty, breaks AJAX compatibility
- **Wrong**: jQuery dependency for simple tasks → **Right**: Use vanilla JavaScript
  - **Why**: Unnecessary weight, jQuery being phased out

## See Also

- [Library Definitions](library-definitions.md) - How to define libraries
- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - Core initialization pattern
- Reference: [Official JavaScript API Overview](https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview)
