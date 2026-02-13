---
description: Test Drupal across multiple versions, PHP versions, and database types using matrix strategy
drupal_version: "11.x"
---

# Matrix Testing

## When to Use

> Use matrix testing when you need to verify compatibility across multiple Drupal versions, PHP versions, or database types.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Multi-version compatibility | Matrix strategy with `drupal-version` | Ensures module works on all supported versions |
| PHP compatibility testing | Matrix with `php-version` | Catches version-specific bugs |
| Selective combinations | `include` and `exclude` | Avoid testing unsupported combinations |
| Fast failure vs. complete testing | `fail-fast: false` | Complete results vs. quick feedback |

## Pattern

```yaml
strategy:
  fail-fast: false
  matrix:
    drupal: ['10.3', '11.0']
    php: ['8.2', '8.3']
    include:
      - drupal: '10.3'
        php: '8.1'
    exclude:
      - drupal: '11.0'
        php: '8.1'
steps:
  - run: composer create-project drupal/recommended-project:^${{ matrix.drupal }}
```

## Common Mistakes

- **Wrong**: Using `fail-fast: true` in CI → **Right**: Hides failures in other matrix combinations
- **Wrong**: Testing deprecated version combinations → **Right**: Wastes CI minutes
- **Wrong**: Not using matrix outputs in job names → **Right**: Hard to identify which combination failed

## See Also

- Previous: [Drupal Stack Setup](drupal-stack-setup.md)
- Next: [Code Quality Checks](code-quality-checks.md)
- Reference: [GitHub Actions matrix strategy](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)
