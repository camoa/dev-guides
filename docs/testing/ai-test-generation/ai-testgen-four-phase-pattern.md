---
description: The Plan → Review → Generate → Heal four-phase pattern — the spine of every AI test generation cycle.
tldr: "Every AI test generation cycle runs four phases: Plan (Planner agent writes a Markdown spec), Review (human approves), Generate (Generator writes code from the spec), Heal (Healer fixes locators when CI breaks). Never skip Plan or Review; the spec is the only artifact non-developers can review, and editing tests instead of the spec causes silent drift."
---

# The Four-Phase Pattern

## When to Use

> Use this pattern for every AI test generation cycle. It is the spine — not a shortcut for large tests.

## Decision

| Skip phase | When |
|---|---|
| Plan | Never — even a one-paragraph plan is better than no plan |
| Review | Never — without review, the loop has no spec |
| Generate | Sometimes — for very small additions, hand-write the test from the plan |
| Heal | Sometimes — for major UI rewrites, regenerate from the plan instead |

## Pattern

Artifacts in version control:

```
specs/                          # plans — human source of truth
├── contact-form.md
├── search.md
└── user-registration.md

tests/                          # generated code — regenerable from specs/
├── contact-form.spec.ts
├── search.spec.ts
├── user-registration.spec.ts
└── seed.spec.ts                # state bootstrap — handwritten

fixtures/                       # data fixtures referenced by plans + tests
├── users.ts
└── content.ts
```

Both `specs/` and `tests/` go to git. The spec is reviewable in PRs; the test is executable. The Healer modifies tests; humans modify specs.

### Why Split Into Four Phases

| Phase | What it protects against |
|---|---|
| Plan | Auto-generated tests no human ever reviewed at the intent level |
| Review | AI-encoded misinterpretations of what "correct" means |
| Generate | Plan-format chaos — Generator only works against plans that follow a schema |
| Heal | Tests that need rewriting on every UI tweak |

## Common Mistakes

- **Wrong**: Letting the Healer auto-commit → **Right**: every locator change should be human-approved or the suite drifts away from the plan
- **Wrong**: Editing tests, not the plan, when intent changes → **Right**: the plan is source of truth; next regeneration overwrites edits made to generated code
- **Wrong**: No plan stage at all → **Right**: the most common adoption failure — you lose the only artifact non-developers can review

## See Also

- [Overview](ai-testgen-overview.md)
- [Test Plan Format](ai-testgen-plan-format.md)
- [End-to-End Workflow](ai-testgen-end-to-end-workflow.md)
- [Playwright Test Agents](ai-testgen-playwright-test-agents.md)
