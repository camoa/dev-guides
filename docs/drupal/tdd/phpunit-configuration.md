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

**Minimal phpunit.xml setup for Drupal 11** — copy `/core/phpunit.xml.dist` to `phpunit.xml` at the project root, beside `composer.json`, then rewrite its paths and adjust the env vars. That is where drupal.org's current "Running PHPUnit tests" page puts it: "Make a copy of this file with a name phpunit.xml and place it next to your composer.json file and vendor folder." Every `-c phpunit.xml` in this guide points at that copy.

Do not run tests with `-c web/core`. That reads core's own `phpunit.xml.dist`, whose suites scan every contrib module and whose `SIMPLETEST_DB` ships empty. One broken test class anywhere in contrib can then take down a `--testsuite` run. The same drupal.org page still says `cd core` and shows `-c web/core` in its command examples — an older section it has not reconciled with its own file-placement advice, which is why both forms are in the wild.

**Copying the file is not enough — rewrite the relative paths inside it.** PHPUnit resolves `bootstrap` and every testsuite `<directory>` against the directory holding the config file, and core's dist is written for `core/`. Moved to the project root, `bootstrap="tests/bootstrap.php"` and suite directories such as `modules/**/tests/src/Unit` point at nothing.

drupal.org states the fix for Drupal 11+: "Next to bootstrap=, PATH-TO: The path to your core directory, relative to the phpunit.xml file ... change `bootstrap="PATH-TO/core/tests/bootstrap.php"` to `bootstrap="web/core/tests/bootstrap.php"`". Three parts need the docroot prefix: `bootstrap=`, every testsuite `<directory>`, and the browser-output directory. The last one resolves differently — Drupal's HTML logging extension calls `realpath()` on it, so it is read against the directory you run from, not against the config file.
```xml
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/11.5/phpunit.xsd"
         bootstrap="web/core/tests/bootstrap.php"
         failOnWarning="true">
  <php>
    <env name="SIMPLETEST_BASE_URL" value="http://project.ddev.site"/>
    <env name="SIMPLETEST_DB" value="mysql://db:db@db/db"/>
    <env name="BROWSERTEST_OUTPUT_DIRECTORY" value="web/sites/simpletest/browser_output"/>
  </php>
  <testsuites>
    <testsuite name="unit">
      <directory>web/modules/custom/*/tests/src/Unit</directory>
    </testsuite>
    <testsuite name="kernel">
      <directory>web/modules/custom/*/tests/src/Kernel</directory>
    </testsuite>
    <testsuite name="functional">
      <directory>web/modules/custom/*/tests/src/Functional</directory>
    </testsuite>
    <testsuite name="functional-javascript">
      <directory>web/modules/custom/*/tests/src/FunctionalJavascript</directory>
    </testsuite>
  </testsuites>
</phpunit>
```

Those four suites are what every `--testsuite` command in this guide names, and they cover the project's own modules only. The block is not optional decoration: with no `<testsuites>` at all, `--testsuite unit` is a usage error — PHPUnit prints its usage block and exits 1. Add `web/themes/custom/*/tests/src/...` directories the same way when the project's themes carry tests.

**Drupal 10 fallback**: Change schema to `https://schema.phpunit.de/9.6/phpunit.xsd` and replace `<source>` with `<coverage processUncoveredFiles="true">` if your module targets Drupal 10 only.

**The docroot is not always `web/`**: it is a convention, not a rule. Acquia projects use `docroot/`, and some projects put Drupal at the repository root with no subfolder at all. The project states its own answer in `composer.json` under `extra.drupal-scaffold.locations.web-root`, and a DDEV project repeats it as `docroot:` in `.ddev/config.yaml`. Read one of those before you copy the snippet above. Every rewritten path in it — `bootstrap`, the suite directories, the browser-output directory — carries the docroot in front, while `-c phpunit.xml` itself does not. Wherever this guide writes `web/`, read your project's docroot, and read a bare file location such as `modules/my_module/tests/` as relative to that same docroot.

**DDEV database URL** is always `mysql://db:db@db/db`.

**Environment variables (CI/CD alternative)**:
```bash
export SIMPLETEST_BASE_URL=http://localhost:8080
export SIMPLETEST_DB=mysql://drupal:drupal@127.0.0.1/test_db
./vendor/bin/phpunit -c phpunit.xml
```

Reference: `/core/phpunit.xml.dist` lines 28-60

## Common Mistakes

- Using https:// in SIMPLETEST_BASE_URL for JavaScript tests → "invalid cookie domain" exception (use http://)
- Forgetting to create sites/simpletest directory → tests fail on browser output
- Not installing drupal/core-dev → PHPUnit missing (`composer require drupal/core-dev --dev`)
- Declaring `phpunit/phpunit` explicitly in module composer.json → version conflicts with what core-dev requires; let core-dev pin it
- Hardcoding absolute paths in phpunit.xml → breaks when teammates clone repo (use relative paths from project root)
- Committing phpunit.xml to version control → leaks local environment config (add to .gitignore, commit phpunit.xml.dist instead)
- Using the PHPUnit 9.6 schema on a Drupal 11 project → schema mismatch warnings/errors; match schema to the resolved PHPUnit major version

## See Also

- [TDD Workflow: RED-GREEN-REFACTOR](tdd-workflow-red-green-refactor.md)
- [Unit Tests with UnitTestCase](unit-tests.md)
- Reference: `/core/tests/README.md` lines 22-34
- [Running PHPUnit tests | Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-tests)
- [Setting Up PHPUnit Testing for Drupal in DDEV](https://www.thedroptimes.com/43998/setting-phpunit-testing-drupal-in-ddev-step-step-guide)
