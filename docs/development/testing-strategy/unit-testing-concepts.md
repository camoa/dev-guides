---
description: Unit testing — what belongs in a unit test, the FIRST properties, and how to avoid coupling tests to implementation.
tldr: Unit tests verify one function or class in isolation — no DB, no HTTP, no filesystem. Apply the FIRST properties (Fast, Isolated, Repeatable, Self-validating, Timely). Test observable behavior, not private implementation details; one logical assertion per test.
---

# Unit Testing Concepts

## When to Use

> Use unit tests when the code has meaningful logic that can be verified without external state. Do not write unit tests for pass-through functions, framework behavior, or private implementation details.

## Decision

| Write a unit test when... | Skip unit tests when... |
|---|---|
| There is branching logic (if/switch, loops with conditionals) | Function has no logic (getter, setter, pass-through) |
| There are edge cases to handle (nulls, empty, negative, encoding) | Framework provides the behavior — test your usage, not the framework |
| A calculation or transformation must be correct | Testing private implementation details |
| A parsing/serialization operation could fail silently | |

## Pattern

```python
# Arrange: set up inputs, no external dependencies
# Act: call the unit under test
# Assert: verify the output or state change

def test_discount_applies_only_when_minimum_met():
    cart = Cart(items=[Item(price=10), Item(price=15)])
    discount = PercentDiscount(rate=0.10, minimum_order=30)
    total = discount.apply(cart.subtotal())
    assert total == 22.50  # 25 * 0.90

def test_discount_skipped_below_minimum():
    cart = Cart(items=[Item(price=10)])
    discount = PercentDiscount(rate=0.10, minimum_order=30)
    total = discount.apply(cart.subtotal())
    assert total == 10.00  # no discount applied
```

**FIRST properties** — Good unit tests are Fast, Isolated, Repeatable, Self-validating, Timely. One test, one logical assertion, one reason to fail.

## Common Mistakes

- **Wrong**: Using a real database "because it's easier to set up" → **Right**: Use a fake or stub; keeps the test fast and order-independent
- **Wrong**: One test asserts many independent behaviors → **Right**: Split into separate tests; when it fails you know which behavior broke
- **Wrong**: Testing internal variable names or method call order → **Right**: Test observable outputs only; survives refactoring
- **Wrong**: One HTTP call per assertion in a "unit test" → **Right**: A test that makes HTTP calls is not a unit test regardless of name
- **Wrong**: Happy-path only → **Right**: Add parameterized cases for boundaries and nulls
- **Wrong**: Asserting on a printed message to tell which branch ran → **Right**: The wording was never promised; give the code a return value or an error type to assert on instead

Isolation says what a unit test must not touch. It does not say what the test may assert on — see [What a Test May Couple To](what-a-test-may-couple-to.md) for that half.

## See Also

- [Test Pyramid vs. Trophy](test-pyramid-vs-trophy.md) | Next: [Integration Testing Concepts](integration-testing-concepts.md)
- Related: [What a Test May Couple To](what-a-test-may-couple-to.md) — what a test may assert on
- Related: [Test Doubles](test-doubles.md) — how to isolate dependencies
- Related: [Test Structure and Naming](test-structure-and-naming.md) — AAA structure
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — TDD unit testing section
- Reference: Martin Fowler, [UnitTest](https://martinfowler.com/bliki/UnitTest.html)
