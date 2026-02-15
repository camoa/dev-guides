---
description: Test Drupal plugins including blocks, field types, formatters, widgets, and views plugins.
---

# Testing Plugins

## When to Use
Testing blocks, field types, field formatters, field widgets, views plugins, and other plugin derivatives.

## Decision
| Plugin type | Minimum test type | Why |
|---|---|---|
| Block | Kernel | Needs block manager, rendering |
| Field type/formatter/widget | Kernel | Needs entity/field system |
| Views plugin | Kernel | Needs Views, database |
| Condition plugin | Unit (if simple) or Kernel | Depends on context requirements |

## Pattern
**Testing a block plugin (Kernel)**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;

class MyBlockTest extends KernelTestBase {

  protected static $modules = ['system', 'block', 'my_module'];

  public function testBlockRendering(): void {
    $plugin_manager = $this->container->get('plugin.manager.block');
    $config = ['label' => 'Test Block'];

    $block = $plugin_manager->createInstance('my_module_block', $config);
    $build = $block->build();

    $this->assertArrayHasKey('#markup', $build);
    $this->assertStringContainsString('Expected content', $build['#markup']);
  }
}
```

**Testing a field formatter (Kernel)**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\entity_test\Entity\EntityTest;
use Drupal\KernelTests\KernelTestBase;

class MyFormatterTest extends KernelTestBase {

  protected static $modules = ['field', 'entity_test', 'my_module'];

  protected function setUp(): void {
    parent::setUp();
    $this->installEntitySchema('entity_test');
    // Create field instance, attach formatter
  }

  public function testFormatterOutput(): void {
    $entity = EntityTest::create(['my_field' => 'test value']);
    $display = $entity->get('my_field')->view(['type' => 'my_formatter']);

    $output = $this->container->get('renderer')->renderRoot($display);
    $this->assertStringContainsString('formatted: test value', $output);
  }
}
```

**Testing plugin discovery (Unit)**:
```php
public function testPluginAnnotation(): void {
  $plugin_manager = $this->container->get('plugin.manager.block');
  $definitions = $plugin_manager->getDefinitions();

  $this->assertArrayHasKey('my_module_block', $definitions);
  $this->assertEquals('My Block', $definitions['my_module_block']['admin_label']);
}
```

Reference: `/core/modules/block/tests/src/Kernel/BlockViewBuilderTest.php`

## Common Mistakes
- Not installing required modules for plugin manager -- "Plugin manager not found"
- Testing rendering without installing entity schema -- "Table doesn't exist"
- Hardcoding plugin IDs instead of using constants -- string typos not caught
- Not testing plugin derivatives -- base plugin works but derivatives broken
- Forgetting to test access control in block plugins -- blocks visible when they shouldn't be

## See Also
- [Testing Services](testing-services.md)
- [Testing Forms](testing-forms.md)
- Reference: `/core/modules/block/tests/src/Kernel/BlockViewBuilderTest.php`
- Example: `/core/modules/field/tests/src/Kernel/`
