---
description: Arrange-Act-Assert (AAA) structure, Given-When-Then, one logical assertion per test, and naming conventions that communicate intent.
tldr: "Structure every test as Arrange/Act/Assert with blank lines between phases — one Act per test. Name tests to describe what is tested, under what conditions, and what the expected outcome is. One logical assertion per test: multiple asserts are fine if they all verify facets of the same single outcome."
---

# Test Structure and Naming

## When to Use

> Apply AAA structure and descriptive naming to every test you write. Good structure is the difference between a test that communicates its intent when it fails and one that requires reverse-engineering.

## Decision

| Naming style | Pattern | Example |
|---|---|---|
| Underscored | `method_condition_expected` | `calculateTotal_vipCustomer_appliesDiscount` |
| Should-style | `should_expected_when_condition` | `should_apply_discount_when_customer_is_vip` |
| Plain English | Prose sentence | `"applies 10% discount for VIP customers"` |

Choose one style and enforce it across the project. Anti-name patterns: `test1`, `testCalculator`, `test_order_processing`, `test_it_works` — provide no information about expected behavior.

## Pattern

```javascript
// AAA with blank lines between phases
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

**One logical assertion per test** — multiple `expect` statements are fine if they all verify facets of the same single outcome:

```python
# GOOD: Three asserts, one logical outcome (the user object is correct)
def test_registration_creates_valid_user():
    user = register('alice@example.com', 'S3cret!')
    assert user.email == 'alice@example.com'
    assert user.password_hash != 'S3cret!'
    assert user.is_active is True

# BAD: Two unrelated outcomes — split these
def test_registration():
    user = register('alice@example.com', 'S3cret!')
    assert user.email == 'alice@example.com'  # outcome 1
    email_spy.assert_called_once()            # outcome 2: when this fails, which broke?
```

## Common Mistakes

- **Wrong**: Multiple "Act" phases in one test → **Right**: Split into separate tests; each test verifies one behavior
- **Wrong**: Assertions in the Arrange phase → **Right**: Setup failures should be errors, not assertion failures
- **Wrong**: No blank lines between AAA phases → **Right**: Visual separation makes the structure readable
- **Wrong**: Long Arrange blocks obscuring what is tested → **Right**: Extract factory/builder methods; `createVipCustomerWithItems()` reads better than 15 lines
- **Wrong**: Test name mirrors the method name (`test_calculateTotal`) → **Right**: Document the scenario and expected outcome

## See Also

- [Test Doubles](test-doubles.md) | Next: [Determinism and Flakiness](determinism-and-flakiness.md)
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — Testing Patterns section (GWT and AAA examples)
- Reference: Automation Panda, [Arrange-Act-Assert](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)
