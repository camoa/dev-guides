---
description: "Define JavaScript libraries in *.libraries.yml with dependencies and configuration"
tldr: "Every JS addition to a module or theme must be defined in a library. Core pattern: MODULE.libraries.yml with js:, dependencies:, and optional css:/version:/attributes:. Gotcha: missing core/drupal or core/once breaks behaviors and once() respectively."
drupal_version: "11.x"
---

# Library Definitions

## When to Use

> Every time you add JavaScript to a module or theme. All JS must be defined in a library.

## Decision

Libraries are defined in `*.libraries.yml` files and contain JavaScript files, CSS files, dependencies, and metadata. They enable Drupal's aggregation system, dependency resolution, and conditional loading.

## Pattern

**Basic library structure** (`MODULE.libraries.yml`):
```yaml
feature:
  js:
    js/feature.js: {}
  dependencies:
    - core/drupal
    - core/once
```

**Advanced library with options**:
```yaml
admin:
  version: 1.x
  js:
    js/admin.js:
      minified: true
      attributes:
        defer: true
  css:
    theme:
      css/admin.css: {}
  dependencies:
    - core/drupal
    - core/jquery
    - core/drupal.ajax
```

**External library**:
```yaml
external:
  js:
    https://cdn.example.com/library.min.js:
      type: external
      minified: true
      attributes:
        defer: true
```

**Reference examples**:
- `/core/core.libraries.yml` - Core library definitions
- `/modules/contrib/webform/webform.libraries.yml` - Complex contrib patterns

**Official documentation**: https://www.drupal.org/docs/develop/creating-modules/adding-assets-css-js-to-a-drupal-module-via-librariesyml

## Common Mistakes

- **Missing core/drupal dependency** - WHY: Drupal.behaviors won't exist, code breaks
- **Missing core/once dependency** - WHY: once() function undefined, initialization fails
- **Omitting version number** - WHY: Cache busting issues, outdated JS served
- **Loading everything in header** - WHY: Blocks rendering, poor performance. Footer is default and correct for most JS
- **Not using defer attribute** - WHY: Scripts block HTML parsing, slower page loads

## See Also

- [Core Dependencies](core-dependencies.md) - Common dependency patterns
- [Conditional Loading](conditional-loading.md) - When to load libraries
- [Performance Optimization](performance-optimization.md) - Library performance patterns
