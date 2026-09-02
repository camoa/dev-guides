---
description: "Pyramid vs. Trophy — choosing the right test shape for your stack to balance unit, integration, and E2E effort."
tldr: "Use the Pyramid (many unit tests) for logic-heavy backends and PHP/Drupal; use the Trophy (mostly integration) for React/Next.js frontends. The right shape is the one that catches the bugs your stack actually produces."
---

# Test Pyramid vs. Trophy

## When to Use

> When deciding how to allocate test effort across unit, integration, and E2E tests for a project or feature. The "shape" you choose determines your feedback speed, maintenance cost, and confidence level.

## Decision: Which Shape Fits Your Stack

| If your stack looks like... | Lean toward... | Rationale |
|---|---|---|
| Business logic-heavy backend (rules engines, financial, permissions) | Pyramid — many unit tests | Logic is verifiable in isolation; unit tests are cheap and comprehensive |
| Modern JS/TS frontend, React, Next.js | Trophy — mostly integration | Components are only meaningful in context; React Testing Library and Vitest make integration tests fast |
| Drupal (PHP modules, services, forms) | Pyramid with Kernel tests in the middle | PHPUnit Unit → Kernel → Functional matches the Drupal test type hierarchy |
| Distributed microservices / APIs | Pyramid + contract tests at boundaries | Service boundaries need contract coverage; unit tests handle internal logic |
| UI-heavy app (CMS, admin tools) | Trophy + selective VR | Interactions matter more than units; visual regression catches regressions unit tests miss |
| CLI tools, shell scripts, build tooling | Pyramid — extract logic into callable units | A script driven end to end can only be asserted on stdout and exit codes, which are not contracts; pull decisions into functions that return values |

## The Shapes

**Test Pyramid** (Mike Cohn, ~2009):
```
         [E2E]         ← few, slow, high confidence
        [INTEG.]       ← some, medium speed
    [UNIT / UNIT / UNIT] ← many, fast, low individual confidence
      [STATIC ANALYSIS]  ← free — linters, type checkers
```

- Maximize fast unit tests; minimize slow E2E tests
- Best fit: backend systems, pure business logic, languages where unit tests are cheap (Go, Python, PHP/Drupal)
- Risk: over-reliance on mocks at the unit layer creates tests that pass but don't reflect real behavior

**Testing Trophy** (Kent C. Dodds, 2018):
```
      [E2E]            ← some (more than pyramid)
    [INTEGRATION]      ← MOST — highest ROI tier
  [UNIT UNIT UNIT]     ← some (not majority)
  [STATIC ANALYSIS]    ← free foundation
```

- Integration tests give the best ROI: real component interactions, no full browser overhead
- Best fit: React/Next.js frontends, REST APIs tested at the HTTP layer, Node.js services
- "Write tests. Not too many. Mostly integration." — Kent C. Dodds
- Risk: integration tests are slower than unit tests; suite can become sluggish without discipline

**Choosing a ratio:**

Neither shape is universally correct. The right metric is: **what level of test catches the bugs that actually occur?** For frontend React apps, most bugs appear in component interactions, not isolated pure functions — so the Trophy fits. For a complex PHP tax-calculation library, most bugs appear in logic branches — so the Pyramid fits.

## Common Mistakes

- Copying the Pyramid shape blindly for all projects → Leads to massive mock-heavy unit suites that miss real integration bugs
- 100% unit, 0% integration → High confidence in components, zero confidence in whether they work together
- One giant E2E suite instead of a balanced pyramid → CI takes 30+ minutes; developers skip running it
- Conflating "more tests = better" with "right-shaped tests = better" → The shape matters as much as the count

## See Also

- ← Previous: [Testing Strategy Overview](testing-strategy-overview.md) | Next: [Unit Testing Concepts](unit-testing-concepts.md) →
- Related: [Unit Testing Concepts](unit-testing-concepts.md), [Integration Testing Concepts](integration-testing-concepts.md)
- Reference: Martin Fowler, [TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)
- Reference: Kent C. Dodds, [The Testing Trophy and Testing Classifications](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
