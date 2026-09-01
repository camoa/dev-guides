---
description: FIRST principles for unit tests, what a test may couple to, and characteristics of good unit tests
tldr: "Writing any unit test: follow FIRST, and assert only on a promised contract - a return value, a state change, a documented error - never on a log line or call order nobody promised to keep stable."
---

# Unit Testing Fundamentals

## When to Use
Writing any unit test, whether in TDD workflow or traditional testing approach. These principles define what makes a good unit test.

## FIRST Principles

Good unit tests follow the **FIRST** acronym:

**F - Fast**
- Tests should execute in milliseconds
- Slow tests won't be run frequently
- If your test suite takes more than a few seconds, developers will skip running it
- Mock external dependencies (databases, APIs, file systems) to keep tests fast

**I - Isolated / Independent**
- Each test should be self-contained
- Tests should not depend on execution order
- One test's failure should not cause others to fail
- Each test should set up its own data and clean up after itself

**R - Repeatable**
- Same input = same output, every time
- No dependence on current date/time, random numbers, network state
- Tests should pass whether run alone or with other tests
- Tests should pass on any machine, any time

**S - Self-validating**
- Test should automatically determine pass/fail
- No manual inspection of output
- No manual steps required
- Clear assertion that validates expected behavior

**T - Timely**
- Tests are written at the right time
- In TDD: tests written before production code
- In traditional testing: tests written in same timeframe as code
- Not "we'll add tests later" (which rarely happens)

## What a Test May Couple To

FIRST says what a unit test must not touch. It does not say what the test may assert on, and that is the gap that lets a test couple to something nobody promised.

A test may depend only on a contract someone actually promised:

- A returned value
- A persisted or observable state change
- A documented exit code or error type

The exact wording of a log line, a printed message, or an internal call order is not a contract. It leaks out of the implementation; nobody agreed to keep it stable. A test that matches on it breaks when someone rewords a sentence, and that break carries no information.

Size is a proxy for this and usually a good one, but it is not the property. A one-line assertion on a printed sentence is small and badly coupled.

A test that depends on one contract has three reasons to change, and two of them are defects: the behavior changed (legitimate, and it should be stated in words), the interface changed, or the test was wrong.

## Pattern: FIRST in Action

```python
# GOOD: Follows FIRST principles
class TestOrderCalculator:
    def test_calculates_total_with_tax(self):
        # F: Runs in milliseconds (no database calls)
        # I: Creates its own test data, doesn't depend on other tests
        # R: Same inputs always produce same output
        # S: Clear assertion, no manual checking
        # T: Written alongside/before the implementation

        calculator = OrderCalculator()
        order = Order(items=[
            Item(price=10.00, quantity=2),
            Item(price=5.00, quantity=1)
        ])

        total = calculator.calculate_total(order, tax_rate=0.10)

        assert total == 27.50  # (20 + 5) * 1.10

# BAD: Violates multiple FIRST principles
class TestOrderCalculator:
    def test_order_processing(self):
        # NOT FAST: Hits real database
        db.connect('production_db')

        # NOT ISOLATED: Depends on database state from previous tests
        order = db.get_order(id=123)

        # NOT REPEATABLE: Uses current date
        if datetime.now().day == 15:
            discount = 0.15
        else:
            discount = 0.10

        # NOT SELF-VALIDATING: Requires manual inspection
        print(f"Total: {calculator.process(order)}")

        # NOT TIMELY: Test written 6 months after code
```

## What Makes a Good Unit Test?

**Tests One Thing**: Each test should verify a single behavior. If test name needs "and", split into multiple tests.

**Clear Test Name**: Name describes what is being tested and expected outcome.
- Good: `test_calculate_total_applies_tax_rate`
- Bad: `test1`, `testCalculator`, `test_order`

**Arrange-Act-Assert Structure**: Clear three-phase structure (see [Testing Patterns](testing-patterns.md))

**No Conditional Logic**: Tests should not have if/else or loops. If you need conditionals, write separate tests for each case.

**Fails for One Reason**: When test fails, it should be obvious what broke.

## Common Mistakes

- Tests that are actually integration tests - Use real dependencies instead of mocks; run slowly; belong in integration test suite
- Multiple assertions testing different concepts - Split into separate tests; when one fails, unclear which behavior broke
- Tests depending on execution order - Use setup/teardown methods; each test must work in isolation
- Testing implementation instead of behavior - Tests break when refactoring even though behavior unchanged (see [Anti-Patterns](anti-patterns.md))
- Not running tests frequently - Fast, isolated tests can run on every save; slow/coupled tests get skipped

## See Also
- Previous: [When Not to Write a Test](when-not-to-write-a-test.md) | Next: [Test Doubles](test-doubles.md)
- Related: [Testing Patterns](testing-patterns.md) for test structure
- Related: [TDD Anti-Patterns](anti-patterns.md)
- Related: [Testing Strategy - Unit Testing Concepts](https://camoa.github.io/dev-guides/development/testing-strategy/unit-testing-concepts/) - what counts as a unit, and unit vs behavioral tests
- Reference: [FIRST Principles of Testing](https://medium.com/pragmatic-programmers/unit-tests-are-first-fast-isolated-repeatable-self-verifying-and-timely-a83e8070698e)
- Reference: [Apps Developer Blog: FIRST Principle](https://www.appsdeveloperblog.com/the-first-principle-in-unit-testing/)
