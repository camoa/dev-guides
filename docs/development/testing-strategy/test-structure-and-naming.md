---
description: "Arrange-Act-Assert (AAA) structure, Given-When-Then, one logical assertion per test, and naming conventions that communicate intent."
tldr: "Structure every test as Arrange/Act/Assert with blank lines between phases — one Act per test. Name tests to describe what is tested, under what conditions, and what the expected outcome is. One logical assertion per test: multiple asserts are fine if they all verify facets of the same single outcome."
---

# Test Structure and Naming

## When to Use

> Every time you write a test. Good structure and naming are not aesthetics — they are the difference between a test that communicates its intent when it fails and a test that requires reverse-engineering.

## Arrange-Act-Assert (AAA)

The universal pattern for test structure. Divide every test into three explicit phases:

**Arrange** — set up the preconditions: create objects, configure stubs, prepare input data.
**Act** — execute the single behavior under test: call the method, make the HTTP request, fire the event.
**Assert** — verify the outcome: check return values, state changes, or side effects.

```javascript
test('calculates discounted total when VIP customer', () => {
  // ARRANGE
  const cart = new Cart([new Item('Widget', 50.00)]);
  const customer = new Customer({ tier: 'vip' });

  // ACT
  const total = cart.calculateTotal(customer);

  // ASSERT
  expect(total).toBe(45.00); // 10% VIP discount
});
```

Blank lines between phases are a visual signal — use them. One "Act" per test; if you catch yourself writing two actions with two sets of assertions, you have two tests.

## Given-When-Then (GWT)

BDD terminology for the same structure. Use GWT when writing tests from a behavior/specification perspective, especially in Gherkin-based tools or when tests serve as living documentation:

```
Given: a VIP customer with one item in their cart
When: checkout total is calculated
Then: the VIP discount of 10% is applied
```

GWT and AAA are semantically identical; choose based on team convention and tooling.

## One Logical Assertion per Test

"One assertion per test" is often misquoted. The correct principle is: **one logical assertion per test** — one behavior or outcome being verified. A test may use multiple `assert`/`expect` statements if they all verify facets of the same single outcome:

```python
# GOOD: Three assertions, one logical outcome (the user object is correct)
def test_registration_creates_valid_user():
    user = register('alice@example.com', 'S3cret!')
    assert user.email == 'alice@example.com'
    assert user.password_hash != 'S3cret!'   # not stored as plain text
    assert user.is_active is True            # account is active

# BAD: Two assertions, two unrelated outcomes — split these
def test_registration():
    user = register('alice@example.com', 'S3cret!')
    assert user.email == 'alice@example.com'     # outcome 1: user created
    email_spy.assert_called_once()               # outcome 2: email was sent
    # When this test fails, which behavior broke?
```

## Naming Conventions

A test name should tell you — without reading the code — **what** is tested, **under what conditions**, and **what the expected outcome is**:

| Style | Pattern | Example |
|---|---|---|
| Underscored | `method_condition_expected` | `calculateTotal_vipCustomer_appliesDiscount` |
| Should-style | `should_expected_when_condition` | `should_apply_discount_when_customer_is_vip` |
| Plain English | Prose sentence | `"applies 10% discount for VIP customers"` |

Choose one style and enforce it across the project. Inconsistency costs more than any single naming choice.

**Anti-name patterns:**
- `test1`, `testCalculator` — no information
- `test_order_processing` — too vague; which aspect of order processing?
- `test_it_works` — works how?

## Common Mistakes

- Multiple "Act" phases in one test → Split into separate tests; each test verifies exactly one behavior
- Assertions in the Arrange phase → You are testing your test setup; if setup fails, it should be an error, not an assertion failure
- No blank lines between AAA phases → Hard to read; the structure becomes invisible
- Long Arrange blocks that obscure what is being tested → Extract a factory or builder; `createVipCustomerWithItems()` is more readable than 15 lines of object construction
- Test names that mirror the method name (`test_calculateTotal`) → The name says nothing about expected behavior; document the scenario and outcome

## See Also

- ← Previous: [Test Doubles](test-doubles.md) | Next: [Determinism and Flakiness](determinism-and-flakiness.md) →
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — Testing Patterns section (GWT and AAA examples)
- Reference: Automation Panda, [Arrange-Act-Assert](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)
