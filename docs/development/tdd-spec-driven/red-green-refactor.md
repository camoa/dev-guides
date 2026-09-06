---
description: Step-by-step Red-Green-Refactor workflow with decision points at each phase
tldr: "Every time you implement a new feature or fix a bug using TDD. This is the core TDD workflow."
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
   - The right reason is that the behavior is absent. A failure you produced by breaking or reverting working code is a different signal (see [What a Failing Test Proves](what-a-failing-test-proves.md))

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

### REFACTOR when an agent implements

REFACTOR is where agents grow code and quietly drop guards. Run it as a separate step, under the same constraints as GREEN plus two of its own: no new tests and no changed assertions, and a diff-size budget.

The frozen tests are the only proof the refactor preserved behavior. A guard, branch, or edge case with no test pinning it can be removed here and the suite will not notice. A mutation run at the end of the feature is the outer check for that - see [What TDD Covers](what-tdd-covers.md).

```javascript
// WRONG - this is not a refactor. Read to the end of the block.
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
| RED | The test only fails once you break or revert working code | That is mutation verification, not RED. The assertion was authored from the implementation, so it cannot constrain the design (see [What a Failing Test Proves](what-a-failing-test-proves.md)) |
| GREEN | Implementation seems too simple/dumb | That's fine - refactor will improve it, or next test will force better design |
| GREEN | You're tempted to add extra features | Stop - add only enough to pass this test; write another test for new features |
| REFACTOR | A test fails | Default: you broke something - revert and refactor more carefully. Only judge the test brittle if you can name the implementation detail it asserts on (see [Refactoring with Confidence](refactoring-confidence.md)) |
| REFACTOR | Code smells obvious but fix requires new behavior | Stop refactoring; write a new test for that behavior first |

## Common Mistakes

- Skipping RED phase by writing code first - You lose the design benefit of thinking through behavior first
- Producing RED by breaking working code, or by running a code-first test against an old tree - The test does fail, and the run order does look correct, but the assertion came from the implementation and can only ratify it (see [What a Failing Test Proves](what-a-failing-test-proves.md))
- Writing complex tests that test multiple behaviors - Each test should verify one thing; break into multiple tests
- Editing a test in GREEN to make it pass - GREEN is for production code only. If the test itself is wrong, stop, return to RED, and change it there deliberately (see [Changing Existing Tests](changing-existing-tests.md))
- Spending too long on GREEN trying to write perfect code - Green phase is about speed; refactor is about quality
- Forgetting to refactor - The most common mistake; leads to messy code despite test coverage
- Refactoring without running tests - Always run tests after each small refactor step
- Adding features during REFACTOR - Refactoring should only improve structure, never change behavior

## See Also
- Previous: [The Three Laws of TDD](three-laws-tdd.md) | Next: [Changing Existing Tests](changing-existing-tests.md)
- Related: [What a Failing Test Proves](what-a-failing-test-proves.md) - how to tell a real RED from a manufactured one
- Reference: [Test-Driven Development Wikipedia](https://en.wikipedia.org/wiki/Test-driven_development)
- Reference: [Martin Fowler on TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
