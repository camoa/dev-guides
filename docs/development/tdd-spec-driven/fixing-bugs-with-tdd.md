---
description: The reproduce-fix-stop sequence for TDD bug fixes, and why only one test belongs in a bug-fix change
tldr: "Fixing a bug: write one failing test that reproduces it, fix only until that test passes, then stop - don't add tests for untouched behavior or strengthen neighboring assertions in the same change."
---

# Fixing Bugs with TDD

## When to Use
A defect has been reported or found, and code that already exists is wrong. This is the second most common use of the cycle after new features, and it has its own stopping rule.

## The sequence
1. **Reproduce first.** Write one failing test that demonstrates the bug. It must fail for the bug's reason, not for a setup error - read the failure message and confirm it is the symptom you were sent to fix.
2. **Fix.** Change production code until that test passes. Nothing else.
3. **Stop.** Run the suite. If it is green, you are done.

A bug fix with no test that failed before it is a fix nobody can verify.

## What not to do while you are in there
The suite you are standing in front of belongs to the changes that created it. A bug fix is not an invitation to review it.

- Do not add tests for behavior the bug did not touch
- Do not strengthen assertions in neighboring tests because you noticed they were weak. That is a finding - write it down and leave the test alone
- Do not split a test you find too large. Same reason
- Do not raise coverage because this change lowered it. A coverage floor is a signal to look, not an instruction to write tests here

Every one of those is worth doing. None of them belongs in the same change as a bug fix, because each one makes the fix harder to review and impossible to revert cleanly.

## Why one test is the right number
The reproducing test is the evidence that the bug existed and is gone. A second test that passed before your change proves nothing about the bug and will be read later as though it did.

If the bug reveals a whole class of untested cases, that is a real finding and worth its own change. Record it. Do not fold it in.

## Common Mistakes
- Fixing the code first and adding the test after - You never saw it fail, so you do not know the test detects the bug
- Writing the reproducing test at a larger scope than the bug - An end-to-end test for a parsing bug passes for reasons unrelated to the parser
- Refactoring while fixing - You cannot tell whether a failure came from the fix or the restructure. Never change behavior and structure at the same time
- Adding a test per edge case you thought of while reading the code - The bug report is the scope
- Treating a fix round's rising assertion count as thoroughness - It usually means the tests cannot tell your branches apart

## See Also
- Previous: [Changing Existing Tests](changing-existing-tests.md) | Next: [What TDD Covers](what-tdd-covers.md)
- Related: [Red-Green-Refactor Workflow](red-green-refactor.md) - the cycle this specializes
- Related: [Refactoring with Confidence](refactoring-confidence.md) - why a fix and a refactor stay separate
