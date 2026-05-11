---
description: Plan vs code boundary — what belongs in the Markdown test plan versus what belongs in generated Playwright code.
tldr: Scenario intent, step lists, acceptance criteria, negative assertions, and field labels (user-facing) belong in the plan. CSS selectors, wait tactics, fixtures, and data construction belong in generated code or seed tests. Rule of thumb: if a manual tester could act on it by reading the rendered page, it goes in the plan.
---

# Plan vs Code Boundary

## When to Use

> Use this guide when deciding what belongs in the plan versus what belongs in the generated code — during authoring, review, or when a plan starts growing implementation details.

## Decision

| Concern | Belongs in | Why |
|---|---|---|
| Scenario intent ("user submits a valid form") | Plan | Reviewable by non-devs |
| Step list (numbered actions) | Plan | Reviewable; maps 1:1 to test code |
| Acceptance criteria ("success message visible") | Plan | Non-developer can confirm |
| Negative assertions ("no email sent on validation failure") | Plan | Crucial; non-devs must see them |
| Out-of-scope notes | Plan | Constraint on the Generator |
| Field labels ("Your name") | Plan | User-facing — change rarely; aids reviewers |
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

## Pattern

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

- **Wrong**: Putting selectors in plans → **Right**: plans stay behavioral; reviewers can't read selectors; Healer can't fix them when the plan overrides
- **Wrong**: Putting business logic in tests → **Right**: should be in fixtures or seed tests, not duplicated per scenario
- **Wrong**: Hardcoding literal copy in the plan → **Right**: one product-copy change breaks every plan

## See Also

- [Test Plan Format](ai-testgen-plan-format.md)
- [Acceptance Criteria](ai-testgen-acceptance-criteria.md)
- [Playwright Test Agents](ai-testgen-playwright-test-agents.md)
