---
description: Run Drupal PHPUnit tests locally and in CI/CD with filtering, debugging, and DDEV support.
---

# Running Tests

## When to Use
Executing tests locally, in CI/CD, filtering by group/tag, debugging failures.

## Decision
| Scenario | Command | Notes |
|---|---|---|
| Run single test file | `./vendor/bin/phpunit path/to/TestFile.php` | Fastest for development |
| Run test suite (unit/kernel/functional) | `./vendor/bin/phpunit --testsuite unit` | Organized by type |
| Run specific group | `./vendor/bin/phpunit --group my_module` | Module-specific tests |
| Run with coverage | `./vendor/bin/phpunit --coverage-html reports/` | Requires Xdebug |
| DDEV environment | `ddev exec ./vendor/bin/phpunit ...` | Inside DDEV container |

## Pattern
**Basic test execution**:
```bash
# From Drupal root
./vendor/bin/phpunit -c web/core web/core/modules/node/tests/src/Kernel/NodeAccessTest.php
```

**With DDEV**:
```bash
ddev exec ./vendor/bin/phpunit -c web/core web/modules/custom/my_module/tests/
```

**Running by test suite**:
```bash
# Unit tests only (fast)
./vendor/bin/phpunit -c web/core --testsuite unit

# Kernel tests
./vendor/bin/phpunit -c web/core --testsuite kernel

# Functional (browser) tests
./vendor/bin/phpunit -c web/core --testsuite functional

# JavaScript tests (requires chromedriver)
chromedriver --port=4444 &
./vendor/bin/phpunit -c web/core --testsuite functional-javascript
```

**Filtering by group**:
```bash
# Run all tests in "my_module" group
./vendor/bin/phpunit --group my_module

# Exclude groups
./vendor/bin/phpunit --exclude-group Composer
```

**Debugging failures**:
```bash
# Verbose output
./vendor/bin/phpunit -v

# Stop on first failure
./vendor/bin/phpunit --stop-on-failure

# Filter to specific method
./vendor/bin/phpunit --filter testMethodName
```

**CI/CD integration (GitLab CI example)**:
```yaml
test:
  script:
    - composer install
    - export SIMPLETEST_BASE_URL=http://localhost
    - export SIMPLETEST_DB=mysql://root:root@mysql/drupal
    - ./vendor/bin/phpunit -c web/core --testsuite unit,kernel
```

Reference: `/core/tests/README.md` lines 45-79

## Common Mistakes
- Not specifying `-c` flag -- PHPUnit uses wrong config or no config
- Running tests from wrong directory -- paths broken
- Forgetting to start chromedriver for JS tests -- connection failures
- Running all tests when only one module changed -- wastes time (use `--group`)
- Not setting `SIMPLETEST_DB` environment variable -- database tests fail

## See Also
- Reference: `/core/tests/README.md`
- DDEV guide: [Running Drupal's PHPUnit test suites on DDEV | Matt Glaman](https://mglaman.dev/blog/running-drupals-phpunit-test-suites-ddev)
