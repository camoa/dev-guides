---
description: Functional/system testing — verifying feature-level behavior through the full stack in-process, without a real browser.
tldr: Functional tests verify feature behavior via HTTP or equivalent without a browser — real stack, real DB, no browser rendering engine. In Drupal this is BrowserTestBase/FunctionalJavascript; use for permission enforcement, multi-step workflows, and feature regressions you cannot easily reach via integration tests.
---

# Functional Testing Concepts

## When to Use

> Use functional tests when the feature involves configuration, routing, permissions, or multi-request workflows that integration tests cannot easily exercise. Do not use them for logic variants — those belong in unit tests.

## What Functional Tests Catch

- Feature regressions: "This endpoint used to return 200, now it returns 403"
- Auth and permission enforcement at the feature level
- Response format correctness (JSON schema, HTML structure)
- Multi-step workflows (form submit → confirmation → database write → email)
- Configuration-driven behavior (does enabling Feature Flag X change the response?)

## Decision

| Term | Scope | Browser? | Real DB? |
|---|---|---|---|
| Integration | Two or more components in the same process | No | Typically yes (test DB) |
| Functional / System | Feature-level behavior, full stack in-process | No | Yes (test DB) |
| E2E | User journey through real browser + real stack | Yes | Yes |

Functional tests are the right choice when:
- The feature requires Drupal's permission system (access callbacks, route requirements)
- The workflow spans multiple HTTP requests (wizard-style forms, OAuth redirects)
- You need to test routing or middleware that integration tests cannot reach
- You want to test an entire user story without the overhead of a real browser

## Pattern

```php
// Drupal functional test (PHPUnit BrowserTestBase)
// Tests the feature from the outside: HTTP → Drupal → DB
class UserRegistrationTest extends BrowserTestBase {
  public function testRegistrationCreatesUserAndSendsEmail(): void {
    $this->drupalGet('user/register');
    $this->submitForm([
      'mail' => 'alice@example.com',
      'pass[pass1]' => 'S3cretPass!',
      'pass[pass2]' => 'S3cretPass!',
    ], 'Create new account');
    $this->assertSession()->statusCodeEquals(200);
    $this->assertSession()->pageTextContains('Registration successful');
    $user = user_load_by_mail('alice@example.com');
    $this->assertNotNull($user);
  }
}
```

## Common Mistakes

- **Wrong**: Using functional tests for logic that unit tests can cover → **Right**: Functional tests are slow; logic belongs at the unit level
- **Wrong**: Testing every logic variant through a functional test → **Right**: Test variants with unit tests; use functional for the integration wire-up
- **Wrong**: Not cleaning up state between functional tests → **Right**: Use proper setup/teardown; leftover state causes intermittent failures
- **Wrong**: Conflating "functional" with "E2E" → **Right**: Functional runs in-process; E2E uses a real browser — different costs and failure modes

## See Also

- [Integration Testing Concepts](integration-testing-concepts.md) | Next: [E2E Testing Concepts](e2e-testing-concepts.md)
- Related: [drupal/testing](https://camoa.github.io/dev-guides/drupal/testing/) — Drupal functional and FunctionalJavascript test setup
- Related: [drupal/tdd](https://camoa.github.io/dev-guides/drupal/tdd/) — TDD per Drupal feature type
