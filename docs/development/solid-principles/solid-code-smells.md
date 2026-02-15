---
description: Code smells that indicate SOLID violations — Large Class, Switch on Type, Empty Override, Feature Envy, Shotgun Surgery, and more with detection and refactoring guidance.
---

# SOLID Code Smells

## When to Use This Guide

During code reviews, use these smells to detect SOLID violations early.

## Code Smell: Large Class (SRP Violation)

**Indicators**:
- Class > 300 lines
- > 10 public methods
- Many unrelated private methods
- Requires scrolling to understand

**Detection**:
```bash
# Find large classes
grep -c "public function" *.php | awk -F: '$2 > 10'
```

**Questions to Ask**:
- Can I describe this class without "and" or "or"?
- Do all methods relate to the same responsibility?
- If I change feature X, does this class change?

**Refactor**: Extract Class, Extract Module.

## Code Smell: Switch/Case on Type (OCP Violation)

**Indicators**:
```php
switch ($type) {
    case 'typeA': /* ... */ break;
    case 'typeB': /* ... */ break;
    case 'typeC': /* ... */ break;
}
```

**Or**:
```typescript
if (obj instanceof ClassA) { /* ... */ }
else if (obj instanceof ClassB) { /* ... */ }
else if (obj instanceof ClassC) { /* ... */ }
```

**Why it smells**:
- Adding new type requires modifying this code
- Same switch pattern repeated in multiple places
- Violates OCP (closed for modification)

**Refactor**: Replace Conditional with Polymorphism.

## Code Smell: Empty Override (LSP Violation)

**Indicators**:
```python
class Base:
    def method(self): pass

class Derived(Base):
    def method(self):
        pass  # Empty: does nothing
```

**Or**:
```typescript
class Derived extends Base {
  method() {
    throw new Error("Not supported");
  }
}
```

**Why it smells**:
- Subtype refuses inherited behavior
- Runtime errors instead of compile-time safety
- Violates substitutability

**Refactor**: Separate hierarchies, don't inherit what you can't fulfill.

## Code Smell: Feature Envy (SRP/ISP Violation)

**Indicators**:
```php
class OrderReport {
    public function generate(Order $order) {
        $customer = $order->getCustomer();
        $email = $customer->getEmail();
        $name = $customer->getName();
        $address = $customer->getAddress();
        $city = $customer->getCity();
        // Uses Customer data more than Order data
    }
}
```

**Why it smells**:
- Class is more interested in another class's data
- Indicates misplaced responsibility

**Refactor**: Move method to the envied class.

## Code Smell: Data Clumps (ISP Violation)

**Indicators**:
- Same group of parameters passed together repeatedly
```typescript
function createUser(name: string, email: string, address: string, city: string, zip: string) {}
function updateUser(id: string, name: string, email: string, address: string, city: string, zip: string) {}
function validateUser(name: string, email: string, address: string, city: string, zip: string) {}
```

**Why it smells**:
- Missing abstraction
- Indicates a concept that deserves its own type

**Refactor**: Introduce Parameter Object.
```typescript
interface UserData {
  name: string;
  email: string;
  address: string;
  city: string;
  zip: string;
}

function createUser(userData: UserData) {}
```

## Code Smell: Shotgun Surgery (SRP/OCP Violation)

**Indicators**:
- One conceptual change requires editing many classes
- Example: Adding a new field requires changing 10+ files

**Why it smells**:
- Responsibility is spread across many classes
- High coupling

**Refactor**: Move related code together (Move Method, Move Field).

## Code Smell: Inappropriate Intimacy (DIP Violation)

**Indicators**:
```python
class OrderProcessor:
    def process(self, order):
        # Directly accesses database internals
        connection = MySQLConnection()
        connection.host = "localhost"
        connection.port = 3306
        connection.connect()
        connection.execute("INSERT INTO orders ...")
```

**Why it smells**:
- High-level code knows low-level details
- Tight coupling to concrete implementation

**Refactor**: Depend on abstraction, inject dependency.

## Code Smell: Primitive Obsession (SRP Violation)

**Indicators**:
- Using primitives instead of domain objects
```typescript
function processPayment(amount: number, currency: string, cardNumber: string, cvv: string, expiry: string) {}
```

**Why it smells**:
- Validation logic scattered
- No encapsulation of related data

**Refactor**: Introduce Value Object.
```typescript
class Money {
  constructor(readonly amount: number, readonly currency: string) {}
}

class CreditCard {
  constructor(readonly number: string, readonly cvv: string, readonly expiry: string) {}
}

function processPayment(amount: Money, card: CreditCard) {}
```

## Code Smell: Long Parameter List (ISP Violation)

**Indicators**:
- > 4 parameters
```php
public function createInvoice($customer, $items, $taxRate, $discount, $currency, $dueDate, $notes) {}
```

**Why it smells**:
- Hard to remember parameter order
- Often indicates missing abstraction

**Refactor**: Introduce Parameter Object, Preserve Whole Object.

## Code Smell: Comments Explaining "What" (SRP Violation)

**Indicators**:
```python
# Calculate discount for premium customers
if customer.type == 'premium':
    discount = 0.1
else:
    discount = 0
```

**Why it smells**:
- Code isn't self-explanatory
- Comment necessary because logic is misplaced

**Refactor**: Extract Method.
```python
def calculate_discount(customer):
    return 0.1 if customer.is_premium() else 0

discount = calculate_discount(customer)
```

## Detection Checklist

**During code review, ask**:
- Can I describe each class's purpose in one sentence?
- Are there switch/if-else chains on type?
- Do subtypes throw "not supported" errors?
- Are dependencies injected or created internally?
- Are interfaces small and focused?
- Is behavior co-located with data?
- Are abstractions generic, not tied to one implementation?
