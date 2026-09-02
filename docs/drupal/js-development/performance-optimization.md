---
description: "JavaScript performance optimization strategies for better user experience and SEO"
tldr: "Minimize JavaScript weight, load conditionally, use defer, implement debounce/throttle, and avoid layout thrashing on every implementation — performance is not optional. Gotcha: reading layout properties in a loop forces multiple reflows."
drupal_version: "11.x"
---

# Performance Optimization

## When to Use

> Every JavaScript implementation - performance is not optional. Frontend performance directly impacts user experience and SEO.

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

**Reference**: https://www.drupal.org/project/drupal/issues/1587536 - Defer/async patterns

## Common Mistakes

- **Loading JS globally without conditions** - WHY: Unused JS on most pages, wasted bandwidth
- **No defer attribute** - WHY: Blocks HTML parsing, poor Core Web Vitals
- **Disabling aggregation in production** - WHY: Multiple HTTP requests, no minification
- **Heavy operations without debounce** - WHY: Executes too frequently, freezes UI
- **Reading layout properties in loops** - WHY: Forces multiple reflows, severe performance penalty

## See Also

- [Debounce and Throttle](debounce-and-throttle.md) - Event optimization
- [Conditional Loading](conditional-loading.md) - When to load libraries
