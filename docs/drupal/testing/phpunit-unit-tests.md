---
description: Write PHPUnit Unit tests for pure PHP logic with no Drupal dependencies
tldr: "Write Unit tests for pure PHP logic that has no Drupal dependencies: calculations, data transformations, validation logic, utility functions, and algorithm implementations."
drupal_version: "11.x"
---

# PHPUnit Unit Tests

## When to Use

Write Unit tests for pure PHP logic that has no Drupal dependencies: calculations, data transformations, validation logic, utility functions, and algorithm implementations.

## Decision

| If your code... | Use Unit Tests | Why |
|-----------------|----------------|-----|
| Has no Drupal service dependencies | Yes | Fastest execution, no container overhead |
| Can be tested with mocked dependencies | Yes | Full control over test environment |
| Performs calculations or transformations | Yes | Pure logic testing without side effects |
| Requires database or entity operations | No, use Kernel | Unit tests don't have database access |
| Needs configuration or services from container | No, use Kernel | Unit tests don't bootstrap container |

## Pattern

```php
<?php
namespace Drupal\Tests\my_module\Unit;

use Drupal\Tests\UnitTestCase;
use Drupal\my_module\Calculator;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\Attributes\Group;

/**
 * Tests the Calculator service.
 */
#[Group('my_module')]
#[CoversClass(Calculator::class)]
class CalculatorTest extends UnitTestCase {

  protected Calculator $calculator;

  protected function setUp(): void {
    parent::setUp();
    
    // Mock dependencies
    $configFactory = $this->getConfigFactoryStub([
      'my_module.settings' => ['precision' => 2],
    ]);
    
    $this->calculator = new Calculator($configFactory);
  }

  #[DataProvider('additionProvider')]
  public function testAdd($a, $b, $expected): void {
    $result = $this->calculator->add($a, $b);
    $this->assertEquals($expected, $result);
  }

  public static function additionProvider(): array {
    return [
      'positive numbers' => [2, 3, 5],
      'negative numbers' => [-2, -3, -5],
      'mixed signs' => [10, -5, 5],
      'with zero' => [0, 5, 5],
    ];
  }

  public function testDivideByZeroThrowsException(): void {
    $this->expectException(\InvalidArgumentException::class);
    $this->expectExceptionMessage('Division by zero');
    
    $this->calculator->divide(10, 0);
  }
}
```

**File Location**: `modules/my_module/tests/src/Unit/CalculatorTest.php`

**Test metadata belongs in PHP attributes, not doc-comments.** PHPUnit 11.5.56, the runner Drupal 11.4.5 resolves, prints a runner deprecation the moment it reads metadata from a doc-comment: `Metadata in doc-comments is deprecated and will no longer be supported in PHPUnit 12. Update your test code to use attributes instead.` Core has already moved — 317 test files in core's `node` and `user` modules carry `#[Group(...)]`, and none carry the `@group` annotation. Core's test discovery still parses the annotation first, so the old form keeps working today and you will meet it in older modules; write attributes in new code. Use `#[CoversClass(...)]` for class-level coverage, or `#[CoversMethod(Calculator::class, 'add')]` when you want per-method precision — pick one and stay with it.

## Common Mistakes

- Bootstrapping Drupal in unit tests → Use Kernel tests instead
- Not mocking dependencies → Tests become integration tests
- Testing multiple behaviors in one test → Use `#[DataProvider]` for variations
- Forgetting `parent::setUp()` → Missing critical test setup
- Not using `#[CoversClass]` → Unclear what code is being tested
- Declaring a data provider as `public function` instead of `public static function` → PHPUnit prints `Data Provider method ...::additionProvider() is not static`, then `No tests found in class` and `No tests executed!`, and exits 2

**WHY these are mistakes**: Unit tests must be fast and isolated. Bootstrapping Drupal defeats the purpose. Unmocked dependencies create fragile tests that break when dependencies change. Multiple behaviors in one test make failures harder to diagnose. A non-static data provider is the costliest of these. PHPUnit does not fail the one test: it drops every test the provider feeds, and when that is the only test in the class the run prints `No tests found in class` and `No tests executed!`. A class with other tests keeps them and prints `ERRORS!` instead. Either way the provider's own cases are never asserted.

## See Also

- [Framework Selection Decision Matrix](framework-selection-decision-matrix.md)
- [PHPUnit Kernel Tests](phpunit-kernel-tests.md)
- Reference: [Mocking Entities and Services with PHPUnit - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/mocking-entities-and-services-with-phpunit-and-mocks)
- Reference: `/core/tests/Drupal/Tests/UnitTestCase.php`
