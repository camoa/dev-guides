---
description: "The brake on excess tests within a TDD change: what the loop requires, what counts as excess, and what remains mandatory regardless"
tldr: "TDD requires one specification per behavior a change creates, seen failing before the code existed; anything else is excess unless it's a different discipline's test, but excess is never an excuse to skip the one required test."
---

# When Not to Write a Test

## When to Use
A change is in front of you and the discipline says add a test. Reviewing a change whose test additions outweigh its code. Deciding whether one more test earns its place.

## What the loop actually requires
For a change, red-green-refactor produces **one specification per behavior the change creates, at the smallest tier that answers the question, each seen to fail before the code existed.**

That is the whole requirement. Anything else the change adds is one of two things, and both are fine as long as they are named honestly: a test from a different discipline, which has its own phase and is counted separately (see [What TDD Covers](what-tdd-covers.md)), or excess.

## Decision

| The test... | Why it is excess | Instead |
|---|---|---|
| was written after the code and never seen red | It ratifies what was built instead of constraining what will be, and will grow to fit whatever was written | Delete it. If the behavior is worth pinning, write it again from the contract without reading the implementation |
| covers behavior this change did not create or touch | It belongs to a different change; here it inflates the diff and cannot be reverted with the fix | Record it as a finding and leave the test out |
| sits at a larger tier than the question needs | It duplicates a smaller test's coverage and buys a slower, vaguer failure | Move it down a tier |
| is a second test for the same behavior at another tier, with no reason recorded | The same duplication wearing a tier label | Keep the smallest one; if both are needed, record why |
| asserts on a surface nobody promised — message wording, call order, private state | It is not a weak specification; there was no promise, so it is not a specification at all | Assert on the promised contract, or extract one for the code to promise |
| exists to raise a coverage number | Coverage finds gaps; it does not decide that a gap must be filled here | Read the gap. Write a test only where a behavior is genuinely unspecified |
| is a benchmark, a scan or a snapshot counted as TDD coverage | It answers a different question | Keep it, run it, count it separately |

## The two questions
Before a test goes into a change, it should answer both:

1. **Which behavior does this test specify?** A test that cannot name one is measuring, searching or ratifying — all legitimate elsewhere, none of them this.
2. **Was it seen to fail before the code existed?** If not, the test has never demonstrated that it can fail, and nothing yet distinguishes it from an assertion that is always true.

A test that fails either question does not belong in this change. That is the brake, and it needs no threshold because it is derived from the loop's own definition.

## Reading a climbing test-to-code ratio
A ratio of test lines to implementation lines is worth reporting and worth reading. It is not worth enforcing: any number picked would be gamed or ignored, and a single round is not a trend.

What a climbing ratio across repair rounds usually means, in rough order of likelihood:

- Tests are being written after the code, so each round ratifies the round before it
- Assertions are landing on printed output because the code exposes no promised surface — the repair is to give it one, not to assert harder
- New tests restate behavior an existing test already covers, one tier up
- The unit under test does too much, so every case needs its own setup

Each has a different repair, which is why the number is a symptom to read rather than a limit to hit.

## What this does not license
This is not permission to skip. **"Too simple to test" remains not a reason** — simple now is complex later, and a one-line flag or exit code is exactly the kind of behavior that regresses silently.

The brake removes tests that specify nothing. It never removes the one test a new behavior requires, and a change that adds behavior with no failing test written first has not met the discipline, however small the diff.

## Common Mistakes
- Reading this as "write fewer tests" → It is "write the tests the loop requires and stop", which for a new behavior is never zero
- Adding an assertion to an existing test rather than a new test, to keep the count down → The count was never the target, and see [Changing Existing Tests](changing-existing-tests.md) for who may change an assertion at all
- Deleting a ratifying test without replacing it when the behavior is real → The behavior is still unspecified; write the test properly instead
- Treating a rising assertion count in a fix round as thoroughness → It usually means the tests cannot tell the branches apart
- Using a coverage drop as the instruction to write tests in the change that caused it → A coverage floor is a signal to look, not an instruction to write here

## See Also
- Previous: [What TDD Covers](what-tdd-covers.md) | Next: [Unit Testing Fundamentals](unit-testing-fundamentals.md)
- Related: [Changing Existing Tests](changing-existing-tests.md) — who may change or delete a test once it exists
- Related: [Fixing Bugs with TDD](fixing-bugs-with-tdd.md) — the same stopping rule, applied to a defect
- Related: [Test Coverage Strategy](test-coverage.md) — why coverage is a gap-finding tool and not a goal
- Related: [Testing Strategy — What a Test May Couple To](https://camoa.github.io/dev-guides/development/testing-strategy/what-a-test-may-couple-to/) — the promised-contract line in full
- Reference: Kent Beck, in [TDD, AI agents and coding with Kent Beck](https://newsletter.pragmaticengineer.com/p/tdd-ai-agents-and-coding-with-kent) (The Pragmatic Engineer, June 2025) — "The genie doesn't want to do TDD. It wants to write the code and then write tests that pass"
- Reference: Andre Hora, [Are Coding Agents Generating Over-Mocked Tests?](https://arxiv.org/pdf/2602.00409) (MSR 2026) — measured a 23% test-commit ratio for coding agents against 13% otherwise, with tests that mock the function under test or snapshot buggy output
