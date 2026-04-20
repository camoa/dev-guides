---
description: Drupal Test-Driven Development guide covering PHPUnit test types, TDD workflow, testing patterns, and quality gates for Drupal 11.x.
guide-meta:
  concepts:
    - Drupal TDD
    - PHPUnit
    - UnitTestCase
    - KernelTestBase
    - BrowserTestBase
    - WebDriverTestBase
    - test traits
    - spec-driven Drupal
    - Nightwatch.js
    - coverage metrics
  not:
    - tool-agnostic TDD theory
    - CI/CD pipeline setup (see drupal/github-actions)
  requires: []
  complements:
    - drupal/testing
    - drupal/github-actions
    - drupal/services
  specializes: development/tdd-spec-driven
  category: drupal
---

# Drupal Test-Driven Development

**Drupal 11.x** | **PHPUnit 10.5+**

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose the right test type | [Test Type Decision Matrix](test-type-decision-matrix.md) | Choose the right test type based on what you're testing and the level of Drupal infrastructure required. |
| Apply RED-GREEN-REFACTOR cycle | [TDD Workflow: RED-GREEN-REFACTOR](tdd-workflow-red-green-refactor.md) | Applying the Test-Driven Development cycle to Drupal module development. Use this workflow when building new features, refactoring existing code, or fixing bugs where the expected behavior can be specified upfront. |
| Set up PHPUnit configuration | [PHPUnit Configuration](phpunit-configuration.md) | Before running any PHPUnit tests in Drupal. |
| Write a unit test | [Unit Tests with UnitTestCase](unit-tests.md) | Testing pure PHP logic with no Drupal dependencies: utility classes, value objects, algorithms, data transformations. |
| Write a kernel test | [Kernel Tests with KernelTestBase](kernel-tests.md) | Testing services, entities, database operations, and other Drupal integrations without HTTP overhead. Sweet spot for most Drupal testing. |
| Write a browser test | [Browser Tests with BrowserTestBase](browser-tests.md) | Testing complete user workflows: page rendering, form submission, access control, multi-step processes requiring HTTP. |
| Write a JavaScript test | [JavaScript Tests with WebDriverTestBase](javascript-tests.md) | Testing JavaScript interactions, AJAX callbacks, dynamic DOM manipulation requiring a real browser. |
| Use test traits | [Test Traits & Utilities](test-traits-utilities.md) | Reusing common test setup patterns: creating users, nodes, content types, blocks, etc. |
| Create a test module | [Test Modules](test-modules.md) | Providing fixtures, mock services, test-specific config, or hooks for testing custom modules. |
| Test a service | [Testing Services](testing-services.md) | Verifying service logic, dependency injection, container integration. |
| Test a plugin | [Testing Plugins](testing-plugins.md) | Testing blocks, field types, field formatters, field widgets, views plugins, and other plugin derivatives. |
| Test a form | [Testing Forms](testing-forms.md) | Verifying form structure, validation, submission, and AJAX behaviors. |
| Test entities | [Testing Entities](testing-entities.md) | Testing entity CRUD, field values, entity references, computed fields, validation. |
| Test permissions | [Testing Access & Permissions](testing-access-permissions.md) | Verifying permission checks, role-based access, entity access, route access. |
| Test routes/controllers | [Testing Routes & Controllers](testing-routes-controllers.md) | Testing custom routes, controller methods, route parameters, response codes. |
| Test configuration | [Testing Configuration](testing-configuration.md) | Testing config schema, config import/export, default config, config overrides. |
| Test events/hooks | [Testing Events & Hooks](testing-events-hooks.md) | Verifying event subscribers work, hooks fire correctly, alter hooks modify data as expected. |
| Apply TDD to Drupal modules | [Spec-Driven Drupal Development](spec-driven-drupal-development.md) | Applying TDD principles to Drupal module development: write specification, write test, implement feature. |
| Test JavaScript with Nightwatch | [Nightwatch.js Testing](nightwatch-testing.md) | JavaScript functional testing for complex UI interactions, accessibility testing, cross-browser testing. |
| Run tests | [Running Tests](running-tests.md) | Executing tests locally, in CI/CD, filtering by group/tag, debugging failures. |
| Measure code coverage | [Coverage Metrics Strategy](coverage-metrics-strategy.md) | Measuring how much of your code is executed during tests, identifying untested code paths, setting coverage targets for CI/CD. |
| Set up quality gates | [Quality Gates & Audit Checklist](quality-gates-audit-checklist.md) | Establishing automated quality checks at different stages of development to catch issues early, enforce standards, and prevent broken code from reaching production. |
| Follow best practices | [Best Practices & Patterns](best-practices-patterns.md) | Writing maintainable, fast, reliable tests that verify behavior, not implementation. |
| Avoid common mistakes | [Anti-Patterns & Common Mistakes](anti-patterns-common-mistakes.md) | Avoid these patterns that lead to slow, brittle, unmaintainable tests. |
| Find test resources | [Code Reference Map](code-reference-map.md) |  |
