---
description: Write Drupal unit tests with UnitTestCase for pure PHP logic with no Drupal dependencies.
---

# Unit Tests with UnitTestCase

## When to Use
Testing pure PHP logic with no Drupal dependencies: utility classes, value objects, algorithms, data transformations.

## Decision
| If your code needs... | Can you use UnitTestCase? | Alternative |
|---|---|---|
| No database, no services, no Drupal APIs | YES -- ideal use case | -- |
| Configuration from config entities | NO -- requires container | KernelTestBase |
| Entity CRUD operations | NO -- requires database | KernelTestBase |
| Dependency-injected services | MAYBE -- mock the services | KernelTestBase if mocking too complex |
| Translation (t()) or string formatting | YES -- mock TranslationInterface | -- |

## Pattern
**Minimal unit test structure**:
```php
namespace Drupal\Tests\my_module\Unit;

use Drupal\Tests\UnitTestCase;

class MyUtilityClassTest extends UnitTestCase {

  protected function setUp(): void {
    parent::setUp();
    // No Drupal bootstrap, no container
  }

  public function testCalculation(): void {
    $result = MyUtilityClass::calculate(10, 5);
    $this->assertEquals(15, $result);
  }
}
```

**Mocking a service dependency**:
```php
$mock_config = $this->createMock(ConfigFactoryInterface::class);
$mock_config->method('get')->willReturn($config_object_mock);
$service = new MyService($mock_config);
```

**File location**: `modules/my_module/tests/src/Unit/MyUtilityClassTest.php`

Reference: `/core/tests/Drupal/Tests/UnitTestCase.php`

## Common Mistakes
- Testing code that uses `\Drupal::service()` -- fails because container not available (refactor to dependency injection)
- Not mocking all dependencies -- test fails with "Call to member function on null"
- Over-mocking makes test brittle -- if mocking more than 3 services, use KernelTestBase instead
- Testing Drupal core functionality -- test YOUR code, not Drupal's
- Not using `::class` for namespaced classes in mocks -- string typos not caught until runtime

## See Also
- Reference: `/core/tests/Drupal/Tests/UnitTestCase.php`
- Example: `/core/modules/system/tests/src/Unit/Menu/MenuLinkTreeTest.php`
