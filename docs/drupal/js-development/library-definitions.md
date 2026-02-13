---
description: Define JavaScript libraries in *.libraries.yml with dependencies and configuration
drupal_version: "10.x/11.x"
---

# Library Definitions

## When to Use

> Use every time you add JavaScript to a module or theme. All JS must be defined in a library.

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

## Common Mistakes

- **Wrong**: No core/drupal dependency → **Right**: Always include core/drupal
  - **Why**: Drupal.behaviors won't exist, code breaks
- **Wrong**: No core/once dependency → **Right**: Include core/once when using once()
  - **Why**: once() function undefined, initialization fails
- **Wrong**: No version number → **Right**: Include version for cache busting
  - **Why**: Cache busting issues, outdated JS served
- **Wrong**: Loading everything in header → **Right**: Footer is default and correct for most JS
  - **Why**: Blocks rendering, poor performance
- **Wrong**: No defer attribute → **Right**: Use defer for non-blocking load
  - **Why**: Scripts block HTML parsing, slower page loads

## See Also

- [Core Dependencies](core-dependencies.md) - Common dependency patterns
- [Conditional Loading](conditional-loading.md) - When to load libraries
- [Performance Optimization](performance-optimization.md) - Library performance patterns
- Reference: `/core/core.libraries.yml` - Core library examples
- Reference: [Adding Assets to Modules](https://www.drupal.org/docs/develop/creating-modules/adding-assets-css-js-to-a-drupal-module-via-librariesyml)
