---
description: Set up PHPUnit configuration for Drupal 11 testing with DDEV, local, or CI/CD environments using PHPUnit ^11.5.x via drupal/core-dev.
tldr: "Before running any PHPUnit tests in Drupal, copy /core/phpunit.xml.dist and set SIMPLETEST_BASE_URL and SIMPLETEST_DB. PHPUnit resolves transitively from drupal/core-dev — Drupal 11 requires ^11.5.50, Drupal 10 requires ^9.x. Never declare phpunit/phpunit directly in your module's composer.json."
drupal_version: "11.x"
---

# PHPUnit Configuration

## When to Use

> Before running any PHPUnit tests in Drupal.

## Decision

| Environment | Configuration approach | Why |
|---|---|---|
| Local development with DDEV | Copy phpunit.xml.dist, set SIMPLETEST_BASE_URL to DDEV site URL | DDEV provides database, use http://project.ddev.site |
| Local development without DDEV | Copy phpunit.xml.dist, configure SIMPLETEST_DB manually | Need manual database URL like mysql://user:pass@localhost/db |
| CI/CD pipeline (GitLab, GitHub Actions) | Environment variables, no phpunit.xml file | CI environments set vars dynamically |
| Testing JavaScript | Add chromedriver setup, ensure MINK_DRIVER_ARGS_WEBDRIVER configured | WebDriver requires Selenium/chromedriver on port 4444 |

## Pattern

**PHPUnit version by Drupal core**: Do **not** declare `phpunit/phpunit` in your module's `composer.json` — it resolves transitively from `drupal/core-dev`:
- **Drupal 11**: `drupal/core-dev ^11` → PHPUnit `^11.5.50`
- **Drupal 10**: `drupal/core-dev ^10` → PHPUnit `^9.x`

**Minimal phpunit.xml setup for Drupal 11** (copy from `/core/phpunit.xml.dist` and adjust env vars):
```xml
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/11.5/phpunit.xsd"
         bootstrap="web/core/tests/bootstrap.php"
         failOnWarning="true">
  <php>
    <env name="SIMPLETEST_BASE_URL" value="http://project.ddev.site"/>
    <env name="SIMPLETEST_DB" value="mysql://db:db@db/db"/>
    <env name="BROWSERTEST_OUTPUT_DIRECTORY" value="sites/simpletest/browser_output"/>
  </php>
</phpunit>
```

**Drupal 10 fallback**: Change schema to `https://schema.phpunit.de/9.6/phpunit.xsd` and replace `<source>` with `<coverage processUncoveredFiles="true">` if your module targets Drupal 10 only.

**DDEV-specific paths**: If Drupal is in `web/` subdirectory, adjust bootstrap path accordingly. DDEV database URL is always `mysql://db:db@db/db`.

**Environment variables (CI/CD alternative)**:
```bash
export SIMPLETEST_BASE_URL=http://localhost:8080
export SIMPLETEST_DB=mysql://drupal:drupal@127.0.0.1/test_db
./vendor/bin/phpunit -c web/core
```

Reference: `/core/phpunit.xml.dist` lines 28-60

## Common Mistakes

- **Wrong**: Using https:// in SIMPLETEST_BASE_URL for JavaScript tests → **Right**: Use http:// or get "invalid cookie domain" exception
- **Wrong**: Forgetting to create sites/simpletest directory → **Right**: Create it before running browser tests
- **Wrong**: Not installing drupal/core-dev → **Right**: `composer require drupal/core-dev --dev` (PHPUnit comes from here)
- **Wrong**: Declaring `phpunit/phpunit` explicitly in module composer.json → **Right**: Let core-dev pin it; explicit declarations cause version conflicts
- **Wrong**: Hardcoding absolute paths in phpunit.xml → **Right**: Use relative paths from project root so teammates don't break
- **Wrong**: Committing phpunit.xml to version control → **Right**: Add to .gitignore, commit phpunit.xml.dist instead
- **Wrong**: Using the PHPUnit 9.6 schema on a Drupal 11 project → **Right**: Match schema to the resolved PHPUnit major version (`11.5` for Drupal 11)

## See Also

- [TDD Workflow: RED-GREEN-REFACTOR](tdd-workflow-red-green-refactor.md)
- [Unit Tests with UnitTestCase](unit-tests.md)
- Reference: `/core/tests/README.md` lines 22-34
- [Running PHPUnit tests | Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-tests)
- [Setting Up PHPUnit Testing for Drupal in DDEV](https://www.thedroptimes.com/43998/setting-phpunit-testing-drupal-in-ddev-step-step-guide)
