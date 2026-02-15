---
description: Choosing the right abstraction mechanism to eliminate duplication - functions, classes, composition, and configuration
---

# Abstraction Strategies

## When to Use

When deciding how to eliminate duplication through abstraction — choosing the right abstraction mechanism for the situation.

## Decision Framework

| If duplication is... | Use | Why |
|---------------------|-----|-----|
| **Procedural logic** (algorithms, calculations) | Functions | Simplest, most composable |
| **Related data + behavior** | Classes/Objects | Encapsulation, state management |
| **Cross-cutting concerns** (logging, auth) | Decorators, Middleware, Aspects | Separate concerns from business logic |
| **Shared behavior across unrelated types** | Mixins, Traits, Interfaces | Composition without inheritance coupling |
| **Platform/language differences** | Adapter pattern, abstraction layer | Isolate platform-specific code |
| **Complex initialization** | Factory pattern, Builder pattern | Centralize object creation logic |
| **Variation in algorithm** | Strategy pattern, polymorphism | Runtime behavior selection |

## Abstraction Techniques

### 1. Extract Function (Simplest)

```javascript
// BEFORE: Duplicated logic
function processUserOrder(user, order) {
  const tax = order.amount * 0.08;
  const total = order.amount + tax;
  // ...
}

function processGuestOrder(guest, order) {
  const tax = order.amount * 0.08;
  const total = order.amount + tax;
  // ...
}

// AFTER: Extract function
function calculateTotal(amount) {
  const tax = amount * 0.08;
  return amount + tax;
}

function processUserOrder(user, order) {
  const total = calculateTotal(order.amount);
  // ...
}

function processGuestOrder(guest, order) {
  const total = calculateTotal(order.amount);
  // ...
}
```

### 2. Extract Class/Module

```python
# BEFORE: Validation logic scattered
class UserController:
    def create(self, data):
        if not data.get('email') or '@' not in data['email']:
            raise ValueError('Invalid email')
        if len(data.get('password', '')) < 8:
            raise ValueError('Password too short')
        # ...

class RegistrationController:
    def register(self, data):
        if not data.get('email') or '@' not in data['email']:
            raise ValueError('Invalid email')
        if len(data.get('password', '')) < 8:
            raise ValueError('Password too short')
        # ...

# AFTER: Extract validator class
class UserValidator:
    @staticmethod
    def validate_email(email):
        if not email or '@' not in email:
            raise ValueError('Invalid email')

    @staticmethod
    def validate_password(password):
        if len(password or '') < 8:
            raise ValueError('Password too short')

    @classmethod
    def validate_user_data(cls, data):
        cls.validate_email(data.get('email'))
        cls.validate_password(data.get('password'))
```

### 3. Composition Over Inheritance

```typescript
// AVOID: Deep inheritance hierarchies
class Animal { eat() {} }
class Mammal extends Animal { breathe() {} }
class Dog extends Mammal { bark() {} }
class Puppy extends Dog { playful() {} }
// Rigid, hard to change, couples unrelated behaviors

// PREFER: Composition with traits/mixins
interface Eater { eat(): void; }
interface Breather { breathe(): void; }
interface Barker { bark(): void; }

class Dog implements Eater, Breather, Barker {
  eat() { /* ... */ }
  breathe() { /* ... */ }
  bark() { /* ... */ }
}
// Flexible, can mix behaviors independently
```

### 4. Configuration Over Code

```php
// BEFORE: Hardcoded variations
class EmailNotifier {
    public function send($message) {
        $smtp = new SmtpClient('smtp.gmail.com', 587);
        $smtp->send($message);
    }
}

class SmsNotifier {
    public function send($message) {
        $api = new TwilioApi('api.twilio.com', '8080');
        $api->send($message);
    }
}

// AFTER: Configuration-driven
class Notifier {
    private $client;

    public function __construct($config) {
        $this->client = ClientFactory::create($config);
    }

    public function send($message) {
        $this->client->send($message);
    }
}

// Usage driven by config, not code changes
$emailNotifier = new Notifier(['type' => 'smtp', 'host' => 'smtp.gmail.com']);
$smsNotifier = new Notifier(['type' => 'twilio', 'host' => 'api.twilio.com']);
```

## Common Mistakes

- **Premature abstraction** — Creating abstractions before understanding the variance; leads to wrong abstractions
- **Over-engineering** — Using complex patterns (Abstract Factory, Command) when simple function would suffice
- **Deep inheritance hierarchies** — Fragile base class problem, hard to change, couples implementations
- **God objects** — Single class/module handling too many responsibilities because it was "DRY"
- **Leaky abstractions** — Abstraction exposes implementation details, defeating its purpose
- **Cargo cult patterns** — Applying design patterns because "best practice" without understanding trade-offs

## See Also

- [Over-DRY Anti-Patterns](over-dry-anti-patterns.md)
- [Composition over inheritance - Wikipedia](https://en.wikipedia.org/wiki/Composition_over_inheritance)
