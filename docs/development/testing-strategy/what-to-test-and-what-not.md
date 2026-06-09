---
description: Risk/ROI matrix for test coverage — test behavior not implementation, what not to test, and the Testing Library principle.
tldr: Test observable behavior, not implementation details. High-risk code (auth, money, complex logic, API boundaries) deserves heavy test investment; framework internals, trivial delegation, and generated code get none. A test that breaks on refactor when behavior is unchanged is testing the wrong thing.
---

# What to Test and What Not To

## When to Use

> Apply this matrix when planning coverage for a new feature, reviewing existing tests for ROI, or feeling pressure to test everything. Deciding what not to test is as important as deciding what to test.

## Decision

| Code type | Risk | Test investment | Why |
|---|---|---|---|
| Business logic (rules, calculations, state machines) | High | Unit tests, parameterized edge cases | Bugs here lose money or trust |
| Auth and permissions | High | Integration + functional | Silent auth bugs are security vulnerabilities |
| Data transformations and parsing | High | Unit, table-driven | Edge cases and encoding errors are hard to spot |
| API boundaries (request/response) | High | Integration at the HTTP layer | Serialization bugs reach all consumers |
| Critical user journeys (checkout, login) | High | E2E smoke test + integration | Must work end-to-end for the app to function |
| UI component interactions | Medium | Integration (Testing Library style) | Most UI bugs are in component composition, not isolation |
| Simple CRUD with no business logic | Low | One integration test to verify wiring | Trivial logic; wiring test confirms hook-up |
| Third-party library behavior | None | Do not test it | Trust the library; test your usage of it |
| Generated code (ORMs, scaffolding) | None | Do not test it | The generator is tested; not its output |
| Trivial getters/setters | None | Do not test them | No logic to break |

## Pattern

```python
# BAD: tests implementation (private field)
def test_vip_discount_sets_discount_flag():
    cart = Cart()
    cart.apply_vip()
    assert cart._discount_rate == 0.10  # breaks on any rename

# GOOD: tests observable behavior
def test_vip_discount_reduces_total_by_10_percent():
    cart = Cart(items=[Item(price=100)])
    cart.apply_vip()
    assert cart.total() == 90.00  # survives any refactor that preserves behavior
```

**What not to test:**
- Framework and library internals — test your configuration produces the expected output, not that the framework works
- Trivial delegation — a method that only passes through to another method
- Private methods — test through the public API; if they need direct testing, extract them to their own class
- Assertions that can never fail given the Arrange phase

## Common Mistakes

- **Wrong**: Testing private methods directly → **Right**: Couples tests to implementation; breaks on every refactor
- **Wrong**: Testing third-party libraries → **Right**: Test your usage of them; if the library is broken, its own tests should catch it
- **Wrong**: Happy-path only → **Right**: Most bugs live at boundaries; always add edge case tests for logic-heavy code
- **Wrong**: Testing that mocks return the right value → **Right**: You configured the mock; this tests nothing
- **Wrong**: Over-testing trivial code to hit coverage targets → **Right**: Reduces signal-to-noise; lowers ROI of every test

## See Also

- [Coverage Philosophy](coverage-philosophy.md) | Next: [Best Practices and Anti-Patterns](best-practices-and-anti-patterns.md)
- Related: [Test Doubles](test-doubles.md) — which external things to stub vs keep real
- Reference: Kent C. Dodds, [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles)
- Reference: Martin Fowler, [UnitTest — "The Solitary Unit Test"](https://martinfowler.com/bliki/UnitTest.html)
