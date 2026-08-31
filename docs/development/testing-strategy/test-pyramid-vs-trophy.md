---
description: Pyramid vs. Trophy — choosing the right test shape for your stack to balance unit, integration, and E2E effort.
tldr: Use the Pyramid (many unit tests) for logic-heavy backends and PHP/Drupal; use the Trophy (mostly integration) for React/Next.js frontends. The right shape is the one that catches the bugs your stack actually produces.
---

# Test Pyramid vs. Trophy

## When to Use

> Use the Pyramid when most bugs live in isolated logic. Use the Trophy when most bugs appear in component interactions. Neither is universally correct.

## Decision

| If your stack looks like... | Lean toward... | Rationale |
|---|---|---|
| Business logic-heavy backend (rules, financial, permissions) | Pyramid — many unit tests | Logic is verifiable in isolation; unit tests are cheap and comprehensive |
| Modern JS/TS frontend, React, Next.js | Trophy — mostly integration | Components are only meaningful in context; RTL + Vitest make integration tests fast |
| Drupal (PHP modules, services, forms) | Pyramid with Kernel tests in the middle | PHPUnit Unit → Kernel → Functional matches the Drupal test type hierarchy |
| Distributed microservices / APIs | Pyramid + contract tests at boundaries | Service boundaries need contract coverage; unit tests handle internal logic |
| UI-heavy app (CMS, admin tools) | Trophy + selective VR | Interactions matter more than units; visual regression catches regressions unit tests miss |
| CLI tools, shell scripts, build tooling | Pyramid — extract logic into callable units | A script driven end to end can only be asserted on stdout and exit codes, which are not contracts; pull decisions into functions that return values |

## Pattern

**Test Pyramid** (Mike Cohn, ~2009):
```
         [E2E]         ← few, slow, high confidence
        [INTEG.]       ← some, medium speed
    [UNIT / UNIT / UNIT] ← many, fast, low individual confidence
      [STATIC ANALYSIS]  ← free — linters, type checkers
```

**Testing Trophy** (Kent C. Dodds, 2018):
```
      [E2E]            ← some (more than pyramid)
    [INTEGRATION]      ← MOST — highest ROI tier
  [UNIT UNIT UNIT]     ← some (not majority)
  [STATIC ANALYSIS]    ← free foundation
```

The right metric: **what level of test catches the bugs that actually occur in your stack?**

## Common Mistakes

- **Wrong**: Copying the Pyramid shape blindly for all projects → **Right**: Evaluate where bugs actually occur in your stack
- **Wrong**: 100% unit, 0% integration → **Right**: High unit confidence + zero confidence in whether they work together is a false positive
- **Wrong**: One giant E2E suite instead of a balanced shape → **Right**: CI takes 30+ minutes; developers skip it
- **Wrong**: "More tests = better" → **Right**: Shape matters as much as count

## See Also

- [Testing Strategy Overview](testing-strategy-overview.md) | Next: [Unit Testing Concepts](unit-testing-concepts.md)
- Related: [Unit Testing Concepts](unit-testing-concepts.md), [Integration Testing Concepts](integration-testing-concepts.md)
- Reference: Martin Fowler, [TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)
- Reference: Kent C. Dodds, [The Testing Trophy and Testing Classifications](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
