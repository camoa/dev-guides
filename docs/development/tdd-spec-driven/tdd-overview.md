---
description: What TDD is, why it matters, when to use it, and common mistakes to avoid
---

# TDD Overview

## When to Use
You're starting a new feature, fixing a bug, or working on complex business logic where you want to catch errors early and design better code through tests.

## What is TDD?

Test-Driven Development (TDD) is a software development practice where you **write a failing test before you write any production code**. This inverts the traditional approach of writing code first and testing later.

The core cycle is simple:
1. **Red** - Write a test that fails (because the feature doesn't exist yet)
2. **Green** - Write the minimum code to make the test pass
3. **Refactor** - Clean up the code while keeping tests green

## Why TDD Matters

**Early Bug Detection**: Writing tests first means bugs are caught during development, not in production. Teams using TDD report 40-90% reduction in defect density compared to traditional approaches.

**Better Design**: Tests force you to think about how your code will be used before you write it. This leads to more modular, loosely coupled designs because tightly coupled code is hard to test.

**Living Documentation**: Tests describe what the code does in executable form. Unlike comments, tests never lie - if they pass, the behavior is correct.

**Refactoring Confidence**: Comprehensive test coverage means you can refactor fearlessly. If tests stay green, behavior is preserved.

**Faster Feedback**: Running tests takes seconds compared to manual testing cycles that take hours or days.

## When TDD Shines

- **Complex business logic** with many edge cases
- **Long-lived projects** where maintenance matters
- **Team environments** where code changes hands
- **Regulated industries** requiring audit trails and quality evidence
- **Refactoring legacy code** where you need safety nets

## When to Skip TDD

- **Quick prototypes** or throwaway spikes to explore ideas
- **UI exploration** where visual design is still fluid
- **Tight deadlines** with simple, well-understood problems (though this is debatable)
- **Trivial code** like getters/setters with no logic

## Common Mistakes

- Writing tests after code - Defeats the design benefits; tests become an afterthought
- Skipping refactor step - Accumulates technical debt, code becomes messy despite test coverage
- Testing implementation instead of behavior - Tests break on every refactor, defeating the purpose
- Aiming for 100% coverage - Wastes time on trivial tests, creates false confidence (see [Test Coverage Strategy](test-coverage.md))

## See Also
- Next: [TDD vs Traditional Testing](tdd-vs-traditional.md)
- Reference: [Test-Driven Development: Is TDD Relevant in 2024?](https://www.scrumlaunch.com/blog/test-driven-development-in-2024)
- Reference: [AI-Powered TDD Guide 2025](https://www.nopaccelerate.com/test-driven-development-guide-2025/)
