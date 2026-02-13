---
description: Optimizing component loading with automatic libraries, caching, and lazy loading
drupal_version: "11.x"
---

# Performance

## When to Use

> Use this when optimizing component loading, debugging slow page loads with many components, or implementing caching strategies.

## Decision: Performance Optimization Strategy

| Optimization | Pattern | Why |
|--------------|---------|-----|
| Automatic library loading | Components generate asset libraries | Assets only load when component renders |
| Library dependencies | Declare shared dependencies | Optimize loading order, share common libraries |
| Render caching | `#cache` in render arrays | Cache component output when possible |
| Lazy loading | BigPipe for heavy components | Load below-fold/modal components async |
| CSS optimization | Simple, scoped selectors | Minimize file size and complexity |

## Pattern

Automatic library loading:

- Generated format: `core/components.{provider}--{component-name}`
- Includes matching `.css` and `.js` files
- Auto-attached when component renders
- Aggregated with other libraries in production

**WHY automatic is better**: No manual library management. Assets only load when component actually used on page.

Library dependencies for optimized loading:

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

Render caching:

```php
// In render array
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

Lazy loading components with BigPipe:

```twig
{# Use BigPipe for heavy components #}
{{ attach_library('core/drupal.ajax') }}

<div
  data-big-pipe-placeholder-id="..."
  data-drupal-ajax-processor="big_pipe"
>
  {# Heavy component loads async #}
  {{ include('my_theme:heavy-component', {...}) }}
</div>
```

CSS performance (simple, scoped selectors):

```css
/* ✓ GOOD: Simple, scoped selectors */
.my-component { }
.my-component__element { }
.my-component--variant { }

/* ✗ BAD: Deep nesting, complex selectors */
.my-component .wrapper .inner .element .child { }
.my-component:not(.variant):not(.disabled) > * + * { }
```

## Common Mistakes

- **Wrong**: Including heavy JavaScript libraries in every component → **Right**: Bloats page weight. Use `libraryDependencies` to share common libraries across components.
- **Wrong**: Not enabling CSS/JS aggregation in production → **Right**: Individual component files create many HTTP requests. Enable aggregation in production settings.
- **Wrong**: Over-componentizing (components for every small element) → **Right**: Each component has overhead. Group related elements together when they always appear together.

## See Also

- [JavaScript in SDCs](javascript-in-sdcs.md)
- [SCSS/CSS in SDCs](scss-css-in-sdcs.md)
- [Drupal Caching Best Practices](https://www.qed42.com/insights/drupal-caching-best-practices-and-performance-monitoring)
