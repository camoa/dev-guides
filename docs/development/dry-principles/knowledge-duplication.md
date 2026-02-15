---
description: Ensuring business rules, validation logic, and domain knowledge exist in only one authoritative place
---

# Knowledge Duplication

## When to Use

When ensuring business rules, validation logic, data schemas, and domain knowledge exist in only one authoritative place.

## Decision Framework

| Knowledge Type | Single Source of Truth | How to Propagate |
|----------------|------------------------|------------------|
| **Business rules** | Domain model / service layer | Function calls, shared library |
| **Validation rules** | Schema definition (JSON Schema, Zod, etc.) | Code generation, runtime validation |
| **Data structures** | Type definitions, database schema | ORM, codegen from schema |
| **Configuration** | Config files, environment variables | Config service, typed config classes |
| **API contracts** | OpenAPI spec, Protocol Buffers | Code generation for clients/servers |
| **Documentation** | Code comments, docstrings | Generated API docs (Sphinx, JSDoc, etc.) |

## The Core Problem

Knowledge duplication is more insidious than code duplication because it's harder to detect and maintain:

```python
# KNOWLEDGE DUPLICATION: Business rule expressed in 4 places

# Place 1: Frontend validation (JavaScript)
if (age < 18) {
  showError("Must be 18 or older");
}

# Place 2: Backend validation (Python)
if user.age < 18:
    raise ValidationError("Must be 18 or older")

# Place 3: Database constraint
ALTER TABLE users ADD CONSTRAINT age_check CHECK (age >= 18);

# Place 4: Documentation
"""
User registration requires age >= 18
"""

# What happens when requirement changes to 21?
# All four places must be updated — easy to miss one
```

## Pattern: Single Source of Truth

```typescript
// SCHEMA AS SINGLE SOURCE (Zod example)
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email().min(5),
  age: z.number().int().min(18),
  username: z.string().min(3).max(20),
});

type User = z.infer<typeof UserSchema>;

// Frontend: Use schema directly
function validateUserInput(data: unknown): User {
  return UserSchema.parse(data); // Throws if invalid
}

// Backend: Same schema
app.post('/users', (req, res) => {
  const user = UserSchema.parse(req.body);
  // Process validated user
});

// Database: Generate constraints from schema
// (Using Prisma or similar ORM that derives DB schema from types)

// Documentation: Auto-generate from schema
// (Using tools like zod-to-json-schema -> OpenAPI spec)

// RESULT: Change minimum age in ONE place, propagates everywhere
```

## Configuration as Knowledge

```python
# ANTI-PATTERN: Magic numbers scattered throughout code
def calculate_shipping(weight):
    if weight > 50:  # What is 50? Why 50?
        return weight * 2.5
    return weight * 1.8

def is_heavy_package(weight):
    return weight > 50  # Duplicated knowledge

# DRY SOLUTION: Named constants with single source
class ShippingConfig:
    HEAVY_PACKAGE_THRESHOLD_LBS = 50
    HEAVY_PACKAGE_RATE = 2.5
    STANDARD_RATE = 1.8

def calculate_shipping(weight):
    threshold = ShippingConfig.HEAVY_PACKAGE_THRESHOLD_LBS
    if weight > threshold:
        return weight * ShippingConfig.HEAVY_PACKAGE_RATE
    return weight * ShippingConfig.STANDARD_RATE

def is_heavy_package(weight):
    return weight > ShippingConfig.HEAVY_PACKAGE_THRESHOLD_LBS
```

## Common Mistakes

- **Hardcoding business rules in multiple layers** — Frontend, backend, database all have different versions
- **Documenting behavior separately from code** — Documentation drifts out of sync with implementation
- **Manual synchronization** — Expecting developers to "remember" to update all places
- **No schema-driven development** — Data structures defined independently in each layer
- **Treating symptoms instead of cause** — Fixing bugs in one place but missing duplicated logic elsewhere

## See Also

- [DRY in Configuration](dry-in-configuration.md)
- [DRY Across Boundaries](dry-across-boundaries.md)
- [Single Source of Truth - Wikipedia](https://en.wikipedia.org/wiki/Single_source_of_truth)
