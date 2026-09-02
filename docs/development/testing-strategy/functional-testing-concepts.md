---
description: "Functional/system testing — verifying feature-level behavior through the full stack in-process, without a real browser."
tldr: "Functional tests verify feature behavior via HTTP or equivalent without a browser — real stack, real DB, no browser rendering engine. In Drupal this is BrowserTestBase/FunctionalJavascript; use for permission enforcement, multi-step workflows, and feature regressions you cannot easily reach via integration tests."
---

# Functional Testing Concepts

## When to Use

> When you need to verify that the system behaves correctly from a **feature/user-behavior perspective** — not at the component level, but at the "does this feature do what it is supposed to do?" level. Functional tests exercise the system end-to-end within a controlled environment, without necessarily going through a real browser.

## Functional vs. Integration vs. E2E

These terms are used inconsistently across communities. For this guide:

| Term | Scope | Browser? | Real DB? |
|---|---|---|---|
| Integration | Two or more components in the same process | No | Typically yes (test DB) |
| Functional / System | Feature-level behavior, full stack in-process | No | Yes (test DB) |
| E2E | User journey through real browser + real stack | Yes | Yes |

A **functional test** exercises the system's feature behavior from the outside (HTTP request or equivalent), but without a real browser rendering engine. It answers: "If I call this feature, does it do what the spec says?"

In Drupal, PHPUnit's `Functional` and `FunctionalJavascript` test classes are functional tests in this sense. In a Next.js API route context, calling the route handler directly with a test HTTP client is a functional test.

## What Functional Tests Catch

- Feature regressions: "This endpoint used to return 200, now it returns 403"
- Auth and permission enforcement at the feature level
- Response format correctness (JSON schema, HTML structure)
- Multi-step workflows (form submit → confirmation → database write → email)
- Configuration-driven behavior (does enabling Feature Flag X change the response?)

## Pattern

```php
// Drupal functional test (PHPUnit BrowserTestBase)
// Tests the feature from the outside: HTTP → Drupal → DB
// No real browser, but real Drupal bootstrap

class UserRegistrationTest extends BrowserTestBase {
  public function testRegistrationCreatesUserAndSendsEmail(): void {
    // Arrange
    $this->drupalGet('user/register');
    // Act
    $this->submitForm([
      'mail' => 'alice@example.com',
      'pass[pass1]' => 'S3cretPass!',
      'pass[pass2]' => 'S3cretPass!',
    ], 'Create new account');
    // Assert
    $this->assertSession()->statusCodeEquals(200);
    $this->assertSession()->pageTextContains('Registration successful');
    $user = user_load_by_mail('alice@example.com');
    $this->assertNotNull($user);
  }
}
```

## When Functional Tests Are the Right Choice

- The feature involves configuration, routing, or middleware that integration tests cannot easily exercise
- You need to test Drupal's permission system (access callbacks, route requirements)
- The workflow spans multiple HTTP requests (wizard-style forms, OAuth redirects)
- You want to test an entire user story without the overhead of a real browser

## Common Mistakes

- Using functional tests for logic that is better covered by unit tests → Functional tests are slow; logic belongs at the unit level
- Testing every variant through a functional test → Test logic variants with unit tests; test the integration wire-up with one or two functional tests
- Not cleaning up state between functional tests → Test pollution causes intermittent failures; use proper setup/teardown
- Conflating "functional" with "E2E" → Functional tests run in-process; E2E uses a real browser; they have different costs and failure modes

## See Also

- ← Previous: [Integration Testing Concepts](integration-testing-concepts.md) | Next: [E2E Testing Concepts](e2e-testing-concepts.md) →
- Related: [drupal/testing](https://camoa.github.io/dev-guides/drupal/testing/) — Drupal functional and FunctionalJavascript test setup
- Related: [drupal/tdd](https://camoa.github.io/dev-guides/drupal/tdd/) — TDD per Drupal feature type
