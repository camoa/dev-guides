---
description: Test plugin architectures with PHPUnit unit and functional tests
drupal_version: "11.x"
---

# Testing & Debugging

## When to Use

> Test plugin architectures at unit level for plugin managers and service collectors. Use functional tests for REST API endpoints and integration workflows.

## Decision

| Test Type | Use When | Why |
|-----------|----------|-----|
| Unit tests | Plugin manager logic | Isolate plugin discovery and instantiation |
| Unit tests | Service collector aggregation | Test service collection without container |
| Unit tests | Provider proxy event dispatching | Verify event flow without external dependencies |
| Functional tests | REST API endpoints | Test full HTTP request/response cycle |
| Functional tests | Plugin integration workflows | Verify multi-plugin coordination |

## Pattern

**Foundation Pattern - Unit Test**:

```php
<?php
namespace Drupal\Tests\foundation_module\Unit;

use PHPUnit\Framework\TestCase;

class ServiceGatewayTest extends TestCase {
  public function testGatewayExecution() {
    $gateway = $this->createMockGateway();

    // Test supported method types
    $method_types = $gateway->getSupportedMethodTypes();
    $this->assertContains('example_method', $method_types);

    // Test operation execution
    $result = $gateway->executeOperation('example_method', ['test' => 'data']);
    $this->assertTrue($result['success']);
  }
}
```

**Provider Pattern - Proxy Event Test**:

```php
<?php
namespace Drupal\Tests\my_module\Unit;

use PHPUnit\Framework\TestCase;

class ServiceProviderProxyTest extends TestCase {
  public function testProxyEventDispatching() {
    $provider = $this->createMock(ServiceProviderInterface::class);
    $eventDispatcher = $this->createMock(EventDispatcherInterface::class);

    // Verify events are dispatched
    $eventDispatcher->expects($this->exactly(2))
      ->method('dispatch')
      ->withConsecutive(
        [$this->isInstanceOf(PreServiceEvent::class)],
        [$this->isInstanceOf(PostServiceEvent::class)]
      );

    $proxy = new ServiceProviderProxy($provider, $eventDispatcher, $this->loggerFactory, $this->uuid);
    $proxy->executeService(new ServiceInput([]), 'config');
  }
}
```

**Service Collector - Unit Test**:

```php
<?php
namespace Drupal\Tests\orchestration\Unit;

use PHPUnit\Framework\TestCase;

class ServicesProviderManagerTest extends TestCase {
  public function testServiceCollection() {
    $manager = new ServicesProviderManager();

    $provider = $this->createMock(ServicesProviderInterface::class);
    $provider->method('getId')->willReturn('test_provider');
    $provider->method('getAll')->willReturn([
      new Service($provider, 'test_service', 'Test Service', 'Description')
    ]);

    $manager->addServicesProvider($provider);

    $services = $manager->getAllServices();
    $this->assertCount(1, $services);
    $this->assertEquals('test_provider::test_service', array_key_first($services));
  }
}
```

**REST API - Functional Test**:

```php
<?php
namespace Drupal\Tests\orchestration\Functional;

use Drupal\Tests\BrowserTestBase;

class RestApiTest extends BrowserTestBase {
  protected static $modules = ['orchestration', 'orchestration_eca'];

  public function testServicesEndpoint() {
    $this->drupalLogin($this->drupalCreateUser(['use orchestration']));

    $response = $this->drupalGet('/orchestration/services', [], ['Accept' => 'application/json']);
    $this->assertSession()->statusCodeEquals(200);

    $services = json_decode($response, TRUE);
    $this->assertIsArray($services);
    $this->assertArrayHasKey('id', $services[0]);
  }
}
```

## Common Mistakes

- **Wrong**: Testing only plugin discovery → **Right**: Test both discovery and instantiation with configuration
- **Wrong**: No mock for external APIs in provider tests → **Right**: Mock external dependencies to avoid network calls
- **Wrong**: Functional tests without proper permissions → **Right**: Create user with correct permissions for REST endpoint access

## See Also

- [Foundation + Extension Pattern](foundation-extension-pattern.md)
- [Provider Plugin Pattern](provider-plugin-pattern.md)
- [Service Collector Pattern](service-collector-pattern.md)
- Reference: Commerce Payment module tests
- Reference: [PHPUnit in Drupal](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal)
- Reference: [REST API Testing](https://www.drupal.org/docs/automated-testing/functional-testing)
