---
description: Execute Drupal PHPUnit tests locally and in CI/CD with filtering, debugging, and DDEV support.
tldr: "Executing tests locally, in CI/CD, filtering by group/tag, debugging failures."
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

`-c phpunit.xml` is the copy at the project root that [PHPUnit Configuration](phpunit-configuration.md) builds, and the reason not to point `-c` at `web/core` instead is given there. Run every command below from the project root, and read the `web/` in the paths as your own docroot.

**`--testsuite` and a path argument do not combine.** Give PHPUnit a path and it never maps the configured suites, so the flag is dropped without a word and the path decides what runs. Every command below is one or the other: a suite-wide run, or a path-scoped run. A path-scoped run is also why a broken contrib class cannot reach you -- the suites are never read.

**Basic test execution**:
```bash
# From the project root
./vendor/bin/phpunit -c phpunit.xml web/core/modules/node/tests/src/Kernel/NodeAccessTest.php
```

**With DDEV**:
```bash
ddev exec ./vendor/bin/phpunit -c phpunit.xml web/modules/custom/my_module/tests/
```

**Running by test suite**:
```bash
# Unit tests only (fast)
./vendor/bin/phpunit -c phpunit.xml --testsuite unit

# Kernel tests
./vendor/bin/phpunit -c phpunit.xml --testsuite kernel

# Functional (browser) tests
./vendor/bin/phpunit -c phpunit.xml --testsuite functional

# JavaScript tests (requires chromedriver)
chromedriver --port=4444 &
./vendor/bin/phpunit -c phpunit.xml --testsuite functional-javascript
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
# Details of every issue raised (deprecations, notices, warnings)
./vendor/bin/phpunit --display-all-issues

# Stop on first failure
./vendor/bin/phpunit --stop-on-failure

# Filter to specific method
./vendor/bin/phpunit --filter testMethodName
```

PHPUnit 10 removed `--verbose` and its `-v` short form -- the option is declared in `9.6.xsd` and gone from `10.0.xsd` onward. A Drupal 10 project still takes it, because core-dev there resolves PHPUnit 9; on Drupal 11 it exits with `Unknown option "-v"`. `--display-all-issues` is the replacement.

**CI/CD integration (GitLab CI example)**:
```yaml
test:
  script:
    - composer install
    - export SIMPLETEST_BASE_URL=http://localhost
    - export SIMPLETEST_DB=mysql://root:root@mysql/drupal
    - ./vendor/bin/phpunit -c phpunit.xml --testsuite unit,kernel
```

Reference: `/core/tests/README.md` lines 45-79

## Common Mistakes
- Not specifying `-c` flag -- PHPUnit uses wrong config or no config
- Running tests from wrong directory -- paths broken
- Forgetting to start chromedriver for JS tests -- connection failures
- Running all tests when only one module changed -- wastes time (use `--group`)
- Not setting `SIMPLETEST_DB` environment variable -- database tests fail

## See Also
- [Nightwatch.js Testing](nightwatch-testing.md)
- [Coverage Metrics Strategy](coverage-metrics-strategy.md)
- Reference: `/core/tests/README.md`
- [Running Drupal's PHPUnit test suites on DDEV | Matt Glaman](https://mglaman.dev/blog/running-drupals-phpunit-test-suites-ddev)
