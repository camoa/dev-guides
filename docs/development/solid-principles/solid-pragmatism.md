---
description: When to bend SOLID rules — balancing principles with YAGNI, KISS, and pragmatic decision-making based on project context.
---

# SOLID vs Pragmatism

## When to Bend the Rules

SOLID principles are **guidelines, not laws**. Dogmatic adherence creates over-engineered, unreadable code. Apply pragmatism.

## Decision: SOLID vs YAGNI Tension

| Principle | YAGNI Conflict | Resolution |
|---|---|---|
| **SRP** | Splitting classes prematurely | Split when class has **actual** multiple reasons to change, not hypothetical ones |
| **OCP** | Creating abstractions "just in case" | Wait for second variation before abstracting |
| **LSP** | Deep inheritance hierarchies | Prefer composition; inheritance only for true "is-a" relationships |
| **ISP** | Interfaces with one method | Split only when clients **actually** need different subsets |
| **DIP** | Abstracting every dependency | Abstract at architectural boundaries, not internal implementation details |

**YAGNI Rule**: "You Aren't Gonna Need It" -- don't implement something until it's necessary, not "potentially useful."

## Pattern: When SOLID Hurts

**Violation of KISS (Keep It Simple, Stupid)**:

```typescript
// Over-engineered (SOLID taken too far)
interface IStringFormatter {
  format(input: string): string;
}

class UpperCaseFormatter implements IStringFormatter {
  format(input: string): string {
    return input.toUpperCase();
  }
}

class FormatterFactory {
  create(type: string): IStringFormatter {
    if (type === 'uppercase') return new UpperCaseFormatter();
    throw new Error('Unknown formatter');
  }
}

const formatter = new FormatterFactory().create('uppercase');
console.log(formatter.format('hello')); // "HELLO"

// Simple, pragmatic solution
console.log('hello'.toUpperCase()); // "HELLO"
```

**When complexity outweighs benefit**: If you have one formatter, used in one place, SOLID is over-engineering.

## Decision Framework: Apply SOLID When...

| Scenario | Apply SOLID? | Why |
|---|---|---|
| Building a library/framework | Yes | Consumers need extensibility |
| Team > 5 developers | Yes | Prevents stepping on each other |
| Domain is complex | Yes | SOLID manages complexity |
| Requirements change frequently | Yes | Flexibility is valuable |
| Small script/prototype | No | Simplicity > flexibility |
| Stable, well-understood domain | No | Over-engineering |
| Solo project, < 1000 lines | No | Overhead not worth it |
| One-off data migration | No | Throw-away code |

## Pattern: Pragmatic SOLID

**Start simple, refactor toward SOLID**:

1. **Write the simplest code that works**
2. **When you add the second variation**, apply OCP
3. **When class has two change reasons**, apply SRP
4. **When tests are hard**, apply DIP
5. **When clients use different subsets**, apply ISP
6. **When inheritance breaks**, check LSP

**Example** (Python):
```python
# Initial implementation (simple)
class OrderProcessor:
    def process(self, order):
        # Calculate total
        total = sum(item.price for item in order.items)

        # Apply discount
        if order.customer_type == 'premium':
            total *= 0.9

        # Save to database
        db.execute("INSERT INTO orders ...")

        # Send email
        send_email(order.customer.email, "Order confirmed")

# After growth (refactored toward SOLID)
class OrderProcessor:
    def __init__(self, repository: IOrderRepository, notifier: INotifier):
        self.repository = repository
        self.notifier = notifier

    def process(self, order: Order):
        self.repository.save(order)
        self.notifier.notify(order.customer)
```

**Don't prematurely abstract**: If you only have regular and premium customers, a simple `if` is fine. Wait until you have 3-4 types before abstracting to a strategy pattern.

## Common Mistakes

- **Applying SOLID everywhere** -- Small scripts don't need DIP. Why: over-engineering kills productivity
- **Premature abstraction** -- "We might need to swap databases someday." Why: YAGNI violation
- **Ignoring team experience** -- Junior team struggling with advanced patterns. Why: code becomes unreadable
- **Forgetting readability** -- 10 classes for simple logic. Why: destroys comprehension
- **SOLID as a checklist** -- "Did I apply all 5?" Why: principles are context-dependent
- **Refactoring stable code** -- "Let's make this more SOLID." Why: if it works and doesn't change, leave it alone

## The Sunk Cost Fallacy

**Bad reason to apply SOLID**: "We already started abstracting, so we must finish."
**Good reason**: "This abstraction is paying off; let's continue."

If SOLID refactoring isn't improving testability, flexibility, or readability -- stop.

## Trade-offs: SOLID Costs

**Benefits**:
- Testable code
- Flexible architecture
- Easier to change

**Costs**:
- More classes/files
- Indirection (harder to trace)
- Upfront design time
- Learning curve

**Decision**: Apply SOLID when benefits > costs.
