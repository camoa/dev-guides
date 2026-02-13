---
description: Overview of Drupal's five testing frameworks and when to use each one
drupal_version: "11.x"
---

# Testing Framework Overview

## When to Use

Every Drupal module should include automated testing. Use this guide to understand the five testing frameworks Drupal provides and when each is appropriate.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Test pure PHP logic with no Drupal dependencies | PHPUnit Unit Tests | Fastest execution, no database or container overhead |
| Test service integration with database and container | PHPUnit Kernel Tests | Minimal bootstrap, access to Drupal services |
| Test complete user workflows via HTTP | PHPUnit Functional Tests | Full Drupal installation, simulated browser |
| Test JavaScript and AJAX interactions | PHPUnit FunctionalJavascript Tests | Real browser with WebDriver, executes JavaScript |
| Measure performance impact and regression | Gander Performance Tests | OpenTelemetry tracing, performance budgets |

## Pattern

```php
// Core Drupal Testing Frameworks (5 Active)

// 1. Unit Tests - tests/src/Unit/
namespace Drupal\Tests\my_module\Unit;
use Drupal\Tests\UnitTestCase;

// 2. Kernel Tests - tests/src/Kernel/
namespace Drupal\Tests\my_module\Kernel;
use Drupal\KernelTests\KernelTestBase;

// 3. Functional Tests - tests/src/Functional/
namespace Drupal\Tests\my_module\Functional;
use Drupal\Tests\BrowserTestBase;

// 4. FunctionalJavascript Tests - tests/src/FunctionalJavascript/
namespace Drupal\Tests\my_module\FunctionalJavascript;
use Drupal\FunctionalJavascriptTests\WebDriverTestBase;

// 5. Gander Performance Tests - tests/src/FunctionalJavascript/
namespace Drupal\Tests\my_module\FunctionalJavascript;
use Drupal\FunctionalJavascriptTests\PerformanceTestBase;
```

**Note**: Nightwatch.js is deprecated as of Drupal 9.4 and should not be used for new tests.

## Common Mistakes

- **Wrong**: Using Functional tests when Unit/Kernel would suffice → **Right**: Use the simplest test type that validates your code (faster execution and easier maintenance)
- **Wrong**: Not testing at all → **Right**: Start with minimal Unit/Kernel coverage for core logic
- **Wrong**: Skipping JavaScript tests for AJAX features → **Right**: Use FunctionalJavascript for any AJAX or client-side interactions
- **Wrong**: Testing everything in one test method → **Right**: One test method per behavior, use `@dataProvider` for variations
- **Wrong**: Not using `@dataProvider` for similar test cases → **Right**: DRY principle applies to tests too

## See Also

- [Framework Selection Decision Matrix](framework-selection-decision-matrix.md)
- [PHPUnit Unit Tests](phpunit-unit-tests.md)
- [PHPUnit Kernel Tests](phpunit-kernel-tests.md)
- [PHPUnit Functional Tests](phpunit-functional-tests.md)
- Reference: [Types of tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/types-of-tests)
- Reference: [PHPUnit in Drupal - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal)
