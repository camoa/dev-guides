---
description: Run unit, kernel, functional, and JavaScript tests with PHPUnit in GitHub Actions
drupal_version: "11.x"
---

# PHPUnit Testing

## When to Use

> Use for automated unit, kernel, functional, and JavaScript tests for Drupal modules.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Unit tests (no DB) | `--testsuite unit` | Fast, isolated, no Drupal bootstrap |
| Kernel tests (minimal Drupal) | `--testsuite kernel` | Tests services, plugins with minimal overhead |
| Functional tests (full site) | `--testsuite functional` | Full browser simulation, slow but comprehensive |
| JavaScript tests | `--testsuite functional-javascript` + Selenium | Tests AJAX, dynamic interactions |
| Code coverage | `--coverage-clover` with Xdebug | Identifies untested code paths |

## Pattern

Basic test run:
```yaml
- name: Install Drupal
  run: |
    ./vendor/bin/drush site:install minimal --yes \
      --db-url=mysql://root:root@127.0.0.1:3306/drupal
    ./vendor/bin/drush en my_module --yes

- name: Run PHPUnit
  run: |
    ./vendor/bin/phpunit \
      --configuration web/core/phpunit.xml.dist \
      --testsuite unit,kernel,functional \
      web/modules/custom/my_module
```

JavaScript tests with Selenium:
```yaml
services:
  selenium:
    image: selenium/standalone-chrome:latest
    ports: ['4444:4444']
steps:
  - name: JavaScript tests
    env:
      MINK_DRIVER_ARGS_WEBDRIVER: '["chrome", {"browserName":"chrome","chromeOptions":{"args":["--headless"]}}, "http://selenium:4444/wd/hub"]'
    run: ./vendor/bin/phpunit --testsuite functional-javascript
```

## Common Mistakes

- **Wrong**: Running all test suites sequentially → **Right**: Use separate jobs for functional vs. unit/kernel
- **Wrong**: Not waiting for database service → **Right**: Tests fail with connection errors
- **Wrong**: Missing SIMPLETEST_BASE_URL → **Right**: Functional tests can't reach the site
- **Wrong**: Using outdated phpunit.xml.dist → **Right**: Incompatible test configuration

## Security

Never commit credentials to phpunit.xml. Use environment variables for database URLs.

## Performance

Run unit/kernel tests in one job, functional in another. Cache Drupal installation between test suites. Use `--stop-on-failure` in development, full suite in CI.

## Coverage

Set minimum coverage thresholds in phpunit.xml. Fail builds below threshold. Upload coverage reports to services like Codecov.

## See Also

- Previous: [Code Quality Checks](code-quality-checks.md)
- Next: [Theme Asset Compilation](theme-asset-compilation.md)
- Reference: [Drupal PHPUnit documentation](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal)
- Reference: [PHPUnit GitHub Actions examples](https://gorannikolovski.com/blog/github-actions-and-drupal)
- Reference: `core/tests/README.md`
