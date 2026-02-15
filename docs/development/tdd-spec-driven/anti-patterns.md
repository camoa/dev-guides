---
description: Classic and modern TDD anti-patterns including The Liar, Excessive Setup, The Giant, and over-mocking
---

# TDD Anti-Patterns

## When to Use
You're practicing TDD or reviewing tests and want to identify common mistakes that reduce test value or create maintenance burden.

## Classic Anti-Patterns (James Carr's List)

**The Liar**
Test passes but doesn't actually test what it claims to test.

```python
# BAD: Test claims to verify password hashing but doesn't
def test_password_is_hashed():
    user = User(password='secret123')
    user.save()
    # Liar: Doesn't actually verify password was hashed
    assert user.password is not None  # Passes even if password stored in plain text!

# GOOD: Actually verifies hashing
def test_password_is_hashed():
    user = User(password='secret123')
    user.save()
    saved_user = db.get_user(user.id)
    assert saved_user.password != 'secret123'  # Verify it's not plain text
    assert bcrypt.verify('secret123', saved_user.password)  # Verify it's properly hashed
```

**Excessive Setup**
Test requires extensive setup that obscures what's actually being tested.

```javascript
// BAD: Setup overwhelms the actual test
test('user can checkout cart', () => {
  const db = new Database();
  db.connect();
  db.migrate();
  const userRepo = new UserRepository(db);
  const productRepo = new ProductRepository(db);
  const orderRepo = new OrderRepository(db);
  const paymentService = new PaymentService(config);
  const emailService = new EmailService(config);
  const inventoryService = new InventoryService(db);
  const checkoutService = new CheckoutService(
    userRepo, productRepo, orderRepo, paymentService, emailService, inventoryService
  );
  const user = userRepo.create({ name: 'Alice' });
  const product1 = productRepo.create({ name: 'Book', price: 20 });
  const product2 = productRepo.create({ name: 'Pen', price: 5 });
  const cart = new Cart(user);
  cart.add(product1, 1);
  cart.add(product2, 2);

  // Finally, the actual test
  const order = checkoutService.checkout(cart);
  expect(order.total).toBe(30);
});

// GOOD: Use factories and fixtures
test('user can checkout cart', () => {
  const user = createUser();
  const cart = createCart(user, [
    { product: 'Book', price: 20, quantity: 1 },
    { product: 'Pen', price: 5, quantity: 2 }
  ]);

  const order = checkoutService.checkout(cart);
  expect(order.total).toBe(30);
});
```

**The Giant**
Test tries to test everything at once.

```python
# BAD: Testing multiple behaviors in one test
def test_user_registration():
    # Tests validation, hashing, saving, email sending, logging, metrics...
    with pytest.raises(ValueError):
        register_user('', 'password')

    with pytest.raises(ValueError):
        register_user('alice@example.com', '')

    user = register_user('alice@example.com', 'secret123')
    assert user.id is not None
    assert user.password != 'secret123'
    assert bcrypt.verify('secret123', user.password)
    assert email_service.send_welcome.called
    assert log_service.log.called_with('User registered: alice@example.com')
    assert metrics.increment.called_with('user.registration.success')

# GOOD: Separate tests for each behavior
def test_registration_rejects_empty_email():
    with pytest.raises(ValueError, match='email'):
        register_user('', 'password')

def test_registration_rejects_empty_password():
    with pytest.raises(ValueError, match='password'):
        register_user('alice@example.com', '')

def test_registration_hashes_password():
    user = register_user('alice@example.com', 'secret123')
    assert user.password != 'secret123'
    assert bcrypt.verify('secret123', user.password)

def test_registration_sends_welcome_email():
    register_user('alice@example.com', 'secret123')
    email_service.send_welcome.assert_called_once_with('alice@example.com')
```

**Slow Poke**
Test runs slowly because it uses real external dependencies.

```php
// BAD: Tests hit real database and external API
public function testUserCanPurchaseProduct() {
    $db = new MySQLDatabase('production_host');  // Real database
    $paymentGateway = new StripeAPI('live_key');  // Real Stripe API

    $user = User::create($db, ['balance' => 100]);
    $product = Product::create($db, ['price' => 50]);

    $result = $paymentGateway->charge($user, $product->price);  // Real API call
    $user->addProduct($product);

    $this->assertTrue($result->success);
}

// GOOD: Use fakes/mocks for external dependencies
public function testUserCanPurchaseProduct() {
    $db = new InMemoryDatabase();  // Fast in-memory fake
    $paymentGateway = $this->createMock(PaymentGateway::class);
    $paymentGateway->method('charge')->willReturn(new Success());

    $user = User::create($db, ['balance' => 100]);
    $product = Product::create($db, ['price' => 50]);

    $result = $paymentGateway->charge($user, $product->price);
    $user->addProduct($product);

    $this->assertTrue($result->success);
}
```

