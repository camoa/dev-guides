---
description: Test Drupal services with unit mocks, kernel container integration, and service replacement patterns.
---

# Testing Services

## When to Use
Verifying service logic, dependency injection, container integration.

## Decision
| Service uses... | Test type | Pattern |
|---|---|---|
| No Drupal dependencies | Unit | Mock all dependencies |
| Database, config, entities | Kernel | Use real container |
| HTTP context, current route | Browser | Full Drupal install |

## Pattern
**Unit test with mocked dependencies**:
```php
namespace Drupal\Tests\my_module\Unit;

use Drupal\my_module\Service\DataProcessor;
use Drupal\Tests\UnitTestCase;

class DataProcessorTest extends UnitTestCase {

  public function testProcessData(): void {
    $mock_logger = $this->createMock(LoggerInterface::class);
    $mock_logger->expects($this->once())->method('info');

    $service = new DataProcessor($mock_logger);
    $result = $service->processData(['key' => 'value']);

    $this->assertEquals('processed', $result['status']);
  }
}
```

**Kernel test with real container**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;

class MyServiceTest extends KernelTestBase {

  protected static $modules = ['system', 'my_module'];

  public function testServiceIntegration(): void {
    $service = $this->container->get('my_module.my_service');
    $result = $service->doSomething();
    $this->assertNotEmpty($result);
  }
}
```

**Replacing service with mock in Kernel test**:
```php
use Drupal\Core\DependencyInjection\ServiceModifierInterface;

class MyServiceTest extends KernelTestBase implements ServiceModifierInterface {

  public function alter(ContainerBuilder $container): void {
    $container->getDefinition('my_module.external_api')
      ->setClass(MockExternalApi::class);
  }
}
```

Reference: `/core/modules/system/tests/src/Unit/Routing/AdminRouteSubscriberTest.php`

## Common Mistakes
- Using `\Drupal::service()` in service class -- impossible to unit test (inject dependencies via constructor)
- Not mocking external API calls -- tests fail when API down, slow tests
- Testing service in isolation when integration matters -- use Kernel test to verify container wiring
- Over-mocking makes test meaningless -- if mocking everything, test verifies nothing
- Forgetting to call `expects()` on mock -- mock created but never verified

## See Also
- [Test Modules](test-modules.md)
- [Testing Plugins](testing-plugins.md)
- [Mocking Entities and Services with PHPUnit | Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/mocking-entities-and-services-with-phpunit-and-mocks)
- [Services and dependency injection in Drupal](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/services-and-dependency-injection-in-drupal)
