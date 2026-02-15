---
description: Step-by-step Red-Green-Refactor workflow with decision points at each phase
---

# Red-Green-Refactor Workflow

## When to Use
Every time you implement a new feature or fix a bug using TDD. This is the core TDD workflow.

## Steps

1. **RED - Write a Failing Test**
   - Think about the next small piece of behavior you need
   - Write a test that describes that behavior
   - Run the test and verify it fails for the right reason
   - A test that passes without any implementation means your test is broken

```javascript
// RED: Test for parsing a user's full name
describe('UserNameParser', () => {
  it('splits full name into first and last', () => {
    const parser = new UserNameParser();
    const result = parser.parse('John Doe');
    expect(result).toEqual({ first: 'John', last: 'Doe' });
  });
});
// Output: UserNameParser is not defined
```

2. **GREEN - Make the Test Pass (Quickly)**
   - Write the simplest code that makes the test pass
   - Ignore code quality at this step - just make it work
   - Hard-coding values is fine if it passes the test
   - "Commit whatever sins necessary" - Kent Beck

```javascript
// GREEN: Simplest implementation that passes
class UserNameParser {
  parse(fullName) {
    const parts = fullName.split(' ');
    return { first: parts[0], last: parts[1] };
  }
}
// Output: Test passes
```

3. **REFACTOR - Improve the Code**
   - Clean up duplication
   - Improve names, structure, clarity
   - Extract methods/functions if needed
   - Tests must stay green throughout refactoring
   - If a test fails during refactor, you broke something - undo and try again

```javascript
// REFACTOR: Handle edge cases we realized during implementation
class UserNameParser {
  parse(fullName) {
    if (!fullName || typeof fullName !== 'string') {
      throw new Error('Invalid name');
    }
    const parts = fullName.trim().split(/\s+/); // Handle multiple spaces
    return {
      first: parts[0],
      last: parts.slice(1).join(' ')  // Handle middle names
    };
  }
}
// Wait - we just changed behavior without a test!
// This is wrong. Undo and write tests for edge cases first.
```

4. **Repeat - Add Next Test**
   - Once tests are green and code is clean, return to RED
   - Write the next failing test for the next small behavior
   - Repeat the cycle

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| RED | Test passes without implementation | Your test doesn't actually test new behavior - rewrite it |
| RED | Test fails to compile | That's fine - compilation failures are failures; move to GREEN |
| GREEN | Implementation seems too simple/dumb | That's fine - refactor will improve it, or next test will force better design |
| GREEN | You're tempted to add extra features | Stop - add only enough to pass this test; write another test for new features |
| REFACTOR | A test fails | You broke something - revert and refactor more carefully |
| REFACTOR | Code smells obvious but fix requires new behavior | Stop refactoring; write a new test for that behavior first |

## Common Mistakes

- Skipping RED phase by writing code first - You lose the design benefit of thinking through behavior first
- Writing complex tests that test multiple behaviors - Each test should verify one thing; break into multiple tests
- Making tests pass with production changes instead of test fixes - If test is wrong, fix the test in RED phase
- Spending too long on GREEN trying to write perfect code - Green phase is about speed; refactor is about quality
- Forgetting to refactor - The most common mistake; leads to messy code despite test coverage
- Refactoring without running tests - Always run tests after each small refactor step
- Adding features during REFACTOR - Refactoring should only improve structure, never change behavior

## See Also
- Previous: [The Three Laws of TDD](three-laws-tdd.md) | Next: [Unit Testing Fundamentals](unit-testing-fundamentals.md)
- Reference: [Test-Driven Development Wikipedia](https://en.wikipedia.org/wiki/Test-driven_development)
- Reference: [Martin Fowler on TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
