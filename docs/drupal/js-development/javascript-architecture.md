---
description: "Drupal's library-based JavaScript architecture with behaviors, drupalSettings, and AJAX system"
tldr: "Understand how Drupal loads and manages JavaScript before implementing any JS functionality. Core pattern: libraries define assets, behaviors initialize them, once() prevents duplicate processing."
drupal_version: "11.x"
---

# JavaScript Architecture

## When to Use

> Understanding how Drupal loads and manages JavaScript before implementing any JS functionality.

## Decision

Drupal uses a library-based asset management system where all JavaScript is defined in `*.libraries.yml` files and attached via PHP render arrays. This architecture enables dependency management, aggregation, conditional loading, and AJAX compatibility.

**Key architectural concepts**:
- **Libraries** define collections of JS/CSS assets with dependencies
- **Behaviors** provide AJAX-compatible initialization pattern
- **drupalSettings** passes server-side data to JavaScript
- **Once API** prevents duplicate initialization
- **AJAX system** automatically re-runs behaviors on dynamic content

## Pattern

**Core JavaScript system location**:
- `/core/misc/drupal.js` - Core Drupal object and behaviors system
- `/core/misc/ajax.js` - AJAX framework and commands
- `/core/assets/vendor/once/once.js` - Once API for preventing duplicate processing

**Library system workflow**:
1. Define library in `MODULE.libraries.yml`
2. Declare dependencies (core/drupal, core/once, etc.)
3. Attach library via `#attached` in render array
4. Drupal loads dependencies, aggregates, and injects into page
5. Behaviors automatically execute on page load and AJAX updates

**Reference**: Official documentation at https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview

## Common Mistakes

- **Inline JavaScript in templates** - WHY: Bypasses aggregation, breaks caching, creates CSP violations
- **Direct `<script>` tags** - WHY: No dependency management, no aggregation, defeats asset system
- **Global DOM operations without context** - WHY: Performance penalty, breaks AJAX compatibility
- **jQuery dependency for simple tasks** - WHY: Unnecessary weight, jQuery being phased out

## See Also

- [Library Definitions](library-definitions.md) - How to define libraries
- [Drupal.behaviors Pattern](drupal-behaviors-pattern.md) - Core initialization pattern
- Reference: [Official JavaScript API Overview](https://www.drupal.org/docs/drupal-apis/javascript-api/javascript-api-overview)
