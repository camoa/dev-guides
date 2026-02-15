---
description: Test config schema validation, default config values, config forms, and config overrides in Drupal.
---

# Testing Configuration

## When to Use
Testing config schema, config import/export, default config, config overrides.

## Decision
| Config aspect | Test approach | Test type |
|---|---|---|
| Config schema valid | SchemaCheckTestTrait | Kernel |
| Config values correct after install | Load config, assert values | Kernel |
| Config form saves correctly | Submit form, load config | Browser |
| Config overrides work | Test with settings.php override | Kernel |

## Pattern
**Testing config schema (Kernel)**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;

class ConfigSchemaTest extends KernelTestBase {

  use SchemaCheckTestTrait;

  protected static $modules = ['my_module'];

  public function testConfigSchema(): void {
    $config = $this->config('my_module.settings');
    $this->assertConfigSchema(
      $this->getConfigSchemaChecker(),
      'my_module.settings',
      $config->get()
    );
  }
}
```

**Testing default config values**:
```php
public function testDefaultConfig(): void {
  $this->installConfig(['my_module']);
  $config = $this->config('my_module.settings');

  $this->assertEquals('default_value', $config->get('setting_key'));
  $this->assertEquals(10, $config->get('numeric_setting'));
}
```

**Testing config form (Browser)**:
```php
namespace Drupal\Tests\my_module\Functional;

use Drupal\Tests\BrowserTestBase;

class ConfigFormTest extends BrowserTestBase {

  protected $defaultTheme = 'stark';
  protected static $modules = ['my_module'];

  public function testConfigForm(): void {
    $admin = $this->drupalCreateUser(['administer site configuration']);
    $this->drupalLogin($admin);

    $this->drupalGet('admin/config/my-module');
    $this->submitForm(['setting_key' => 'new_value'], 'Save configuration');

    $config = $this->config('my_module.settings');
    $this->assertEquals('new_value', $config->get('setting_key'));
  }
}
```

**Testing config overrides**:
```php
public function testConfigOverride(): void {
  $this->config('my_module.settings')
    ->set('overridable_value', 'original')
    ->save();

  // Override in test
  $settings = Settings::getAll();
  $settings['my_module.settings']['overridable_value'] = 'overridden';
  new Settings($settings);

  $config = $this->config('my_module.settings');
  $this->assertEquals('overridden', $config->get('overridable_value'));
}
```

Reference: `/core/modules/system/tests/src/Kernel/System/`

## Common Mistakes
- Not calling `installConfig()` before testing config -- config doesn't exist
- Testing editable config in Unit tests -- config system needs container (use Kernel)
- Not validating config schema -- invalid config accepted, breaks site later
- Forgetting to clear cache after config changes -- tests see stale values
- Not testing config dependencies -- module uninstall leaves orphaned config

## See Also
- [Testing Routes & Controllers](testing-routes-controllers.md)
- [Testing Events & Hooks](testing-events-hooks.md)
- Reference: `/core/tests/Drupal/Tests/SchemaCheckTestTrait.php`
- Example: `/core/modules/config/tests/src/Kernel/`
