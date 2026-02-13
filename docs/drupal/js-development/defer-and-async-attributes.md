---
description: Non-blocking JavaScript loading with defer and async attributes
drupal_version: "10.x/11.x"
---

# Defer and Async Attributes

## When to Use

> Use as default for most JavaScript - improves page load performance by allowing non-blocking script loading.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Standard feature with dependencies | Defer | Downloads parallel, executes in order after DOM ready |
| Independent tracking/analytics | Async | Downloads parallel, executes immediately when ready |
| Most Drupal JavaScript | Defer | Best balance of performance and predictability |

**Defer** (recommended): Downloads in parallel, executes in order after DOM ready. **Async** (rare): Downloads in parallel, executes immediately when ready (order not guaranteed).

## Pattern

**Defer** (best for most JavaScript):

```yaml
feature:
  js:
    js/feature.js:
      attributes:
        defer: true
```

**How defer works**:

1. Browser continues parsing HTML
2. Script downloads in background
3. Executes after DOM ready, before DOMContentLoaded
4. Multiple defer scripts execute in order

**Async** (rarely needed):

```yaml
analytics:
  js:
    js/tracking.js:
      attributes:
        async: true  # Independent script, order doesn't matter
```

**When to use async**: Analytics, tracking, scripts with no dependencies that don't manipulate DOM.

## Common Mistakes

- **Wrong**: Using async for dependent scripts → **Right**: Use defer for dependencies
  - **Why**: Execution order unpredictable, dependency errors
- **Wrong**: No defer on footer scripts → **Right**: Add defer for optimization
  - **Why**: Misses performance optimization opportunity
- **Wrong**: Defer on header-loaded critical scripts → **Right**: Use one strategy
  - **Why**: Defeats purpose of header placement
- **Wrong**: Assuming defer works with aggregation → **Right**: Test configuration
  - **Why**: Aggregation may remove defer, verify behavior

## See Also

- [Header vs Footer Loading](header-vs-footer-loading.md) - Script placement strategy
- Reference: [Defer/Async Performance](https://www.drupal.org/project/drupal/issues/1587536)
- Reference: [Reducing Render-Blocking Resources](https://drupalzone.com/tutorial/performance-optimization/27-reducing-render-blocking-resources)
