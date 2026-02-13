---
description: PHPCS, PHPStan, deprecation detection, and security audits for Drupal code
drupal_version: "11.x"
---

# Code Quality Checks

## When to Use

> Use before running tests to validate code standards, security, and static analysis.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Drupal coding standards | PHPCS with Drupal/DrupalPractice | Community standard, catches common issues |
| Static analysis | PHPStan level 1+ | Finds type errors, undefined variables |
| Deprecation detection | drupal-check | Identifies deprecated API usage before upgrades |
| Security vulnerabilities | `composer audit` | Checks dependencies for known CVEs |
| Frontend linting | ESLint, Stylelint | Catches JavaScript/CSS issues |

## Pattern

```yaml
- name: Code quality
  run: |
    ./vendor/bin/phpcs --standard=Drupal,DrupalPractice \
      --extensions=php,module,inc,install,theme,yml \
      modules/custom themes/custom
    ./vendor/bin/phpstan analyse modules/custom --level=1
    ./vendor/bin/drupal-check modules/custom
    composer audit --format=json
```

## Common Mistakes

- **Wrong**: Running PHPCS without DrupalPractice → **Right**: Misses Drupal-specific best practices
- **Wrong**: Ignoring `composer audit` warnings → **Right**: Deploys known vulnerabilities
- **Wrong**: Not caching PHPCS results → **Right**: Slow repeated runs
- **Wrong**: Using outdated PHPStan baseline → **Right**: Hides new issues

## Security

Run `composer audit` on every build. Fail builds with high/critical vulnerabilities. Keep dependencies updated.

## Performance

Cache PHPCS installed_paths. Use `--report=junit` for better CI integration.

## Standards

Enforce PHPStan level 1 minimum. Increase level gradually. Use project-specific phpstan.neon for custom rules.

## See Also

- Previous: [Matrix Testing](matrix-testing.md)
- Next: [PHPUnit Testing](phpunit-testing.md)
- Reference: [Drupal coding standards](https://www.drupal.org/docs/develop/standards)
- Reference: `/modules/contrib/coder/`
