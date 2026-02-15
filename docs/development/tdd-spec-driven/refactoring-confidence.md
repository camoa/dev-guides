---
description: Safe refactoring workflow under test coverage, code smells, and when to refactor
---

# Refactoring with Confidence

## When to Use
Code works but is messy, duplicated, or hard to understand. You want to improve structure without breaking behavior. Comprehensive test coverage is your safety net.

## Refactoring Under Test Coverage

**The Golden Rule:** Never refactor and change behavior at the same time.

**Refactoring workflow:**
1. Ensure tests are green and cover the code you're refactoring
2. Make one small refactoring change
3. Run tests - if they pass, behavior is preserved
4. Commit
5. Repeat

If tests fail during refactoring:
- You broke something - Undo and try smaller change
- Or test was brittle (testing implementation) - Fix test to test behavior

## When to Refactor

**Red-Green-Refactor**: Refactor as part of TDD cycle after test passes

**Rule of Three**: First time, just do it. Second time, notice duplication. Third time, refactor.

**Before adding feature**: Clean up area where you'll add code (Boy Scout Rule: leave code cleaner than you found it)

**After code review**: Address reviewer feedback about code quality

**When you don't understand code**: Refactor to clarity as you read it

**When tests are hard to write**: Code that's hard to test is poorly designed; refactor for testability

## Code Smells That Demand Refactoring

**Long Method/Function** (> 20-30 lines)
- Refactor: Extract smaller functions with clear names
- Test strategy: Keep existing tests at high level, add tests for extracted functions

**Duplicated Code**
- Refactor: Extract common code to shared function/method
- Test strategy: Ensure tests cover all uses before extracting

**Large Class** (> 200-300 lines, many responsibilities)
- Refactor: Split into multiple classes with single responsibility
- Test strategy: Tests will need restructuring; extract one responsibility at a time

**Long Parameter List** (> 3-4 parameters)
- Refactor: Introduce parameter object or builder
- Test strategy: Update test setup to use new parameter approach

**Feature Envy** (method uses another object's data more than its own)
- Refactor: Move method to the class it's envious of
- Test strategy: Move tests with the method

**Primitive Obsession** (using primitives instead of small objects)
- Refactor: Replace primitive with value object
- Test strategy: Tests become clearer with value objects

## Pattern: Safe Refactoring

```python
# Before refactoring: Long method with duplication
def process_order(order):
    # Validate
    if not order.items:
        raise ValueError("Order has no items")
    if not order.customer:
        raise ValueError("Order has no customer")
    if not order.customer.email:
        raise ValueError("Customer has no email")

    # Calculate total
    total = 0
    for item in order.items:
        total += item.price * item.quantity

    # Apply tax
    tax_rate = 0.08 if order.customer.state == 'CA' else 0.06
    total = total * (1 + tax_rate)

    # Apply discount
    if order.customer.is_vip:
        total = total * 0.9

    # Save and send email
    db.save(order)
    email.send(order.customer.email, f"Order total: ${total}")

    return total

# Tests are green - now refactor

# Step 1: Extract validation
def validate_order(order):
    if not order.items:
        raise ValueError("Order has no items")
    if not order.customer:
        raise ValueError("Order has no customer")
    if not order.customer.email:
        raise ValueError("Customer has no email")

# Run tests - still green

# Step 2: Extract calculation
def calculate_order_total(order):
    subtotal = sum(item.price * item.quantity for item in order.items)
    tax_rate = 0.08 if order.customer.state == 'CA' else 0.06
    total_with_tax = subtotal * (1 + tax_rate)

    if order.customer.is_vip:
        return total_with_tax * 0.9
    return total_with_tax

# Run tests - still green

# Step 3: Refactor main function
def process_order(order):
    validate_order(order)
    total = calculate_order_total(order)
    db.save(order)
    email.send(order.customer.email, f"Order total: ${total}")
    return total

# Run tests - still green
# Commit: "Refactor process_order into smaller functions"

# Step 4: Add tests for extracted functions (now that we're confident they work)
def test_validate_order_catches_missing_items():
    with pytest.raises(ValueError, match="no items"):
        validate_order(Order(items=[], customer=Customer()))

def test_calculate_total_applies_vip_discount():
    order = Order(
        items=[Item(price=100, quantity=1)],
        customer=Customer(state='CA', is_vip=True)
    )
    assert calculate_order_total(order) == 97.2  # 100 * 1.08 * 0.9
```

## Test Coverage Requirements for Refactoring

**Before refactoring:**
- High-level tests covering behavior (integration/E2E)
- Unit tests for complex logic you're refactoring
- All tests green

**After refactoring:**
- Same high-level tests still green (behavior unchanged)
- New unit tests for extracted methods (if they're non-trivial)
- Coverage should be same or better

**Don't:**
- Delete tests because code structure changed
- Write new tests for every tiny extracted function
- Update tests to match new internal structure (tests should be implementation-agnostic)

## Common Mistakes

- Refactoring without tests - High risk of breaking behavior; add characterization tests first if none exist
- Refactoring and adding features simultaneously - Can't tell if failure is from refactor or new feature; do separately
- Making large refactoring in one commit - Hard to review and debug if something breaks; refactor in small steps
- Not running tests after each change - Defeats the purpose of tests as safety net; run tests constantly
- Updating tests to match refactored code - If tests need updates after behavior-preserving refactor, they were testing implementation
- Refactoring because "it might be useful someday" - Refactor when you need to, not speculatively

## See Also
- Previous: [Test Coverage Strategy](test-coverage.md) | Next: [TDD Anti-Patterns](anti-patterns.md)
- Related: [Red-Green-Refactor Workflow](red-green-refactor.md)
- Reference: [Martin Fowler: Refactoring](https://martinfowler.com/books/refactoring.html)
- Reference: [Martin Fowler: Code Smell](https://martinfowler.com/bliki/CodeSmell.html)
