---
description: Understanding what DRY actually means - knowledge duplication vs code duplication
---

# DRY Overview

## When to Use

When making architectural decisions about code organization, abstraction, and knowledge representation across your entire software system.

## The Original Definition

**DRY (Don't Repeat Yourself)** was coined by Andrew Hunt and Dave Thomas in their 1999 book "The Pragmatic Programmer: From Journeyman to Master." The principle states:

> "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."

This is fundamentally about **knowledge duplication**, not just code duplication. The principle extends to database schemas, test plans, build systems, and documentation.

## Knowledge vs Code Duplication

| Aspect | Knowledge Duplication | Code Duplication |
|--------|----------------------|------------------|
| **What it is** | Same business rule/intent expressed in multiple places | Similar or identical code blocks in multiple locations |
| **Why it matters** | Changes to business logic require updates in multiple places | Mechanical copy-paste, may not represent same knowledge |
| **DRY applies?** | Always — violates the core principle | Sometimes — depends on whether knowledge is truly shared |
| **Example** | Validation rules in frontend JS, backend API, database constraints | Similar for-loops in unrelated features |

## Core Insight

DRY is about expressing the same **thing** in two different places, possibly in two totally different ways. It's about duplication of intent and knowledge, not just syntactic similarity.

## Pattern

```typescript
// KNOWLEDGE DUPLICATION (violates DRY)
// Frontend validation
if (email.length < 5 || !email.includes('@')) {
  throw new Error('Invalid email');
}

// Backend validation (same business rule, different code)
if len(email) < 5 or '@' not in email:
    raise ValueError('Invalid email')

// Database constraint (same rule, third place)
CREATE TABLE users (
  email VARCHAR(255) CHECK (LENGTH(email) >= 5 AND email LIKE '%@%')
);

// DRY SOLUTION: Single source of truth
// Shared schema definition (e.g., JSON Schema, Zod, Protocol Buffers)
const emailSchema = z.string().email().min(5);
// Frontend uses schema
// Backend uses schema
// Database constraints generated from schema
```

## Common Mistakes

- **Eliminating all code similarity** — Not all similar code represents the same knowledge; incidental duplication may be acceptable
- **Ignoring non-code duplication** — Database schemas, configs, and documentation can violate DRY just as badly as code
- **Premature abstraction** — Creating abstractions before understanding the problem space leads to wrong abstractions
- **Confusing DRY with code golf** — DRY is about maintainability and single source of truth, not minimizing lines of code
- **Applying DRY blindly across boundaries** — Different contexts (e.g., microservices) may need independent representations

## See Also

- [The Pragmatic Programmer excerpt on DRY](https://media.pragprog.com/titles/tpp20/dry.pdf)
- [Wikipedia: Don't Repeat Yourself](https://en.wikipedia.org/wiki/Don't_repeat_yourself)