## Modern Anti-Patterns (2024-2025)

**The Mockery**
Over-mocking that tests mocks instead of real code.

```typescript
// BAD: Mocking everything, including your own code
test('processes order', () => {
  const validator = mock<OrderValidator>();
  const calculator = mock<PriceCalculator>();
  const repository = mock<OrderRepository>();
  const emailer = mock<EmailService>();

  validator.validate.mockReturnValue(true);
  calculator.calculate.mockReturnValue(100);
  repository.save.mockReturnValue({ id: 1 });

  const processor = new OrderProcessor(validator, calculator, repository, emailer);
  processor.process(order);

  expect(validator.validate).toHaveBeenCalled();
  expect(calculator.calculate).toHaveBeenCalled();
  expect(repository.save).toHaveBeenCalled();
  // We're testing that mocks were called, not that code works!
});

// GOOD: Mock only external boundaries
test('processes order', () => {
  const db = new InMemoryDatabase();  // Real for our code
  const emailer = mock<EmailService>();  // Mock external service

  const processor = new OrderProcessor(db, emailer);
  const order = processor.process({ items: [...], customer: {...} });

  expect(order.total).toBe(100);  // Test actual behavior
  expect(db.getOrder(order.id)).toBeDefined();  // Verify it saved
  expect(emailer.send).toHaveBeenCalledWith(customer.email);  // Verify side effect
});
```

**Test Obsession**
Testing trivial code or testing just to hit coverage percentage.

```python
# BAD: Testing trivial getters/setters
class User:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

# Don't waste time on this:
def test_get_name():
    user = User('Alice')
    assert user.get_name() == 'Alice'

def test_set_name():
    user = User('Alice')
    user.set_name('Bob')
    assert user.name == 'Bob'

# GOOD: Test actual behavior
def test_user_full_name_combines_first_and_last():
    user = User(first_name='Alice', last_name='Smith')
    assert user.full_name() == 'Alice Smith'
```

**Skipping Refactor**
Following red-green but never refactoring, accumulating technical debt.

```go
// BAD: Code that passed tests but was never refactored
func ProcessOrder(o *Order) error {
    if o.Items == nil || len(o.Items) == 0 {
        return errors.New("no items")
    }
    t := 0.0
    for _, i := range o.Items {
        t += i.Price * float64(i.Qty)
    }
    if o.Customer.State == "CA" {
        t = t * 1.08
    } else {
        t = t * 1.06
    }
    if o.Customer.VIP {
        t = t * 0.9
    }
    o.Total = t
    return nil
}

// GOOD: Refactored for clarity (tests stay green)
func ProcessOrder(order *Order) error {
    if err := validateOrder(order); err != nil {
        return err
    }

    subtotal := calculateSubtotal(order.Items)
    taxRate := getTaxRate(order.Customer.State)
    totalWithTax := subtotal * (1 + taxRate)

    if order.Customer.VIP {
        totalWithTax *= VIP_DISCOUNT_RATE
    }

    order.Total = totalWithTax
    return nil
}
```

## Common Mistakes

- Tests depend on execution order - Each test must be independent; use setup/teardown
- Testing private methods directly - Test through public interface; private methods are implementation details
- Hard-coded dates/times/random values - Use dependency injection or test doubles for non-deterministic inputs
- Assertions with no failure message - When test fails, message should explain what broke
- Copy-paste test code - Leads to duplication and maintenance burden; use test helpers/factories
- Not deleting obsolete tests - Old tests for removed features waste time and confuse developers

## See Also
- Previous: [Refactoring with Confidence](refactoring-confidence.md) | Next: [Security Best Practices](security-best-practices.md)
- Related: [Unit Testing Fundamentals](unit-testing-fundamentals.md) (what makes good tests)
- Related: [Test Doubles](test-doubles.md) (when to mock)
- Reference: [TDD Anti-Patterns by James Carr](https://marabesi.com/tdd/tdd-anti-patterns.html)
- Reference: [Software Testing Anti-patterns](https://blog.codepipes.com/testing/software-testing-antipatterns.html)
