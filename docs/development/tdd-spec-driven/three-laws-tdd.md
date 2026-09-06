---
description: Robert C. Martin's three laws of TDD and the rapid test-first discipline cycle
tldr: "Every TDD cycle runs on these three laws; Law 2 - stop the test the moment it fails, not when it feels complete - is the one most often skipped."
---

# The Three Laws of TDD

## When to Use
Every TDD cycle. These three laws are the default discipline, not an optional purist mode - Law 2 is the only rule in this guide that bounds how much test you write at once.

## The Laws (Robert C. Martin / Uncle Bob)

1. **You may not write production code unless it is to make a failing unit test pass**
   - No implementation code without a failing test first
   - Even a single line of production code requires a failing test

2. **You may not write more of a unit test than is sufficient to fail**
   - Stop writing the test as soon as it fails
   - Compilation failures count as failures
   - Write just enough test to define the next small piece of behavior

3. **You may not write more production code than is sufficient to pass the failing test**
   - Stop as soon as the test passes
   - Don't add "future" features or clever abstractions
   - Write the simplest thing that could possibly work

Law 2 is the one most often skipped. "Sufficient to fail" means you stop writing the test the moment it fails - not when it feels complete. A test written past that point is specifying behavior you have not yet decided to build.

## Pattern: Following the Laws

```python
# RED (Law 2: Write just enough test to fail)
def test_add_returns_sum_of_two_numbers():
    calculator = Calculator()
    result = calculator.add(2, 3)
    assert result == 5  # FAILS - Calculator.add() doesn't exist

# GREEN (Law 3: Write minimum code to pass)
class Calculator:
    def add(self, a, b):
        return a + b  # Simple implementation - passes the test

# Don't write: def add(self, *args): return sum(args)
# Law 3: That's more than needed to pass THIS test

# Next RED (Law 1: No production code without failing test)
def test_add_handles_negative_numbers():
    calculator = Calculator()
    result = calculator.add(-1, 1)
    assert result == 0  # This already passes! Our simple implementation handles it
```

## The Rhythm

The three laws create a rapid cycle, often **measured in minutes or even seconds**:
1. Write a few lines of test (10-30 seconds)
2. Run test, watch it fail (5 seconds)
3. Write minimal code to pass (30 seconds - 2 minutes)
4. Run test, watch it pass (5 seconds)
5. Refactor if needed (30 seconds - 2 minutes)
6. Repeat

## Agent variant: batched RED per slice

When the test author and the implementer are separate contexts, handing over one test at a time is impractical. The accepted variant is: the author writes the tests for one slice of the work - a small group of behaviors that can go green without stubbing later work - each seen to fail because its behavior is absent, then freezes them. The implementer works through them one at a time under Law 3.

What this keeps: absence-RED for every test, and an oracle written before and outside the implementation. What it gives up: the design feedback that comes from authoring one test at a time. Keep slices small so the loss stays small.

A slice whose tests cannot be written without guessing the interface is an architecture gap, not a reason to write the code first.

This rhythm keeps you in "flow" - never more than a minute or two from running tests.

## Why These Laws Matter

**Prevents over-engineering**: Law 3 stops you from writing speculative code "we might need someday"

**Maintains focus**: Laws 1 and 2 keep you working on one small piece at a time

**Creates comprehensive coverage**: Following the laws naturally produces high test coverage

**Builds working software incrementally**: Every few minutes you have working, tested code

## Kent Beck's Original Formulation (Slightly Different)

1. **Red**: Write a little test that doesn't work, perhaps doesn't even compile
2. **Green**: Make the test work quickly, committing whatever sins necessary in the process
3. **Refactor**: Eliminate all duplication created in merely getting the test to work

Beck's version emphasizes the emotional/aesthetic journey (red-green-clean) while Uncle Bob's version emphasizes the strict discipline.

## Common Mistakes

- Writing multiple tests before any production code - Violates Law 1; creates too much to implement at once
- Writing full implementation because "I know what's needed" - Violates Law 3; skips the incremental design process
- Not running tests immediately - Loses the fast feedback that makes TDD work
- Skipping refactor because tests pass - The most common TDD failure; leads to code rot despite test coverage

## See Also
- Previous: [TDD vs Traditional Testing](tdd-vs-traditional.md) | Next: [Red-Green-Refactor Workflow](red-green-refactor.md)
- Reference: [The Cycles of TDD - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html)
- Reference: [Canon TDD - Kent Beck](https://tidyfirst.substack.com/p/canon-tdd)
