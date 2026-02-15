---
description: Practical refactoring strategies for Single Responsibility Principle — when to split, detection patterns, and when NOT to split.
---

# SRP in Practice

## When to Refactor Toward SRP

Refactor when you experience:
- Tests that require mocking unrelated dependencies
- Changes in one feature breaking unrelated features
- Difficulty naming a class without "and" or "Manager"
- Classes exceeding ~200-300 lines (soft threshold)

## Pattern: Detecting Violations

**Code Smell Checklist**:
1. Count reasons to change -- if > 1, split
2. List dependencies -- unrelated deps indicate mixed concerns
3. Check test setup -- excessive mocking suggests too many responsibilities
4. Review method names -- unrelated verbs indicate low cohesion

**Python Example**:
```python
# Violation: mixed data access and business logic
class Invoice:
    def calculate_total(self):
        return sum(item.price for item in self.items)

    def save_to_database(self):
        db.execute("INSERT INTO invoices ...")

    def generate_pdf(self):
        return PDF(self.data)

# SRP-Compliant
class Invoice:
    def calculate_total(self):
        return sum(item.price for item in self.items)

class InvoiceRepository:
    def save(self, invoice: Invoice):
        db.execute("INSERT INTO invoices ...")

class InvoicePDFGenerator:
    def generate(self, invoice: Invoice) -> PDF:
        return PDF(invoice.data)
```

## Refactoring Strategy

**Step 1: Identify Responsibilities**
List everything the class does. Group related actions.

**Step 2: Extract by Responsibility**
Create new classes for each group. Use Extract Class refactoring.

**Step 3: Update Dependencies**
Replace direct calls with dependency injection.

**Step 4: Test in Isolation**
Each new class should have focused unit tests.

## Decision: When NOT to Split

| Scenario | Action | Why |
|---|---|---|
| Class is stable and rarely changes | Keep together | Premature abstraction adds complexity |
| Responsibilities are tightly coupled | Keep together | Splitting creates awkward dependencies |
| Class is < 50 lines and cohesive | Keep together | Over-engineering hurts readability |
| Team is unfamiliar with domain | Keep together initially | Split when patterns emerge |

## Common Mistakes

- **Extracting too early** -- Wait for actual change pressure before splitting. Why: YAGNI violation, speculative complexity
- **Creating circular dependencies** -- If A needs B and B needs A after splitting, you split wrong. Why: indicates incorrect responsibility boundaries
- **Splitting data and behavior** -- Keep related data and methods together (rich domain models). Why: anemic models push logic elsewhere
- **One class per method** -- SRP doesn't mean "one public method". Why: over-granularity destroys cohesion
- **Ignoring the axis of change** -- Split along actual change axes, not arbitrary groupings. Why: doesn't solve the maintenance problem

## Performance Considerations

**Myth**: SRP hurts performance due to object proliferation.
**Reality**: Modern compilers/runtimes optimize object creation. Maintainability gains outweigh micro-optimizations.

**When performance matters**: Profile first. If SRP-compliant design is a bottleneck (rare), document the trade-off and optimize locally.
