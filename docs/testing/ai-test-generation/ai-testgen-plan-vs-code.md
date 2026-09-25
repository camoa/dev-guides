---
description: Plan vs code boundary — what belongs in the Markdown test plan versus what belongs in generated Playwright code.
tldr: "Scenario intent, step lists, acceptance criteria, negative assertions, and field labels (user-facing) belong in the plan. CSS selectors, wait tactics, fixtures, and data construction belong in generated code or seed tests. Rule of thumb: if a manual tester could act on it by reading the rendered page, it goes in the plan."
---

# Plan vs Code Boundary

## When to Use

> Deciding what belongs in the plan vs what belongs in the generated code.

## Decision

| Concern | Belongs in | Why |
|---|---|---|
| Scenario intent ("user submits a valid form") | Plan | Reviewable by non-devs |
| Step list (numbered actions) | Plan | Reviewable; maps 1:1 to test code |
| Acceptance criteria ("success message visible") | Plan | Non-developer can confirm |
| Negative assertions ("no email sent on validation failure") | Plan | Crucial; non-devs must see them |
| Out-of-scope notes | Plan | Constraint on the Generator |
| Field labels ("Your name") | Plan | These are user-facing — change rarely; expressing them aids reviewers |
| CSS selectors | Generated code | Implementation detail; Healer's job |
| Wait/timeout tactics | Generated code | Playwright handles via web-first assertions |
| Test helpers / fixtures | Code | Reusable across tests; plan references by name |
| Data construction (`drush user:create`) | Seed test or fixture loader | Procedural; plan just names what's needed |

### Selector Hints — The Gray Zone

| Selector hint | Plan or code? |
|---|---|
| Accessible name ("Click the 'Submit' button") | **Plan** — this is behavior |
| Disambiguator ("the 'Delete' button in the row for 'Test Article'") | **Plan** — behavior |
| CSS class (`.btn-primary`) | Code — implementation |
| Test ID (`data-testid`) | Gray — only put in plan if the design team owns the contract |

Rule of thumb: if a manual tester could act on the hint by reading the rendered page, it belongs in the plan.

## Pattern: behavioral language

```markdown
<!-- Good — plan stays behavioral -->
**Steps:**
1. Click the "Send message" button

<!-- Bad — selector in plan -->
**Steps:**
1. Click `button.btn-primary[type="submit"]`
```

The Generator handles selector derivation. If the plan locks in a selector, the Healer has to fight the plan instead of the test.

## Common Mistakes

- **Putting selectors in plans** — turns plans into code; reviewers can't read; Healer can't fix
- **Putting business logic in tests** — should be in fixtures or seed tests, not duplicated per scenario
- **Hardcoding literal copy in the plan** — locks in current strings; one product-copy change breaks every plan

## See Also

- [Test Plan Format](ai-testgen-plan-format.md)
- [Acceptance Criteria](ai-testgen-acceptance-criteria.md)
- [Playwright Test Agents](ai-testgen-playwright-test-agents.md)
