---
description: Follow best practices for test organization, data, performance, security, reliability, and maintainability in Drupal testing.
---

# Best Practices & Patterns

## When to Use
Writing maintainable, fast, reliable tests that verify behavior, not implementation.

## Best Practices

### Test Organization
- **One assertion per concept**: Don't mix unrelated assertions in one test method
- **Descriptive test names**: `testUnpublishedNodeNotVisibleToAnonymous()` not `testNode()`
- **Use #[Group] attributes**: Tag tests by module, feature, speed
- **Test files mirror source**: `src/Service/DataProcessor.php` -> `tests/src/Unit/Service/DataProcessorTest.php`

### Test Data
- **Use traits for fixtures**: NodeCreationTrait, UserCreationTrait -- don't reinvent
- **Randomize when possible**: `randomMachineName()` prevents test pollution
- **Explicit over implicit**: `createUser(['view content'])` better than `createUser()` (permissions clear)
- **Clean up in tearDown**: For Kernel tests, explicitly delete created entities if not using Browser test auto-cleanup

### Performance
- **Minimize module list**: Only install modules you need -- every module adds overhead
- **Prefer Kernel over Browser**: 10x faster, use Browser only when HTTP context required
- **Prefer Unit over Kernel**: 100x faster, use Kernel only when container/database required
- **Parallel execution**: Use `--process-isolation` for independent tests (slower per test, faster overall)
- **Avoid full installs in Kernel**: Use `enableModules()`, `installConfig()` selectively

### Security
- **Test permission boundaries**: Verify users WITHOUT permission are denied
- **Test CSRF protection**: Ensure forms reject requests without valid tokens
- **Test XSS prevention**: Verify user input is sanitized (e.g., `check_markup()` applied)
- **Test access bypass carefully**: Don't use `bypass node access` as default test user -- masks bugs
- **Test input validation**: Verify form validation rejects malicious input

### Reliability
- **Don't depend on test execution order**: Each test should be independent
- **Avoid sleeps**: Use `waitForElement()` in JS tests, not `sleep()`
- **Mock external services**: Don't call real APIs in tests -- slow, unreliable, requires network
- **Use assertSame over assertEquals**: Catches type mismatches (`'1'` vs `1`)
- **Expect exceptions explicitly**: Use `$this->expectException()` to test error handling

### Maintainability
- **Test behavior, not implementation**: Don't assert on internal service calls, assert on outcomes
- **Avoid brittle selectors**: Use semantic CSS classes (`.success-message`) not layout classes (`.col-md-6`)
- **Don't test core**: Test YOUR code's integration with core, not core functionality
- **Keep tests readable**: If test setup is >20 lines, extract to helper method
- **Document non-obvious test logic**: Why you're testing this edge case

## Patterns

### Arrange-Act-Assert
```php
public function testFeature(): void {
  // Arrange: Set up test state
  $user = $this->createUser(['access content']);
  $node = $this->createNode(['status' => 1]);

  // Act: Perform action under test
  $access = $node->access('view', $user);

  // Assert: Verify outcome
  $this->assertTrue($access);
}
```

### Data Providers for Multiple Cases
```php
/**
 * @dataProvider providerStatusCodes
 */
public function testRouteAccess($path, $permissions, $expected_code): void {
  $user = $this->createUser($permissions);
  $this->drupalLogin($user);
  $this->drupalGet($path);
  $this->assertSession()->statusCodeEquals($expected_code);
}

public function providerStatusCodes(): array {
  return [
    'admin page denied' => ['/admin', [], 403],
    'admin page allowed' => ['/admin', ['access administration pages'], 200],
    'content page allowed' => ['/node/1', ['access content'], 200],
  ];
}
```

### Testing Exception Handling
```php
public function testInvalidInputThrowsException(): void {
  $this->expectException(\InvalidArgumentException::class);
  $this->expectExceptionMessage('Invalid data format');

  $service = $this->container->get('my_module.service');
  $service->process(['invalid' => 'data']);
}
```

## Common Mistakes
- Testing framework code (PHPUnit, Drupal core) -- wastes time
- 100% code coverage goal -- tests getters/setters, no value
- Tests coupled to implementation -- refactoring breaks tests unnecessarily
- Not running tests before committing -- broken code reaches repo
- Ignoring test failures ("flaky test, will fix later") -- technical debt accumulates

## See Also
- [Quality Gates & Audit Checklist](quality-gates-audit-checklist.md)
- [Anti-Patterns & Common Mistakes](anti-patterns-common-mistakes.md)
- [PHPUnit in Drupal | Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal)
