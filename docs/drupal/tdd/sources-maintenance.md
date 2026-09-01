---
description: "Source references and maintenance manifest for the tdd guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install
Path: `/home/camoa/workspace/contrib/web/`

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Types of tests - Drupal.org | https://www.drupal.org/docs/develop/automated-testing/types-of-tests | 1, 3, 4, 5 | 2026-02-15 |
| Running PHPUnit tests - Drupal.org | https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-tests | 3, 20 | 2026-02-15 |
| PHPUnit in Drupal - Drupal.org | https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal | 1, 3, 4, 5 | 2026-02-15 |
| Setting Up PHPUnit Testing for Drupal in DDEV - The DropTimes | https://www.thedroptimes.com/43998/setting-phpunit-testing-drupal-in-ddev-step-step-guide | 3 | 2026-02-15 |
| Running PHPUnit JavaScript tests - Drupal.org | https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-javascript-tests | 7 | 2026-02-15 |
| Mocking Entities and Services with PHPUnit - Drupal.org | https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/mocking-entities-and-services-with-phpunit-and-mocks | 10 | 2026-02-15 |
| PHPUnit and Drupal Test Traits - Drupal at your Fingertips | https://www.drupalatyourfingertips.com/dtt | 8 | 2026-02-15 |
| Introduction to Testing in Drupal - Drupalize.me | https://drupalize.me/tutorial/introduction-testing-drupal | 1, 23 | 2026-02-15 |
| Test Driven Development in Drupal - Oliver Davies | https://www.oliverdavies.uk/blog/writing-new-drupal-8-module-using-test-driven-development-tdd | 18 | 2026-02-15 |
| Test Driven Development for Decoupled Drupal - Lullabot | https://www.lullabot.com/articles/test-driven-development-decoupled-drupal | 18, 24 | 2026-02-15 |
| Running Drupal's PHPUnit test suites on DDEV - Matt Glaman | https://mglaman.dev/blog/running-drupals-phpunit-test-suites-ddev | 20 | 2026-02-15 |
| Services and dependency injection in Drupal - Drupal.org | https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/services-and-dependency-injection-in-drupal | 10 | 2026-02-15 |
| JavaScript testing using Nightwatch - Drupal.org | https://www.drupal.org/docs/develop/automated-testing/javascript-testing-using-nightwatch | 19 | 2026-09-01 |
| Change record: JS testing using nightwatch (added in 8.6) | https://www.drupal.org/node/2968570 | 19 | 2026-09-01 |
| #3467492 Replace Nightwatch with Playwright (policy, accepted Nov 2025) | https://www.drupal.org/project/drupal/issues/3467492 | 19 | 2026-09-01 |
| #3553673 Migrate from Nightwatch to Playwright (open, Drupal 12) | https://www.drupal.org/project/drupal/issues/3553673 | 19 | 2026-09-01 |
| #3338664 Migrate Nightwatch Axe tests to PHPUnit (open) | https://www.drupal.org/project/drupal/issues/3338664 | 19 | 2026-09-01 |
| Red, Green, Refactor - Codecademy | https://www.codecademy.com/article/tdd-red-green-refactor | 2 | 2026-02-15 |
| The Cycles of TDD - Uncle Bob | https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html | 2 | 2026-02-15 |
| PCOV or Xdebug - The PHP Consulting Company | https://thephp.cc/articles/pcov-or-xdebug | 21 | 2026-02-15 |
| Code Coverage - PHPUnit Manual | https://docs.phpunit.de/en/10.5/code-coverage.html | 21 | 2026-02-15 |
| Measuring and Improving Code Coverage in PHPUnit - Medium | https://roman-huliak.medium.com/measuring-and-improving-code-coverage-in-phpunit-e1ed275e890f | 21 | 2026-02-15 |
| Git hooks to improve code quality - Medium | https://aicha-fatrah.medium.com/git-hooks-to-improve-code-quality-grumphp-phpcs-phpcpd-and-phpstan-5129b41b94b5 | 22 | 2026-02-15 |
| GitHub Actions workflows for PHP CI/CD | https://zuniweb.com/blog/github-actions-workflows-for-php-ci/cd-with-composer-phpstan-and-deployment/ | 22 | 2026-02-15 |
| Effortless Code Quality: Pre-Commit Hooks Guide for 2025 | https://gatlenculp.medium.com/effortless-code-quality-the-ultimate-pre-commit-hooks-guide-for-2025-57ca501d9835 | 22 | 2026-02-15 |

## Code Sources
| Module | Relative Path | Guide Sections | Drupal Version |
|--------|---------------|----------------|----------------|
| Core tests | `core/tests/` | All | 11.x |
| PHPUnit config | `core/phpunit.xml.dist` | 2 | 11.x |
| Test README | `core/tests/README.md` | 2, 18, 19 | 11.x |
| UnitTestCase | `core/tests/Drupal/Tests/` | 3 | 11.x |
| KernelTestBase | `core/tests/Drupal/KernelTests/` | 4 | 11.x |
| BrowserTestBase | `core/tests/Drupal/Tests/` | 5 | 11.x |
| WebDriverTestBase | `core/tests/Drupal/FunctionalJavascriptTests/` | 6 | 11.x |
| User module tests | `core/modules/user/tests/` | 7, 13 | 11.x |
| Node module tests | `core/modules/node/tests/` | 7, 12, 13, 22 | 11.x |
| Block module tests | `core/modules/block/tests/` | 10, 22 | 11.x |
| System module tests | `core/modules/system/tests/` | 8, 14, 22 | 11.x |
| Nightwatch tests | `core/tests/Drupal/Nightwatch/` | 18 | 11.x |
| Test traits | `core/tests/Drupal/Tests/Traits/` | 7 | 11.x |

---
