---
description: Unit, kernel, and functional testing strategies for media source plugins
drupal_version: "11.x"
---

# Testing Strategies

## When to Use

> Use layered testing to ensure media source plugin works correctly across different scenarios and prevent regressions.

## Decision

| Test Type | Tests What | Speed | Dependency |
|-----------|-----------|-------|------------|
| **Unit tests** | Metadata extraction logic, helper methods | Fast (< 1s) | None (mocked services) |
| **Kernel tests** | Database operations, entity integration | Medium (2-5s) | Database required |
| **Functional tests** | UI forms, Media Library, display | Slow (10-30s) | Full Drupal bootstrap |

## Pattern

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
    // Mock dependencies, create plugin instance
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

## Common Mistakes

- **Wrong**: Not mocking external services → **Right**: Mock HTTP client and API responses
- **Wrong**: No test coverage for error conditions → **Right**: Test API failures, timeouts
- **Wrong**: Only testing happy path → **Right**: Test validation failures, missing data
- **Wrong**: Functional tests for logic → **Right**: Unit tests for logic, functional for UI
- **Wrong**: No test for Media Library integration → **Right**: Test custom widgets in inline forms

## See Also

- Previous: [Performance Optimization](performance-optimization.md)
- Next: [Anti-Patterns](anti-patterns.md)
- Reference: core/modules/media/tests/
