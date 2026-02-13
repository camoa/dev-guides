---
description: Write PHPUnit Unit tests for pure PHP logic with no Drupal dependencies
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

/**
 * Tests the Calculator service.
 *
 * @group my_module
 * @coversDefaultClass \Drupal\my_module\Calculator
 */
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

  /**
   * @covers ::add
   * @dataProvider additionProvider
   */
  public function testAdd($a, $b, $expected): void {
    $result = $this->calculator->add($a, $b);
    $this->assertEquals($expected, $result);
  }

  public function additionProvider(): array {
    return [
      'positive numbers' => [2, 3, 5],
      'negative numbers' => [-2, -3, -5],
      'mixed signs' => [10, -5, 5],
      'with zero' => [0, 5, 5],
    ];
  }

  /**
   * @covers ::divide
   */
  public function testDivideByZeroThrowsException(): void {
    $this->expectException(\InvalidArgumentException::class);
    $this->expectExceptionMessage('Division by zero');
    
    $this->calculator->divide(10, 0);
  }
}
```

**File Location**: `modules/my_module/tests/src/Unit/CalculatorTest.php`

## Common Mistakes

- **Wrong**: Bootstrapping Drupal in unit tests → **Right**: Use Kernel tests for Drupal integration
- **Wrong**: Not mocking dependencies → **Right**: Mock all external dependencies for isolation
- **Wrong**: Testing multiple behaviors in one test → **Right**: Use `@dataProvider` for variations
- **Wrong**: Forgetting `parent::setUp()` → **Right**: Always call parent setup methods
- **Wrong**: Not using `@covers` annotation → **Right**: Document what code is being tested

## See Also

- [Framework Selection Decision Matrix](framework-selection-decision-matrix.md)
- [PHPUnit Kernel Tests](phpunit-kernel-tests.md)
- Reference: [Mocking Entities and Services with PHPUnit - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/mocking-entities-and-services-with-phpunit-and-mocks)
- Reference: `/core/tests/Drupal/Tests/UnitTestCase.php`
