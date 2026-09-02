---
description: "Enable JavaScript aggregation and minification for production performance"
tldr: "Always enable JavaScript aggregation in production — Drupal aggregates files into a single bundle, minifies, and serves with far-future cache headers. Gotcha: always test with aggregation enabled before deployment, since it works in dev and can break in production."
drupal_version: "11.x"
---

# Aggregation and Minification

## When to Use

> Production environments - always enable JavaScript aggregation for performance.

## Decision

Drupal aggregates multiple JavaScript files into single bundle, minifies, and serves with far-future cache headers. Configure via Performance settings.

## Pattern

**Enable in settings** (admin/config/development/performance):
- "Aggregate JavaScript files" - ON (production)
- Combines multiple JS files into fewer bundles
- Reduces HTTP requests
- Applies minification

**Library configuration**:
```yaml
feature:
  js:
    js/feature.js:
      preprocess: true    # Include in aggregation (default)
      minified: false     # Not pre-minified, aggregate will minify
```

**Pre-minified external library**:
```yaml
external:
  js:
    https://cdn.example.com/lib.min.js:
      type: external
      minified: true      # Skip minification
      preprocess: false   # Don't aggregate external
```

**Testing aggregated JS**: Always test with aggregation enabled before deployment.

## Common Mistakes

- **preprocess: false on custom JS** - WHY: Prevents aggregation, extra HTTP request per file
- **Minifying already-minified files** - WHY: Wastes processing time, potential corruption
- **Not testing with aggregation** - WHY: Works in dev, breaks in production
- **Disabling aggregation for debugging** - WHY: Forget to re-enable, production performance suffers

## See Also

- [Performance Optimization](performance-optimization.md) - Overall performance strategy
