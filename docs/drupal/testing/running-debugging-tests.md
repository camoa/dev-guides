---
description: Command-line patterns for running and debugging PHPUnit tests in Drupal modules
tldr: "Use this guide when executing tests locally or in CI/CD, or when debugging failing tests."
drupal_version: "11.x"
---

# Running and Debugging Tests

## When to Use

Use this section when executing tests locally or in CI/CD, or when debugging failing tests.

## Pattern: Running Tests from Command Line

Point `-c` at your own `phpunit.xml` at the project root, beside `composer.json` and `vendor/`. That is where drupal.org's current "Running PHPUnit tests" page puts it, in words and in a directory diagram: "Make a copy of this file with a name phpunit.xml and place it next to your composer.json file and vendor folder." One honest caveat: the command section further down that same page has not been reconciled with it and still says "All example commands in this document assumes that you and the configuration file phpunit.xml are located in the core directory: `cd core`", showing `-c web/core`. That is why you will meet both forms in the wild.

**Copying the file is not the whole job — its paths have to be rewritten.** PHPUnit resolves every relative path in a configuration file against the directory that file sits in, and core's `phpunit.xml.dist` is written for `core/`. Three things in the copy break the moment it moves to the project root:

- **`bootstrap=`** — core ships `bootstrap="tests/bootstrap.php"`. drupal.org states the fix for Drupal 11+: `PATH-TO` is "the path to your core directory, relative to the phpunit.xml file", so change `bootstrap="PATH-TO/core/tests/bootstrap.php"` to `bootstrap="web/core/tests/bootstrap.php"` for a `web/` docroot.
- **the browser-output directory** — the `outputDirectory` parameter on the HTML output logging extension, `sites/simpletest/browser_output` in core's copy. Core's own comment says it resolves against the working directory of the process running PHPUnit, so it no longer lands where you expect once you run from the project root.
- **every `<directory>` in the testsuites** — core's suites read `tests/Drupal/Tests`, `modules/**/tests/src/Unit` and `../modules/*/**/tests/src/Unit`, all relative to `core/`. From the project root they point at nothing, so each one needs the docroot in front: `web/core/tests/Drupal/Tests`, `web/modules/*/**/tests/src/Unit`.

Fill in `SIMPLETEST_DB` and `SIMPLETEST_BASE_URL` while you are in there. Core's `phpunit.xml.dist`, the file you copied from, ships both empty.

Do **not** reach for `-c <docroot>/core` instead. That reads core's own `phpunit.xml.dist`, whose suites scan every contrib module on the site (`../modules/*/**/tests/src/...`). Run a whole suite that way and one broken test class anywhere in contrib takes your run down with it — a risk that belongs to the suite form alone, because a path argument never maps the configured suites at all.

**`--testsuite` and a path argument do not combine.** When a path argument is present PHPUnit ignores the configured suites entirely, so the `--testsuite` flag is silently dropped and the path decides what runs. Pick one shape per command: a suite-wide run with `--testsuite` and no path, or a path-scoped run with a path and no `--testsuite`.

```bash
# Run from the project root, beside composer.json and phpunit.xml.
# Set DOCROOT to your project's own docroot - see Testing Infrastructure Setup.
DOCROOT=web

# Suite-wide: the suites in phpunit.xml decide what runs, so no path argument.
./vendor/bin/phpunit -c phpunit.xml --testsuite=unit
./vendor/bin/phpunit -c phpunit.xml --testsuite=kernel
./vendor/bin/phpunit -c phpunit.xml --testsuite=functional

# Path-scoped: the path decides what runs, so no --testsuite flag.
# All tests for a module:
./vendor/bin/phpunit -c phpunit.xml "$DOCROOT/modules/my_module/tests/"
# One test type for a module:
./vendor/bin/phpunit -c phpunit.xml "$DOCROOT/modules/my_module/tests/src/Kernel"
# One test file:
./vendor/bin/phpunit -c phpunit.xml "$DOCROOT/modules/my_module/tests/src/Unit/MyServiceTest.php"

# Run specific test method
./vendor/bin/phpunit -c phpunit.xml --filter testSpecificMethod "$DOCROOT/modules/my_module/"

# Run with coverage report
./vendor/bin/phpunit -c phpunit.xml --coverage-html reports/coverage "$DOCROOT/modules/my_module/"

# Run by group
./vendor/bin/phpunit -c phpunit.xml --group my_module
./vendor/bin/phpunit -c phpunit.xml --group Performance

# Show the details of every issue a test triggers.
# PHPUnit 10 removed --verbose, so on Drupal 11 use --display-all-issues.
# --verbose still works on Drupal 10, which runs PHPUnit 9.
./vendor/bin/phpunit -c phpunit.xml --display-all-issues "$DOCROOT/modules/my_module/"

# Run JavaScript tests (requires ChromeDriver)
chromedriver --port=9515 &  # Start ChromeDriver first
./vendor/bin/phpunit -c phpunit.xml --testsuite=functional-javascript
```

## Pattern: Debugging Test Failures

```php
// Add debug output to tests
public function testDebugExample(): void {
  $result = $this->service->process($data);
  
  // Dump variables
  var_dump($result);
  print_r($result);
  
  // Use PHPUnit assertions for better error messages
  $this->assertEquals(
    'expected_value',
    $result,
    'Custom message: Result did not match expected value'
  );
  
  // Debug page content in Functional tests
  $this->drupalGet('some/path');
  file_put_contents('/tmp/debug.html', $this->getSession()->getPage()->getContent());
  
  // Debug JavaScript console in FunctionalJavascript tests
  $logs = $this->getSession()->getDriver()->getWebDriverSession()->log('browser');
  var_dump($logs);
}
```

## Pattern: Using BROWSERTEST_OUTPUT_DIRECTORY

```xml
<!-- In phpunit.xml -->
<env name="BROWSERTEST_OUTPUT_DIRECTORY" value="/tmp/browser_output"/>
<env name="BROWSERTEST_OUTPUT_FILE" value="browser_output.html"/>
```

When Functional or FunctionalJavascript tests fail, Drupal writes HTML output to this directory for inspection.

## Decision: ChromeDriver Setup for JavaScript Tests

| Environment | Setup Command | Notes |
|-------------|---------------|-------|
| **Local (Linux)** | `chromedriver --port=9515 &` | Start before running tests |
| **Local (Mac)** | `chromedriver --port=9515 &` | Install via `brew install chromedriver` |
| **Docker** | Use selenium/standalone-chrome image | Configure MINK_DRIVER_ARGS_WEBDRIVER |
| **CI/CD** | Install chromedriver in pipeline | Run as background process |

## Common Mistakes

- Running JavaScript tests without ChromeDriver running → Connection refused errors
- Not setting SIMPLETEST_DB environment variable → Database connection failures
- Using wrong PHPUnit config file → Tests can't find bootstrap
- Running all tests on every commit → Slow feedback loop
- Not using `--filter` for debugging → Running hundreds of tests to debug one

**WHY these are mistakes**: Test infrastructure must be properly configured or tests fail with cryptic errors. ChromeDriver is a separate process that must be running. Environment variables configure test database and base URL. Running full test suites on every code change wastes time - use `--filter` to run specific tests during development.

## See Also

- [Testing Infrastructure Setup](testing-infrastructure-setup.md)
- [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md)
- [Best Practices & Anti-Patterns](best-practices-anti-patterns.md)
- Reference: [Running PHPUnit tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-tests)
- Reference: [Running PHPUnit JavaScript tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-javascript-tests)
