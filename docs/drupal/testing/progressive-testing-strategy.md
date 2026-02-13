---
description: Progressive approach to building testing coverage from MVP to production-ready modules
drupal_version: "11.x"
---

# Progressive Testing Strategy

## When to Use

Use this progressive approach when building testing coverage for a new module or improving coverage for an existing module. Start simple and add complexity as the module matures.

## Decision: Testing Coverage Phases

| Phase | Coverage | Test Types | Focus |
|-------|----------|------------|-------|
| **MVP** | 30-40% | Unit + Kernel | Core logic and integration |
| **Feature Complete** | 60-70% | + Functional | Admin UI and workflows |
| **Production Ready** | 80%+ | + FunctionalJS + Gander | JavaScript and performance |

## Pattern: Phase 1 - Foundation Testing (MVP)

```php
// Create abstract base classes for consistency

// tests/src/Unit/MyModuleUnitTestBase.php
namespace Drupal\Tests\my_module\Unit;
use Drupal\Tests\UnitTestCase;

abstract class MyModuleUnitTestBase extends UnitTestCase {
  // Common mocks and setup for unit tests
  protected function getConfigStub(array $config = []): object {
    return $this->getConfigFactoryStub([
      'my_module.settings' => $config,
    ]);
  }
}

// tests/src/Kernel/MyModuleKernelTestBase.php
namespace Drupal\Tests\my_module\Kernel;
use Drupal\KernelTests\KernelTestBase;

abstract class MyModuleKernelTestBase extends KernelTestBase {
  protected static $modules = ['system', 'user', 'my_module'];
  
  protected function setUp(): void {
    parent::setUp();
    $this->installEntitySchema('user');
    $this->installConfig(['my_module']);
  }
}
```

**Priority**: Test core business logic and Drupal integration first.

## Pattern: Phase 2 - Feature Testing

```php
// tests/src/Functional/MyModuleFunctionalTestBase.php
namespace Drupal\Tests\my_module\Functional;
use Drupal\Tests\BrowserTestBase;

abstract class MyModuleFunctionalTestBase extends BrowserTestBase {
  protected $defaultTheme = 'stark';
  protected static $modules = ['my_module'];
  
  protected function setUp(): void {
    parent::setUp();
    
    // Create standard test users
    $this->adminUser = $this->drupalCreateUser([
      'administer my module',
      'access administration pages',
    ]);
  }
}
```

**Priority**: Add admin interface and user workflow testing.

## Pattern: Phase 3 - Production Ready

```php
// tests/src/FunctionalJavascript/MyModuleJavaScriptTestBase.php
namespace Drupal\Tests\my_module\FunctionalJavascript;
use Drupal\FunctionalJavascriptTests\WebDriverTestBase;

abstract class MyModuleJavaScriptTestBase extends WebDriverTestBase {
  protected $defaultTheme = 'stark';
  protected static $modules = ['my_module'];
}

// tests/src/FunctionalJavascript/MyModulePerformanceTestBase.php
namespace Drupal\Tests\my_module\FunctionalJavascript;
use Drupal\FunctionalJavascriptTests\PerformanceTestBase;

abstract class MyModulePerformanceTestBase extends PerformanceTestBase {
  protected static $modules = ['my_module'];
  protected $profile = 'minimal';
}
```

**Priority**: Add JavaScript interactions and performance validation.

## Common Mistakes

- **Wrong**: Trying to achieve 100% coverage immediately → **Right**: Start with 30-40% coverage of critical paths
- **Wrong**: Writing performance tests before features stabilize → **Right**: Add performance tests in final phase
- **Wrong**: Skipping base test classes → **Right**: Create abstract base classes to reduce duplication
- **Wrong**: Not prioritizing high-risk code → **Right**: Test critical business logic first
- **Wrong**: Writing all tests at once → **Right**: Progressive approach provides early feedback

## See Also

- [Framework Selection Decision Matrix](framework-selection-decision-matrix.md)
- [Testing Infrastructure Setup](testing-infrastructure-setup.md)
- [Gander Performance Testing](gander-performance-testing.md)
- Reference: [Automated testing - Drupal.org](https://www.drupal.org/docs/develop/automated-testing)
