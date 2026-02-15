---
description: Imposed, inadvertent, impatient, and interdeveloper duplication - identifying and addressing each type
---

# Four Types of Duplication

## When to Use

When analyzing whether duplication in your codebase is problematic and deciding how to address it.

## Decision Framework

Hunt and Thomas identify four types of duplication, each requiring different approaches:

| Type | Description | When to Eliminate | How to Address |
|------|-------------|-------------------|----------------|
| **Imposed** | Duplication forced by environment, language, or platform constraints | Always, if possible | Code generation, build tools, meta-programming |
| **Inadvertent** | Developers don't realize they're duplicating knowledge | Always | Refactor to shared abstractions, normalize data models |
| **Impatient** | Shortcuts taken under pressure or laziness | Usually | Refactor when requirements stabilize, pay down tech debt |
| **Interdeveloper** | Multiple developers duplicate knowledge across modules | Always | Communication, code review, shared libraries, documentation |

## Pattern Examples

```python
# IMPOSED DUPLICATION
# API schema must match in OpenAPI spec and implementation
# Solution: Generate one from the other
openapi: 3.0.0
paths:
  /users:
    get:
      responses:
        '200':
          schema:
            type: array
            items:
              $ref: '#/components/schemas/User'

# Generated from schema (not hand-written)
@dataclass
class User:
    id: int
    email: str
    name: str

# INADVERTENT DUPLICATION
# Two classes with same responsibility, different names
class UserValidator:
    def validate_email(self, email): ...

class AccountChecker:
    def verify_email(self, email): ...  # Same logic!

# Solution: Recognize and consolidate
class UserValidator:
    def validate_email(self, email): ...

# IMPATIENT DUPLICATION
# Copy-paste instead of refactoring
def process_orders():
    orders = db.query("SELECT * FROM orders WHERE status='pending'")
    for order in orders:
        # ... 50 lines of processing

def process_returns():
    returns = db.query("SELECT * FROM returns WHERE status='pending'")
    for return in returns:
        # ... same 50 lines, slightly modified

# Solution: Extract shared logic
def process_items(items, item_type):
    for item in items:
        # ... shared processing logic

# INTERDEVELOPER DUPLICATION
# Team A builds feature, Team B unaware, builds similar feature
# teams/checkout/payment_validator.py
class PaymentValidator: ...

# teams/billing/payment_validator.py (written independently)
class PaymentValidator: ...

# Solution: Shared libraries, API catalogs, architecture reviews
```

## Common Mistakes

- **Treating all duplication the same** — Inadvertent duplication needs refactoring; imposed duplication needs tooling
- **Ignoring interdeveloper duplication** — Leads to parallel implementations and wasted effort
- **Accepting impatient duplication indefinitely** — Accumulates as technical debt, eventually becomes unmaintainable
- **Over-engineering solutions to imposed duplication** — Sometimes duplication is the pragmatic choice when tooling cost exceeds benefit

## See Also

- [The Pragmatic Programmer on types of duplication](https://media.pragprog.com/titles/tpp20/dry.pdf)
