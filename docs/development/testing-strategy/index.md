---
description: Testing Strategy — stack-agnostic decisions for what to test, which test type to reach for, and how to build a balanced, maintainable suite.
guide-meta:
  concepts:
    - testing strategy
    - test pyramid
    - testing trophy
    - unit testing
    - integration testing
    - functional testing
    - e2e testing
    - end-to-end testing
    - visual regression testing
    - contract testing
    - API testing
    - performance testing
    - accessibility testing
    - a11y testing
    - test doubles
    - stub
    - mock
    - spy
    - fake
    - dummy
    - test structure
    - arrange act assert
    - AAA
    - given when then
    - flaky tests
    - test determinism
    - coverage philosophy
    - branch coverage
    - mutation testing
    - what to test
    - testing anti-patterns
    - FIRST properties
  not:
    - Drupal-specific test setup (see drupal/testing)
    - Playwright API usage (see testing/playwright)
    - ATK test catalog (see testing/atk)
    - AI test generation workflow (see testing/ai-test-generation)
    - visual regression tooling details (see testing/visual-regression)
    - TDD red-green-refactor workflow (see development/tdd-spec-driven)
  requires: []
  complements:
    - development/tdd-spec-driven
    - drupal/testing
    - drupal/tdd
    - testing/playwright
    - testing/visual-regression/workflow
    - testing/atk
    - testing/ai-test-generation
    - development/security-practices
  specializes: ""
  category: dev-practices
---

# Testing Strategy

| I need to... | Guide | Summary |
|---|---|---|
| Understand the cost/confidence/speed model and risk-based investment | [Testing Strategy Overview](testing-strategy-overview.md) | Testing is a cost/confidence tradeoff, not a boolean. Use risk-based investment — test money, auth, and complex logic heavily; test trivial code lightly. Goodhart's Law applies — coverage targets without quality enforcement catch nothing. |
| Choose between Pyramid and Trophy for my stack | [Test Pyramid vs. Trophy](test-pyramid-vs-trophy.md) | Use the Pyramid (many unit tests) for logic-heavy backends and PHP/Drupal; use the Trophy (mostly integration) for React/Next.js frontends. The right shape is the one that catches the bugs your stack actually produces. |
| Know what belongs in a unit test and the FIRST properties | [Unit Testing Concepts](unit-testing-concepts.md) | Unit tests verify one function or class in isolation — no DB, no HTTP, no filesystem. Apply FIRST properties (Fast, Isolated, Repeatable, Self-validating, Timely). Test observable behavior, not private details; one logical assertion per test. |
| Know what integration tests cover and where their boundaries sit | [Integration Testing Concepts](integration-testing-concepts.md) | Integration tests verify seams between components using a real test database and real internal implementations, stubbing only external third-party services. They deliver the highest ROI per test in most modern applications. |
| Know what functional/system tests cover vs. integration tests | [Functional Testing Concepts](functional-testing-concepts.md) | Functional tests verify feature behavior via HTTP or equivalent without a browser — real stack, real DB, no browser rendering engine. Use for permission enforcement, multi-step workflows, and feature regressions that integration tests cannot easily exercise. |
| Understand E2E tests: value, cost, and when to add them | [E2E Testing Concepts](e2e-testing-concepts.md) | E2E tests verify complete user journeys through a real browser — use them sparingly for critical paths only. 10–100x slower than integration tests; use data-testid selectors and never test logic variants in E2E. |
| Use visual regression testing without drowning in noise | [Visual Regression Concepts](visual-regression-concepts.md) | VR testing captures screenshots and diffs pixels against a baseline. Earns its keep for stable component libraries; adds friction when UI is still changing. Requires deterministic rendering — disable animations, pin browser versions. |
| Test API contracts and service boundaries | [Contract & API Testing Concepts](contract-api-testing-concepts.md) | Contract tests encode what a consumer expects from a provider, letting each deploy independently. Justified when different teams own consumer and provider; overkill for same-repo services. Schema validation via OpenAPI is a simpler alternative. |
| Test performance systematically without polluting unit tests | [Performance Testing Concepts](performance-testing-concepts.md) | Run performance tests in a dedicated CI stage on a stable environment, never in the unit suite. Set explicit budgets (P95 latency, Core Web Vitals) and enforce them. Always profile before optimizing. |
| Test accessibility — what automation covers and what it cannot | [Accessibility Testing Concepts](accessibility-testing-concepts.md) | Automated a11y tools catch ~35% of detectable WCAG issues. The rest requires manual keyboard navigation and screen reader testing. Add axe-playwright to E2E tests and jest-axe to component tests. |
| Choose the right test double: stub, mock, spy, fake, or dummy | [Test Doubles](test-doubles.md) | Use stubs to return controlled values, mocks to verify side effects occurred, fakes for realistic in-memory alternatives. Never mock your own internal code — mock only at the boundary (external services). |
| Structure tests for readability and one-assertion clarity | [Test Structure and Naming](test-structure-and-naming.md) | Structure every test as Arrange/Act/Assert with blank lines between phases — one Act per test. Name tests to describe scenario and expected outcome. Multiple asserts are fine if they verify facets of the same single outcome. |
| Fix or prevent flaky, non-deterministic tests | [Determinism and Flakiness](determinism-and-flakiness.md) | A suite with 5% flakiness has 99.9% chance of at least one failure per run. Root causes: time/date, randomness, shared state, async timing, real network. Fix by injecting clock/random dependencies and waiting for specific conditions rather than sleeping. |
| Use coverage metrics correctly without gaming the number | [Coverage Philosophy](coverage-philosophy.md) | Coverage tells you which lines were NOT executed, not whether tests verify correct behavior. Use branch coverage over line coverage. Mutation testing is the most reliable quality signal for critical modules. |
| Decide what is worth testing and what is not | [What to Test and What Not To](what-to-test-and-what-not.md) | Test observable behavior, not implementation details. High-risk code (auth, money, complex logic, API boundaries) deserves heavy investment; framework internals, trivial delegation, and generated code get none. |
| Identify and fix the most costly testing anti-patterns | [Best Practices and Anti-Patterns](best-practices-and-anti-patterns.md) | Tests are production code — apply the same review standards. Key anti-patterns: The Liar, The Mockery, The Sleeper, The Optimist. Every feature needs explicit security test cases for auth, permissions, and input handling. |
| Map any verification need to the right test type quickly | [Choosing a Test Type](choosing-a-test-type.md) | Master decision matrix mapping verification needs to test types. Most features need a combination: unit for logic, integration for seams, E2E for critical journeys only. Quick reference by stack included. |
