---
description: "Which tests belong to the TDD red-green loop versus outer verification (E2E, visual regression, performance, accessibility, security scans)"
tldr: "A test belongs to the TDD loop only if it can be written before the code and watched to fail; E2E, visual regression, performance, and security scans are outer verification, not TDD coverage - driving a browser is not the discriminator."
---

# What TDD Covers

## When to Use
Deciding whether a test belongs to the TDD loop or to a different discipline. Reading a coverage claim that mixes both. Being told to add more tests and not knowing which kind is being asked for.

## The one question that separates them
**Can this test be written before the code and watched to fail for the right reason?**

That is what makes a test a *specification*: someone promised a behavior, and the test states the promise ahead of the implementation. A test that cannot be written first is not a worse test. It is a different instrument, answering a different question, and it belongs to a different phase of the work.

## Decision

| Test kind | Can it be written first and seen to fail? | In the TDD loop |
|---|---|---|
| Unit test of a behavior you are about to write | Yes | Yes |
| Integration test of a seam you are about to create | Yes | Yes |
| A framework's in-process functional or browser tier (Drupal `BrowserTestBase`, `WebDriverTestBase`) | Yes | Yes |
| Property-based test | Yes — state the property, then satisfy it | Yes |
| Consumer-driven contract test | Yes — the contract is written before either side | Yes |
| Golden or snapshot test | Only if the expected file is authored before the code | Only then |
| Browser E2E of a user journey | No — it needs the assembled system | No |
| Visual regression | No — there is no baseline until something renders | No |
| Performance and load tests | No — the threshold comes from measuring, not from a promise | No |
| Accessibility scan (axe, Lighthouse) | No — it sweeps a standard, not a behavior you named | No |
| Security scan, SAST, dependency audit | No — same shape: a catalog sweep over existing code | No |
| Mutation testing | No — it needs a suite to mutate | No |
| Fuzzing | No — it needs code to fuzz | No |
| Exploratory and manual QA | No | No |

None of the "No" rows is discouraged by being there. Several are mandatory on any serious project. They are simply not what red-green-refactor produces, and counting them as though they were hides how much of the actual behavior has been specified.

## Two loops, and the line between them is not the browser
TDD is the inner loop. The test constrains a unit that does not exist yet, and when it fails it names the thing that broke.

E2E, visual regression, performance and the scanners are outer verification. They run against code that already stands, they cannot drive design — an E2E test can never tell you to inject a dependency — and when one fails you know the system broke without knowing where.

The tempting discriminator is "drives a browser," and it is wrong. Drupal's `FunctionalJavascript` tier drives a real browser and sits squarely inside the loop: it is a PHPUnit tier, written before the code, run red then green. A CLI tool's fixture-driven end-to-end test drives the built binary as a subprocess and is also inside the loop, for the same reason. The line is whether the test was written to constrain code that does not exist yet, or to verify a journey through code that already does.

## Why the distinction pays
When a rule says every behavior needs a test, and the suite in front of you contains a benchmark, an axe sweep and three snapshot files regenerated from output, the count looks healthy while the behavior itself has nothing specifying it. Reporting the two groups separately is what makes that visible.

The same split explains why mutation testing cannot settle whether a suite is good. Mutation proves a test is coupled to the code — which is exactly what a test written from finished code already is.

## Common Mistakes
- Counting E2E, VR and scan results as TDD coverage → The number rises while the behaviors stay unspecified
- Treating "it drives a browser" as the discriminator → Drupal Functional and FunctionalJavascript tiers are TDD tiers; Playwright journeys are not
- Regenerating a golden file from program output and calling it a test → The expectation now comes from the code, so it can never contradict it
- Reaching for an E2E test to drive a design decision → It cannot express one; the feedback arrives too late and too coarse to change a seam
- Skipping the outer disciplines because they are not TDD → They catch what unit tests structurally cannot

## See Also
- Previous: [Fixing Bugs with TDD](fixing-bugs-with-tdd.md) | Next: [When Not to Write a Test](when-not-to-write-a-test.md)
- Related: [Red-Green-Refactor Workflow](red-green-refactor.md) — the loop this defines the boundary of
- Related: [Testing Strategy — Choosing a Test Type](https://camoa.github.io/dev-guides/development/testing-strategy/choosing-a-test-type/) — picking the type once you know which loop you are in
- Related: [Testing Strategy — E2E Testing Concepts](https://camoa.github.io/dev-guides/development/testing-strategy/e2e-testing-concepts/) and [Visual Regression Concepts](https://camoa.github.io/dev-guides/development/testing-strategy/visual-regression-concepts/)
- Reference: Trail of Bits, [Mutation testing for the agentic era](https://blog.trailofbits.com/2026/04/01/mutation-testing-for-the-agentic-era/) (April 2026) — why killing a mutant proves a test is coupled to the implementation rather than conformant to a specification
