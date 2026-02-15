---
description: Eliminating repeated setup, data creation, and assertion patterns in test suites without sacrificing clarity
---

# DRY in Testing

## When to Use

When writing test suites and encountering repeated setup, teardown, or assertion patterns across tests.

## Decision Framework

| If you have... | Use | Why |
|----------------|-----|-----|
| **Repeated setup/teardown** | Fixtures, setUp/tearDown | Eliminate duplication, ensure consistency |
| **Repeated test data creation** | Factories, Builders | Generate realistic test data programmatically |
| **Repeated assertions** | Custom matchers, assertion helpers | Make tests more readable, DRY |
| **Similar test structure** | Parameterized tests | Test multiple inputs with same logic |
| **Shared mocks/stubs** | Mock factories, fixture modules | Reuse test doubles consistently |
| **Repeated integration setup** | Test harness, test containers | Standardize environment setup |

## Pattern: Test Fixtures

```python
# BEFORE: Duplicated setup in every test
class TestUserService(unittest.TestCase):
    def test_create_user(self):
        db = Database('sqlite:///:memory:')
        db.migrate()
        service = UserService(db)
        # Test logic...
        db.close()

    def test_update_user(self):
        db = Database('sqlite:///:memory:')
        db.migrate()
        service = UserService(db)
        # Test logic...
        db.close()

    def test_delete_user(self):
        db = Database('sqlite:///:memory:')
        db.migrate()
        service = UserService(db)
        # Test logic...
        db.close()

# AFTER: DRY with fixtures
class TestUserService(unittest.TestCase):
    def setUp(self):
        """Runs before each test."""
        self.db = Database('sqlite:///:memory:')
        self.db.migrate()
        self.service = UserService(self.db)

    def tearDown(self):
        """Runs after each test."""
        self.db.close()

    def test_create_user(self):
        # Just test logic — setup is DRY
        user = self.service.create_user('test@example.com', 'password')
        self.assertEqual(user.email, 'test@example.com')

    def test_update_user(self):
        user = self.service.create_user('test@example.com', 'password')
        updated = self.service.update_user(user.id, email='new@example.com')
        self.assertEqual(updated.email, 'new@example.com')
```

## Pattern: Factories for Test Data

```typescript
// ANTI-PATTERN: Repeated object creation
test('creates order with items', () => {
  const user = {
    id: 1,
    email: 'test@example.com',
    name: 'Test User',
    createdAt: new Date(),
  };
  const order = { id: 1, userId: user.id, total: 100, status: 'pending' };
  // Test...
});

test('processes order payment', () => {
  const user = {
    id: 1,
    email: 'test@example.com',
    name: 'Test User',
    createdAt: new Date(),
  };
  const order = { id: 1, userId: user.id, total: 100, status: 'pending' };
  // Test...
});

// DRY: Factory pattern
class UserFactory {
  static create(overrides = {}) {
    return {
      id: Math.floor(Math.random() * 1000),
      email: 'test@example.com',
      name: 'Test User',
      createdAt: new Date(),
      ...overrides,
    };
  }
}

class OrderFactory {
  static create(overrides = {}) {
    return {
      id: Math.floor(Math.random() * 1000),
      userId: 1,
      total: 100,
      status: 'pending',
      ...overrides,
    };
  }
}

test('creates order with items', () => {
  const user = UserFactory.create();
  const order = OrderFactory.create({ userId: user.id });
  // Test is now focused on behavior, not data setup
});

test('processes high-value order', () => {
  const user = UserFactory.create({ email: 'vip@example.com' });
  const order = OrderFactory.create({ userId: user.id, total: 10000 });
  // Easy to create variations
});
```

## Pattern: Parameterized Tests

```python
# ANTI-PATTERN: Repeated test structure
def test_discount_for_regular_customer():
    price = calculate_discount(100, 'regular')
    assert price == 100

def test_discount_for_vip_customer():
    price = calculate_discount(100, 'vip')
    assert price == 80

def test_discount_for_gold_customer():
    price = calculate_discount(100, 'gold')
    assert price == 90

# DRY: Parameterized test
import pytest

@pytest.mark.parametrize('customer_type,expected_price', [
    ('regular', 100),
    ('vip', 80),
    ('gold', 90),
])
def test_discount_calculation(customer_type, expected_price):
    price = calculate_discount(100, customer_type)
    assert price == expected_price
```

## Pattern: Custom Assertions

```javascript
// ANTI-PATTERN: Repeated assertion logic
test('validates email format', () => {
  const result = validateEmail('test@example.com');
  expect(result.valid).toBe(true);
  expect(result.errors).toEqual([]);
  expect(result.warnings).toEqual([]);
});

test('validates phone format', () => {
  const result = validatePhone('555-1234');
  expect(result.valid).toBe(true);
  expect(result.errors).toEqual([]);
  expect(result.warnings).toEqual([]);
});

// DRY: Custom matcher
expect.extend({
  toBeValidValidationResult(received) {
    const pass = received.valid === true
      && received.errors.length === 0
      && received.warnings.length === 0;

    return {
      pass,
      message: () => `Expected validation result to be valid, got ${JSON.stringify(received)}`,
    };
  },
});

test('validates email format', () => {
  expect(validateEmail('test@example.com')).toBeValidValidationResult();
});

test('validates phone format', () => {
  expect(validatePhone('555-1234')).toBeValidValidationResult();
});
```

## When NOT to DRY Tests

**Keep duplication when:**

- Tests become harder to understand with abstraction
- Each test covers fundamentally different scenarios
- Abstraction hides important test details
- Test readability > test code DRY

**Dan North's principle**: "Duplication is far cheaper than the wrong abstraction" applies even more to tests -- test clarity is paramount.

## Common Mistakes

- **Over-abstracting tests** — Tests become unreadable, hard to debug when they fail
- **Shared state between tests** — Tests become order-dependent, fail non-deterministically
- **Magic fixtures** — Test setup so abstracted that readers can't understand test context
- **DRY assertions over clarity** — Custom matchers that hide what's being tested
- **Not resetting state** — Fixtures leak state across tests

## See Also

- [Abstraction Strategies](abstraction-strategies.md)
- [Pytest Fixtures Documentation](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [Test Automation Frameworks (2026)](https://testrigor.com/blog/test-automation-frameworks/)
