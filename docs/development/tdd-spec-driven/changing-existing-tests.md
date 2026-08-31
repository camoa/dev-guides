---
description: Who may add, change, or delete a test at each TDD phase, and why a reviewer never edits the test it's judging
tldr: "Before changing an assertion or deleting a test, check the mutability matrix for who may touch it; an adversarial reviewer never edits or deletes a test it's judging - it files a finding instead."
---

# Changing Existing Tests

## When to Use
Before you change an assertion in a test that already exists, before you delete a test, and before you dispatch an agent to review work it did not write. This section says who holds the pen. It does not say what a test should assert - see [Unit Testing Fundamentals](unit-testing-fundamentals.md) for that.

## Why an assertion change is not a small edit
Adding a test is visible: the count moves and the diff is obvious. Changing an assertion inside a test that already exists is invisible. The count does not move, coverage does not move, and the diff reads as a refinement. But the contract moved.

After that, a red test no longer tells you which of two things happened: the code regressed, or the target moved. Both produce the same red. Only the record of who changed what separates them.

## The mutability matrix

| Role / phase | Add a test | Change an assertion | Delete a test | Change production code |
|---|---|---|---|---|
| Author, RED | One, minimal | This is authoring it, not changing it | No | No |
| Author, GREEN | No | No | No | Yes |
| Author, REFACTOR | No | No | No | Behavior-preserving only |
| Bug fix | One reproducing test | No | No | Yes |
| Feature removal | No | No | Yes, the removed feature's tests, in the same commit | Yes |
| Adversarial reviewer | No | No | No | No. It emits a finding |

## The reviewer's output is a finding, not a commit
An agent that can change the test it is judging is not verifying. It is grading its own homework. This is the same defect as a builder deciding whether its own repair worked, and it has the same fix.

A reviewer that judges a test weak, wrong, or obsolete says so, and routes the finding back to the author or to the spec. It never edits the test and it never deletes one. Where a tool can enforce this it should: a reviewing agent's write access should not include test files. That is the one row of this matrix a tool can enforce outright rather than by asking.

## The one exception, and why it is narrow
A bug fix may reveal that a test asserted the wrong thing. The test then has to be correctable, or a flat prohibition gets bypassed rather than satisfied.

Treat that as a finding about the test, not as routine maintenance. Say in words what the test asserted and why that was never the requirement, and record it where a reviewer will read it. Tightening a limit because the code genuinely got smaller and loosening one to admit code that should not pass produce the same shape of diff. Only the words separate them.

## What counts as an assertion change
An assertion change is a contract change, whoever makes it.

Assertion changes:
- Changing an expected value, a matcher, or a boundary
- Adding an assertion to a test that already exists
- Removing an assertion
- Widening a limit, a tolerance, or a timeout

Not assertion changes:
- Renaming a variable inside the test
- Replacing a fragile locator or selector with a stable one that targets the same thing
- Extracting a fixture or a factory without changing what is asserted

The dividing line is whether the set of program behaviors that pass the test changed. If it did, the contract moved.

## Common Mistakes
- Editing a test in GREEN to make it pass - GREEN is for production code only. If the test itself is wrong, stop, return to RED, and change it there deliberately
- Judging a test brittle so you may change it - A test is brittle only when you can name the implementation detail it asserts on. Name it and record the name. If you cannot name one, the code regressed
- Letting the agent that wrote the code also judge the test - It resolves every ambiguity in favor of being finished
- Deleting a test because it looks obsolete - Only the change that removes the feature removes its tests, and it removes them in the same commit
- Reading a growing assertion count as growing confidence - Assertions added while fixing code that already existed usually ratify what the code does instead of constraining it

## See Also
- Previous: [Red-Green-Refactor Workflow](red-green-refactor.md) | Next: [Fixing Bugs with TDD](fixing-bugs-with-tdd.md)
- Related: [Unit Testing Fundamentals](unit-testing-fundamentals.md) - what a test may couple to
- Related: [AI Test Generation - Four-Phase Pattern](https://camoa.github.io/dev-guides/testing/ai-test-generation/ai-testgen-four-phase-pattern/) - the same rule specialized for generated E2E suites
