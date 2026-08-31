---
description: Cross-cutting testing best practices and the anti-pattern catalog — Liar, Giant, Slow Poke, Mockery, Sleeper, and more.
tldr: "Tests are production code — apply the same review standards. Key anti-patterns: The Liar (passes but verifies nothing), The Mockery (mocking your own code), The Sleeper (sleep instead of condition waits), The Optimist (happy path only). Every feature needs explicit security test cases for auth, permissions, and input handling."
---

# Best Practices and Anti-Patterns

## When to Use

> Use as a checklist during code review, when evaluating an inherited test suite, or before merging a feature. These patterns apply across all test types.

## Decision

**Core best practices:**
- Make tests readable first, clever never — a failing test at 11 PM must be understood in 60 seconds
- Each test is an island — no shared mutable state, no execution-order dependencies
- Tests are production code — same review standards: meaningful names, DRY through helpers, no dead code
- A failing test must point to exactly one bug
- Unit suite must run in under 10 seconds — profile, parallelize, mock aggressively

## Pattern

These fixes are the test author's to apply, while writing or while the change is still theirs. A reviewer that finds one of these in a test it did not write raises it as a finding and does not edit the test — see [TDD & Spec-Driven Development — Changing Existing Tests](https://camoa.github.io/dev-guides/development/tdd-spec-driven/changing-existing-tests/).

**Anti-pattern catalog:**

| Anti-pattern | Problem | Fix |
|---|---|---|
| **The Liar** | Passes but doesn't verify claimed behavior (`assert user.password is not None`) | Assert the specific behavior (`assert user.password != 'secret'`) |
| **The Giant** | One test verifies many unrelated behaviors; when it fails, you don't know which | One behavior per test |
| **The Slow Poke** | Unit test hits real DB, real HTTP, or real filesystem; CI bottleneck | Stub or fake all external systems in unit tests |
| **The Mockery** | Every dependency mocked including internal code; tests verify mock calls, not output | Mock only external boundaries; use real implementations for your code |
| **Hardcoded Dates** | Embeds today's date or unseeded random values | Inject clock and random dependencies; stub in tests |
| **The Optimist** | Tests only the happy path; all error/null/boundary cases untested | Add parameterized cases for boundaries, nulls, error conditions |
| **The Sleeper** | `await sleep(1000)` to wait for async | Wait for the specific condition |
| **Copy-Paste Tests** | Duplicated test code with minor variations | Extract factory methods or parameterized tests |
| **Invisible Assertion** | Test with no assertions "passes" because it runs without throwing | Always assert; use a linter rule to fail tests with no assertions |

**Security test cases — required for every feature handling user input, auth, or permissions:**
- SQL injection payloads are handled safely
- XSS payloads are escaped on output
- Unauthorized users cannot access protected resources
- Expired or tampered tokens are rejected
- Rate limiting triggers under load

## Common Mistakes

- **Wrong**: Deleting tests instead of fixing them → **Right**: Fix the bug or the test; hiding a failing test hides the bug
- **Wrong**: Commenting out failing tests → **Right**: Creates invisible debt; quarantine with a ticket instead
- **Wrong**: "Green CI = done" → **Right**: CI only runs the tests you have; untested behavior is still untested
- **Wrong**: Retroactive test writing just to hit coverage → **Right**: Post-hoc tests describe current behavior (including bugs); TDD tests describe intended behavior
- **Wrong**: "Hard to test" = "not worth testing" → **Right**: Hard to test means poorly designed; refactor for testability first

## See Also

- [What to Test and What Not To](what-to-test-and-what-not.md) | Next: [Choosing a Test Type](choosing-a-test-type.md)
- Related: [development/security-practices](https://camoa.github.io/dev-guides/development/security-practices/)
- Related: [testing/ai-test-generation](https://camoa.github.io/dev-guides/testing/ai-test-generation/)
- Reference: Kostis Kapelonis, [Software Testing Anti-patterns](https://blog.codepipes.com/testing/software-testing-antipatterns.html)
