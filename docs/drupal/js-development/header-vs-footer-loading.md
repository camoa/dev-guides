---
description: Choose header or footer placement for JavaScript loading based on criticality
drupal_version: "10.x/11.x"
---

# Header vs Footer Loading

## When to Use

> Use when JavaScript affects critical rendering or initial page display. Otherwise, use default footer loading.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Non-critical UI enhancement | Footer (default) | Better performance, doesn't block HTML parsing |
| Critical pre-render script | Header with `header: true` | Must execute before page render |
| Standard interactive feature | Footer with defer | Non-blocking, executes after DOM ready |

**Default: Load in footer** (after HTML parsing). Only load in header for JS that must execute before page render. Since Drupal 8, footer is the performance-optimized default.

## Pattern

**Footer loading** (default, no configuration needed):

```yaml
feature:
  js:
    js/feature.js: {}  # Loads in footer by default
```

**Header loading** (rare, only for critical UI):

```yaml
critical:
  js:
    js/critical.js:
      header: true
```

**Defer attribute** (best practice for most JavaScript):

```yaml
enhanced:
  js:
    js/enhanced.js:
      attributes:
        defer: true  # Loads async, executes after DOM ready
```

## Common Mistakes

- **Wrong**: Loading non-critical JS in header → **Right**: Use footer (default)
  - **Why**: Blocks HTML parsing, delays page render, poor Core Web Vitals
- **Wrong**: Using header: true by default → **Right**: Footer is faster for user experience
  - **Why**: Footer doesn't block rendering
- **Wrong**: No defer attribute → **Right**: Add defer for performance
  - **Why**: Misses optimization opportunity
- **Wrong**: Mixing defer with header placement → **Right**: Use one strategy
  - **Why**: Defeats purpose of defer, creates confusion

## See Also

- [Performance Optimization](performance-optimization.md) - Script loading strategies
- [Defer and Async Attributes](defer-and-async-attributes.md) - Non-blocking load patterns
- Reference: [Header vs Footer Discussion](https://www.drupal.org/project/drupal/issues/784626)
