---
description: Ensuring media source plugin works correctly across different scenarios and preventing regressions.
---

# Testing Strategies

### When to Use

Ensuring media source plugin works correctly across different scenarios and preventing regressions.

### Decision

| Test Type | Tests What | Speed | Dependency |
|-----------|-----------|-------|------------|
| **Unit tests** | Metadata extraction logic, helper methods | Fast (< 1s) | None (mocked services) |
| **Kernel tests** | Database operations, entity integration | Medium (2-5s) | Database required |
| **Functional tests** | UI forms, Media Library, display | Slow (10-30s) | Full Drupal bootstrap |

### Pattern

Unit test for metadata extraction (12 lines):
```php
namespace Drupal\Tests\yourmodule\Unit\Plugin\media\Source;

use Drupal\Tests\UnitTestCase;
use Drupal\yourmodule\Plugin\media\Source\CustomApi;

class CustomApiTest extends UnitTestCase {
  public function testMetadataExtraction(): void {
    $source = $this->createPluginInstance();
    $media = $this->createMock(MediaInterface::class);
    $media->method('get')->willReturn($this->createSourceFieldMock('item-123'));

    $title = $source->getMetadata($media, 'title');

    $this->assertEquals('Expected Title', $title);
  }

  protected function createPluginInstance(): CustomApi {
    $entity_type_manager = $this->createMock(EntityTypeManagerInterface::class);
    $entity_field_manager = $this->createMock(EntityFieldManagerInterface::class);
    $field_type_manager = $this->createMock(FieldTypePluginManagerInterface::class);
    $config_factory = $this->createMock(ConfigFactoryInterface::class);

    return new CustomApi([], 'custom_api', ['id' => 'custom_api'],
      $entity_type_manager, $entity_field_manager, $field_type_manager, $config_factory);
  }
}
```

Kernel test for field creation (8 lines):
```php
namespace Drupal\Tests\yourmodule\Kernel;

use Drupal\KernelTests\Core\Entity\EntityKernelTestBase;

class CustomApiKernelTest extends EntityKernelTestBase {
  protected static $modules = ['media', 'yourmodule'];

  public function testSourceFieldCreation(): void {
    $media_type = $this->createMediaType('custom_api');
    $source = $media_type->getSource();
    $field = $source->createSourceField($media_type);

    $this->assertInstanceOf(FieldConfigInterface::class, $field);
    $this->assertEquals('string', $field->getType());
  }
}
```

### Common Mistakes

- Not mocking external services → Unit tests make real API calls, fail without network
- No test coverage for error conditions → Plugin crashes when API unavailable
- Only testing happy path → Bugs appear when validation fails, fields missing
- Functional tests for logic → Slow test suite, wastes CI time
- No test for Media Library integration → Custom widgets break selection UI

**WHY:**
- **Mock external dependencies**: Unit tests run in isolation; real HTTP calls make tests slow, flaky, and dependent on external services
- **Error condition coverage**: APIs fail 1-5% of the time in production; untested error paths cause white screens
- **Happy path bias**: Most bugs occur in edge cases (empty values, malformed URLs, missing metadata); testing only success cases misses 80% of issues
- **Test at right level**: Unit tests for logic (fast feedback), kernel for entity operations (integration), functional for UI (user acceptance)

### See Also

- Previous: [Performance Optimization](index.md)
- Next: [Anti-Patterns](index.md)
- Reference: core/modules/media/tests/