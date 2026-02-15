---
description: Identifying and deciding how to address duplicated code blocks - true vs incidental duplication
---

# Code Duplication

## When to Use

When identifying and deciding how to address duplicated code blocks in your codebase.

## Decision Framework

| Type of Code Duplication | Violates DRY? | Action |
|--------------------------|---------------|--------|
| **Exact copy-paste** (same logic, same purpose) | Yes | Extract to function/class |
| **Similar structure, same knowledge** (e.g., validation rules) | Yes | Abstract to shared utility |
| **Similar syntax, different purpose** (incidental) | No | Leave separate |
| **Boilerplate required by framework** (imposed) | No | Accept or use code generation |
| **Temporarily duplicated during refactoring** | No | Acceptable as intermediate state |

## Detecting Code Duplication

**Syntactic duplication**: Identical or near-identical code blocks

- Tools: jscpd, PMD CPD, SonarQube
- Look for: Copy-pasted functions, repeated patterns

**Semantic duplication**: Different code expressing same knowledge

- Requires: Manual code review, understanding business logic
- Look for: Multiple implementations of same business rule

**Structural duplication**: Similar code shape for different purposes

- Decision: Often acceptable (incidental duplication)
- Example: Multiple API endpoints with similar request/response handling

## When to Abstract vs When to Keep Duplicate

**Abstract when:**

- Third instance appears (Rule of Three)
- Business logic is identical across instances
- Changes always apply to all instances
- Abstraction simplifies understanding

**Keep duplicate when:**

- Only 1-2 instances exist
- Code serves different purposes despite similarity
- Requirements are still evolving
- Abstraction would introduce coupling
- Code is simple and self-contained

## Pattern

```php
// EXAMPLE 1: True duplication (violates DRY)
class OrderController {
  public function create($data) {
    if (empty($data['amount']) || $data['amount'] < 0) {
      throw new ValidationException('Invalid amount');
    }
    if (empty($data['customer_id'])) {
      throw new ValidationException('Customer required');
    }
    // ... process order
  }
}

class InvoiceController {
  public function create($data) {
    if (empty($data['amount']) || $data['amount'] < 0) {
      throw new ValidationException('Invalid amount');
    }
    if (empty($data['customer_id'])) {
      throw new ValidationException('Customer required');
    }
    // ... process invoice
  }
}

// DRY SOLUTION: Extract shared validation
class FinancialValidator {
  public static function validateAmount($amount) {
    if (empty($amount) || $amount < 0) {
      throw new ValidationException('Invalid amount');
    }
  }

  public static function validateCustomer($customerId) {
    if (empty($customerId)) {
      throw new ValidationException('Customer required');
    }
  }
}

// EXAMPLE 2: Incidental duplication (OK to keep separate)
class UserRepository {
  public function findById($id) {
    return $this->db->query("SELECT * FROM users WHERE id = ?", [$id]);
  }
}

class ProductRepository {
  public function findById($id) {
    return $this->db->query("SELECT * FROM products WHERE id = ?", [$id]);
  }
}
// These look similar but serve different domains — forced abstraction
// would couple unrelated concepts (User and Product)
```

## Common Mistakes

- **Abstracting incidental duplication** — Couples unrelated code, introduces unnecessary complexity
- **Copy-pasting instead of extracting utility** — Maintenance nightmare when logic changes
- **Over-generalizing abstractions** — Abstract "findById" across all entities creates god-object repository
- **Ignoring the cost of abstraction** — Every abstraction adds indirection; keep simple code simple
- **Forgetting to delete duplicated code after extracting** — Leaves dead code and confusion

## See Also

- [Rule of Three](rule-of-three.md)
- [Code Smells and Detection](code-smells-detection.md)
