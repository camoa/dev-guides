---
description: Run independent GitHub Actions jobs concurrently to reduce total workflow time
drupal_version: "11.x"
---

# Parallel Execution

## When to Use

> Use when running independent jobs concurrently to reduce total workflow time.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Independent quality checks | Separate jobs for PHPCS, PHPStan, tests | No dependencies, can run in parallel |
| Sequential deployment | `needs:` keyword | Deployment only after all tests pass |
| Fail-fast development | `fail-fast: true` in matrix | Quick feedback on first failure |
| Complete CI results | `fail-fast: false` in matrix | See all failures before fixing |

## Pattern

```yaml
jobs:
  phpcs:
    runs-on: ubuntu-latest
    steps: [run PHPCS]

  phpstan:
    runs-on: ubuntu-latest
    steps: [run PHPStan]

  unit-tests:
    runs-on: ubuntu-latest
    steps: [run unit tests]

  functional-tests:
    runs-on: ubuntu-latest
    needs: [phpcs, phpstan]  # Wait for quality checks
    steps: [run functional tests]

  deploy:
    runs-on: ubuntu-latest
    needs: [unit-tests, functional-tests]  # Wait for all tests
    if: github.ref == 'refs/heads/main'
    steps: [deploy to staging]
```

## Common Mistakes

- **Wrong**: Running all tests sequentially → **Right**: Wastes CI time
- **Wrong**: Not using `needs:` for deployment → **Right**: Deploys before tests complete
- **Wrong**: Too many parallel jobs → **Right**: Hits GitHub Actions concurrency limits
- **Wrong**: Sharing state between parallel jobs → **Right**: Race conditions, flaky tests

## Performance

Run linting and static analysis in parallel. Run unit tests before slow functional tests. Use matrix strategy for multi-version testing. Limit to 5-10 parallel jobs to stay within free tier limits.

## Development Standards

Use `needs:` to create dependency graph. Group related checks in single jobs when they share setup. Use job outputs to pass data between jobs.

## Anti-patterns

Don't parallelize interdependent jobs (use `needs:`). Don't run deployment in parallel with tests (always sequential). Don't share artifacts without explicit upload/download (jobs can't access each other's filesystem).

## See Also

- Previous: [Caching Strategies](caching-strategies.md)
- Next: [Secret Management](secret-management.md)
- Reference: [GitHub Actions job dependencies](https://docs.github.com/en/actions/using-jobs/using-jobs-in-a-workflow)
