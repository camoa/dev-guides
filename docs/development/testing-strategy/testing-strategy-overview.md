---
description: "Testing as an economics problem — how to balance speed, confidence, and cost to invest testing effort where it returns the most value."
tldr: "Testing is a cost/confidence tradeoff, not a boolean. Use risk-based investment — test money, auth, and complex logic heavily; test trivial code lightly. Goodhart's Law applies — coverage targets without quality enforcement catch nothing."
---

# Testing Strategy Overview

## When to Use

> Every time you start a new feature, plan a sprint, or evaluate a test suite. Testing is not a boolean (tested/untested) — it is an economics problem. Understanding the cost/speed/confidence model lets you invest testing effort where it returns the most value.

## The Three Levers

Every testing decision trades off three forces:

**Speed** — how fast the test runs and how fast the feedback arrives. A test run in 5 ms runs 1,000× during a workday. A test requiring a browser launch does not.

**Confidence** — how much the test tells you about real system behavior. A unit test verifies one function. An E2E test verifies the whole user journey. High confidence from a single test is expensive to obtain.

**Cost** — the total effort: write time, run time, maintenance burden, flakiness rate. Tests are not free. An unmaintained flaky test suite is worse than no suite at all — it trains developers to ignore failures.

The strategy decision is: **for this risk, at this stage, what is the minimum test investment that provides sufficient confidence?**

## Risk-Based Testing

Not all code carries the same risk. Test investment should track risk exposure:

| Risk category | Examples | Test investment |
|---|---|---|
| Money, permissions, auth | Payment logic, access checks, auth tokens | High: unit + integration + contract |
| Core user journeys | Checkout, login, content publish | Medium-high: integration + E2E for critical path |
| Complex business logic | Tax calculation, discount rules, state machines | High: unit (parameterized) + integration |
| UI rendering, styling | Component layout, CSS visual | Low-medium: unit or visual regression, not E2E |
| Configuration, trivial CRUD | Simple getters, config read | Low: spot-check; do not over-invest |
| Generated/framework code | ORM-generated queries, scaffolding | None: trust the generator; test your usage of it |

**Goodhart's Law applies to testing**: "When a measure becomes a target, it ceases to be a good measure." Coverage percentages, test counts, and pass rates are indicators — not goals. Optimizing for the indicator without managing the underlying risk produces test suites that look good and catch nothing.

## When to Test More, When to Test Less

Test more when:
- Code handles money, authentication, authorization, or PII
- Logic will be maintained by multiple developers over years
- Bugs in this area caused production incidents previously
- Requirements are complex with many edge cases

Test less (or differently) when:
- You are exploring — spike code, throw it away when it works
- The "tests" would just mirror the implementation
- UI is still in flux and visual design is changing weekly
- You are writing framework/infrastructure code that has its own test suite

## Common Mistakes

- Testing everything equally → Concentrates effort on trivial code while leaving risky logic under-tested
- No testing plan before coding starts → Tests get written post-hoc, test-for-coverage, or skipped
- Treating tests as overhead → Tests are the primary feedback mechanism; skipping them defers cost, never eliminates it
- Skipping tests under deadline pressure → Bugs found in production cost 5–10× more to fix than bugs found during development

## See Also

- Next: [Test Pyramid vs. Trophy](test-pyramid-vs-trophy.md)
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — TDD workflow that drives this strategy
- Reference: Google "Software Engineering at Google" Chapter 11 (Why Write Tests?) — Titus Winters et al. (2020)
