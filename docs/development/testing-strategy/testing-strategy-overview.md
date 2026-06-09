---
description: Testing as an economics problem — how to balance speed, confidence, and cost to invest testing effort where it returns the most value.
tldr: Testing is a cost/confidence tradeoff, not a boolean. Use risk-based investment — test money, auth, and complex logic heavily; test trivial code lightly. Goodhart's Law applies — coverage targets without quality enforcement catch nothing.
---

# Testing Strategy Overview

## When to Use

> Use this decision model every time you start a new feature, plan a sprint, or evaluate a test suite. Testing is an economics problem, not a checkbox.

## Decision

| Risk category | Examples | Test investment |
|---|---|---|
| Money, permissions, auth | Payment logic, access checks, auth tokens | High: unit + integration + contract |
| Core user journeys | Checkout, login, content publish | Medium-high: integration + E2E for critical path |
| Complex business logic | Tax calculation, discount rules, state machines | High: unit (parameterized) + integration |
| UI rendering, styling | Component layout, CSS visual | Low-medium: unit or visual regression, not E2E |
| Configuration, trivial CRUD | Simple getters, config read | Low: spot-check; do not over-invest |
| Generated/framework code | ORM-generated queries, scaffolding | None: trust the generator; test your usage of it |

## Pattern

The three levers every testing decision trades off:

- **Speed** — how fast the test runs. A test in 5 ms runs 1,000× during a workday. A browser launch does not.
- **Confidence** — how much the test tells you about real behavior. A unit test verifies one function. An E2E test verifies the whole journey.
- **Cost** — write time + run time + maintenance burden + flakiness rate. An unmaintained flaky suite is worse than no suite.

The strategy decision: **for this risk, at this stage, what is the minimum test investment that provides sufficient confidence?**

## Common Mistakes

- **Wrong**: Testing everything equally → **Right**: Concentrate effort on high-risk code (auth, money, complex logic)
- **Wrong**: Writing tests post-hoc, test-for-coverage → **Right**: Plan test strategy before coding starts
- **Wrong**: Treating tests as overhead → **Right**: Tests are the primary feedback mechanism; skipping defers cost, never eliminates it
- **Wrong**: Skipping tests under deadline pressure → **Right**: Bugs found in production cost 5–10× more to fix than bugs found during development

## See Also

- Next: [Test Pyramid vs. Trophy](test-pyramid-vs-trophy.md)
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — TDD workflow that drives this strategy
- Reference: Titus Winters et al., "Software Engineering at Google" Ch. 11 (Why Write Tests?)
