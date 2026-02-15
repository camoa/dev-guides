---
description: Daily SOLID decision framework — decision tree, apply-or-skip matrix, security and performance best practices, and anti-pattern avoidance checklist.
---

# Best Practices Decision Framework

## When to Use This Framework

Use this framework for daily development decisions: designing classes, reviewing code, refactoring legacy code.

## Decision Tree: Which SOLID Principle to Apply?

```
Is this a new class/interface?
|- YES: Apply SRP -> One reason to change
|   +- Will it need variations?
|       |- YES: Apply OCP -> Design for extension
|       |   +- Using inheritance?
|       |       |- YES: Check LSP -> Ensure substitutability
|       |       +- NO: Continue
|       +- NO: Keep simple (YAGNI)
|
+- NO: Modifying existing code?
    +- Does class do too much?
        |- YES: Refactor toward SRP
        +- NO: Adding variation?
            |- YES: Apply OCP -> Extend, don't modify
            +- NO: Continue

Does this interface have > 5 methods?
|- YES: Do all clients use all methods?
|   |- NO: Apply ISP -> Split interface
|   +- YES: Keep cohesive interface
+- NO: Continue

Does this class create its dependencies?
|- YES: Is it at an architectural boundary?
|   |- YES: Apply DIP -> Inject dependencies
|   +- NO: Internal detail -> OK to keep simple
+- NO: Continue
```

## Decision Matrix: Apply SOLID or Stay Simple?

| Factor | Apply SOLID | Stay Simple |
|---|---|---|
| **Team size** | > 3 developers | Solo or pair |
| **Codebase size** | > 10k lines | < 1k lines |
| **Change frequency** | Weekly releases | Yearly releases |
| **Expected lifetime** | Years | Weeks (prototype) |
| **Domain complexity** | High (finance, healthcare) | Low (CRUD app) |
| **Testability requirement** | High (CI/CD, TDD) | Low (manual testing) |
| **API/Library** | Public API | Internal use only |

## Security Best Practices

**DIP for Security**:
- Don't create security-critical dependencies (auth, crypto) directly
- Inject vetted implementations (bcrypt, jwt libraries)
- Abstract authentication to enable security updates without business logic changes

**Example** (PHP):
```php
// WRONG: Direct dependency on crypto implementation
class UserService {
    public function hashPassword($password) {
        return md5($password); // INSECURE, hard to change
    }
}

// CORRECT: Depend on abstraction
interface IPasswordHasher {
    public function hash(string $password): string;
    public function verify(string $password, string $hash): bool;
}

class BcryptPasswordHasher implements IPasswordHasher {
    public function hash(string $password): string {
        return password_hash($password, PASSWORD_BCRYPT);
    }

    public function verify(string $password, string $hash): bool {
        return password_verify($password, $hash);
    }
}

class UserService {
    public function __construct(private IPasswordHasher $hasher) {}

    public function hashPassword(string $password): string {
        return $this->hasher->hash($password);
    }
}
// Can upgrade to Argon2 by injecting new implementation
```

**SRP for Security Auditing**:
- Isolate security-critical code in dedicated classes
- Easier to audit, test, and secure
- Example: `AuthenticationService`, `AuthorizationService`, `EncryptionService`

## Performance Best Practices

**Myth**: SOLID principles hurt performance.
**Reality**: Maintainable code is easier to optimize.

**Performance Considerations**:

1. **Profile before optimizing**: Don't sacrifice SOLID for micro-optimizations without data
2. **Hot path exceptions**: In proven bottlenecks, document trade-offs
3. **Lazy loading**: DIP enables lazy initialization of expensive dependencies
4. **Caching**: OCP enables adding caching decorators without modifying core logic

**Example** (TypeScript):
```typescript
// DIP enables performance optimization via decorator
interface IUserRepository {
  findById(id: string): User;
}

class DatabaseUserRepository implements IUserRepository {
  findById(id: string): User {
    // Expensive database call
  }
}

// Add caching without modifying original
class CachedUserRepository implements IUserRepository {
  constructor(
    private repository: IUserRepository,
    private cache: Map<string, User>
  ) {}

  findById(id: string): User {
    if (this.cache.has(id)) {
      return this.cache.get(id)!;
    }
    const user = this.repository.findById(id);
    this.cache.set(id, user);
    return user;
  }
}

// Swap implementations based on needs
const repo = isDevelopment
  ? new DatabaseUserRepository()
  : new CachedUserRepository(new DatabaseUserRepository(), new Map());
```

## Development Standards

**Prefer composition over inheritance**:
- Inheritance creates tight coupling
- Composition is flexible (swap at runtime)
- Use inheritance only for true "is-a" relationships

**Dependency Injection Standards**:
- Constructor injection for required dependencies
- Setter injection for optional dependencies
- Avoid Service Locator (hides dependencies)

**Interface Design Standards**:
- Interfaces should be client-focused (ISP)
- Abstract enough to support multiple implementations (DIP)
- Small and cohesive (ISP)

**Testing Standards**:
- If you can't mock a dependency -- DIP violation
- If test setup is complex -- SRP violation (too many dependencies)
- If changing one feature breaks unrelated tests -- OCP/SRP violation

## Anti-Pattern Avoidance Checklist

**Before committing code**:
- No god objects (> 300 lines or > 10 methods per class)
- No switch/case on type (use polymorphism)
- No empty method overrides (LSP violation)
- No `new` keyword in business logic (inject dependencies)
- No methods implementing interface they don't use (ISP)
- No NotImplementedError in production code (design flaw)

## Quick Reference: SOLID in One Sentence Each

| Principle | One-Sentence Rule |
|---|---|
| **SRP** | A class should have one reason to change. |
| **OCP** | Extend behavior without modifying existing code. |
| **LSP** | Subtypes must be substitutable for their base types. |
| **ISP** | Clients shouldn't depend on methods they don't use. |
| **DIP** | Depend on abstractions, not concrete implementations. |
