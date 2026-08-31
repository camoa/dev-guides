---
description: When AI test generation pays off — decision guide for choosing between generation, hand-writing, and deferring.
tldr: Use AI generation when backfilling coverage on an existing site or translating a user story into tests. Skip it when you can't articulate what "correct" looks like — the agent will pick a definition for you. Always go plan-first; code without a reviewed plan skips the only review gate a non-developer can use.
---

# AI Test Generation — Overview

## When to Use

> Use AI test generation when the site exists, behavior is defined, and you need coverage you don't have time to write by hand. Do not use it when intent is unclear — the AI will encode whatever it finds, which may be the bug.

## Decision

| If you're... | Do this |
|---|---|
| Backfilling test coverage on an existing site | Use AI generation per flow, review each plan, commit |
| Doing TDD on a net-new feature | Write the plan yourself first; let AI generate the code from your plan |
| Reproducing a bug for a regression test | Describe the bug to the Planner; review the plan; generate |
| Maintaining a stable suite where UI changes | Let the Healer fix locators; review every change |
| Writing a test for behavior you can't articulate yet | Don't generate — figure out the intent first |

Reproduce-first is the general rule, not a Playwright one: write the failing test that demonstrates the bug before changing any production code, and add only that one. See [Fixing Bugs with TDD](https://camoa.github.io/dev-guides/development/tdd-spec-driven/fixing-bugs-with-tdd/).

## Pattern

```
Intent (user story / code / prompt)
     ↓
Planner agent
     ↓
Markdown test plan  ← HUMAN REVIEWS HERE
     ↓
Generator agent
     ↓
Playwright code     ← HUMAN REVIEWS HERE
     ↓
Runs in CI
     ↓ (when locators drift)
Healer agent
     ↓
Patched Playwright code  ← HUMAN REVIEWS HERE
```

Three review gates. Skipping any of them defeats the workflow.

## Common Mistakes

- **Wrong**: Generating code directly from a prompt without the plan stage → **Right**: plan first, every time — it's the only review gate a non-developer can use
- **Wrong**: Treating AI tests as final on commit → **Right**: review every output as if a junior engineer wrote it
- **Wrong**: Using AI generation when you can't articulate what "correct" looks like → **Right**: define intent first; then generate

## See Also

- [The Four-Phase Pattern](ai-testgen-four-phase-pattern.md)
- [Anti-Patterns](ai-testgen-anti-patterns.md)
- [Playwright (E2E)](../playwright/index.md)
- [Automated Testing Kit (ATK)](../atk/index.md)
- [TDD & Spec-Driven Development](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — the general TDD cycle this specializes for generated E2E suites
