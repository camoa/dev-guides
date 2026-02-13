---
description: JavaScript performance optimization strategies for better user experience and SEO
drupal_version: "10.x/11.x"
---

# Performance Optimization

## When to Use

> Use for every JavaScript implementation - performance is not optional. Frontend performance directly impacts user experience and SEO.

## Decision

Minimize JavaScript weight, load conditionally, use defer attribute, implement debounce/throttle, avoid layout thrashing. Drupal provides aggregation system - use it.

## Pattern

**Script loading strategy**:

```yaml
optimized:
  js:
    js/feature.js:
      attributes:
        defer: true      # Non-blocking load, executes after DOM ready
      preprocess: true   # Include in aggregation
      minified: false    # Let Drupal aggregate/minify
  version: 1.x           # Cache busting
```

**Conditional loading**:

```php
// Only load on article nodes
if ($node->bundle() === 'article') {
  $variables['#attached']['library'][] = 'module/article-feature';
}
```

**Lazy initialization**:

```javascript
// Don't initialize heavy features until needed
element.addEventListener('click', function init() {
  // Remove listener after first use
  element.removeEventListener('click', init);

  // Now initialize heavy feature
  initializeHeavyFeature(element);
}, {once: true}); // Native once option
```

**Avoid layout thrashing**:

```javascript
// BAD: Read-write-read-write causes reflows
elements.forEach(el => {
  const height = el.offsetHeight; // Read (forces reflow)
  el.style.height = height + 10 + 'px'; // Write
});

// GOOD: Batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight); // All reads
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px'; // All writes
});
```

## Common Mistakes

- **Wrong**: Loading JS globally without conditions → **Right**: Use conditional loading
  - **Why**: Unused JS on most pages, wasted bandwidth
- **Wrong**: No defer attribute → **Right**: Add defer to library definition
  - **Why**: Blocks HTML parsing, poor Core Web Vitals
- **Wrong**: Disabling aggregation in production → **Right**: Enable aggregation
  - **Why**: Multiple HTTP requests, no minification
- **Wrong**: Heavy operations without debounce → **Right**: Debounce high-frequency handlers
  - **Why**: Executes too frequently, freezes UI
- **Wrong**: Reading layout properties in loops → **Right**: Batch reads, then writes
  - **Why**: Forces multiple reflows, severe performance penalty

## See Also

- [Debounce and Throttle](debounce-and-throttle.md) - Event optimization
- [Conditional Loading](conditional-loading.md) - When to load libraries
- [Aggregation and Minification](aggregation-and-minification.md) - Production optimization
- Reference: [Defer/Async Patterns](https://www.drupal.org/project/drupal/issues/1587536)
