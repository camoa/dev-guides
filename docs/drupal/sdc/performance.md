---
description: Performance optimization strategies for SDC components including caching and asset loading
drupal_version: "11.x"
---

# Performance

## When to Use

> Use this when optimizing component loading, debugging slow page loads with many components, or implementing caching strategies.

## Decision

| Optimization | Use Case | Why |
|--------------|----------|-----|
| Automatic library loading | Default behavior | Assets only load when component renders |
| Library dependencies | Share common libraries | Avoid duplicating jQuery, Bootstrap, etc. |
| Render caching | Static component output | Cache component HTML with proper cache tags |
| Lazy loading | Below-fold components | Defer non-critical component rendering |
| CSS/JS aggregation | Production | Reduce HTTP requests |

## Pattern

**Automatic Library Loading:**
- Generated format: `core/components.{provider}--{component-name}`
- Includes matching `.css` and `.js` files
- Auto-attached when component renders
- Aggregated with other libraries in production

**Library Dependencies:**
```yaml
libraryDependencies:
  - core/drupal
  - core/once

libraryOverrides:
  js:
    my-component.js:
      attributes: { defer: true }  # Non-blocking load
      preprocess: true             # Enable aggregation
```

**Render Caching:**
```php
$build = [
  '#type' => 'component',
  '#component' => 'my_theme:card',
  '#props' => [...],
  '#cache' => [
    'keys' => ['card', $node->id()],
    'contexts' => ['user.permissions'],
    'tags' => $node->getCacheTags(),
    'max-age' => 3600,
  ],
];
```

**CSS Performance:**
```css
/* ✓ GOOD: Simple, scoped selectors */
.my-component { }
.my-component__element { }
.my-component--variant { }

/* ✗ BAD: Deep nesting, complex selectors */
.my-component .wrapper .inner .element .child { }
```

## Common Mistakes

- **Wrong**: Including heavy JS libraries in every component → **Right**: Use `libraryDependencies` to share common libraries
- **Wrong**: Not enabling CSS/JS aggregation in production → **Right**: Enable aggregation in production settings
- **Wrong**: Over-componentizing (components for every small element) → **Right**: Group related elements that always appear together

## See Also

- [JavaScript in SDCs](javascript-in-sdcs.md)
- [SCSS/CSS in SDCs](scss-css-in-sdcs.md)
- [Drupal Caching Best Practices](https://www.qed42.com/insights/drupal-caching-best-practices-and-performance-monitoring)
