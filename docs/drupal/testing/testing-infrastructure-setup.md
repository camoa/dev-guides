---
description: Set up directory structure, phpunit.xml configuration, and testing dependencies for Drupal modules
tldr: "Configure phpunit.xml and composer.json for Drupal module testing. Drupal 11 uses PHPUnit ^11.5 (via drupal/core-dev) with the PHPUnit 11 schema and <source> element; Drupal 10 uses PHPUnit ^9.x — never declare phpunit/phpunit directly to avoid version conflicts."
drupal_version: "11.x"
---

# Testing Infrastructure Setup

## When to Use

Use this section when setting up a new module for testing or configuring CI/CD pipelines for automated test execution.

## Decision: Directory Structure

The configuration file sits at the project root. The tests sit in the module.

```
project-root/
├── composer.json
├── phpunit.xml                       # PHPUnit configuration - here, not in the module
├── vendor/
└── web/                              # the docroot: yours may be docroot/, or nothing at all
    └── modules/my_module/
        ├── src/                      # Module source code
        ├── tests/                    # Test files
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
        └── composer.json
```

## Pattern: phpunit.xml Configuration

**Drupal 11** resolves PHPUnit `^11.5.50`, so use the PHPUnit 11 schema and the modern `<source>` element — the old `<coverage>` element was removed in PHPUnit 10. **Drupal 10** resolves PHPUnit `^9.x`. Which version you get is decided by `drupal/core-dev`, not by you; see composer.json Test Dependencies below.

**The docroot is not always `web/`.** It is a convention, not a rule: Acquia projects use `docroot/`, and some projects have Drupal at the repository root with no subfolder at all. A project's own answer is in `composer.json` under `extra.drupal-scaffold.locations.web-root`, and a DDEV project states the same thing as `docroot:` in `.ddev/config.yaml`. Read one of those before you copy a path out of this guide. Wherever the examples below write `web/`, substitute your own docroot, and read a bare module path such as `modules/my_module/tests/` as relative to that docroot. PHPUnit resolves every relative path in the file against the directory holding the file, so a config at the project root reaches down into the docroot — see [Running and Debugging Tests](running-debugging-tests.md) for what breaks when you copy core's `phpunit.xml.dist` up to the root without rewriting it.

**Drupal 11 — phpunit.xml** (PHPUnit 11 schema, `<source>` element):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Placed at the project root, beside composer.json and vendor/. Every path
     below is relative to that root. -->
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/11.5/phpunit.xsd"
         bootstrap="web/core/tests/bootstrap.php"
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
      <directory>web/modules/my_module/tests/src/Unit</directory>
    </testsuite>
    <testsuite name="kernel">
      <directory>web/modules/my_module/tests/src/Kernel</directory>
    </testsuite>
    <testsuite name="functional">
      <directory>web/modules/my_module/tests/src/Functional</directory>
    </testsuite>
    <testsuite name="functional-javascript">
      <directory>web/modules/my_module/tests/src/FunctionalJavascript</directory>
    </testsuite>
  </testsuites>

  <!-- PHPUnit 10+ uses <source> instead of <coverage> -->
  <source>
    <include>
      <directory suffix=".php">web/modules/my_module/src</directory>
    </include>
    <exclude>
      <directory>web/modules/my_module/tests</directory>
    </exclude>
  </source>
</phpunit>
```

Widen the suite directories to `web/modules/custom/*/tests/src/Unit` when the project has several of its own modules, and add `web/themes/custom/*/tests/src/...` when its themes carry tests. The `-c phpunit.xml` in [Running and Debugging Tests](running-debugging-tests.md) points at this file and at no other.

**A contrib module developed in its own checkout is the one exception.** Canvas, for example, ships a `phpunit.xml.dist` beside its own `composer.json` with `bootstrap="../../../core/tests/bootstrap.php"` — enough `../` segments to climb from wherever the module is symlinked or cloned into a host site back out to that site's `core/`. Count those segments against your own checkout; they are not portable between layouts.

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

- Hardcoding database credentials in phpunit.xml → Security risk, version control issues
- Not setting `SIMPLETEST_BASE_URL` → Functional tests fail
- Missing ChromeDriver for JavaScript tests → Tests error with connection failures
- Wrong bootstrap path → Tests can't find Drupal core
- Not excluding test directory from coverage → Inflated coverage metrics
- Declaring `phpunit/phpunit` directly in composer.json → Version conflicts with the one `drupal/core-dev` resolves
- Using the PHPUnit 9 `<coverage>` element on Drupal 11 → The element was removed in PHPUnit 10; use `<source>` with the `11.5` schema URL

**WHY these are mistakes**: PHPUnit configuration must match your environment. Database credentials should come from environment variables, not committed files. Functional and JavaScript tests require specific environment setup. Wrong paths cause cryptic failures. Coverage metrics should only measure production code, not test code.

## See Also

- [Progressive Testing Strategy](progressive-testing-strategy.md)
- [Running and Debugging Tests](running-debugging-tests.md)
- [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md)
- Reference: [Running PHPUnit tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-tests)
- Reference: `/core/phpunit.xml.dist`
