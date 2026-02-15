---
description: Test Drupal event subscribers, hook implementations, and alter hooks.
---

# Testing Events & Hooks

## When to Use
Verifying event subscribers work, hooks fire correctly, alter hooks modify data as expected.

## Decision
| Type | Test approach | Test type |
|---|---|---|
| Event subscriber | Dispatch event, assert subscriber ran | Kernel |
| Hook implementation | Trigger hook, verify side effect | Kernel or Browser |
| Alter hook | Call API, verify altered result | Kernel |

## Pattern
**Testing event subscriber (Kernel)**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Symfony\Component\EventDispatcher\EventDispatcherInterface;

class EventSubscriberTest extends KernelTestBase {

  protected static $modules = ['my_module'];

  public function testSubscriberExecuted(): void {
    $dispatcher = $this->container->get('event_dispatcher');
    $event = new MyCustomEvent(['data' => 'original']);

    $dispatcher->dispatch($event, MyCustomEvent::EVENT_NAME);

    $this->assertEquals('modified', $event->getData());
  }
}
```

**Testing hook implementation via test module**:
```php
// In my_module_test.module
function my_module_test_node_presave($node) {
  \Drupal::state()->set('hook_fired', TRUE);
}

// In test
public function testHookFires(): void {
  $node = Node::create(['type' => 'page', 'title' => 'Test']);
  $node->save();

  $this->assertTrue(\Drupal::state()->get('hook_fired'));
}
```

**Testing alter hook**:
```php
public function testFormAlter(): void {
  $form_builder = $this->container->get('form_builder');
  $form = $form_builder->getForm('Drupal\node\NodeForm', Node::create(['type' => 'page']));

  // My module adds a custom field via hook_form_alter
  $this->assertArrayHasKey('my_custom_field', $form);
}
```

Reference: `/core/tests/Drupal/KernelTests/Core/`

## Common Mistakes
- Testing core hooks instead of custom implementations -- wastes time
- Not using test modules to isolate hook testing -- real module conflicts with test expectations
- Forgetting to enable test module in `$modules` -- hook doesn't fire
- Testing event subscriber in Unit test -- no event dispatcher available (use Kernel)
- Not verifying hook execution order when multiple modules implement same hook -- race conditions

## See Also
- Reference: `/core/lib/Drupal/Core/Test/EventSubscriber/`
