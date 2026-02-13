---
description: Write kernel tests for ECA plugins to verify configuration, execution, and token handling
drupal_version: "11.x"
---

# Kernel Testing

## When to Use

> Write kernel tests for all ECA plugins to verify configuration, execution logic, token handling, and integration with Drupal services. Kernel tests run faster than browser tests and provide sufficient coverage for most plugin logic.

## Decision

| Test Type | Use For | Test Class |
|-----------|---------|------------|
| Kernel test | Plugin logic, services, tokens | `KernelTestBase` |
| Unit test | Pure logic, no dependencies | `UnitTestCase` |
| Functional test | UI configuration, workflows | `BrowserTestBase` |

## Pattern

```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;

/**
 * Tests for custom ECA action.
 *
 * @group my_module
 * @group eca
 */
class MyActionTest extends KernelTestBase {

  /**
   * {@inheritdoc}
   */
  protected static $modules = [
    'system',
    'user',
    'eca',
    'eca_base',
    'my_module',
  ];

  /**
   * The action plugin manager.
   */
  protected $actionManager;

  /**
   * The token service.
   */
  protected $tokenService;

  /**
   * {@inheritdoc}
   */
  protected function setUp(): void {
    parent::setUp();

    $this->installEntitySchema('user');
    $this->installSchema('system', ['sequences']);

    $this->actionManager = $this->container->get('plugin.manager.action');
    $this->tokenService = $this->container->get('eca.token_services');
  }

  /**
   * Tests action configuration.
   */
  public function testActionConfiguration(): void {
    $action = $this->actionManager->createInstance('my_module_custom_action', [
      'input_field' => 'test_input',
      'result_token' => 'test_result',
    ]);

    $config = $action->getConfiguration();
    $this->assertEquals('test_input', $config['input_field']);
    $this->assertEquals('test_result', $config['result_token']);
  }

  /**
   * Tests action execution.
   */
  public function testActionExecution(): void {
    // Set up token data
    $this->tokenService->addTokenData('test_input', 'sample_value');

    // Create and execute action
    $action = $this->actionManager->createInstance('my_module_custom_action', [
      'input_field' => '[test_input]',
      'result_token' => 'test_result',
    ]);

    $action->execute(NULL);

    // Verify results
    $result = $this->tokenService->getTokenData('test_result');
    $this->assertNotEmpty($result);
    $this->assertEquals(1, $result['success']);
  }

  /**
   * Tests action error handling.
   */
  public function testActionError(): void {
    $action = $this->actionManager->createInstance('my_module_custom_action', [
      'input_field' => 'invalid_input',
      'result_token' => 'test_result',
    ]);

    $action->execute(NULL);

    $result = $this->tokenService->getTokenData('test_result');
    $this->assertEquals(0, $result['success']);
    $this->assertNotEmpty($result['error']);
  }
}
```

## Common Mistakes

- **Wrong**: Not installing required schemas → **Right**: Database errors during tests
- **Wrong**: Missing module dependencies → **Right**: Services not available
- **Wrong**: Not cleaning up token service between tests → **Right**: Test pollution
- **Wrong**: Testing UI instead of logic → **Right**: Use functional tests for UI
- **Wrong**: No error case tests → **Right**: Only testing happy path
- **Wrong**: Not testing token replacement → **Right**: Core plugin functionality untested

## See Also

- [Debugging Workflows](debugging-workflows.md) for debugging tools
- [Action Plugin Basics](action-plugin-basics.md) for action structure
- [Complex Token Structures](complex-token-structures.md) for token testing

**References:**
- Drupal Testing: https://www.drupal.org/docs/automated-testing/phpunit-in-drupal
- ECA Tests: `/modules/contrib/eca/tests/src/Kernel/`
