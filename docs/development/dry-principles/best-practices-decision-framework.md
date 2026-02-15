---
description: Practical decision framework for abstraction, duplication, and code organization including security and performance
---

# Best Practices Decision Framework

## When to Use

When making architectural decisions about abstraction, duplication, and code organization.

## The DRY Decision Tree

```
-- Code looks duplicated
|
|-- Does it represent the same KNOWLEDGE?
|  |-- No -> Keep separate (incidental duplication)
|  +-- Yes
|
|-- How many instances?
|  |-- 1-2 -> Keep duplicated (WET/AHA approach)
|  +-- 3+
|
|-- Are requirements stable?
|  |-- No -> Keep duplicated until stable
|  +-- Yes
|
|-- Do all instances always change together?
|  |-- No -> Might be incidental despite similarity
|  +-- Yes
|
+-- Can you create simple abstraction?
   |-- No -> Keep duplicated (wrong abstraction worse than duplication)
   +-- Yes -> Abstract it (DRY)
```

## Core Principles

1. **DRY is about knowledge, not code** -- Same intent = violates DRY, even if different syntax
2. **Prefer duplication over wrong abstraction** -- Wrong abstraction is harder to fix than duplication
3. **Wait for Rule of Three** -- Don't abstract until third instance (usually)
4. **Let patterns emerge** -- Understand variance before abstracting (AHA principle)
5. **Context matters** -- Microservices, layers, domains may need independent representations
6. **Abstractions have cost** -- Indirection, complexity, cognitive load; balance against benefit

## Security Best Practices

| Practice | Why | How |
|----------|-----|-----|
| **Never duplicate security logic** | Inconsistencies create vulnerabilities | Centralize auth, validation, sanitization |
| **Single source for access control** | Multiple implementations -> gaps in enforcement | Use policy engine or authorization service |
| **Validate at every boundary** | Frontend validation is UX; backend is security | DRY the schema, not the validation call |
| **Schema-driven input validation** | Prevents injection, ensures consistency | JSON Schema, Zod, Protocol Buffers |
| **Centralized secret management** | Secrets scattered in code -> leaks | Use secrets manager (Vault, AWS Secrets Manager) |

```python
# SECURITY ANTI-PATTERN: Duplicated authorization logic
# routes/admin.py
if user.role != 'admin':
    raise Forbidden()

# routes/reports.py
if user.role != 'admin':
    raise Forbidden()

# Problem: Easy to forget check, inconsistent enforcement

# BETTER: Centralized authorization
from functools import wraps

def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if g.user.role != role:
                raise Forbidden()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_role('admin')
def admin_dashboard():
    pass

@require_role('admin')
def view_reports():
    pass

# Single source of truth for authorization logic
```

## Performance Best Practices

| Practice | Why | How |
|----------|-----|-----|
| **Extract repeated expensive operations** | Avoid redundant computation | Cache, memoize, or compute once |
| **DRY database queries** | Reduces N+1 queries, improves performance | Query utilities, ORM with eager loading |
| **Shared constants for thresholds** | Ensures consistent behavior, easy tuning | Config files, environment variables |
| **Avoid over-abstraction in hot paths** | Indirection has cost; inline when necessary | Profile, measure, inline critical sections |

```javascript
// PERFORMANCE ANTI-PATTERN: Repeated expensive computation
function getUserOrders(userId) {
  const user = database.query('SELECT * FROM users WHERE id = ?', userId);
  const orders = database.query('SELECT * FROM orders WHERE user_id = ?', userId);
  return { user, orders };
}

function getUserPayments(userId) {
  const user = database.query('SELECT * FROM users WHERE id = ?', userId);
  const payments = database.query('SELECT * FROM payments WHERE user_id = ?', userId);
  return { user, payments };
}
// User fetched twice! N+1 problem if called in loop

// BETTER: DRY with caching
const userCache = new Map();

function getUser(userId) {
  if (!userCache.has(userId)) {
    userCache.set(userId, database.query('SELECT * FROM users WHERE id = ?', userId));
  }
  return userCache.get(userId);
}

function getUserOrders(userId) {
  return {
    user: getUser(userId),
    orders: database.query('SELECT * FROM orders WHERE user_id = ?', userId),
  };
}
```

## Development Standards

| Standard | Rationale | Example |
|----------|-----------|---------|
| **Single source for business rules** | Changes apply consistently | Validation schemas, policy engines |
| **DRY configuration, WET implementation** | Config should be DRY; implementations can vary | Shared defaults, environment overrides |
| **Code generation over manual sync** | Manual sync always drifts | OpenAPI -> clients, Protobuf -> types |
| **Separate models per boundary** | Coupling through shared schema is fragile | DTOs, view models, domain entities |
| **Composition over inheritance** | Inheritance creates deep coupling | Interfaces, traits, mixins |

## When to Refactor Duplication

**Immediate refactoring needed when:**

- Security logic is duplicated (authorization, validation, sanitization)
- Business rules duplicated across layers (frontend, backend, database)
- Third+ instance appears and pattern is clear
- Bug found in duplicated code (fix reveals divergence)

**Defer refactoring when:**

- Only 1-2 instances exist
- Requirements still evolving rapidly
- Duplication is incidental (similar syntax, different purpose)
- Abstraction would be complex and unclear

**Red flags -- existing abstraction might be wrong:**

- Lots of conditionals or special cases in abstraction
- Callers pass `null`, `undefined`, or empty values frequently
- Changes always require modifying the abstraction
- Abstraction has many configuration options/parameters
- Understanding abstraction requires reading multiple files

## Common Mistakes

- **Dogmatic DRY enforcement** — Ignores context, creates wrong abstractions
- **Ignoring security duplication** — Leads to vulnerabilities from inconsistent enforcement
- **Premature optimization via abstraction** — Measure first; abstractions have cost
- **Never refactoring WET code** — Duplication becomes entrenched, causes divergence
- **Treating all duplication equally** — Some duplication (incidental, across boundaries) is acceptable
