---
description: Create test modules for fixtures, mock services, test-specific config, and hook testing.
---

# Test Modules

## When to Use
Providing fixtures, mock services, test-specific config, or hooks for testing custom modules.

## Decision
| Need | Create test module? | Alternative |
|---|---|---|
| Test-specific config entities | YES | -- |
| Mock implementation of service | YES | Mock in test class |
| Custom entity type for testing | YES | -- |
| Hook implementations to verify hook firing | YES | -- |
| Simple data fixtures | NO | Create in test setUp() |

## Pattern
**Test module structure**:
```
modules/my_module/tests/modules/my_module_test/
  my_module_test.info.yml
  my_module_test.services.yml (optional)
  src/
    Service/
      MockExternalApi.php
  config/install/ (optional)
    node.type.test_content_type.yml
```

**Minimal info file** (`my_module_test.info.yml`):
```yaml
name: My Module Test
type: module
description: 'Test fixtures for My Module'
package: Testing
core_version_requirement: ^11
dependencies:
  - my_module
```

**Mock service** (`my_module_test.services.yml`):
```yaml
services:
  my_module.external_api:
    class: Drupal\my_module_test\Service\MockExternalApi
    decorates: my_module.external_api
```

**Using test module in tests**:
```php
protected static $modules = ['my_module', 'my_module_test'];

protected function setUp(): void {
  parent::setUp();
  // Test module automatically loaded, services available
  $mock_api = $this->container->get('my_module.external_api');
}
```

**File location**: `modules/my_module/tests/modules/my_module_test/`

Reference: `/core/modules/node/tests/modules/node_test/`

## Common Mistakes
- Creating test module as real contrib module -- pollutes production site if accidentally enabled
- Not declaring parent module dependency -- services/schema missing
- Forgetting to include test module in `$modules` array -- test module not loaded
- Placing test modules outside `/tests/modules/` -- PHPUnit can't find them
- Over-engineering test modules -- if mock fits in 10 lines, don't create a module (mock in test class)

## See Also
- [Test Traits & Utilities](test-traits-utilities.md)
- [Testing Services](testing-services.md)
- Reference: `/core/modules/system/tests/modules/`
- Example: `/core/modules/node/tests/modules/node_test/`
