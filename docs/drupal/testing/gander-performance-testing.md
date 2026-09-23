---
description: Write Gander performance tests to measure site-wide performance impact using OpenTelemetry tracing
tldr: "Write Gander performance tests for modules with site-wide performance impact: event subscribers that fire on every request, cache invalidation logic, bulk operations, or features that execute complex queries."
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
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\Attributes\RequiresPhpExtension;
use PHPUnit\Framework\Attributes\RunTestsInSeparateProcesses;

/**
 * Tests the my_module performance characteristics.
 */
#[Group('my_module')]
#[Group('Performance')]
#[Group('#slow')]
#[RequiresPhpExtension('apcu')]
#[RunTestsInSeparateProcesses]
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

- Running performance tests without APCu enabled → Inaccurate cache metrics
- Not warming caches before hot cache tests → Measuring cold cache instead
- Setting unrealistic performance budgets → Tests always fail
- Testing performance too early in development → Budgets change as features evolve
- Not comparing with/without module enabled → Unknown actual impact

**WHY these are mistakes**: Performance tests measure real system behavior, which requires production-like conditions. APCu provides accurate cache metrics. Cache warming is required for realistic hot-cache measurements. Performance budgets must be based on actual measurements, not guesses. Always measure baseline performance without your module to understand true impact.

## See Also

- [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md)
- [Progressive Testing Strategy](progressive-testing-strategy.md)
- [Best Practices & Anti-Patterns](best-practices-anti-patterns.md)
- Reference: [Performance tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/performance-tests)
- Reference: `/core/tests/Drupal/FunctionalJavascriptTests/PerformanceTestBase.php`
