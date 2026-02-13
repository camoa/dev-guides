---
description: Debug common GitHub Actions failures in Drupal workflows
drupal_version: "11.x"
---

# Troubleshooting

## When to Use

> Use when debugging common GitHub Actions failures in Drupal workflows.

## Decision

| If you see | Likely cause | Fix |
|-----------|-------------|-----|
| Composer memory errors | PHP memory limit too low | Add `COMPOSER_MEMORY_LIMIT=-1` |
| Database connection refused | Service not ready | Add health checks and wait loop |
| File permission errors | Wrong user/group ownership | Use `chmod`/`chown` in setup steps |
| Cache hit but dependencies wrong | Stale cache from old lockfile | Update cache key to include lockfile hash |
| Tests pass locally, fail in CI | Environment differences | Match PHP version, extensions, DB version |

## Pattern

Composer memory:
```yaml
- name: Install dependencies
  env:
    COMPOSER_MEMORY_LIMIT: -1
  run: composer install --no-interaction
```

Database readiness:
```yaml
- name: Wait for MySQL
  run: |
    while ! mysqladmin ping -h127.0.0.1 -uroot -proot --silent; do
      echo "Waiting for MySQL..."
      sleep 2
    done
```

Debug workflow:
```yaml
- name: Debug environment
  run: |
    php -v
    composer --version
    mysql --version
    env | grep -i drupal
    ls -la web/sites/default/
```

## Common Mistakes

- **Wrong**: Not checking service health before tests → **Right**: Connection errors
- **Wrong**: Using `npm install` instead of `npm ci` → **Right**: Version mismatches
- **Wrong**: Running multiple Composer installs → **Right**: Lock file conflicts
- **Wrong**: Not clearing caches between workflow runs → **Right**: Stale state

## Development Standards

Enable debug logging with `ACTIONS_STEP_DEBUG`. Use `tmate` action for interactive debugging. Save logs as artifacts for failed workflows. Test workflow changes in feature branch before merging.

## Anti-patterns

Don't use `sudo` unnecessarily (security risk and indicates bad setup). Don't suppress error output (hides root cause). Don't skip validation steps to save time (failures happen in production instead).

## See Also

- Previous: [Environment Protection](environment-protection.md)
- Reference: [GitHub Actions debugging](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/using-workflow-run-logs)
- Reference: [GitHub Actions community forum](https://github.com/orgs/community/discussions/categories/actions)
