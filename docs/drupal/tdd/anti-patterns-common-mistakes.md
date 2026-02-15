---
description: Avoid Drupal testing anti-patterns including wrong test types, over-mocking, sleep waits, and shared state.
---

# Anti-Patterns & Common Mistakes

## When to Use
Avoid these patterns that lead to slow, brittle, unmaintainable tests.

## Anti-Patterns

### Using Wrong Test Type
**Problem**: BrowserTestBase for testing service logic
**Why it's bad**: 10-30 seconds per test vs 0.5 seconds for Kernel test -- no benefit, massive cost
**Fix**: Use lightest test type that can verify requirement -- Unit for pure logic, Kernel for services/database, Browser only for HTTP simulation

**Example**:
```php
// ANTI-PATTERN: Browser test for service logic
class MyServiceTest extends BrowserTestBase {
  public function testServiceMethod(): void {
    $this->drupalGet('/'); // Unnecessary HTTP overhead
    $service = \Drupal::service('my_module.service');
    $result = $service->calculate(10);
    $this->assertEquals(20, $result);
  }
}

// CORRECT: Kernel test
class MyServiceTest extends KernelTestBase {
  public function testServiceMethod(): void {
    $service = $this->container->get('my_module.service');
    $result = $service->calculate(10);
    $this->assertEquals(20, $result);
  }
}
```

### Testing Implementation Instead of Behavior
**Problem**: Asserting on internal method calls instead of outcomes
**Why it's bad**: Tests break when refactoring, even if behavior unchanged
**Fix**: Assert on observable behavior -- return values, database state, rendered output

**Example**:
```php
// ANTI-PATTERN: Testing implementation
public function testServiceCallsLogger(): void {
  $mock_logger = $this->createMock(LoggerInterface::class);
  $mock_logger->expects($this->once())->method('info'); // Brittle
  $service = new MyService($mock_logger);
  $service->doSomething();
}

// CORRECT: Testing behavior
public function testServiceReturnsProcessedData(): void {
  $service = $this->container->get('my_module.service');
  $result = $service->doSomething();
  $this->assertEquals('expected result', $result);
}
```

### Over-Mocking
**Problem**: Mocking every dependency with complex mock setup
**Why it's bad**: Test becomes harder to maintain than the code it tests; doesn't verify real integration
**Fix**: Use Kernel test to leverage real container, or question if code is too coupled

**Example**:
```php
// ANTI-PATTERN: Mocking 5+ dependencies
public function testComplexService(): void {
  $mock1 = $this->createMock(Service1::class);
  $mock2 = $this->createMock(Service2::class);
  $mock3 = $this->createMock(Service3::class);
  // ... 10 lines of mock setup ...
  $service = new ComplexService($mock1, $mock2, $mock3);
  // Test becomes unreadable
}

// CORRECT: Use Kernel test with real container
public function testComplexService(): void {
  $service = $this->container->get('my_module.complex_service');
  $result = $service->process(['data' => 'value']);
  $this->assertEquals('expected', $result);
}
```

### Sleep Instead of Wait
**Problem**: Using `sleep(2)` in JavaScript tests
**Why it's bad**: Flaky tests (sometimes 2 seconds isn't enough), unnecessarily slow
**Fix**: Use `waitForElement()`, `waitForText()`, or custom wait conditions

**Example**:
```php
// ANTI-PATTERN: Hardcoded sleep
public function testAjax(): void {
  $page->click('#trigger-ajax');
  sleep(2); // Sometimes fails, sometimes wastes time
  $this->assertSession()->pageTextContains('Result');
}

// CORRECT: Wait for condition
public function testAjax(): void {
  $page->click('#trigger-ajax');
  $this->assertSession()->waitForText('Result');
}
```

### Testing Core Functionality
**Problem**: Writing tests that verify Drupal core behavior
**Why it's bad**: Wastes time, core already tested, doesn't verify YOUR code
**Fix**: Test your custom logic's integration with core, not core itself

**Example**:
```php
// ANTI-PATTERN: Testing core
public function testNodeSaveWorks(): void {
  $node = Node::create(['type' => 'page', 'title' => 'Test']);
  $node->save();
  $this->assertNotNull($node->id()); // Testing core
}

// CORRECT: Testing your custom logic
public function testCustomNodeProcessing(): void {
  $node = Node::create(['type' => 'page', 'title' => 'Test']);
  $service = $this->container->get('my_module.node_processor');
  $result = $service->processNode($node);
  $this->assertEquals('expected_transformation', $result);
}
```

### Shared Test State
**Problem**: Tests depend on execution order or shared state
**Why it's bad**: Tests fail when run in isolation, hard to debug
**Fix**: Each test creates its own fixtures in `setUp()` or test method

**Example**:
```php
// ANTI-PATTERN: Shared state
protected $sharedNode; // Dangerous

public function testA(): void {
  $this->sharedNode = $this->createNode();
  // ...
}

public function testB(): void {
  // Assumes testA ran first -- fragile
  $this->assertEquals('page', $this->sharedNode->bundle());
}

// CORRECT: Independent tests
public function testA(): void {
  $node = $this->createNode();
  // Test using $node
}

public function testB(): void {
  $node = $this->createNode();
  // Test using $node
}
```

## Common Mistakes

### Security Testing
- Not testing permission denials -- users access restricted content
- Using admin user for all tests -- permission checks never verified
- Not testing CSRF tokens -- forms vulnerable to cross-site requests
- Not testing input sanitization -- XSS vulnerabilities

### Performance Testing
- Installing unnecessary modules -- 2x-5x slower tests
- Using Browser tests when Kernel would work -- 10x slower
- Not using `@group` tags -- can't run fast tests separately
- Running full test suite on every commit -- slow feedback loop

### Reliability
- Hardcoding IDs or paths -- breaks when data changes
- Brittle CSS selectors (`.container > div:nth-child(3)`) -- breaks when HTML changes
- Not cleaning up test data in Kernel tests -- database pollution
- Expecting specific error messages -- breaks when wording changes (test error code/type instead)

### Development Workflow
- Writing tests after implementation -- misses TDD benefits
- Not running tests before commit -- broken code reaches repo
- Ignoring deprecation warnings -- tests break on Drupal upgrade
- Not using coverage reports -- dead code accumulates

## See Also
- Reference: [Test Driven Development for Decoupled Drupal | Lullabot](https://www.lullabot.com/articles/test-driven-development-decoupled-drupal)
