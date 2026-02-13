---
description: Security, performance, and development standards best practices for writing maintainable Drupal tests
drupal_version: "11.x"
---

# Best Practices & Anti-Patterns

## When to Use

Consult this guide when writing tests, reviewing code, or establishing testing standards for your team.

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

## Decision: Development Standards

| Practice | Implementation | Why |
|----------|----------------|-----|
| **Use data providers** | `@dataProvider` for multiple test cases | Reduces code duplication |
| **Test one behavior per method** | Each test verifies one thing | Easier debugging |
| **Use descriptive test names** | Name describes what's tested | Self-documenting tests |
| **Document complex tests** | PHPDoc explains test scenario | Maintainability |
| **Mock external dependencies** | Never call real APIs in tests | Fast, reliable tests |

## Pattern: Development Standards

```php
/**
 * Tests email validation with various input formats.
 *
 * @dataProvider emailProvider
 */
public function testEmailValidation($email, $expected_valid, $description): void {
  $result = $this->validator->validateEmail($email);
  $this->assertEquals($expected_valid, $result, $description);
}

public function emailProvider(): array {
  return [
    'valid email' => ['test@example.com', TRUE, 'Standard email format'],
    'invalid format' => ['notanemail', FALSE, 'Missing @ symbol'],
    'empty string' => ['', FALSE, 'Empty input'],
    'no domain' => ['test@', FALSE, 'Missing domain'],
    'international domain' => ['test@münchen.de', TRUE, 'IDN domain'],
  ];
}
```

## Common Anti-Patterns

**Anti-Pattern 1: Using database queries in Unit tests**

- **Wrong**: Accessing database in Unit tests → Slow tests, database dependencies
- **Right**: Mock data instead → Fast, isolated tests

**Anti-Pattern 2: Not waiting for AJAX in JavaScript tests**

- **Wrong**: Checking content immediately after AJAX trigger → Race conditions, flaky tests
- **Right**: Call `assertWaitOnAjaxRequest()` → Reliable test execution

**Anti-Pattern 3: Using sleep() instead of proper waits**

- **Wrong**: Fixed timing with `sleep(2)` → Unreliable, slow tests
- **Right**: Wait for specific conditions with `waitForText()` → Reliable, fast as possible

**Anti-Pattern 4: Testing multiple behaviors in one method**

- **Wrong**: One test method verifies multiple unrelated things → Hard to debug failures
- **Right**: One behavior per test method → Clear failure messages

**Anti-Pattern 5: Not testing permission boundaries**

- **Wrong**: Only testing happy path with admin user → Security vulnerabilities
- **Right**: Test with users who should NOT have access → Catch access control bugs

## See Also

- [Testing Infrastructure Setup](testing-infrastructure-setup.md)
- [Running and Debugging Tests](running-debugging-tests.md)
- [Gander Performance Testing](gander-performance-testing.md)
- Reference: [PHPUnit best practices - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal)
- Reference: [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
