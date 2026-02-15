---
description: Write Drupal kernel tests with KernelTestBase for services, entities, and database operations without HTTP overhead.
---

# Kernel Tests with KernelTestBase

## When to Use
Testing services, entities, database operations, and other Drupal integrations without HTTP overhead. Sweet spot for most Drupal testing.

## Decision
| Feature | Unit | Kernel | Browser |
|---|---|---|---|
| Container & services | No | Yes | Yes |
| Database access | No | Yes | Yes |
| Entity API | No | Yes | Yes |
| Config system | No | Yes | Yes |
| HTTP requests | No | No | Yes |
| Form rendering/submission | No | No | Yes |
| Speed (seconds per test) | 0.01 | 0.5-2 | 10-30 |

**Use Kernel when**: Service interaction matters, database needed, no user simulation required.

## Pattern
**Basic kernel test setup**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;

class MyServiceTest extends KernelTestBase {

  protected static $modules = ['system', 'user', 'my_module'];

  protected function setUp(): void {
    parent::setUp();
    $this->installEntitySchema('user');
    $this->installConfig(['my_module']);
    $this->installSchema('system', ['sequences']);
  }

  public function testServiceMethod(): void {
    $service = $this->container->get('my_module.my_service');
    $result = $service->doSomething();
    $this->assertNotEmpty($result);
  }
}
```

**Module installation hierarchy**:
1. `protected static $modules` -- loads module services/hooks, no install process
2. `installEntitySchema('entity_type')` -- creates database tables for entity type
3. `installConfig(['module'])` -- imports YAML config from config/install
4. `installSchema('module', ['table'])` -- creates custom tables from hook_schema

**File location**: `modules/my_module/tests/src/Kernel/MyServiceTest.php`

Reference: `/core/tests/Drupal/KernelTests/KernelTestBase.php` lines 69-82

## Common Mistakes
- Forgetting `installEntitySchema()` before entity operations -- "Table 'node' doesn't exist"
- Not declaring module dependencies in `$modules` -- services missing from container
- Using HTTP methods like `$this->drupalGet()` -- kernel tests don't support HTTP (use BrowserTestBase)
- Installing unnecessary modules -- slower tests (only install what you need)
- Not calling `parent::setUp()` -- bootstrap incomplete, random failures

## See Also
- Reference: `/core/tests/Drupal/KernelTests/KernelTestBase.php`
- Example: `/core/modules/block/tests/src/Kernel/BlockViewBuilderTest.php`
- Official documentation: [PHPUnit in Drupal | Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal)
