---
description: Detecting and fixing LSP violations — contract testing, covariance/contravariance, composition over inheritance, and refactoring patterns.
---

# LSP in Practice

## When to Check LSP

During code review, check LSP when:
- Creating subclasses or implementing interfaces
- Overriding methods
- Using polymorphism
- Seeing unexpected behavior with subtypes

## Pattern: Detecting LSP Violations

**Contract Testing** (Python example):
```python
# Base contract test
class BankAccountTests:
    def test_withdraw_reduces_balance(self, account):
        initial = account.balance
        account.withdraw(10)
        assert account.balance == initial - 10

    def test_withdraw_never_goes_negative(self, account):
        account.withdraw(account.balance + 1)
        assert account.balance >= 0

# All subtypes must pass base tests
class CheckingAccountTests(BankAccountTests):
    def setup(self):
        self.account = CheckingAccount(100)

class SavingsAccountTests(BankAccountTests):
    def setup(self):
        self.account = SavingsAccount(100)

# If FixedDepositAccount can't withdraw, it violates LSP
class FixedDepositAccount(BankAccount):
    def withdraw(self, amount):
        raise NotImplementedError("Fixed deposits can't withdraw")
    # LSP VIOLATION: breaks base contract
```

**LSP-Compliant Solution**:
```python
# Separate hierarchies
class Account:
    def deposit(self, amount): pass

class WithdrawableAccount(Account):
    def withdraw(self, amount): pass

class CheckingAccount(WithdrawableAccount):
    def withdraw(self, amount): # implements withdrawal

class FixedDepositAccount(Account):
    # No withdraw method: LSP preserved
```

## Pattern: Covariance and Contravariance

**PHP 7.4+ Example**:
```php
interface AnimalFeeder {
    public function feed(Animal $animal): Food;
}

// LSP-compliant covariance/contravariance
class CatFeeder implements AnimalFeeder {
    // Contravariance: accept broader input (Animal or subtype)
    public function feed(Animal $animal): CatFood {
        // Covariance: return narrower output (Food subtype)
        return new CatFood();
    }
}
```

## Decision: Composition Over Inheritance

| Scenario | Use Inheritance | Use Composition | Why |
|---|---|---|---|
| True "is-a" relationship | Yes | | Car is-a Vehicle (passes LSP) |
| Behavioral substitution required | Yes | | Payment methods implement same contract |
| Code reuse only | | Yes | Stack uses ArrayList, isn't-a ArrayList |
| Multiple behaviors | | Yes | Avoid multiple inheritance issues |

## Pattern: Refactoring LSP Violations

**TypeScript Example**:
```typescript
// Violation: ReadOnlyList inherits from List
class List<T> {
  add(item: T) { /* adds item */ }
  remove(index: number) { /* removes item */ }
  get(index: number): T { /* returns item */ }
}

class ReadOnlyList<T> extends List<T> {
  add(item: T) { throw new Error("Read-only"); } // LSP VIOLATION
  remove(index: number) { throw new Error("Read-only"); } // LSP VIOLATION
}

// LSP-Compliant: separate hierarchies
interface IReadable<T> {
  get(index: number): T;
}

interface IWritable<T> extends IReadable<T> {
  add(item: T): void;
  remove(index: number): void;
}

class List<T> implements IWritable<T> {
  add(item: T) { /* ... */ }
  remove(index: number) { /* ... */ }
  get(index: number): T { /* ... */ }
}

class ReadOnlyList<T> implements IReadable<T> {
  get(index: number): T { /* ... */ }
}
```

## Common Mistakes

- **Implementing interfaces you can't fulfill** -- Adding NotImplementedError methods. Why: violates LSP contract
- **Returning null when base returns object** -- Weakens postcondition. Why: clients don't expect null
- **Throwing exceptions base doesn't throw** -- Violates exception contract. Why: clients can't handle unexpected exceptions
- **Making subtype more restrictive** -- Requiring non-null when base allows null. Why: breaks existing clients
- **Changing semantics of overridden methods** -- save() persists in base, caches in subtype. Why: violates behavioral contract
- **Performance surprises** -- O(1) base method becomes O(n) in subtype. Why: violates implicit performance expectations

## Testing for LSP Compliance

**Automated testing approach**:
1. Write contract tests for base type
2. Run same tests against all subtypes
3. If subtype fails base tests -- LSP violation

**Static analysis** (TypeScript strict mode):
- Enable `strictFunctionTypes` for parameter contravariance checking
- Enable `strictNullChecks` to catch null contract violations
