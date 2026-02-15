---
description: Dependency Inversion Principle — depending on abstractions instead of concrete classes, with dependency injection patterns.
---

# Dependency Inversion Principle (DIP)

## When to Use

When designing layered architectures, building testable systems, or decoupling high-level business logic from low-level implementation details.

## Decision: What DIP Means

**Robert Martin's Definition**:
1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details should depend on abstractions.

**In practice**: Depend on interfaces/contracts, not concrete implementations. Inject dependencies rather than creating them.

| If you... | Problem | Solution |
|---|---|---|
| `new DatabaseConnection()` inside business logic | Tight coupling to DB | Inject `IDataStore` interface |
| Import concrete classes from lower layers | Architectural violation | Depend on abstractions |
| Can't test without real database | Untestable | Mock interface, not implementation |
| Change in low-level detail breaks high-level code | Fragile architecture | Invert dependency direction |

## Pattern: DIP Violation

**PHP Example**:
```php
// Violation: high-level depends on low-level concrete class
class OrderProcessor {
    private MySQLDatabase $database;

    public function __construct() {
        $this->database = new MySQLDatabase(); // VIOLATION: direct instantiation
    }

    public function processOrder(Order $order) {
        $this->database->save($order); // Coupled to MySQL
    }
}
// Can't switch to PostgreSQL without changing OrderProcessor
// Can't test OrderProcessor without real MySQL
```

**DIP-Compliant**:
```php
// Abstraction: both layers depend on this
interface DataStore {
    public function save(Order $order): void;
}

// High-level module depends on abstraction
class OrderProcessor {
    private DataStore $database;

    public function __construct(DataStore $database) {
        $this->database = $database; // Dependency injection
    }

    public function processOrder(Order $order) {
        $this->database->save($order);
    }
}

// Low-level module implements abstraction
class MySQLDatabase implements DataStore {
    public function save(Order $order): void {
        // MySQL-specific implementation
    }
}

// Easy to switch or test
$orderProcessor = new OrderProcessor(new MySQLDatabase());
// Or: new OrderProcessor(new PostgreSQLDatabase());
// Or (test): new OrderProcessor(new MockDataStore());
```

## Pattern: Dependency Injection

**TypeScript Example**:
```typescript
// Without DI (violation)
class UserService {
  private emailSender = new SMTPEmailSender(); // Tight coupling

  register(user: User) {
    this.emailSender.send(user.email, "Welcome!");
  }
}

// With DI (DIP-compliant)
interface EmailSender {
  send(to: string, message: string): void;
}

class UserService {
  constructor(private emailSender: EmailSender) {}

  register(user: User) {
    this.emailSender.send(user.email, "Welcome!");
  }
}

class SMTPEmailSender implements EmailSender {
  send(to: string, message: string): void { /* SMTP logic */ }
}

// Usage
const userService = new UserService(new SMTPEmailSender());
// Or: new UserService(new SendGridEmailSender());
// Or (test): new UserService(new MockEmailSender());
```

## DIP vs Dependency Injection

**DIP** (principle): Depend on abstractions, not concretions.
**DI** (pattern): Inject dependencies from outside rather than creating them inside.

**DI enables DIP**: Injection allows swapping implementations that satisfy the abstraction.

## Common Mistakes

- **Creating interfaces for every class** -- Wait until you need swappability. Why: YAGNI, premature abstraction
- **Anemic interfaces** -- Interface that mirrors one concrete class exactly. Why: no actual abstraction
- **Depending on frameworks** -- Business logic importing framework classes directly. Why: framework changes break business logic
- **Service Locator anti-pattern** -- Static `ServiceLocator.get(IDatabase)` hides dependencies. Why: makes dependencies invisible, hurts testability
- **New keyword in business logic** -- `new EmailSender()` inside service. Why: couples to concrete implementation
- **Not inverting at architectural boundaries** -- DIP matters most at layer boundaries (business <-> persistence, core <-> infrastructure). Why: that's where coupling causes most pain
