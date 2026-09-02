---
description: "How to tell a real RED from a manufactured one: absence-RED, mutation-RED and green on arrival, and what each of the three proves"
tldr: "A red run proves the order the commands ran in, not that the test came first: absence-RED constrains the design, mutation-RED only proves the test can fail, and a test green on arrival ratifies code that already works."
---

# What a Failing Test Proves

## When to Use
A test failed before the code was written and you are about to record that as test-first. Reading a report that counts red runs. Reviewing an agent's or a colleague's claim that the discipline was followed.

## Run order is not authoring order
TDD's rules all lean on one fact as proof of discipline: the test ran before the implementation and it failed. That fact does not prove it.

A test written while reading the implementation, then run against a reverted or pre-fix tree, fails at its own assertion for the reason it names. It satisfies every rule TDD states. It is not test-first.

What separates the two is not the order the commands ran in. It is what the author had in front of them when they wrote the assertion. Run order is observable and gets reported. Authoring order is the thing that matters, and nothing records it.

## Decision: three states, usually collapsed into one

| The test... | What that proves | Is it TDD's RED |
|---|---|---|
| fails because the behavior does not exist — **absence-RED** | The assertion came from a requirement, so it constrains the design that follows | Yes |
| fails only after working code is broken or reverted — **mutation-RED** | The test is sensitive, so it can fail at all. It was authored from the code, so it cannot constrain a design that already exists | No |
| passes the moment it is written — **green on arrival** | Nothing yet. It ratifies what the code already did, and it could never have found anything | No |

Mutation-RED is a guard and it is valuable. Green on arrival is legitimate as a characterization or regression test. The error is counting either one as test-first.

## How to tell them apart
The discriminator — what the author was reading — is not observable directly. Three proxies get close:

- **What does the assertion cite?** A requirement or a contract sentence, or the implementation's own field names and internals. The second is a test written from the code.
- **Why did it fail?** The behavior was absent, or the code was broken. Only the first is absence-RED.
- **How many passed immediately?** That is the ratification count, and it is usually not reported at all.

## What to report
Per assertion, which of the three states it was. Then two totals: absence-RED, and green on arrival.

A high green-on-arrival count against a low absence-RED count means the suite ratifies rather than constrains. That is a fact about the suite worth acting on, and no coverage percentage shows it.

## Mutation verification is not the villain
It answers a question every project eventually needs answered: **can this check fail at all?** A check that cannot fire passes forever, and only breaking something on purpose finds it. A test runner whose glob matches no files exits zero; a linter with a broken config reports no findings. Both look exactly like success.

So mutation verification proves sensitivity, and TDD constrains design. Neither substitutes for the other. The failure is not doing it — the failure is presenting its red as evidence that a test came first.

## The revert that proves nothing
Reverting the tree to watch a new spec fail is the common way to fake absence-RED without meaning to. `git stash` stashes the new spec along with the code, so the old spec meets the old code and both pass. Reverting the tree is not reverting the implementation, and the green it produces looks exactly like a correct one.

If you must revert to see a failure, revert the implementation files only and keep the test in the working tree.

## Common Mistakes

- Recording "ran red before the fix" as proof of test-first → It proves the run order, which was never the question
- Breaking working code to produce a red run and calling it RED → That is mutation-RED; it proves sensitivity, never conformance to a promise
- Leaving tests that passed on arrival uncounted → They are the ratification count, and the suite's health cannot be read without it
- Asserting on the implementation's own field names because they were on screen → The assertion now comes from the code, so it can never contradict it
- Reverting the whole tree to watch a new spec fail → The spec goes back with it, and both halves of the old pair agree

## See Also
- Previous: [When Not to Write a Test](when-not-to-write-a-test.md) | Next: [Unit Testing Fundamentals](unit-testing-fundamentals.md)
- Related: [Red-Green-Refactor Workflow](red-green-refactor.md) — the loop whose RED this qualifies
- Related: [What TDD Covers](what-tdd-covers.md) — which tests can be written first at all
- Related: [TDD Anti-Patterns](anti-patterns.md) — Manufactured RED, with an example
- Reference: Trail of Bits, [Mutation testing for the agentic era](https://blog.trailofbits.com/2026/04/01/mutation-testing-for-the-agentic-era/) (April 2026) — killing a mutant proves a test is coupled to the implementation, not that it conforms to a specification
