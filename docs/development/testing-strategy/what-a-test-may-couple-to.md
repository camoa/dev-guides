---
description: What a test may assert on — the contract line between promised return values and unpromised surfaces like printed messages or call order.
tldr: "A test may assert only on promised contracts — return values, state changes, exit codes, exception types, spec'd fields — not on printed message wording or call order. Whole-program output matching is a behavioral test, not a unit test."
drupal_version: "11.x"
---

# What a Test May Couple To

## When to Use

> Deciding what a test should assert on. Reviewing a test that breaks whenever someone rewords a message. Classifying a suite that drives whole programs and matches on their output.

## Decision

| Surface | Is it a contract? | Assert on it |
|---|---|---|
| A returned value | Yes — the caller was promised it | Yes |
| A persisted or observable state change | Yes | Yes |
| A documented exit code | Yes | Yes |
| A thrown exception or error type | Yes | Yes |
| A response status or schema field named in a spec | Yes | Yes |
| The wording of a printed message or log line | No — it leaks out of the implementation | No |
| Internal call order | No | No |
| A private field or method | No | No |
| Rendered markup structure no spec pins | No | No |

## Pattern

The isolation rule tells a unit test what it must not touch: no database, no HTTP, no file system, no clock. It says nothing about what the test may assert on, and that is where tests go wrong quietly.

**A test may depend only on a contract someone actually promised.** A returned value is a promise: the caller was told what comes back. The exact sentence a program prints on its way to returning is not. Nobody agreed to keep that sentence stable, so a test that matches on it breaks when someone rewords it, and the break carries no information about the code.

Size is a proxy for this and usually a good one, but it is not the property. A one-line assertion on a printed sentence is small and badly coupled. A test that exercises a class through several collaborators can be large and perfectly coupled.

**Unit test or behavioral test.** A test that drives a whole program and asserts on its output is a *behavioral test*. It is legitimate, often necessary, and sometimes the only option — a shell script or a command-line tool has no return value to assert on until someone gives it one. It is not a unit test. Counting the two as one number hides how much of a suite is coupled to surfaces nobody promised, which is why a suite can have high coverage and still break on every reword.

**When there is no contract to assert on, that is the finding.** A program whose only observable surface is printed prose has no promised interface. The repair is to give it one — extract the decision into a function that returns a value, an enum, or an error type — not to write more assertions against the prose.

## Common Mistakes

- **Wrong**: Asserting on a printed message to tell which internal branch ran → **Right**: The wording was never promised. Give the code a return value or an error type and assert on that
- **Wrong**: Calling a whole-program test a unit test because it is fast and touches no database → **Right**: Speed and isolation do not make it a unit test; what it couples to does
- **Wrong**: Judging test quality by length → **Right**: Short and badly coupled is common; length is a proxy, coupling is the property
- **Wrong**: Adding assertions on more printed output when a fix is hard to prove → **Right**: That is the signal the code has no promised surface, not that the test needs more detail
- **Wrong**: Reporting unit and behavioral tests as one count → **Right**: Report them separately, or you cannot see the coupling debt

## See Also

- [Unit Testing Concepts](unit-testing-concepts.md) | Next: [Integration Testing Concepts](integration-testing-concepts.md)
- Related: [TDD & Spec-Driven Development — Changing Existing Tests](https://camoa.github.io/dev-guides/development/tdd-spec-driven/changing-existing-tests/) — who may change an assertion once it exists
- Reference: Martin Fowler, [UnitTest](https://martinfowler.com/bliki/UnitTest.html) — solitary vs sociable unit tests
