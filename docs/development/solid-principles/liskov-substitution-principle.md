---
description: Liskov Substitution Principle — when subtypes break substitutability, behavioral contracts, and the classic Rectangle/Square violation.
---

# Liskov Substitution Principle (LSP)

## When to Use

When designing inheritance hierarchies, implementing interfaces, or using polymorphism. LSP ensures subtypes don't break expectations set by base types.

## Decision: What LSP Means

**Barbara Liskov's Definition** (1994): If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering the correctness of the program.

**In practice**: Subtypes must honor the **behavioral contract** of the base type, not just the method signature.

| Base type expects... | Subtype must... | Violation example |
|---|---|---|
| Method never throws exception X | Not throw exception X | Rectangle.setWidth works, Square.setWidth throws |
| Method accepts null input | Accept null input | Base allows null, subtype rejects it |
| Method returns non-empty list | Return non-empty list | Subtype returns empty list |
| Method completes in O(1) | Not degrade to O(n) | Performance contract violation |

## Pattern: LSP Violation (Rectangle/Square)

**Classic Violation** (Java/TypeScript):
```typescript
class Rectangle {
  constructor(protected width: number, protected height: number) {}

  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }

  area(): number { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(w: number) {
    this.width = w;
    this.height = w; // Breaks LSP: unexpected side effect
  }

  setHeight(h: number) {
    this.width = h;
    this.height = h; // Breaks LSP: unexpected side effect
  }
}

// Client code breaks with Square
function resizeRectangle(rect: Rectangle) {
  rect.setWidth(5);
  rect.setHeight(10);
  expect(rect.area()).toBe(50); // Fails for Square (100 instead)
}
```

**LSP-Compliant**:
```typescript
interface Shape {
  area(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area(): number { return this.width * this.height; }
}

class Square implements Shape {
  constructor(private side: number) {}
  area(): number { return this.side * this.side; }
}

// No inheritance, no LSP violation
```

## Pattern: LSP Violation (Bird/Penguin)

**Python Violation**:
```python
class Bird:
    def fly(self):
        return "Flying!"

class Penguin(Bird):
    def fly(self):
        raise NotImplementedError("Penguins can't fly")
        # Breaks LSP: client expects fly() to work
```

**LSP-Compliant**:
```python
class Bird:
    def move(self):
        return "Moving"

class FlyingBird(Bird):
    def fly(self):
        return "Flying!"

class Penguin(Bird):
    def swim(self):
        return "Swimming!"

# Penguin is a Bird, but not a FlyingBird
```

## Behavioral Subtyping Rules

**Preconditions**: Subtype cannot strengthen (require more)
**Postconditions**: Subtype cannot weaken (guarantee less)
**Invariants**: Subtype must preserve base type invariants
**Exceptions**: Subtype cannot throw new checked exceptions

## Common Mistakes

- **Using inheritance for code reuse** -- Inheritance is "is-a", not "has-a". Why: LSP violations when subtype isn't truly substitutable
- **Strengthening preconditions** -- Base allows null, subtype rejects null. Why: clients passing null to base type break with subtype
- **Weakening postconditions** -- Base guarantees non-null return, subtype returns null. Why: clients expecting non-null crash
- **Throwing unexpected exceptions** -- Subtype throws exceptions base doesn't. Why: breaks client exception handling
- **Empty method implementations** -- Subtype implements required method as no-op. Why: violates behavioral contract (NotImplementedError pattern)
- **Performance degradation** -- Base is O(1), subtype is O(n). Why: violates implicit performance contract
