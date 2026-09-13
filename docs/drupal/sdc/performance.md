---
description: "Automatic library loading, library dependency declaration, render caching, and lazy loading for SDCs"
tldr: "Libraries auto-generate per component and load only when the component renders; libraryOverrides is the only key core reads for dependency ordering (core/drupal is appended automatically). A js: or css: key in libraryOverrides replaces the auto-discovered entry rather than adding to it."
drupal_version: "11.x"
---

# Performance

## When to Use

> - You're optimizing component loading
> - You're debugging slow page loads with many components
> - You're implementing caching strategies

## Decision

**Pattern: Automatic Library Loading**

Components automatically generate asset libraries, loaded only when component renders.

**Generated Library Format:**
- `core/components.{provider}--{component-name}`
- Includes matching `.css` and `.js` files
- Auto-attached when component renders
- Aggregated with other libraries in production

**WHY automatic is better:** No manual library management. Assets only load when component actually used on page.

## Pattern

**Pattern: Library Dependencies**

Declare dependencies to optimize loading order. `libraryOverrides` is the only key core reads — there is no `libraryDependencies` (see [Component YAML Schema](component-yaml-schema.md)).

```yaml
libraryOverrides:
  dependencies:
    - core/once          # core/drupal is appended automatically
  js:
    my-component.js:
      attributes: { defer: true }  # Non-blocking load
      preprocess: true             # Enable aggregation
```

The `js:` key here **replaces** the auto-discovered `my-component.js` entry rather than adding to it (`array_merge` at `ComponentPluginManager.php:213-216`), so list the file with the same name you want to keep loading.

**Pattern: Render Caching**

Cache component render output when possible.

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

**Pattern: Lazy Loading Components**

For below-fold or modal components, consider lazy loading.

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

**Pattern: CSS Performance**

Minimize component CSS file size and complexity.

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

**Common Mistake:** Including heavy JavaScript libraries in every component.
**WHY:** Bloats page weight. Use `libraryOverrides: dependencies:` to share one common library across components rather than duplicating code per component.

**Common Mistake:** Not enabling CSS/JS aggregation in production.
**WHY:** Individual component files create many HTTP requests. Enable aggregation in production settings.

**Common Mistake:** Over-componentizing (components for every small element).
**WHY:** Each component has overhead. Group related elements together when they always appear together.

## See Also

- [JavaScript in SDCs](javascript-in-sdcs.md)
- [SCSS/CSS in SDCs](scss-css-in-sdcs.md)
- [Drupal Caching Best Practices](https://www.qed42.com/insights/drupal-caching-best-practices-and-performance-monitoring)
