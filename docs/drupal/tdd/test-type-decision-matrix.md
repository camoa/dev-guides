---
description: Choose the right Drupal test type based on what you need to test and the level of infrastructure required.
---

# Test Type Decision Matrix

## When to Use
Choose the right test type based on what you're testing and the level of Drupal infrastructure required.

## Decision
| If you need to test... | Use... | Why |
|---|---|---|
| Pure PHP logic with no Drupal dependencies | Unit Test (UnitTestCase) | Fastest execution, no database, no container overhead |
| Service integration, database access, entity API without HTTP | Kernel Test (KernelTestBase) | Lightweight Drupal bootstrap, container access, database available |
| Full page rendering, form submission, HTTP requests without JavaScript | Browser Test (BrowserTestBase) | Complete Drupal installation, simulates user browsing |
| JavaScript interactions, AJAX callbacks, DOM manipulation | JavaScript Test (WebDriverTestBase) | Real browser with JS engine via Selenium/chromedriver |
| Composer/build scripts, project scaffolding | Build Test | Tests project structure without Drupal bootstrap |

## Pattern
Test type hierarchy from fastest to slowest:
```
Unit (milliseconds)
  -> no Drupal, pure PHP
Kernel (seconds)
  -> partial bootstrap, services + database
Browser (10+ seconds)
  -> full install, HTTP simulation
JavaScript (20+ seconds)
  -> full install + real browser + JS engine
```

**Speed vs Coverage tradeoff**: Always use the lightest test type that can verify your requirement. Don't use BrowserTestBase to test business logic that UnitTestCase can cover.

## Common Mistakes
- Using BrowserTestBase when KernelTestBase would suffice -- 10x slower tests with no benefit
- Writing Unit tests for code that requires database or container -- tests fail or require extensive mocking that defeats the purpose
- Testing Drupal core functionality instead of your custom code -- wastes time, core already tested
- Not using #[Group] attributes -- impossible to run tests selectively
- Mixing test concerns (testing form + validation + rendering in one test) -- brittle tests that fail for multiple reasons

## See Also
- Reference: `/core/tests/README.md`
- Official documentation: [Types of tests | Drupal.org](https://www.drupal.org/docs/develop/automated-testing/types-of-tests)
