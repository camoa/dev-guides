---
description: Set up directory structure, phpunit.xml configuration, and testing dependencies for Drupal modules
drupal_version: "11.x"
---

# Testing Infrastructure Setup

## When to Use

Use this guide when setting up a new module for testing or configuring CI/CD pipelines for automated test execution.

## Decision: Directory Structure

```
modules/my_module/
├── src/                          # Module source code
├── tests/                        # Test files
│   ├── src/
│   │   ├── Unit/                 # Pure PHP logic tests
│   │   │   ├── Services/
│   │   │   └── Utils/
│   │   ├── Kernel/               # Integration tests
│   │   │   ├── Entity/
│   │   │   └── Services/
│   │   ├── Functional/           # UI and workflow tests
│   │   │   ├── Admin/
│   │   │   └── User/
│   │   └── FunctionalJavascript/ # JS and performance tests
│   │       ├── Ajax/
│   │       └── Performance/
│   └── fixtures/                 # Test data files
├── phpunit.xml                   # PHPUnit configuration
└── composer.json
```

## Pattern: phpunit.xml Configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/9.6/phpunit.xsd"
         bootstrap="../../core/tests/bootstrap.php"
         colors="true"
         beStrictAboutTestsThatDoNotTestAnything="true"
         beStrictAboutOutputDuringTests="true"
         beStrictAboutChangesToGlobalState="true"
         failOnWarning="true">
  
  <php>
    <!-- Required for Functional/JavaScript tests -->
    <env name="SIMPLETEST_BASE_URL" value="http://localhost"/>
    <env name="SIMPLETEST_DB" value="mysql://user:pass@localhost/drupal"/>
    
    <!-- Output directory for browser tests -->
    <env name="BROWSERTEST_OUTPUT_DIRECTORY" value="/tmp/browser_output"/>
    <env name="BROWSERTEST_OUTPUT_FILE" value="/tmp/browser_output.html"/>
    
    <!-- WebDriver configuration for JavaScript tests -->
    <env name="MINK_DRIVER_ARGS_WEBDRIVER" value='["chrome", {"chromeOptions":{"w3c":false}}, "http://localhost:9515"]'/>
  </php>

  <testsuites>
    <testsuite name="unit">
      <directory>./tests/src/Unit</directory>
    </testsuite>
    <testsuite name="kernel">
      <directory>./tests/src/Kernel</directory>
    </testsuite>
    <testsuite name="functional">
      <directory>./tests/src/Functional</directory>
    </testsuite>
    <testsuite name="functional-javascript">
      <directory>./tests/src/FunctionalJavascript</directory>
    </testsuite>
  </testsuites>

  <coverage processUncoveredFiles="true">
    <include>
      <directory suffix=".php">./src</directory>
    </include>
    <exclude>
      <directory>./tests</directory>
    </exclude>
  </coverage>
</phpunit>
```

## Pattern: composer.json Test Dependencies

```json
{
  "name": "drupal/my_module",
  "type": "drupal-module",
  "require": {
    "drupal/core": "^10.3 || ^11"
  },
  "require-dev": {
    "drupal/core-dev": "^10.3 || ^11",
    "phpunit/phpunit": "^9.6",
    "symfony/phpunit-bridge": "^6.4"
  }
}
```

## Common Mistakes

- **Wrong**: Hardcoding database credentials in phpunit.xml → **Right**: Use environment variables or .env files
- **Wrong**: Not setting `SIMPLETEST_BASE_URL` → **Right**: Set base URL for Functional tests
- **Wrong**: Missing ChromeDriver for JavaScript tests → **Right**: Start ChromeDriver before running tests
- **Wrong**: Wrong bootstrap path → **Right**: Use `../../core/tests/bootstrap.php` from module directory
- **Wrong**: Not excluding test directory from coverage → **Right**: Exclude tests/ from coverage metrics

## See Also

- [Progressive Testing Strategy](progressive-testing-strategy.md)
- [Running and Debugging Tests](running-debugging-tests.md)
- [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md)
- Reference: [Running PHPUnit tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-tests)
- Reference: `/core/phpunit.xml.dist`
