---
description: Writing and maintaining technical documentation using code as the single source of truth
---

# DRY in Documentation

## When to Use

When writing and maintaining technical documentation, API docs, code comments, and system documentation.

## Decision Framework

| Documentation Type | Single Source | Generation Method |
|-------------------|---------------|-------------------|
| **API documentation** | Code (types, docstrings, annotations) | JSDoc, Sphinx, Doxygen, OpenAPI |
| **Database schema** | Migration files or ORM models | Schema visualization tools |
| **Configuration options** | Schema definitions (JSON Schema, Zod) | Auto-generated reference docs |
| **Type definitions** | TypeScript/types in source code | Generated `.d.ts` files |
| **Architecture diagrams** | Code structure | Automated diagram generation |
| **User guides** | Feature code + docstrings | MkDocs, Docusaurus from markdown |

## The Problem: Documentation Drift

```python
# ANTI-PATTERN: Documentation duplicates and drifts

def calculate_discount(price, customer_type):
    """
    Calculate discount for a customer.

    Args:
        price: Item price
        customer_type: Either 'regular' or 'premium'

    Returns:
        Discounted price
    """
    # Code was updated but docs weren't!
    if customer_type == 'vip':      # Was 'premium', now 'vip'
        return price * 0.8
    elif customer_type == 'gold':   # New tier not in docs
        return price * 0.9
    return price

# Documentation is now wrong and misleading
```

## Pattern: Code as Documentation (DRY)

```typescript
// GOOD: Types are documentation
type CustomerType = 'regular' | 'vip' | 'gold';

interface DiscountRule {
  customerType: CustomerType;
  multiplier: number;
}

const DISCOUNT_RULES: DiscountRule[] = [
  { customerType: 'vip', multiplier: 0.8 },
  { customerType: 'gold', multiplier: 0.9 },
  { customerType: 'regular', multiplier: 1.0 },
];

/**
 * Calculate discount for a customer.
 *
 * @param price - Item price in cents
 * @param customerType - Customer tier (see {@link CustomerType})
 * @returns Discounted price
 *
 * @example
 * ```ts
 * calculateDiscount(1000, 'vip') // Returns 800
 * ```
 */
function calculateDiscount(price: number, customerType: CustomerType): number {
  const rule = DISCOUNT_RULES.find(r => r.customerType === customerType);
  return price * (rule?.multiplier ?? 1.0);
}

// API docs auto-generated from JSDoc + TypeScript types
// No manual documentation to maintain
```

## Generated Documentation

```python
# Python example with Sphinx autodoc
class UserService:
    """
    Service for managing user accounts.

    This service provides CRUD operations for users and handles
    authentication logic.
    """

    def create_user(self, email: str, password: str) -> User:
        """
        Create a new user account.

        Args:
            email: Valid email address for the user
            password: Password (min 8 characters)

        Returns:
            Created user object

        Raises:
            ValidationError: If email is invalid or password too short
            DuplicateError: If email already exists

        Example:
            >>> service.create_user('test@example.com', 'password123')
            User(id=1, email='test@example.com')
        """
        # Implementation
        pass

# Sphinx generates HTML docs directly from docstrings
# Types are checked by mypy, docs always match code
```

## OpenAPI/Swagger (Schema-Driven Docs)

```yaml
# openapi.yml — Single source for API contract
openapi: 3.0.0
paths:
  /users:
    post:
      summary: Create a new user
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    CreateUserRequest:
      type: object
      required: [email, password]
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          minLength: 8

# Generate from this single source:
# - API documentation (Swagger UI)
# - Client SDKs (openapi-generator)
# - Server stubs
# - Validation schemas
# - Type definitions
```

## Architecture Documentation

```python
# ANTI-PATTERN: Hand-drawn diagrams in separate docs
# (Always out of date, no validation against actual architecture)

# BETTER: Generate diagrams from code structure
# Tools: Mermaid (from markdown), PlantUML, Structurizr

# Example: Generate component diagram from code structure
from pathlib import Path
import ast

def generate_dependency_graph(src_dir):
    """Auto-generate dependency diagram from imports."""
    modules = {}
    for py_file in Path(src_dir).rglob('*.py'):
        tree = ast.parse(py_file.read_text())
        imports = [node.module for node in ast.walk(tree)
                   if isinstance(node, ast.Import)]
        modules[py_file.stem] = imports

    # Generate Mermaid diagram
    print("graph TD")
    for module, deps in modules.items():
        for dep in deps:
            print(f"  {module} --> {dep}")

# Output is always accurate — derived from actual code
```

## Common Mistakes

- **Writing documentation separately from code** — Guaranteed to drift out of sync
- **Documenting what the code does** — Code should be self-documenting; explain WHY, not WHAT
- **No examples in documentation** — Examples are the most valuable part and easiest to auto-generate from tests
- **Manual API documentation** — Auto-generate from types, schemas, and docstrings
- **Outdated diagrams** — Generate from code structure, don't draw manually
- **Copy-pasting code into docs** — Link to source or include file references that auto-update

## See Also

- [Knowledge Duplication](knowledge-duplication.md)
- [Sphinx Documentation Generator](https://www.sphinx-doc.org/)
- [OpenAPI Specification](https://swagger.io/specification/)
