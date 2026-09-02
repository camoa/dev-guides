---
description: "Non-blocking JavaScript loading with defer and async attributes"
tldr: "Use defer for most JavaScript — it downloads in parallel and executes in order after DOM ready; use async only for independent scripts where execution order doesn't matter. Gotcha: aggregation may remove defer, so test the configuration."
drupal_version: "11.x"
---

# Defer and Async Attributes

## When to Use

> Default for most JavaScript - improves page load performance by allowing non-blocking script loading.

## Decision

**Defer** (recommended): Downloads in parallel, executes in order after DOM ready. **Async** (rare): Downloads in parallel, executes immediately when ready (order not guaranteed). Use defer for most cases.

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

**Reference**: https://www.drupal.org/project/drupal/issues/1587536 - Core defer/async support

## Common Mistakes

- **Using async for dependent scripts** - WHY: Execution order unpredictable, dependency errors
- **No defer on footer scripts** - WHY: Misses performance optimization opportunity
- **Defer on header-loaded critical scripts** - WHY: Defeats purpose of header placement
- **Assuming defer works with aggregation** - WHY: Aggregation may remove defer, test configuration

## See Also

- [Header vs Footer Loading](header-vs-footer-loading.md) - Script placement strategy
- Reference: [Defer/Async Performance Guide](https://drupalzone.com/tutorial/performance-optimization/27-reducing-render-blocking-resources)
