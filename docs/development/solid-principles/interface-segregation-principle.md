---
description: Interface Segregation Principle — splitting fat interfaces into focused role interfaces so clients only implement what they need.
---

# Interface Segregation Principle (ISP)

## When to Use

When designing interfaces, APIs, or contracts that multiple clients will implement. ISP prevents forcing clients to depend on methods they don't use.

## Decision: What ISP Means

**Robert Martin's Definition**: "No client should be forced to depend on methods it does not use."

**In practice**: Split large "fat" interfaces into smaller, focused "role" interfaces so clients only implement what they need.

| Symptom | Problem | Solution |
|---|---|---|
| Clients implement methods they don't use | Fat interface | Split into role interfaces |
| Empty/stub method implementations | Interface too broad | Create client-specific interfaces |
| Changes to interface affect unrelated clients | Coupling through unused methods | Segregate by client needs |
| Interface has unrelated method groups | Lack of cohesion | One interface per responsibility |

## Pattern: Fat Interface Violation

**PHP Example**:
```php
// Fat interface: not all workers can do everything
interface Worker {
    public function work(): void;
    public function eat(): void;
    public function sleep(): void;
}

class HumanWorker implements Worker {
    public function work() { /* ... */ }
    public function eat() { /* ... */ }
    public function sleep() { /* ... */ }
}

class RobotWorker implements Worker {
    public function work() { /* ... */ }
    public function eat() { /* VIOLATION: robots don't eat */ }
    public function sleep() { /* VIOLATION: robots don't sleep */ }
}
```

**ISP-Compliant**:
```php
interface Workable {
    public function work(): void;
}

interface Feedable {
    public function eat(): void;
}

interface Restable {
    public function sleep(): void;
}

class HumanWorker implements Workable, Feedable, Restable {
    public function work() { /* ... */ }
    public function eat() { /* ... */ }
    public function sleep() { /* ... */ }
}

class RobotWorker implements Workable {
    public function work() { /* ... */ }
    // No eat/sleep methods: only implements what it needs
}
```

## Pattern: Role Interfaces

**TypeScript Example**:
```typescript
// Fat interface
interface MultiFunctionPrinter {
  print(doc: Document): void;
  scan(doc: Document): Document;
  fax(doc: Document): void;
  staple(doc: Document): void;
}

// Simple printer forced to implement everything
class BasicPrinter implements MultiFunctionPrinter {
  print(doc: Document) { /* ... */ }
  scan(doc: Document) { throw new Error("Not supported"); } // VIOLATION
  fax(doc: Document) { throw new Error("Not supported"); } // VIOLATION
  staple(doc: Document) { throw new Error("Not supported"); } // VIOLATION
}

// ISP-Compliant: role interfaces
interface Printer {
  print(doc: Document): void;
}

interface Scanner {
  scan(doc: Document): Document;
}

interface Fax {
  fax(doc: Document): void;
}

class BasicPrinter implements Printer {
  print(doc: Document) { /* ... */ }
}

class MultiFunctionDevice implements Printer, Scanner, Fax {
  print(doc: Document) { /* ... */ }
  scan(doc: Document) { /* ... */ }
  fax(doc: Document) { /* ... */ }
}
```

## ISP vs SRP

**ISP**: Client-focused. Split interfaces so clients depend only on what they use.
**SRP**: Implementation-focused. Classes should have one reason to change.

**They align**: Fat interfaces often indicate classes with multiple responsibilities.

## Common Mistakes

- **Creating one giant interface** -- Forces all implementers to implement everything. Why: creates unnecessary coupling, stub implementations
- **Using abstract base classes as interfaces** -- Base classes with concrete methods create tight coupling. Why: clients depend on implementation details
- **Not splitting until forced** -- Waiting for the third violation. Why: early split prevents technical debt accumulation
- **Over-splitting** -- Interface per method. Why: destroys cohesion, makes code unreadable
- **Ignoring client needs** -- Splitting by implementation convenience, not client usage. Why: doesn't solve the actual problem
- **Marker interfaces with no methods** -- Used for type tagging. Why: not a SOLID violation, but can be replaced with better patterns (generics, enums)
