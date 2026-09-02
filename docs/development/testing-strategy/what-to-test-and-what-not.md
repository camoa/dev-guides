---
description: "Risk/ROI matrix for test coverage — test behavior not implementation, what not to test, and the Testing Library principle."
tldr: "Test observable behavior, not implementation details. High-risk code (auth, money, complex logic, API boundaries) deserves heavy test investment; framework internals, trivial delegation, and generated code get none. A test that breaks on refactor when behavior is unchanged is testing the wrong thing."
---

# What to Test and What Not To

## When to Use

> When planning test coverage for a new feature, when reviewing existing tests for ROI, or when feeling pressure to test everything. Deciding what not to test is as important as deciding what to test.

## Test Behavior, Not Implementation

The most reusable test principle: **test what a unit does (observable behavior), not how it does it (internal implementation)**.

A test that verifies observable behavior survives refactoring. A test that verifies internal method calls, field names, or execution sequence breaks every time you improve the code.

```python
# BAD: tests implementation (how the discount is stored internally)
def test_vip_discount_sets_discount_flag():
    cart = Cart()
    cart.apply_vip()
    assert cart._discount_rate == 0.10  # testing private field

# GOOD: tests behavior (what the customer observes)
def test_vip_discount_reduces_total_by_10_percent():
    cart = Cart(items=[Item(price=100)])
    cart.apply_vip()
    assert cart.total() == 90.00  # testing observable outcome
```

When `_discount_rate` is renamed, the bad test breaks. When the implementation is replaced with a lookup table, the bad test breaks. The good test survives both changes.

## What to Test: Risk/ROI Matrix

| Code type | Risk | Test investment | Why |
|---|---|---|---|
| Business logic (rules, calculations, state machines) | High | Unit tests, parameterized edge cases | Bugs here lose money or trust |
| Auth and permissions | High | Integration + functional | Silent bugs in auth are security vulnerabilities |
| Data transformations and parsing | High | Unit, table-driven | Edge cases and encoding errors are hard to spot |
| API boundaries (request/response) | High | Integration at the HTTP layer | Serialization bugs reach all consumers |
| Critical user journeys (checkout, login) | High | E2E smoke test + integration | Must work end-to-end for the app to function |
| UI component interactions | Medium | Integration (Testing Library style) | Most UI bugs are in component composition, not isolation |
| Simple CRUD with no business logic | Low | One integration test to verify wiring | Logic is trivial; wiring test confirms it is hooked up |
| Configuration and defaults | Low | One integration test | Just verify it applies |
| Third-party library behavior | None | Do not test it | Trust the library; test your usage of it |
| Generated code (ORMs, scaffolding) | None | Do not test it | The generator should be tested, not its output |
| Trivial getters/setters | None | Do not test them | No logic to break |

## The Testing Library Principle

Kent C. Dodds / Testing Library: "The more your tests resemble the way your software is used, the more confidence they can give you."

This principle guides what to test at each level:
- Test user-visible behavior, not internal state
- Test from the outside (HTTP response, DOM output, return value) rather than from inside (private field, internal method)
- Tests that break when behavior is unchanged and only internal structure changed are testing the wrong thing

## What Not to Test

**Framework and library internals** — Drupal's render pipeline, React's reconciler, ORM query generation. Test that your configuration produces the expected output, not that the framework does its job.

**Trivial delegation** — A method that only calls another method with the same arguments provides no logic to test. Test the delegated method directly.

**Private methods** — Private methods are implementation details. Test them through the public API they support. If a private method is complex enough to warrant direct testing, it probably should be extracted to its own class.

**Code written to make a test pass** — If you wrote helper code purely to satisfy a test (no production use), delete the helper.

**Assertions that can never fail** — A test that asserts `assert True` or `assert response is not None` where `response` can never be `None` given the Arrange phase adds noise with no value.

## Common Mistakes

- Testing private methods directly → Couples tests to implementation; breaks on any refactor regardless of behavior
- Testing third-party libraries → Wastes effort; if the library is broken, its own tests should catch it; test your usage
- Missing edge cases in favor of happy-path only → Most bugs live at boundaries (null, empty, negative, overflow); always add edge case tests for logic-heavy code
- Testing that mocks return the right value → You configured the mock; it will return what you told it; this tests nothing
- Over-testing trivial code to hit coverage targets → Reduces signal-to-noise in the test suite; lowers ROI of every test

## See Also

- ← Previous: [Coverage Philosophy](coverage-philosophy.md) | Next: [Best Practices and Anti-Patterns](best-practices-and-anti-patterns.md) →
- Related: [Test Doubles](test-doubles.md) — which external things to stub vs keep real
- Reference: Kent C. Dodds, [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles)
- Reference: Martin Fowler, [UnitTest — "The Solitary Unit Test"](https://martinfowler.com/bliki/UnitTest.html)
