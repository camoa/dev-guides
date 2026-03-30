---
description: Testing AI-generated Drupal contributions — test type selection by contribution type, what AI-generated tests miss, and how to evaluate test quality
drupal_version: "11.x"
---

# Testing AI Code

## When to Use

> Use this when writing or reviewing tests for AI-generated Drupal contributions and you need to ensure adequate test coverage.

## Decision

| Contribution Type | Minimum Test Requirement | Framework |
|------------------|------------------------|-----------|
| Bug fix | Test that reproduces the bug + test that verifies the fix | Kernel or Functional test |
| New feature (UI) | Functional test covering user-facing behavior | FunctionalJavascript or Functional test |
| New feature (API) | Kernel test for the service layer | Kernel test |
| Form changes | Functional test with form submission | Functional test |
| Access control | Kernel test with different user roles | Kernel test |
| Plugin/service | Unit test for pure logic, Kernel test for integration | Unit + Kernel test |

## Pattern

**What AI-generated tests miss:**
1. Edge cases — AI tests the happy path; it rarely tests empty input, null values, maximum lengths, or special characters
2. Error conditions — AI rarely tests what happens when a service is unavailable or an entity doesn't exist
3. Access control — AI often tests with admin permissions; test with anonymous, authenticated, and role-specific users
4. Mock-heavy tests that don't catch real issues — use Kernel tests to test with actual Drupal services

**Testing commands:**

```bash
# Run specific test class
php vendor/bin/phpunit -c web/core web/modules/custom/my_module/tests/src/Kernel/MyServiceTest.php

# Run all tests for a module
php vendor/bin/phpunit -c web/core --group=my_module

# Run with verbose output
php vendor/bin/phpunit -c web/core --verbose --debug web/modules/custom/my_module/tests/
```

**Questions to ask about AI-generated tests:**
- Does the test actually verify the behavior, or just verify that code runs without errors?
- Are assertions specific enough? (`assertNotEmpty` is weak; `assertEquals('expected', $actual)` is strong)
- Does the test set up realistic data?
- Would this test catch a regression if someone changed the implementation?

## Common Mistakes

- **Wrong**: Accepting tests that "pass" without reading them → **Right**: AI-generated tests may pass by testing nothing meaningful (e.g., asserting a service exists without testing its behavior)
- **Wrong**: Using only Unit tests → **Right**: Unit tests are fast but don't catch integration issues; most Drupal contributions need at least Kernel tests
- **Wrong**: Mocking Drupal services unnecessarily in Kernel tests → **Right**: In Kernel tests, real services are available; mocking them hides integration bugs
- **Wrong**: Not testing the negative case → **Right**: If your code should deny access, test that it actually denies access, not just that it grants access to authorized users

## See Also

- [AI Code Review Checklist](ai-code-review-checklist.md)
- [Human Review Requirements](human-review-requirements.md)
- [Coding Standards](coding-standards.md)
