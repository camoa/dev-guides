---
description: Common SOLID anti-patterns — God Object, Modification Cascade, Refused Bequest, Interface Bloat, Service Locator, and more.
---

# SOLID Anti-Patterns

## When to Recognize Violations

During code review, watch for these anti-patterns that violate SOLID principles and cause maintenance pain.

## Anti-Pattern: God Object (SRP Violation)

**Description**: One class doing everything.

**Example** (PHP):
```php
class Application {
    public function authenticateUser($username, $password) { /* ... */ }
    public function renderPage($template, $data) { /* ... */ }
    public function saveToDatabase($entity) { /* ... */ }
    public function sendEmail($to, $message) { /* ... */ }
    public function processPayment($amount) { /* ... */ }
    public function generatePDF($data) { /* ... */ }
}
```

**Why it's bad**:
- Changes for auth, rendering, database, email, payments, PDF generation
- Impossible to test in isolation (mocking nightmare)
- Team members conflict on same file
- Unclear ownership

**Fix**: Split by responsibility (AuthService, ViewRenderer, DatabaseRepository, etc.)

## Anti-Pattern: Modification Cascade (OCP Violation)

**Description**: Adding a feature requires modifying many existing classes.

**Example** (TypeScript):
```typescript
class ShapeDrawer {
  draw(shape: any) {
    if (shape.type === 'circle') {
      // draw circle
    } else if (shape.type === 'square') {
      // draw square
    } else if (shape.type === 'triangle') {
      // draw triangle
    }
    // Adding hexagon requires modifying this method
  }
}

class ShapeAreaCalculator {
  calculate(shape: any) {
    if (shape.type === 'circle') {
      return Math.PI * shape.radius ** 2;
    } else if (shape.type === 'square') {
      return shape.side ** 2;
    }
    // Adding hexagon requires modifying this too
  }
}
```

**Why it's bad**:
- Adding one shape type requires changing multiple files
- Risk of missing a spot (incomplete implementation)
- Can't add shapes without source code access (closed source libraries)

**Fix**: Polymorphism -- each shape implements `draw()` and `area()`.

## Anti-Pattern: Refused Bequest (LSP Violation)

**Description**: Subclass doesn't honor parent's contract.

**Example** (Python):
```python
class Vehicle:
    def start_engine(self):
        return "Engine started"

    def drive(self):
        return "Driving"

class Bicycle(Vehicle):
    def start_engine(self):
        raise NotImplementedError("Bicycles don't have engines") # LSP VIOLATION

    def drive(self):
        return "Pedaling"
```

**Why it's bad**:
- Code expecting `Vehicle` breaks with `Bicycle`
- `NotImplementedError` at runtime (should be compile-time error)
- Violates "is-a" relationship (bicycle isn't a vehicle with an engine)

**Fix**: Separate hierarchies (`EngineVehicle` vs `HumanPoweredVehicle`).

## Anti-Pattern: Interface Bloat (ISP Violation)

**Description**: Forcing implementers to implement methods they don't use.

**Example** (Java):
```java
interface Employee {
    void work();
    void attendMeeting();
    void submitTimesheet();
    void approveExpenses(); // Only managers do this
    void conductInterview(); // Only HR does this
}

class Developer implements Employee {
    public void work() { /* code */ }
    public void attendMeeting() { /* attend */ }
    public void submitTimesheet() { /* submit */ }
    public void approveExpenses() { throw new UnsupportedOperationException(); } // ISP VIOLATION
    public void conductInterview() { throw new UnsupportedOperationException(); } // ISP VIOLATION
}
```

**Why it's bad**:
- Developers forced to implement manager/HR methods
- Runtime exceptions instead of compile-time safety
- Changes to manager methods affect all employees

**Fix**: Role interfaces (`IWorker`, `IManager`, `IInterviewer`).

## Anti-Pattern: Service Locator (DIP Violation)

**Description**: Using a global registry to fetch dependencies.

**Example** (C#):
```csharp
class OrderService {
    public void ProcessOrder(Order order) {
        var repository = ServiceLocator.Get<IOrderRepository>(); // DIP VIOLATION
        var emailService = ServiceLocator.Get<IEmailService>(); // DIP VIOLATION

        repository.Save(order);
        emailService.Send(order.Customer.Email, "Order confirmed");
    }
}
```

**Why it's bad**:
- Dependencies are hidden (not in constructor)
- Hard to test (must configure global ServiceLocator)
- Runtime errors if service not registered
- Couples to ServiceLocator framework

**Fix**: Constructor injection.

## Anti-Pattern: Concrete Dependencies in High-Level Code (DIP Violation)

**Example** (PHP):
```php
class CheckoutService {
    public function checkout(Cart $cart) {
        $payment = new StripePaymentGateway(); // DIP VIOLATION
        $payment->charge($cart->total());
    }
}
```

**Why it's bad**:
- Can't switch to PayPal without changing `CheckoutService`
- Can't test without real Stripe API calls
- High-level business logic depends on low-level implementation detail

**Fix**: Depend on `IPaymentGateway` interface, inject implementation.

## Anti-Pattern: Anemic Domain Model (SRP Misapplication)

**Description**: Separating data from behavior excessively.

**Example** (TypeScript):
```typescript
// Anemic model
class Order {
  items: OrderItem[];
  total: number;
  status: string;
  // No behavior
}

// Behavior in separate "service"
class OrderService {
  calculateTotal(order: Order): number {
    return order.items.reduce((sum, item) => sum + item.price, 0);
  }

  validateOrder(order: Order): boolean {
    return order.items.length > 0;
  }
}
```

**Why it's bad**:
- `Order` doesn't own its behavior (violates encapsulation)
- Business logic scattered across services
- `OrderService` knows too much about `Order` internals

**Fix**: Rich domain model -- put behavior on `Order` class.

## Anti-Pattern: Leaky Abstraction (DIP Violation)

**Example** (Python):
```python
# Abstraction exposes implementation details
class ISQLDatabase(ABC):
    @abstractmethod
    def execute_query(self, sql: str): pass # Leaky: assumes SQL

# Forces non-SQL databases to fake SQL
class MongoDBAdapter(ISQLDatabase):
    def execute_query(self, sql: str):
        # Must translate SQL to MongoDB queries (awkward)
        pass
```

**Why it's bad**:
- Abstraction assumes SQL (not abstract enough)
- Non-SQL implementations are forced into SQL model
- Defeats the purpose of abstraction

**Fix**: Generic abstraction (`IDataStore` with `save()`, `find()`, `delete()`).
