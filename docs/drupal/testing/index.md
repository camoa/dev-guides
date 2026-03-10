---
description: Drupal Testing — automated testing frameworks for modules (PHPUnit Unit, Kernel, Functional, FunctionalJavascript, and Gander performance tests)
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
  specializes: ""
  category: drupal
---

# Drupal Testing

| I need to... | Guide |
|-------------|-------|
| Understand which testing frameworks are available | [Testing Framework Overview](testing-framework-overview.md) |
| Choose the right test type for my module | [Framework Selection Decision Matrix](framework-selection-decision-matrix.md) |
| Write tests for pure PHP logic | [PHPUnit Unit Tests](phpunit-unit-tests.md) |
| Write tests for services and database integration | [PHPUnit Kernel Tests](phpunit-kernel-tests.md) |
| Write tests for admin forms and user workflows | [PHPUnit Functional Tests](phpunit-functional-tests.md) |
| Write tests for AJAX and JavaScript interactions | [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md) |
| Measure performance impact of my module | [Gander Performance Testing](gander-performance-testing.md) |
| Plan testing coverage for a new module | [Progressive Testing Strategy](progressive-testing-strategy.md) |
| Set up PHPUnit configuration | [Testing Infrastructure Setup](testing-infrastructure-setup.md) |
| Follow security and performance best practices | [Best Practices & Anti-Patterns](best-practices-anti-patterns.md) |
| Run tests from the command line | [Running and Debugging Tests](running-debugging-tests.md) |
