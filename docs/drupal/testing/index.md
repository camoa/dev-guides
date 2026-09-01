---
description: Drupal Testing — automated testing frameworks for modules (PHPUnit Unit, Kernel, Functional, FunctionalJavascript, and Gander performance tests)
tracks: []
guide-meta:
  concepts:
    - PHPUnit test types
    - unit tests
    - kernel tests
    - functional tests
    - FunctionalJavascript tests
    - Gander performance testing
    - progressive testing strategy
    - PHPUnit configuration
  not:
    - TDD workflow (see drupal/tdd)
    - GitHub Actions CI (see drupal/github-actions)
  requires: []
  complements:
    - drupal/tdd
    - drupal/github-actions
  category: drupal
---

# Drupal Testing

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand which testing frameworks are available | [Testing Framework Overview](testing-framework-overview.md) | Every Drupal module should include automated testing. Use this guide to understand the five testing frameworks Drupal provides and when each is appropriate. |
| Choose the right test type for my module | [Framework Selection Decision Matrix](framework-selection-decision-matrix.md) | Use this guide when planning testing coverage for a new module or deciding which test type to write for specific functionality. |
| Write tests for pure PHP logic | [PHPUnit Unit Tests](phpunit-unit-tests.md) | Write Unit tests for pure PHP logic that has no Drupal dependencies: calculations, data transformations, validation logic, utility functions, and algorithm implementations. |
| Write tests for services and database integration | [PHPUnit Kernel Tests](phpunit-kernel-tests.md) | Write Kernel tests when you need to test integration with Drupal services, database operations, entity CRUD, or service container interactions without needing a full Drupal installation. |
| Write tests for admin forms and user workflows | [PHPUnit Functional Tests](phpunit-functional-tests.md) | Write Functional tests for complete user workflows: admin configuration forms, content creation/editing, user registration/login, permission testing, and any feature requiring HTTP requests and responses. |
| Write tests for AJAX and JavaScript interactions | [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md) | Write FunctionalJavascript tests only when testing features that require JavaScript execution: AJAX form elements, autocomplete fields, modal dialogs, drag-and-drop interfaces, or client-side validation. |
| Measure performance impact of my module | [Gander Performance Testing](gander-performance-testing.md) | Write Gander performance tests for modules with site-wide performance impact: event subscribers that fire on every request, cache invalidation logic, bulk operations, or features that execute complex queries. |
| Plan testing coverage for a new module | [Progressive Testing Strategy](progressive-testing-strategy.md) | Use this progressive approach when building testing coverage for a new module or improving coverage for an existing module. Start simple and add complexity as the module matures. |
| Set up PHPUnit configuration | [Testing Infrastructure Setup](testing-infrastructure-setup.md) | Configure phpunit.xml and composer.json for Drupal module testing. Drupal 11 uses PHPUnit ^11.5 (via drupal/core-dev) with the PHPUnit 11 schema and <source> element; Drupal 10 uses PHPUnit ^9.x — never declare phpunit/phpunit directly to avoid version conflicts. |
| Follow security and performance best practices | [Best Practices & Anti-Patterns](best-practices-anti-patterns.md) | Consult this guide when writing tests, reviewing code, or establishing testing standards for your team. |
| Run tests from the command line | [Running and Debugging Tests](running-debugging-tests.md) | Use this guide when executing tests locally or in CI/CD, or when debugging failing tests. |
