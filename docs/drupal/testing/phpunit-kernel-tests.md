---
description: Write PHPUnit Kernel tests for service integration, database operations, and entity CRUD without full Drupal installation
drupal_version: "11.x"
---

# PHPUnit Kernel Tests

## When to Use

Write Kernel tests when you need to test integration with Drupal services, database operations, entity CRUD, or service container interactions without needing a full Drupal installation.

## Decision

| If you need... | Use Kernel Tests | Why |
|----------------|------------------|-----|
| Test service integration | Yes | Access to container and dependency injection |
| Entity CRUD operations | Yes | Database and entity storage available |
| Configuration system | Yes | Config system fully functional |
| HTTP requests/responses | No, use Functional | No web server in Kernel tests |
| Test admin forms | No, use Functional | No routing or form rendering |
| Test JavaScript | No, use FunctionalJavascript | No browser environment |

## Pattern

```php
<?php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Drupal\node\Entity\Node;
use Drupal\node\Entity\NodeType;
use Drupal\user\Entity\User;

/**
 * Tests the my_module entity processor service.
 *
 * @group my_module
 */
class EntityProcessorTest extends KernelTestBase {

  protected static $modules = [
    'system', 'user', 'node', 'field', 'text', 'my_module',
  ];

  protected function setUp(): void {
    parent::setUp();

    // Install database schemas
    $this->installEntitySchema('user');
    $this->installEntitySchema('node');
    
    // Install configuration
    $this->installConfig(['system', 'node', 'my_module']);
    
    // Create content type
    NodeType::create([
      'type' => 'article',
      'name' => 'Article',
    ])->save();

    // Create required users (user 0 = anonymous, user 1 = admin)
    User::create(['uid' => 0, 'name' => 'guest'])->save();
    User::create(['uid' => 1, 'name' => 'admin'])->save();
  }

  public function testEntityProcessing(): void {
    $node = Node::create([
      'type' => 'article',
      'title' => 'Test Article',
      'uid' => 1,
    ]);
    $node->save();

    // Test service from container
    $processor = $this->container->get('my_module.entity_processor');
    $result = $processor->process($node);

    $this->assertTrue($result['success']);
    $this->assertEquals('Test Article', $result['title']);
    $this->assertInstanceOf(Node::class, $result['entity']);
  }

  public function testConfigurationIntegration(): void {
    // Test configuration system
    $config = $this->config('my_module.settings');
    $config->set('api_enabled', TRUE)->save();

    $service = $this->container->get('my_module.api_client');
    $this->assertTrue($service->isEnabled());
  }
}
```

**File Location**: `modules/my_module/tests/src/Kernel/EntityProcessorTest.php`

## Common Mistakes

- **Wrong**: Not installing entity schemas → **Right**: Call `installEntitySchema()` for all entities used
- **Wrong**: Not installing configuration → **Right**: Call `installConfig()` for modules with config
- **Wrong**: Not creating required users (uid 0, 1) → **Right**: Create anonymous and admin users in setUp
- **Wrong**: Forgetting to list all required modules in `$modules` → **Right**: Include all dependencies
- **Wrong**: Using `drupalGet()` in Kernel tests → **Right**: Use Functional tests for HTTP layer

## See Also

- [PHPUnit Unit Tests](phpunit-unit-tests.md)
- [PHPUnit Functional Tests](phpunit-functional-tests.md)
- Reference: [Setup tasks in Kernel tests - Drupal.org](https://www.drupal.org/docs/automated-testing/phpunit-in-drupal/setup-tasks-in-kernel-tests)
- Reference: [Making HTTP requests in Kernel tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/making-http-requests-programmatically-in-kernel-tests)
- Reference: `/core/tests/Drupal/KernelTests/KernelTestBase.php`
