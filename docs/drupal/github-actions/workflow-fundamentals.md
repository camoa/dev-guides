---
description: GitHub Actions workflow triggers, structure, and core concepts for Drupal CI/CD
drupal_version: "11.x"
---

# Workflow Fundamentals

## When to Use

> Use GitHub Actions workflows to automate testing, builds, and deployments. Choose triggers based on when automation should run.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Automated testing on commits | `on: push` trigger | Catches issues immediately |
| PR validation before merge | `on: pull_request` trigger | Prevents bad code from merging |
| Scheduled tasks (updates, audits) | `on: schedule` with cron | Regular maintenance without manual intervention |
| Manual deployment control | `on: workflow_dispatch` | Safe production deployments with human approval |

## Pattern

```yaml
name: CI
on:
  push:
    branches: [main]
    paths-ignore: ['docs/**']
  pull_request:
    branches: [main]
env:
  PHP_VERSION: "8.2"
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: ./vendor/bin/phpunit
```

## Common Mistakes

- **Wrong**: Running deployment on every push to main → **Right**: Use `workflow_dispatch` for production
- **Wrong**: Ignoring workflow failures in non-critical paths → **Right**: Set appropriate failure modes
- **Wrong**: Hardcoding branch names → **Right**: Use environment-specific configurations

## See Also

- Next: [Drupal Stack Setup](drupal-stack-setup.md)
- Reference: [GitHub Actions workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
