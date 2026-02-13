---
description: Enable JavaScript aggregation and minification for production performance
drupal_version: "10.x/11.x"
---

# Aggregation and Minification

## When to Use

> Use in production environments - always enable JavaScript aggregation for performance.

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

- **Wrong**: preprocess: false on custom JS → **Right**: Use default preprocess: true
  - **Why**: Prevents aggregation, extra HTTP request per file
- **Wrong**: Minifying already-minified files → **Right**: Mark as minified: true
  - **Why**: Wastes processing time, potential corruption
- **Wrong**: Not testing with aggregation → **Right**: Test production config before deploy
  - **Why**: Works in dev, breaks in production
- **Wrong**: Disabling aggregation for debugging → **Right**: Use dev settings, re-enable for prod
  - **Why**: Easy to forget, production performance suffers

## See Also

- [Performance Optimization](performance-optimization.md) - Overall performance strategy
