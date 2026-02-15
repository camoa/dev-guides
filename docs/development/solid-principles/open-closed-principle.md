---
description: Open/Closed Principle — how to make code extensible without modification using polymorphism, composition, and data-driven logic.
---

# Open/Closed Principle (OCP)

## When to Use

When building systems that need to support new features without modifying existing, tested code. Especially critical in libraries, frameworks, and plugin architectures.

## Decision: Open for Extension, Closed for Modification

| If you need to... | Use... | Why |
|---|---|---|
| Add new payment methods without changing checkout | Strategy pattern + interfaces | Existing code remains untouched |
| Support new file formats in an importer | Polymorphism + factory | Each format is isolated |
| Add middleware to a request pipeline | Decorator or chain of responsibility | Pipeline code doesn't change |
| Extend validation rules | Specification pattern | Core validator is closed |

## Pattern: OCP via Polymorphism

**Violation** (TypeScript):
```typescript
class PaymentProcessor {
  process(payment: Payment, type: string) {
    if (type === 'credit_card') {
      // credit card logic
    } else if (type === 'paypal') {
      // PayPal logic
    } else if (type === 'crypto') {
      // crypto logic
    }
    // Adding new payment type requires modifying this class
  }
}
```

**OCP-Compliant** (TypeScript):
```typescript
interface PaymentMethod {
  process(payment: Payment): Result;
}

class CreditCardPayment implements PaymentMethod {
  process(payment: Payment): Result { /* credit card logic */ }
}

class PayPalPayment implements PaymentMethod {
  process(payment: Payment): Result { /* PayPal logic */ }
}

class PaymentProcessor {
  constructor(private method: PaymentMethod) {}

  process(payment: Payment): Result {
    return this.method.process(payment);
  }
}
// Adding CryptoPayment doesn't modify existing classes
```

**PHP Example**:
```php
// Violation
class DiscountCalculator {
  public function calculate($amount, $customerType) {
    if ($customerType === 'regular') return $amount;
    if ($customerType === 'premium') return $amount * 0.9;
    if ($customerType === 'vip') return $amount * 0.8;
  }
}

// OCP-Compliant
interface DiscountStrategy {
  public function apply(float $amount): float;
}

class RegularDiscount implements DiscountStrategy {
  public function apply(float $amount): float { return $amount; }
}

class PremiumDiscount implements DiscountStrategy {
  public function apply(float $amount): float { return $amount * 0.9; }
}

class DiscountCalculator {
  public function __construct(private DiscountStrategy $strategy) {}

  public function calculate(float $amount): float {
    return $this->strategy->apply($amount);
  }
}
```

## Achieving OCP Through Abstraction

**Three core techniques**:
1. **Polymorphism** -- Use interfaces/abstract classes, let subtypes extend behavior
2. **Composition** -- Inject dependencies, swap implementations
3. **Data-Driven Logic** -- Externalize rules to configuration/database

## Common Mistakes

- **Premature abstraction** -- Don't apply OCP until you have 2+ variations. Why: speculative design adds complexity without benefit (YAGNI violation)
- **Leaky abstractions** -- If adding new behavior requires changing the interface, abstraction is wrong. Why: defeats the "closed" part of OCP
- **Strategy explosion** -- Too many tiny strategy classes for simple variations. Why: over-engineering; use simple conditionals for 2-3 stable cases
- **Ignoring the cost** -- OCP adds indirection. Apply where change is frequent, skip where code is stable. Why: every abstraction has a comprehension cost
- **Using switch/if-else chains on types** -- Classic OCP violation. Why: requires modifying the switch every time you add a type; use polymorphism instead
