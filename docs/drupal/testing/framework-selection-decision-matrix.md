---
description: Decision matrix for selecting the right testing framework based on module complexity and component type
drupal_version: "11.x"
---

# Framework Selection Decision Matrix

## When to Use

Use this guide when planning testing coverage for a new module or deciding which test type to write for specific functionality.

## Decision: Module Complexity Categories

| Module Type | Characteristics | Testing Framework | Setup Time |
|-------------|-----------------|-------------------|------------|
| **Category A: Simple/Utility** | Single service, minimal config, few dependencies | Unit + Kernel | 1-2 hours |
| **Category B: Feature** | Multiple services, admin interfaces, entity integration | Unit + Kernel + Functional | 3-4 hours |
| **Category C: Complex/System** | Multiple submodules, AJAX UI, external APIs, performance impact | Unit + Kernel + Functional + FunctionalJS + Gander | 8+ hours |

## Decision: Component-Based Selection

| Component | Question | Framework | Example |
|-----------|----------|-----------|---------|
| Business Logic | Custom calculations or algorithms? | Unit | Token processors, data transformers |
| Services | Dependency injection? Container interaction? | Kernel | Entity processors, API clients |
| Database | Entity operations? Database queries? | Kernel | Custom entity storage, query builders |
| Admin UI | Configuration forms? Admin interfaces? | Functional | Settings pages, content management |
| User Workflows | Multi-step processes? Form submissions? | Functional | Registration flows, checkout processes |
| AJAX/JavaScript | Dynamic form elements? JavaScript behaviors? | FunctionalJavascript | Autocomplete, live validation |
| Performance | Site-wide performance impact? | Gander | Event subscribers, cache invalidation |

## Pattern: Progressive Testing Strategy

```php
// MVP (Minimum Viable Testing) - 30-40% coverage
tests/src/Unit/MyServiceTest.php          // Core business logic
tests/src/Kernel/MyEntityProcessorTest.php // Drupal integration

// Feature Complete - 60-70% coverage  
tests/src/Functional/AdminFormTest.php     // Add admin UI testing

// Production Ready - 80%+ coverage
tests/src/FunctionalJavascript/AjaxTest.php    // Add JavaScript testing
tests/src/FunctionalJavascript/PerformanceTest.php // Add performance testing
```

## Common Mistakes

- **Wrong**: Starting with FunctionalJavascript tests → **Right**: Write simpler Unit/Kernel tests first to build foundation
- **Wrong**: Testing everything at the Functional level → **Right**: Use fastest test type that validates the behavior
- **Wrong**: Skipping Kernel tests → **Right**: Kernel tests catch integration issues between services
- **Wrong**: Writing performance tests too early → **Right**: Add performance tests after features stabilize
- **Wrong**: Not documenting test type decisions → **Right**: Document coverage goals in README or test base classes

## See Also

- [Testing Framework Overview](testing-framework-overview.md)
- [Progressive Testing Strategy](progressive-testing-strategy.md)
- [PHPUnit Unit Tests](phpunit-unit-tests.md)
- Reference: [Specbee - Write Your First Test Case Using PHPUnit & Kernel in Drupal](https://www.specbee.com/blogs/write-your-first-test-case-using-phpunit-kernel-in-drupal)
