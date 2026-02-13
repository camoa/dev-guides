---
description: Command-line patterns for running and debugging PHPUnit tests in Drupal modules
drupal_version: "11.x"
---

# Running and Debugging Tests

## When to Use

Use this guide when executing tests locally or in CI/CD, or when debugging failing tests.

## Pattern: Running Tests from Command Line

```bash
# Run all tests for a module
./vendor/bin/phpunit -c web/core modules/custom/my_module/tests/

# Run specific test suite
./vendor/bin/phpunit -c web/core --testsuite=unit modules/custom/my_module/
./vendor/bin/phpunit -c web/core --testsuite=kernel modules/custom/my_module/
./vendor/bin/phpunit -c web/core --testsuite=functional modules/custom/my_module/

# Run specific test file
./vendor/bin/phpunit -c web/core modules/custom/my_module/tests/src/Unit/MyServiceTest.php

# Run specific test method
./vendor/bin/phpunit -c web/core --filter testSpecificMethod modules/custom/my_module/

# Run with coverage report
./vendor/bin/phpunit -c web/core --coverage-html reports/coverage modules/custom/my_module/

# Run by @group annotation
./vendor/bin/phpunit -c web/core --group my_module
./vendor/bin/phpunit -c web/core --group Performance

# Run with verbose output
./vendor/bin/phpunit -c web/core --verbose modules/custom/my_module/

# Run JavaScript tests (requires ChromeDriver)
chromedriver --port=9515 &  # Start ChromeDriver first
./vendor/bin/phpunit -c web/core --testsuite=functional-javascript modules/custom/my_module/
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

- **Wrong**: Running JavaScript tests without ChromeDriver running → **Right**: Start ChromeDriver on port 9515 before tests
- **Wrong**: Not setting SIMPLETEST_DB environment variable → **Right**: Configure database connection in phpunit.xml
- **Wrong**: Using wrong PHPUnit config file → **Right**: Use `-c web/core` or module's phpunit.xml
- **Wrong**: Running all tests on every commit → **Right**: Use `--filter` to run specific tests during development
- **Wrong**: Not using `--group` for test organization → **Right**: Tag tests with `@group` and run by group

## See Also

- [Testing Infrastructure Setup](testing-infrastructure-setup.md)
- [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md)
- [Best Practices & Anti-Patterns](best-practices-anti-patterns.md)
- Reference: [Running PHPUnit tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-tests)
- Reference: [Running PHPUnit JavaScript tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-javascript-tests)
