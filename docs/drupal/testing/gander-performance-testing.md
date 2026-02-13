---
description: Write Gander performance tests to measure site-wide performance impact using OpenTelemetry tracing
drupal_version: "11.x"
---

# Gander Performance Testing

## When to Use

Write Gander performance tests for modules with site-wide performance impact: event subscribers that fire on every request, cache invalidation logic, bulk operations, or features that execute complex queries.

## Decision

| Module Type | Use Gander | Why |
|-------------|------------|-----|
| Event-driven modules (ECA, Rules) | Yes | Event cascades can cause performance issues |
| Page request processors | Yes | Affects every page load |
| Mass operations (imports, bulk updates) | Yes | Query count and cache impact matter |
| Cache invalidation logic | Yes | Wrong invalidation destroys performance |
| Simple CRUD operations | No | Standard database operations |
| Admin-only features | Maybe | Low usage frequency, less critical |

## Pattern

```php
<?php
namespace Drupal\Tests\my_module\FunctionalJavascript;

use Drupal\FunctionalJavascriptTests\PerformanceTestBase;

/**
 * Tests the my_module performance characteristics.
 *
 * @group my_module
 * @group Performance
 * @group #slow
 * @requires extension apcu
 */
class MyModulePerformanceTest extends PerformanceTestBase {

  protected static $modules = ['my_module', 'node'];
  protected $defaultTheme = 'stark';
  protected $profile = 'minimal';

  public function testFrontPagePerformanceImpact(): void {
    // Measure cold cache performance
    $performance_data = $this->collectPerformanceData(function() {
      $this->drupalGet('<front>');
    }, 'frontPageColdCache');

    // Set performance expectations
    $expected = [
      'queryCount' => 50,           // Maximum database queries
      'cacheGetCount' => 20,        // Maximum cache reads
      'cacheSetCount' => 15,        // Maximum cache writes
      'cacheDeleteCount' => 0,      // No cache deletes on normal request
      'cacheTagChecksumCount' => 5, // Cache tag validations
    ];
    
    $this->assertSame(200, $performance_data->getStatusCode());
    $this->assertLessThanOrEqual($expected['queryCount'], $performance_data->getQueryCount());
    $this->assertLessThanOrEqual($expected['cacheGetCount'], $performance_data->getCacheGetCount());
  }

  public function testHotCachePerformance(): void {
    // Warm cache
    $this->drupalGet('<front>');
    sleep(1);

    // Measure hot cache performance
    $performance_data = $this->collectPerformanceData(function() {
      $this->drupalGet('<front>');
    }, 'frontPageHotCache');

    // Expect minimal queries with warm cache
    $this->assertLessThanOrEqual(10, $performance_data->getQueryCount());
    $this->assertGreaterThan(5, $performance_data->getCacheGetCount());
  }

  public function testBulkOperationPerformance(): void {
    // Create test content
    $this->createNode(['type' => 'article', 'title' => 'Test']);

    // Measure bulk processing
    $performance_data = $this->collectPerformanceData(function() {
      $service = \Drupal::service('my_module.bulk_processor');
      
      // Process 100 items
      for ($i = 0; $i < 100; $i++) {
        $service->processItem(['id' => $i, 'data' => "test_$i"]);
      }
    }, 'bulkProcessing100Items');

    // Assert reasonable performance bounds
    $this->assertLessThanOrEqual(200, $performance_data->getQueryCount());
    $this->assertLessThanOrEqual(50, $performance_data->getCacheSetCount());
    
    // Ensure we're not invalidating too many caches
    $this->assertLessThanOrEqual(10, $performance_data->getCacheTagInvalidationCount());
  }
}
```

**File Location**: `modules/my_module/tests/src/FunctionalJavascript/MyModulePerformanceTest.php`

**Note**: Performance tests extend `PerformanceTestBase` (since Drupal 10.2) and use OpenTelemetry tracing.

## Common Mistakes

- **Wrong**: Running performance tests without APCu enabled → **Right**: Enable APCu extension for accurate cache metrics
- **Wrong**: Not warming caches before hot cache tests → **Right**: Run request once, then measure second request
- **Wrong**: Setting unrealistic performance budgets → **Right**: Base budgets on actual measurements
- **Wrong**: Testing performance too early in development → **Right**: Add performance tests after features stabilize
- **Wrong**: Not comparing with/without module enabled → **Right**: Measure baseline to understand actual impact

## See Also

- [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md)
- [Progressive Testing Strategy](progressive-testing-strategy.md)
- [Best Practices & Anti-Patterns](best-practices-anti-patterns.md)
- Reference: [Performance tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/performance-tests)
- Reference: `/core/tests/Drupal/FunctionalJavascriptTests/PerformanceTestBase.php`
