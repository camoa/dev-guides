---
description: "Unit testing — what belongs in a unit test, the FIRST properties, and how to avoid coupling tests to implementation."
tldr: "Unit tests verify one function or class in isolation — no DB, no HTTP, no filesystem. Apply the FIRST properties (Fast, Isolated, Repeatable, Self-validating, Timely). Test observable behavior, not private implementation details; one logical assertion per test."
---

# Unit Testing Concepts

## When to Use

> When testing a single function, method, class, or module in isolation — without reaching out to databases, HTTP, file systems, or other modules. Unit tests are the fastest feedback loop in the stack; write them when the code has meaningful logic that can be verified without external state.

## What Is a Unit?

A "unit" is the smallest meaningful behavior you can verify in isolation. The definition is intentionally fuzzy — a "unit" can be:

- A single function (pure or with injected dependencies)
- A class with its collaborators replaced by test doubles
- A module's public API surface, treating its internal structure as an implementation detail

The key word is **isolation**: a unit test verifies one thing's behavior without relying on external systems. If the test hits a database, a file, a network socket, or a clock — it is not a unit test (see [Integration Testing Concepts](integration-testing-concepts.md)).

Isolation is only half the rule. It says what a unit test must not touch; it does not say what the test may assert on. See [What a Test May Couple To](what-a-test-may-couple-to.md) for that half.

## FIRST Properties

Good unit tests are **FIRST**:

| Property | Meaning | Why it matters |
|---|---|---|
| **Fast** | Milliseconds per test | Runs on every keystroke/save; 1,000 tests in < 2s |
| **Isolated** | No shared state between tests | Tests can run in any order, any subset |
| **Repeatable** | Same output for same input, always | No time, randomness, network, or environment dependencies |
| **Self-validating** | Pass/fail determined automatically | No manual inspection needed |
| **Timely** | Written at the right time (ideally first) | Late tests are lower quality; they verify rather than design |

## What Belongs in a Unit Test

Write a unit test when:
- There is branching logic (if/switch, loops with conditionals)
- There are edge cases the function must handle (nulls, empty collections, negative numbers, encoding edge cases)
- A calculation or transformation needs to be correct
- A parsing/serialization operation could fail silently

Do not write a unit test for:
- A function with no logic (a getter, a setter, a pass-through)
- Framework-provided behavior (test your usage of the framework, not the framework itself)
- Private implementation details — test through the public API

## Pattern

```python
# Arrange: set up inputs, no external dependencies
# Act: call the unit under test
# Assert: verify the output or state change

def test_discount_applies_only_when_minimum_met():
    # Arrange
    cart = Cart(items=[Item(price=10), Item(price=15)])
    discount = PercentDiscount(rate=0.10, minimum_order=30)

    # Act
    total = discount.apply(cart.subtotal())

    # Assert
    assert total == 22.50  # 25 * 0.90

def test_discount_skipped_below_minimum():
    cart = Cart(items=[Item(price=10)])
    discount = PercentDiscount(rate=0.10, minimum_order=30)

    total = discount.apply(cart.subtotal())

    assert total == 10.00  # no discount applied
```

One test, one logical assertion, one reason to fail.

## Common Mistakes

- Using a real database "because it's easier to set up" → Makes the test slow, order-dependent, and fragile; use a fake or stub instead
- One test asserts many independent behaviors → When it fails, you don't know which behavior broke; split into separate tests
- Testing implementation details (internal variable names, method call order) → Tests break on every refactor even when behavior is correct; test observable outputs only
- Putting integration logic in a unit test and calling it "fast" → A test that makes one HTTP call for every assertion is not a unit test, regardless of what you name it
- Not testing edge cases → Happy-path-only unit tests give false confidence; add parameterized cases for boundaries and nulls
- Asserting on a printed message to tell which branch ran → The wording was never promised; give the code a return value or an error type to assert on instead

## See Also

- ← Previous: [Test Pyramid vs. Trophy](test-pyramid-vs-trophy.md) | Next: [Integration Testing Concepts](integration-testing-concepts.md) →
- Related: [What a Test May Couple To](what-a-test-may-couple-to.md) — what a test may assert on
- Related: [Test Doubles](test-doubles.md) — how to isolate dependencies
- Related: [Test Structure and Naming](test-structure-and-naming.md) — AAA structure
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — TDD unit testing section
- Reference: Martin Fowler, [UnitTest](https://martinfowler.com/bliki/UnitTest.html)
