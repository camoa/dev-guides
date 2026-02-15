---
description: Test custom routes, controller methods, route parameters, and JSON responses in Drupal.
---

# Testing Routes & Controllers

## When to Use
Testing custom routes, controller methods, route parameters, response codes.

## Decision
| What to test | Test type | Why |
|---|---|---|
| Route returns 200 | Browser | Needs HTTP simulation |
| Route parameters parsed correctly | Kernel or Browser | Depends on complexity |
| Controller logic only | Unit or Kernel | Depends on dependencies |
| Access control on route | Browser | Needs user context |

## Pattern
**Testing route responses (Browser)**:
```php
namespace Drupal\Tests\my_module\Functional;

use Drupal\Tests\BrowserTestBase;

class RouteTest extends BrowserTestBase {

  protected $defaultTheme = 'stark';
  protected static $modules = ['my_module'];

  public function testBasicRoute(): void {
    $this->drupalGet('my-module/page');
    $this->assertSession()->statusCodeEquals(200);
    $this->assertSession()->pageTextContains('Expected content');
  }

  public function testRouteWithParameter(): void {
    $this->drupalGet('my-module/item/123');
    $this->assertSession()->statusCodeEquals(200);
    $this->assertSession()->pageTextContains('Item 123');
  }
}
```

**Testing controller logic (Unit)**:
```php
namespace Drupal\Tests\my_module\Unit;

use Drupal\my_module\Controller\MyController;
use Drupal\Tests\UnitTestCase;

class MyControllerTest extends UnitTestCase {

  public function testBuildMethod(): void {
    $mock_service = $this->createMock(MyServiceInterface::class);
    $mock_service->method('getData')->willReturn(['key' => 'value']);

    $controller = new MyController($mock_service);
    $build = $controller->build();

    $this->assertArrayHasKey('#markup', $build);
  }
}
```

**Testing JSON responses**:
```php
public function testJsonRoute(): void {
  $this->drupalGet('my-module/api/data');
  $this->assertSession()->statusCodeEquals(200);

  $response = $this->getSession()->getPage()->getContent();
  $data = json_decode($response, TRUE);

  $this->assertArrayHasKey('status', $data);
  $this->assertEquals('success', $data['status']);
}
```

Reference: `/core/modules/system/tests/src/Functional/System/`

## Common Mistakes
- Testing controller in isolation when route parameters matter -- use Browser test to verify full request cycle
- Not testing different HTTP methods (GET/POST/PUT/DELETE) -- route works for GET but fails for POST
- Hardcoding URLs in tests -- breaks when routing changes (use Url::fromRoute())
- Not testing route parameter validation -- invalid parameters cause 500 errors
- Forgetting CSRF token for non-GET routes -- POST fails with access denied

## See Also
- [Testing Access & Permissions](testing-access-permissions.md)
- [Testing Configuration](testing-configuration.md)
- Reference: `/core/modules/system/tests/src/Functional/System/`
