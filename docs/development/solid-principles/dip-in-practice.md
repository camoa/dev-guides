---
description: Practical DIP patterns — IoC containers, constructor/setter/interface injection, Ports and Adapters architecture, and testing with DIP.
---

# DIP in Practice

## When to Apply DIP

Apply DIP at:
- **Architectural boundaries**: Business logic <-> Database, Core <-> External APIs
- **Framework boundaries**: Application <-> Framework (Symfony, Laravel, Express)
- **Testability boundaries**: Any code you want to test in isolation

**Don't apply DIP**:
- Within a single module/layer (internal implementation details)
- For stable, unlikely-to-change dependencies (e.g., standard library)
- When the abstraction cost outweighs the benefit

## Pattern: IoC Containers

**Python with dependency-injector**:
```python
from dependency_injector import containers, providers

# Define abstractions
class IEmailService(ABC):
    @abstractmethod
    def send(self, to: str, message: str): pass

class IDatabase(ABC):
    @abstractmethod
    def save(self, entity): pass

# Implementations
class SMTPEmailService(IEmailService):
    def send(self, to: str, message: str):
        # SMTP logic
        pass

class PostgreSQLDatabase(IDatabase):
    def save(self, entity):
        # PostgreSQL logic
        pass

# Container: configures dependencies
class Container(containers.DeclarativeContainer):
    email_service = providers.Singleton(SMTPEmailService)
    database = providers.Singleton(PostgreSQLDatabase)
    user_service = providers.Factory(
        UserService,
        email_service=email_service,
        database=database
    )

# Business logic depends on abstractions
class UserService:
    def __init__(self, email_service: IEmailService, database: IDatabase):
        self.email_service = email_service
        self.database = database

    def register(self, user):
        self.database.save(user)
        self.email_service.send(user.email, "Welcome!")

# Usage
container = Container()
user_service = container.user_service()
```

**PHP with Symfony/Laravel**:
```php
// services.yaml (Symfony)
services:
  App\Service\IEmailService:
    class: App\Service\SMTPEmailService

  App\Repository\IUserRepository:
    class: App\Repository\DoctrineUserRepository

  App\Service\UserService:
    arguments:
      $emailService: '@App\Service\IEmailService'
      $userRepository: '@App\Repository\IUserRepository'
```

## Pattern: Constructor Injection

**Three injection types**:

1. **Constructor Injection** (preferred):
```typescript
class OrderService {
  constructor(
    private readonly repository: IOrderRepository,
    private readonly emailService: IEmailService
  ) {}
}
// Dependencies required, immutable, explicit
```

2. **Setter Injection** (optional dependencies):
```typescript
class OrderService {
  private logger?: ILogger;

  setLogger(logger: ILogger) {
    this.logger = logger;
  }
}
// Dependency is optional
```

3. **Interface Injection** (rarely used):
```typescript
interface IInjectLogger {
  injectLogger(logger: ILogger): void;
}

class OrderService implements IInjectLogger {
  injectLogger(logger: ILogger) { /* ... */ }
}
// Framework calls injection method
```

**Best practice**: Use constructor injection for required dependencies.

## Decision: Abstraction Strategies

| Strategy | When to Use | Example |
|---|---|---|
| Interface | Multiple implementations expected | IPaymentGateway (Stripe, PayPal, Square) |
| Abstract class | Shared behavior + contract | AbstractRepository (base query methods) |
| Functional interface | Single method contract | Callable, Predicate, Comparator |
| Protocol (Python) | Structural subtyping | Any object with `.send()` method |

## Pattern: Ports and Adapters (Hexagonal Architecture)

**TypeScript Example**:
```typescript
// Core domain (no external dependencies)
interface INotificationPort {
  notify(user: User, message: string): void;
}

interface IUserRepositoryPort {
  save(user: User): void;
  findById(id: string): User;
}

class UserRegistrationUseCase {
  constructor(
    private userRepo: IUserRepositoryPort,
    private notifier: INotificationPort
  ) {}

  execute(userData: UserData) {
    const user = new User(userData);
    this.userRepo.save(user);
    this.notifier.notify(user, "Welcome!");
  }
}

// Adapters (infrastructure layer)
class EmailNotificationAdapter implements INotificationPort {
  notify(user: User, message: string) {
    // Email implementation
  }
}

class PostgreSQLUserAdapter implements IUserRepositoryPort {
  save(user: User) { /* PostgreSQL */ }
  findById(id: string): User { /* PostgreSQL */ }
}

// Wiring
const useCase = new UserRegistrationUseCase(
  new PostgreSQLUserAdapter(),
  new EmailNotificationAdapter()
);
```

## Common Mistakes

- **Service Locator pattern** -- `ServiceLocator.get('IDatabase')` hides dependencies. Why: breaks constructor signature, makes testing harder
- **Static dependencies** -- `Logger::log()` instead of injecting `ILogger`. Why: global state, untestable
- **Framework coupling in domain** -- Importing framework classes in business logic. Why: framework upgrade breaks core logic
- **Over-abstracting** -- Interface for every class. Why: YAGNI, premature abstraction
- **Circular dependencies** -- A depends on B, B depends on A. Why: indicates wrong abstraction boundaries
- **Leaky abstractions** -- Interface exposing implementation details (e.g., `ISQLDatabase` with `executeQuery()`). Why: defeats the abstraction

## Testing with DIP

**PHP Example**:
```php
// Production
class OrderService {
    public function __construct(private IPaymentGateway $gateway) {}

    public function checkout(Order $order) {
        return $this->gateway->charge($order->total);
    }
}

// Test
class TestOrderService extends TestCase {
    public function testCheckout() {
        $mockGateway = $this->createMock(IPaymentGateway::class);
        $mockGateway->expects($this->once())
                    ->method('charge')
                    ->with(100.00)
                    ->willReturn(true);

        $service = new OrderService($mockGateway);
        $order = new Order(100.00);

        $this->assertTrue($service->checkout($order));
    }
}
```

## Performance Considerations

**DIP impact**: IoC containers have registration overhead (negligible in most apps).
**Optimization**: Use singletons for expensive-to-create dependencies (database connections).
**Profile first**: DI overhead is rarely a bottleneck. Don't sacrifice testability for micro-optimizations.
