---
description: Set up directory structure, phpunit.xml configuration, and testing dependencies for Drupal modules
tldr: "Configure phpunit.xml and composer.json for Drupal module testing. Drupal 11 uses PHPUnit ^11.5 (via drupal/core-dev) with the PHPUnit 11 schema and <source> element; Drupal 10 uses PHPUnit ^9.x — never declare phpunit/phpunit directly to avoid version conflicts."
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

**Drupal 11** uses PHPUnit `^11.5.50` (resolved transitively from `drupal/core-dev`). Use the PHPUnit 11 schema and the modern `<source>` element — the old `<coverage>` element was removed in PHPUnit 10. **Drupal 10** uses PHPUnit `^9.x`. Never hardcode the PHPUnit version directly; always declare `drupal/core-dev` and let Composer resolve the correct PHPUnit version for your target core.

**Drupal 11 — phpunit.xml** (PHPUnit 11 schema, `<source>` element):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/11.5/phpunit.xsd"
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

  <!-- PHPUnit 10+ uses <source> instead of <coverage> -->
  <source>
    <include>
      <directory suffix=".php">./src</directory>
    </include>
    <exclude>
      <directory>./tests</directory>
    </exclude>
  </source>
</phpunit>
```

**Drupal 10 fallback**: If you must support only Drupal 10, change the schema to `https://schema.phpunit.de/9.6/phpunit.xsd` and replace `<source>` with `<coverage processUncoveredFiles="true">`. Copy the base config from `/core/phpunit.xml.dist` for the target core version.

## Pattern: composer.json Test Dependencies

Do **not** declare `phpunit/phpunit` directly — it is pulled in transitively by `drupal/core-dev` at the version appropriate for your target core. Declaring it explicitly risks version conflicts.

```json
{
  "name": "drupal/my_module",
  "type": "drupal-module",
  "require": {
    "drupal/core": "^10.3 || ^11"
  },
  "require-dev": {
    "drupal/core-dev": "^10.3 || ^11"
  }
}
```

`drupal/core-dev` brings in PHPUnit `^9.x` for Drupal 10 and `^11.5.50` for Drupal 11. If your module drops Drupal 10 support: `"drupal/core-dev": "^11"` is sufficient.

## Common Mistakes

- **Wrong**: Hardcoding database credentials in phpunit.xml → **Right**: Use environment variables or .env files
- **Wrong**: Not setting `SIMPLETEST_BASE_URL` → **Right**: Set base URL for Functional tests
- **Wrong**: Missing ChromeDriver for JavaScript tests → **Right**: Start ChromeDriver before running tests
- **Wrong**: Wrong bootstrap path → **Right**: Use `../../core/tests/bootstrap.php` from module directory
- **Wrong**: Not excluding test directory from coverage → **Right**: Exclude tests/ from coverage metrics
- **Wrong**: Declaring `phpunit/phpunit` directly in composer.json → **Right**: Use `drupal/core-dev` and let it resolve the correct PHPUnit version
- **Wrong**: Using PHPUnit 9 `<coverage>` element in Drupal 11 → **Right**: Use PHPUnit 11 `<source>` element with the `11.5` schema URL

## See Also

- [Progressive Testing Strategy](progressive-testing-strategy.md)
- [Running and Debugging Tests](running-debugging-tests.md)
- [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md)
- Reference: [Running PHPUnit tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-tests)
- Reference: `/core/phpunit.xml.dist`
