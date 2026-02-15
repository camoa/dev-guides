---
description: Arrange-Act-Assert, Given-When-Then, naming conventions, parameterized tests, and setup/teardown
---

# Testing Patterns

## When to Use
Structuring any test - unit, integration, or end-to-end. These patterns create readable, maintainable tests.

## Arrange-Act-Assert (AAA) Pattern

The most popular test structure pattern. Each test has three clear phases:

```javascript
describe('ShoppingCart', () => {
  test('applies percentage discount to total', () => {
    // ARRANGE: Set up test data and dependencies
    const cart = new ShoppingCart();
    cart.addItem({ name: 'Book', price: 20.00 });
    cart.addItem({ name: 'Pen', price: 5.00 });
    const discount = new PercentageDiscount(10); // 10% off

    // ACT: Execute the behavior being tested
    const total = cart.calculateTotal(discount);

    // ASSERT: Verify the outcome
    expect(total).toBe(22.50); // (20 + 5) * 0.90
  });
});
```

**Arrange**: Set up test preconditions
- Create objects
- Set up mocks/stubs
- Prepare test data
- Configure system state

**Act**: Execute the behavior under test
- Usually a single method call
- If you need multiple actions, that's a code smell - might need multiple tests

**Assert**: Verify the outcome
- Check return values
- Verify state changes
- Confirm side effects
- Generally one logical assertion per test (but multiple assertion statements for same concept is fine)

## Given-When-Then (BDD Style)

Identical to Arrange-Act-Assert but uses BDD terminology. Common in Gherkin/Cucumber and RSpec.

```ruby
# RSpec example
describe ShoppingCart do
  it 'applies percentage discount to total' do
    # GIVEN: Set up context
    cart = ShoppingCart.new
    cart.add_item(name: 'Book', price: 20.00)
    cart.add_item(name: 'Pen', price: 5.00)
    discount = PercentageDiscount.new(10)

    # WHEN: Perform action
    total = cart.calculate_total(discount)

    # THEN: Verify outcome
    expect(total).to eq(22.50)
  end
end
```

```gherkin
# Gherkin/Cucumber example
Scenario: Apply percentage discount to cart total
  Given a shopping cart with the following items:
    | item | price |
    | Book | 20.00 |
    | Pen  |  5.00 |
  And a percentage discount of 10%
  When I calculate the total
  Then the total should be 22.50
```

## Test Naming Conventions

**Pattern 1: methodName_stateUnderTest_expectedBehavior**
```java
void calculateTotal_withEmptyCart_returnsZero() { }
void calculateTotal_withPercentageDiscount_appliesDiscountToTotal() { }
void calculateTotal_withExpiredCoupon_throwsInvalidCouponException() { }
```

**Pattern 2: should_expectedBehavior_when_stateUnderTest**
```python
def test_should_return_zero_when_cart_is_empty():
def test_should_apply_discount_when_valid_coupon_provided():
def test_should_throw_exception_when_coupon_expired():
```

**Pattern 3: Plain English (BDD style)**
```javascript
it('returns zero for empty cart')
it('applies discount to cart total')
it('throws error when coupon is expired')
```

Choose one style and be consistent across your project. The name should clearly describe:
1. What you're testing
2. Under what conditions
3. What the expected outcome is

## Table-Driven Tests (Parameterized Tests)

Test multiple scenarios with same logic:

```python
# Python with pytest
@pytest.mark.parametrize("input,expected", [
    (0, 0),
    (1, 1),
    (2, 4),
    (3, 9),
    (10, 100),
    (-5, 25),
])
def test_square_function(input, expected):
    assert square(input) == expected
```

```go
// Go table-driven tests
func TestSquare(t *testing.T) {
    tests := []struct {
        name     string
        input    int
        expected int
    }{
        {"zero", 0, 0},
        {"positive", 3, 9},
        {"negative", -5, 25},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := square(tt.input)
            if result != tt.expected {
                t.Errorf("got %d, want %d", result, tt.expected)
            }
        })
    }
}
```

## Setup and Teardown Patterns

Most test frameworks provide hooks for shared setup/cleanup:

```python
# pytest fixtures
@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db  # Test runs here
    db.disconnect()  # Cleanup after test

def test_user_creation(database):
    user = User.create(database, name='Alice')
    assert user.id is not None
```

```javascript
// Jest beforeEach/afterEach
describe('UserRepository', () => {
  let db;

  beforeEach(() => {
    db = new InMemoryDatabase();
  });

  afterEach(() => {
    db.clear();
  });

  test('saves user to database', () => {
    const repo = new UserRepository(db);
    repo.save({ name: 'Alice' });
    expect(db.count()).toBe(1);
  });
});
```

**Warning**: Shared setup can hide dependencies and make tests less isolated. Prefer explicit setup in each test when possible.

## Common Mistakes

- Multiple "Act" sections - Usually means you're testing multiple behaviors; split into separate tests
- Assertions in Arrange section - You're testing your test setup, not the code under test
- No clear visual separation of phases - Add blank lines between Arrange/Act/Assert for readability
- Reusing test data across tests - Causes coupling; each test should set up own data
- Assertions that test multiple unrelated concepts - Split into multiple tests for clarity when test fails
- Setup/teardown that hides what test actually needs - Makes tests harder to understand; explicit setup often better

## See Also
- Previous: [Test Doubles](test-doubles.md) | Next: [Spec-Driven Development Overview](spec-driven-overview.md)
- Related: [Unit Testing Fundamentals](unit-testing-fundamentals.md) (FIRST principles)
- Reference: [Arrange-Act-Assert Pattern](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)
- Reference: [Given-When-Then vs Arrange-Act-Assert](https://edgibbs.com/2024/12/21/given-when-then-versus-arrange-act-assert/)
