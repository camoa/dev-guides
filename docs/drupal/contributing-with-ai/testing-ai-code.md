---
description: "Testing AI-generated Drupal contributions — test type selection by contribution type, what AI-generated tests miss, and how to evaluate test quality"
tldr: "Use this when writing or reviewing tests for AI-generated Drupal contributions and you need to ensure adequate test coverage."
drupal_version: "11.x"
---

# Testing AI Code

## When to Use

> When writing or reviewing tests for AI-generated Drupal contributions and you need to ensure adequate test coverage.

## Decision: Testing by Contribution Type

| Contribution Type | Minimum Test Requirement | Framework |
|---|---|---|
| Bug fix | Test that reproduces the bug + test that verifies the fix | Kernel or Functional test |
| New feature (UI) | Functional test covering user-facing behavior | FunctionalJavascript or Functional test |
| New feature (API) | Kernel test for the service layer | Kernel test |
| Form changes | Functional test with form submission | Functional test |
| Access control | Kernel test with different user roles | Kernel test |
| Plugin/service | Unit test for pure logic, Kernel test for integration | Unit + Kernel test |

## Pattern: What AI-Generated Tests Miss

1. **Edge cases** — AI tests the happy path. It rarely tests empty input, null values, maximum lengths, special characters, or concurrent access.
2. **Error conditions** — AI rarely tests what happens when a service is unavailable, a database query fails, or an entity doesn't exist.
3. **Access control** — AI often tests with admin permissions. Test with anonymous, authenticated, and role-specific users.
4. **Mock-heavy tests that don't catch real issues** — AI loves mocking. But mocked tests can pass while the real integration fails. Use Kernel tests to test with actual Drupal services.

## Pattern: Testing Commands

```bash
# Run specific test class
php vendor/bin/phpunit -c web/core web/modules/custom/my_module/tests/src/Kernel/MyServiceTest.php

# Run all tests for a module
php vendor/bin/phpunit -c web/core --group=my_module

# Run with verbose output (useful for debugging AI-generated tests)
php vendor/bin/phpunit -c web/core --verbose --debug web/modules/custom/my_module/tests/

# Check test coverage
php vendor/bin/phpunit -c web/core --coverage-html /tmp/coverage web/modules/custom/my_module/tests/
```

## Pattern: Review AI-Generated Tests

Ask these questions about AI-generated tests:
- Does the test actually verify the behavior, or just verify that code runs without errors?
- Are assertions specific enough? (`assertNotEmpty` is weak; `assertEquals('expected', $actual)` is strong)
- Does the test set up realistic data, or use trivial test values?
- Would this test catch a regression if someone changed the implementation?
- Does the test clean up after itself?

## Common Mistakes

- **Accepting tests that "pass" without reading them** — AI-generated tests may pass by testing nothing meaningful (e.g., asserting a service exists without testing its behavior)
- **Using only Unit tests** — Unit tests are fast but don't catch integration issues. Most Drupal contributions need at least Kernel tests.
- **Mocking Drupal services unnecessarily** — In Kernel tests, real services are available. Mocking them hides integration bugs.
- **Not testing the negative case** — If your code should deny access, test that it actually denies access, not just that it grants access to authorized users

## See Also

- [AI Code Review Checklist](ai-code-review-checklist.md) — pre-submission verification
- [Human Review Requirements](human-review-requirements.md) — review standards
- [Coding Standards](coding-standards.md) — code quality expectations
