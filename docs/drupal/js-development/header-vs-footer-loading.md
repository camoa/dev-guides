---
description: "Choose header or footer placement for JavaScript loading based on criticality"
tldr: "Load JavaScript in the footer by default; only use the header for JS that must execute before page render. Gotcha: header: true is a library-level key, a sibling of js: and version:, not a per-file option."
drupal_version: "11.x"
---

# Header vs Footer Loading

## When to Use

> When JavaScript affects critical rendering or initial page display.

## Decision

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
  header: true          # library-level key, a sibling of js: and version:
  version: VERSION
  js:
    js/critical.js: {}
```

**Defer attribute** (best practice for most JavaScript):
```yaml
enhanced:
  js:
    js/enhanced.js:
      attributes:
        defer: true  # Loads async, executes after DOM ready
```

**Reference discussion**: https://www.drupal.org/project/drupal/issues/784626

## Common Mistakes

- **Loading non-critical JS in header** - WHY: Blocks HTML parsing, delays page render, poor Core Web Vitals
- **Using header: true by default** - WHY: Footer is faster for user experience
- **Not using defer attribute** - WHY: Misses performance optimization opportunity
- **Mixing defer with header placement** - WHY: Defeats purpose of defer, creates confusion

## See Also

- [Performance Optimization](performance-optimization.md) - Script loading strategies
- Reference: [Defer/Async Performance](https://www.drupal.org/project/drupal/issues/1587536) - Drupal core discussion
