---
description: Speed up GitHub Actions workflows by caching Composer, npm, and Drupal dependencies
drupal_version: "11.x"
---

# Caching Strategies

## When to Use

> Use to speed up workflow execution by reusing dependencies and build outputs between runs.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Cache Composer dependencies | `actions/cache@v4` with `~/.composer/cache` | Avoids re-downloading packages |
| Cache npm dependencies | `actions/setup-node` with `cache: 'npm'` | Built-in, simpler than manual caching |
| Cache Drupal core/contrib | Custom cache key with composer.lock hash | Faster site installation |
| Invalidate cache on changes | Hash composer.lock or package-lock.json | Automatic invalidation when deps change |

## Pattern

```yaml
- name: Get Composer cache dir
  id: composer-cache
  run: echo "dir=$(composer config cache-files-dir)" >> $GITHUB_OUTPUT

- uses: actions/cache@v4
  with:
    path: ${{ steps.composer-cache.outputs.dir }}
    key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
    restore-keys: |
      ${{ runner.os }}-composer-

- uses: actions/setup-node@v4
  with:
    node-version: '18'
    cache: 'npm'
    cache-dependency-path: 'themes/custom/*/package-lock.json'
```

## Common Mistakes

- **Wrong**: Using `restore-keys` too aggressively → **Right**: Stale dependencies persist
- **Wrong**: Not invalidating cache on lockfile changes → **Right**: Wrong versions installed
- **Wrong**: Caching vendor/ directory → **Right**: Misses platform-specific binaries
- **Wrong**: Not caching npm global cache → **Right**: Slow node_modules installs

## Performance

Cache Composer and npm global caches, not vendor/ or node_modules/. Use `hashFiles()` for automatic invalidation. Set 7-day cache expiry for dependencies.

## Development Standards

Use `restore-keys` for fallback to recent cache. Cache PHPCS installed_paths. Don't cache test databases or Drupal files directory.

## Anti-patterns

Don't cache .git directory (wastes space). Don't share cache between branches (cross-contamination). Don't cache without invalidation keys (stale builds).

## See Also

- Previous: [Multi-Environment Deployment](multi-environment-deployment.md)
- Next: [Parallel Execution](parallel-execution.md)
- Reference: [GitHub Actions caching](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
