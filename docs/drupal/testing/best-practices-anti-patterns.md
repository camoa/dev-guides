---
description: Security, performance, and development standards best practices for writing maintainable Drupal tests
tldr: "Consult this guide when writing tests, reviewing code, or establishing testing standards for your team."
drupal_version: "11.x"
---

# Best Practices & Anti-Patterns

## When to Use

Consult this section when writing tests, reviewing code, or establishing testing standards for your team.

## Decision: Security Best Practices

| Practice | Implementation | Why |
|----------|----------------|-----|
| **Test access control** | Create users with different permissions, verify access denied | Prevents unauthorized access bugs |
| **Test CSRF protection** | Verify form tokens required | Prevents cross-site request forgery |
| **Test input validation** | Submit malicious input, verify sanitization | Prevents XSS and injection attacks |
| **Test permission boundaries** | Test with minimal permissions, verify failures | Prevents privilege escalation |

## Pattern: Security Testing

```php
public function testAccessControl(): void {
  // Test admin access
  $admin = $this->drupalCreateUser(['administer my module']);
  $this->drupalLogin($admin);
  $this->drupalGet('admin/config/my-module');
  $this->assertSession()->statusCodeEquals(200);
  
  // Test unauthorized access
  $user = $this->drupalCreateUser(['access content']);
  $this->drupalLogin($user);
  $this->drupalGet('admin/config/my-module');
  $this->assertSession()->statusCodeEquals(403);
  
  // Test anonymous access
  $this->drupalLogout();
  $this->drupalGet('admin/config/my-module');
  $this->assertSession()->statusCodeEquals(403);
}

public function testXssProtection(): void {
  $malicious = '<script>alert("XSS")</script>';
  
  $this->submitForm(['title' => $malicious], 'Save');
  
  // Verify sanitization
  $this->assertSession()->responseNotContains('<script>');
  $this->assertSession()->responseContains(htmlspecialchars($malicious));
}
```

**Anti-Pattern**: Not testing permission boundaries → Security vulnerabilities in production

**WHY**: Access control bugs are among the most serious security issues. Always test with users who should NOT have access.

## Decision: Performance Best Practices

| Practice | Implementation | Why |
|----------|----------------|-----|
| **Test query counts** | Assert database query limits | Detects N+1 query problems |
| **Test cache efficiency** | Compare cold vs hot cache metrics | Verifies caching works |
| **Test cache invalidation** | Verify caches cleared on updates | Prevents stale data |
| **Test bulk operations** | Process large datasets, measure performance | Catches scalability issues |

## Pattern: Performance Testing

```php
public function testQueryEfficiency(): void {
  // Track queries
  \Drupal::service('database')->enableQueryLog();
  
  // Perform operation
  $service = \Drupal::service('my_module.processor');
  $service->processList($items);
  
  $queries = \Drupal::service('database')->getLog();
  
  // Assert reasonable query count (not N+1)
  $this->assertLessThanOrEqual(10, count($queries));
}

public function testCacheWarmth(): void {
  // Cold cache - expect queries
  $this->drupalGet('my-module/cached-page');
  $cold_performance = $this->getPerformanceData();
  $this->assertGreaterThan(10, $cold_performance['queries']);
  
  // Hot cache - expect no queries
  $this->drupalGet('my-module/cached-page');
  $hot_performance = $this->getPerformanceData();
  $this->assertLessThan(3, $hot_performance['queries']);
}
```

**Anti-Pattern**: Not measuring performance until production → Scalability issues found too late

**WHY**: Performance problems multiply with scale. A query that runs twice on test data might run 10,000 times on production data. Test early.

## Decision: Development Standards

| Practice | Implementation | Why |
|----------|----------------|-----|
| **Use data providers** | `#[DataProvider]` for multiple test cases | Reduces code duplication |
| **Test one behavior per method** | Each test verifies one thing | Easier debugging |
| **Use descriptive test names** | Name describes what's tested | Self-documenting tests |
| **Document complex tests** | PHPDoc explains test scenario | Maintainability |
| **Mock external dependencies** | Never call real APIs in tests | Fast, reliable tests |

## Pattern: Development Standards

```php
use PHPUnit\Framework\Attributes\DataProvider;

/**
 * Tests email validation with various input formats.
 */
#[DataProvider('emailProvider')]
public function testEmailValidation($email, $expected_valid, $description): void {
  $result = $this->validator->validateEmail($email);
  $this->assertEquals($expected_valid, $result, $description);
}

// A data provider must be static, or PHPUnit discards the whole class.
public static function emailProvider(): array {
  return [
    'valid email' => ['test@example.com', TRUE, 'Standard email format'],
    'invalid format' => ['notanemail', FALSE, 'Missing @ symbol'],
    'empty string' => ['', FALSE, 'Empty input'],
    'no domain' => ['test@', FALSE, 'Missing domain'],
    'international domain' => ['test@münchen.de', TRUE, 'IDN domain'],
  ];
}
```

**Anti-Pattern**: Testing multiple behaviors in one method → When it fails, unclear what broke

**WHY**: Tests are documentation. Each test should verify one specific behavior. When a test fails, you should know exactly what broke from the test name alone.

## Common Anti-Patterns

**Anti-Pattern 1**: Using database queries in Unit tests

```php
// WRONG - Unit tests should not access database
public function testCalculation(): void {
  $node = Node::load(1);  // Database access!
  $result = $this->calculator->process($node->get('value'));
}

// RIGHT - Mock the data
public function testCalculation(): void {
  $mock_data = ['value' => 10];
  $result = $this->calculator->process($mock_data['value']);
}
```

**WHY**: Unit tests must be fast and isolated. Database access makes them slow and creates dependencies on database state.

**Anti-Pattern 2**: Not waiting for AJAX in JavaScript tests

```php
// WRONG - Race condition
$page->clickLink('Load More');
$this->assertSession()->pageTextContains('New Content');  // Might not be loaded yet!

// RIGHT - Wait for AJAX
$page->clickLink('Load More');
$this->assertSession()->assertWaitOnAjaxRequest();
$this->assertSession()->pageTextContains('New Content');
```

**WHY**: JavaScript execution is asynchronous. Tests must wait for operations to complete or they become flaky.

**Anti-Pattern 3**: Using `sleep()` instead of proper waits

```php
// WRONG - Fixed timing is unreliable
$page->clickLink('Submit');
sleep(2);  // Hope 2 seconds is enough
$this->assertSession()->pageTextContains('Success');

// RIGHT - Wait for specific condition
$page->clickLink('Submit');
$this->assertSession()->waitForText('Success', 10000);  // Wait up to 10 seconds
```

**WHY**: System load varies. Fixed sleep times cause flaky tests that sometimes pass, sometimes fail. Wait for specific conditions instead.

**Anti-Pattern 4**: Not cleaning up test data

```php
// WRONG - Leaves test pollution
public function testFeature(): void {
  $node = Node::create(['type' => 'article'])->save();
  // Test runs but node remains in database
}

// RIGHT - Tests automatically clean up
// Drupal test base classes handle cleanup automatically
// Just rely on setUp/tearDown
```

**WHY**: Drupal's test base classes automatically clean up. Don't try to manage cleanup manually unless you're using DTT (Drupal Test Traits) with existing sites.

## See Also

- [Testing Infrastructure Setup](testing-infrastructure-setup.md)
- [Running and Debugging Tests](running-debugging-tests.md)
- [Gander Performance Testing](gander-performance-testing.md)
- Reference: [PHPUnit best practices - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal)
- Reference: [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
