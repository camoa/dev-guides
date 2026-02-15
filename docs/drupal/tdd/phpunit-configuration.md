---
description: Set up PHPUnit configuration for Drupal testing with DDEV, local, or CI/CD environments.
---

# PHPUnit Configuration

## When to Use
Before running any PHPUnit tests in Drupal.

## Decision
| Environment | Configuration approach | Why |
|---|---|---|
| Local development with DDEV | Copy phpunit.xml.dist, set SIMPLETEST_BASE_URL to DDEV site URL | DDEV provides database, use http://project.ddev.site |
| Local development without DDEV | Copy phpunit.xml.dist, configure SIMPLETEST_DB manually | Need manual database URL like mysql://user:pass@localhost/db |
| CI/CD pipeline (GitLab, GitHub Actions) | Environment variables, no phpunit.xml file | CI environments set vars dynamically |
| Testing JavaScript | Add chromedriver setup, ensure MINK_DRIVER_ARGS_WEBDRIVER configured | WebDriver requires Selenium/chromedriver on port 4444 |

## Pattern
**Minimal phpunit.xml setup** (copy from `/core/phpunit.xml.dist`):
```xml
<phpunit bootstrap="web/core/tests/bootstrap.php">
  <php>
    <env name="SIMPLETEST_BASE_URL" value="http://project.ddev.site"/>
    <env name="SIMPLETEST_DB" value="mysql://db:db@db/db"/>
    <env name="BROWSERTEST_OUTPUT_DIRECTORY" value="sites/simpletest/browser_output"/>
  </php>
</phpunit>
```

**DDEV-specific paths**: If Drupal is in `web/` subdirectory, adjust bootstrap path accordingly. DDEV database URL is always `mysql://db:db@db/db`.

**Environment variables (CI/CD alternative)**:
```bash
export SIMPLETEST_BASE_URL=http://localhost:8080
export SIMPLETEST_DB=mysql://drupal:drupal@127.0.0.1/test_db
./vendor/bin/phpunit -c web/core
```

Reference: `/core/phpunit.xml.dist` lines 28-60

## Common Mistakes
- Using https:// in SIMPLETEST_BASE_URL for JavaScript tests -- "invalid cookie domain" exception (use http://)
- Forgetting to create sites/simpletest directory -- tests fail on browser output
- Not installing drupal/core-dev -- PHPUnit missing (`composer require drupal/core-dev --dev`)
- Hardcoding absolute paths in phpunit.xml -- breaks when teammates clone repo (use relative paths from project root)
- Committing phpunit.xml to version control -- leaks local environment config (add to .gitignore, commit phpunit.xml.dist instead)

## See Also
- [TDD Workflow: RED-GREEN-REFACTOR](tdd-workflow-red-green-refactor.md)
- [Unit Tests with UnitTestCase](unit-tests.md)
- [Running PHPUnit tests | Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-tests)
- [Setting Up PHPUnit Testing for Drupal in DDEV](https://www.thedroptimes.com/43998/setting-phpunit-testing-drupal-in-ddev-step-step-guide)
