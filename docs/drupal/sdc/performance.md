---
description: "Automatic library loading, library dependency declaration, render caching, and lazy loading for SDCs"
tldr: "Libraries auto-generate per component and load only when the component renders; libraryOverrides is the only key core reads for dependency ordering (core/drupal is appended automatically). A js: or css: key in libraryOverrides replaces the auto-discovered entry rather than adding to it."
drupal_version: "11.x"
---

# Performance

## When to Use

> Use this when you're optimizing component loading, debugging slow page loads with many components, or implementing caching strategies.

## Decision

**Automatic Library Loading.** Components automatically generate asset libraries, loaded only when the component renders.

- Format: `core/components.{provider}--{component-name}`
- Includes matching `.css` and `.js` files.
- Auto-attached when the component renders.
- Aggregated with other libraries in production.

**WHY automatic is better:** no manual library management. Assets only load when the component is actually used on the page.

Declare dependencies to optimize loading order. `libraryOverrides` is the only key core reads — there is no `libraryDependencies` (see [Component YAML Schema](component-yaml-schema.md)).

## Pattern

**Library Dependencies:**

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

**Render Caching:**

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

**Lazy Loading Components** — for below-fold or modal components, consider lazy loading.

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

**CSS Performance** — minimize component CSS file size and complexity.

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

- **Wrong**: Including heavy JavaScript libraries in every component → **Right**: Bloats page weight. Use `libraryOverrides: dependencies:` to share one common library across components rather than duplicating code per component.
- **Wrong**: Not enabling CSS/JS aggregation in production → **Right**: Individual component files create many HTTP requests. Enable aggregation in production settings.
- **Wrong**: Over-componentizing (a component for every small element) → **Right**: Each component has overhead. Group related elements together when they always appear together.

## See Also

- [JavaScript in SDCs](javascript-in-sdcs.md)
- [SCSS/CSS in SDCs](scss-css-in-sdcs.md)
- [Drupal Caching Best Practices](https://www.qed42.com/insights/drupal-caching-best-practices-and-performance-monitoring)
