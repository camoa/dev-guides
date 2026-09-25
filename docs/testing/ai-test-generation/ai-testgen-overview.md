---
description: When AI test generation pays off — decision guide for choosing between generation, hand-writing, and deferring.
tldr: Use AI generation when backfilling coverage on an existing site or translating a user story into tests. Skip it when you can't articulate what "correct" looks like — the agent will pick a definition for you. Always go plan-first; code without a reviewed plan skips the only review gate a non-developer can use.
---

# AI Test Generation — Overview

## When to Use

> AI test generation pays off when:
>
> - The site already exists and you need broad coverage you don't have time to write by hand
> - A PR description / user story / Jira ticket already describes the desired behavior — let an agent translate it
> - You're triaging a regression and need a test that reproduces it quickly
> - Tests need to be re-generated when the UI changes substantially (plan stays, code regenerates)
>
> AI test generation is **not** a substitute for:
>
> - Writing the test plan yourself when intent is unclear — the AI will encode whatever it finds, which may be the bug
> - Reading the code review of a generated test — the Healer can't fix what wasn't right to begin with
> - Designing the test architecture (fixtures, helpers, page objects) — that's a human decision

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

- **Generating code directly from a prompt** without the plan stage — you skip the only review gate a non-developer can use
- **Treating AI tests as final on commit** — review every output as if a junior engineer wrote it, because that's what happened
- **Using AI generation when you can't articulate what "correct" looks like** — the agent will pick a definition for you, and it'll be wrong

## See Also

- [The Four-Phase Pattern](ai-testgen-four-phase-pattern.md)
- [Anti-Patterns](ai-testgen-anti-patterns.md)
- [Playwright (E2E)](../playwright/index.md)
- [Automated Testing Kit (ATK)](../atk/index.md)
- Related: [TDD & Spec-Driven Development](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — the general TDD cycle this specializes for generated E2E suites
