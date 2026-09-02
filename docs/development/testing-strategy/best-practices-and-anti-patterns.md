---
description: "Cross-cutting testing best practices and the anti-pattern catalog — Liar, Giant, Slow Poke, Mockery, Sleeper, and more."
tldr: "Tests are production code — apply the same review standards. Key anti-patterns: The Liar (passes but verifies nothing), The Mockery (mocking your own code), The Sleeper (sleep instead of condition waits), The Optimist (happy path only). Every feature needs explicit security test cases for auth, permissions, and input handling."
---

# Best Practices and Anti-Patterns

## When to Use

> During code review, when evaluating an inherited test suite, or as a checklist before merging a feature. These are cross-cutting patterns and anti-patterns that apply across all test types.

## Core Best Practices

**Make tests readable first, clever never.** A test that fails at 11 PM must be understood by a tired developer in 60 seconds. Optimize for clarity over brevity.

**Each test is an island.** No shared mutable state, no execution-order dependencies, no test that sets up data for another test. Every test sets up its own world and tears it down.

**Tests are production code.** Apply the same code review standards: meaningful names, DRY (through test helpers and factories, not inheritance), no duplication, no dead code. A messy test suite accumulates its own technical debt.

**A failing test must point to exactly one bug.** If a test failure requires you to debug the test before debugging the application, the test is too coarse-grained or too implementation-coupled.

**Maintain test suite speed.** The unit suite must run in under 10 seconds. Anything slower stops being run on every change. Profile, parallelize, and mock aggressively in unit tests.

## Anti-Pattern Catalog

These fixes are the test author's to apply, while writing or while the change is still theirs. A reviewer that finds one of these in a test it did not write raises it as a finding and does not edit the test — see the TDD guide's [Changing Existing Tests](https://camoa.github.io/dev-guides/development/tdd-spec-driven/changing-existing-tests/) section.

**The Liar** — A test that passes but does not actually verify the claimed behavior:

```python
# "Tests" password hashing but assertion is vacuous
def test_password_is_hashed():
    user = User(password='secret')
    assert user.password is not None  # passes even if stored in plain text
```

Fix: assert the specific behavior — `assert user.password != 'secret'` and `assert bcrypt.verify('secret', user.password)`.

**The Giant** — One test that verifies many unrelated behaviors. When it fails, you cannot tell which behavior broke. Fix: one behavior per test.

**The Slow Poke** — A unit test that hits a real database, real HTTP, or real file system. Runs in seconds instead of milliseconds; CI pipeline becomes a bottleneck. Fix: stub or fake all external systems in unit tests.

**The Mockery** — Every dependency is mocked, including internal application code. Tests verify that mocks were called with specific arguments — not that the application produces correct output. Fix: mock only external boundaries; use real implementations for your own code.

**Hardcoded Dates and Random Seeds** — Tests that embed today's date or use unseeded random values produce different results at different times. Fix: inject clock and random dependencies; stub them in tests.

**The Optimistic** — Test only the happy path. All error cases, null inputs, and boundary values are untested. Fix: add parameterized cases for boundaries, nulls, and error conditions.

**The Sleeper** — `await sleep(1000)` to wait for an async operation. Slow, and breaks when the operation takes more than the sleep duration. Fix: wait for the specific condition (DOM element, API response, state change).

**Copy-Paste Tests** — Duplicated test code with minor variations. When setup logic changes, every copy must be updated. Fix: extract factory methods or parameterized tests.

**The Invisible Assertion** — A test with no assertions that "passes" because it runs without throwing. Fix: always assert; use a linter rule to fail tests with no assertions.

## Security Testing Best Practices

Every feature that handles user input, auth, or permissions needs explicit security test cases:

- Test that SQL injection payloads are handled safely (parameterized queries, not string interpolation)
- Test that XSS payloads are escaped on output (not just stripped on input)
- Test that unauthorized users cannot access protected resources (not just that authorized users can)
- Test that expired or tampered tokens are rejected
- Test that rate limiting triggers under load

Security tests are not optional extras — they are correctness tests for a critical class of behavior. Reference: [development/security-practices](https://camoa.github.io/dev-guides/development/security-practices/).

## Testing Checklist for New Features

Before a feature is merged:
- [ ] Happy path is covered by at least one test
- [ ] Edge cases (null, empty, boundary values) are covered for all logic-heavy code
- [ ] Error paths are tested (what happens when it fails?)
- [ ] New code does not require changes to test for other features (isolation preserved)
- [ ] Integration points (DB, external API) are tested with appropriate doubles
- [ ] No new flaky tests introduced (all new tests pass 10 consecutive times)
- [ ] Test names clearly describe scenario and expected outcome
- [ ] CI passes on first run, not "retry until green"

## Common Mistakes

- Deleting tests instead of fixing them → Hiding a failing test hides the bug; fix the bug or the test
- Commenting out failing tests → Same problem as deleting; creates invisible debt
- Green CI = done → CI only runs the tests you have; untested behavior is still untested
- Retroactive test writing just to hit coverage → Post-hoc tests describe current behavior (including bugs) instead of intended behavior; TDD tests describe intended behavior
- Confusing "hard to test" with "not worth testing" → Hard to test means the code is poorly designed; refactor for testability first

## See Also

- ← Previous: [What to Test and What Not To](what-to-test-and-what-not.md) | Next: [Choosing a Test Type](choosing-a-test-type.md) →
- Related: [development/security-practices](https://camoa.github.io/dev-guides/development/security-practices/)
- Related: [testing/ai-test-generation](https://camoa.github.io/dev-guides/testing/ai-test-generation/)
- Reference: Kostis Kapelonis, [Software Testing Anti-patterns](https://blog.codepipes.com/testing/software-testing-antipatterns.html)
