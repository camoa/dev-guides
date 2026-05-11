---
description: Generating test plans from raw developer prompts — clarifying-question patterns and the three failure modes to prevent.
tldr: Raw prompts ("test the checkout flow") produce over-broad crawls, hallucinated fields, and happy-path-only coverage. Prevent this by having the Planner ask five scoping questions before writing, or produce a draft plan with a "Clarifications needed" block. If scope can't be articulated, the Planner picks one representative happy path and one negative case — reviewer extends from there.
---

# Input: Raw Prompt

## When to Use

> Use this guide when a developer types a vague instruction ("Test the checkout flow") and needs to turn it into a bounded, reviewable plan.

## Decision

| Situation | Action |
|---|---|
| Harness allows interactive clarification | Planner asks five scoping questions before writing the plan |
| No interactive clarification available | Planner writes draft with `## Clarifications needed` block |
| Scope genuinely unknowable | Planner picks one happy path + one negative; reviewer extends |

### The Three Failure Modes

1. **Over-broad crawl** — Planner generates 40 scenarios, most low-value
2. **Hallucinated fields** — Planner invents features that don't exist
3. **Happy paths only** — no negative coverage

## Pattern: clarifying questions the Planner should ask

```
Before I write the plan, I need to confirm:

1. What is the entry URL for the flow?
2. Which user role should I assume (anonymous / customer / admin)?
3. What does "done" look like — order confirmation page, email,
   receipt download, all of the above?
4. Are there variants I should exclude — guest checkout, subscription
   products, gift cards?
5. What is out of scope — payment provider integration?
   tax calculation?
```

## Pattern: clarifications block

```markdown
# Checkout flow

## Clarifications needed

Before this plan is final, please confirm:
- Should the test cover the new Stripe Elements form or the legacy redirect?
- Is guest checkout in scope?
- Should I assume a single-item cart or multi-item?

## Draft scope

(Assumes Stripe Elements, registered customer, single-item cart.
If wrong, update the Clarifications block and regenerate.)
```

Reviewer answers the clarifications, regenerates, gets a real plan.

## Common Mistakes

- **Wrong**: Accepting "test everything" as scope → **Right**: produces unreviewable output; every plan needs explicit boundaries
- **Wrong**: Letting the Planner make up acceptance criteria from observed behavior without flagging → **Right**: encodes whatever happens to be there
- **Wrong**: Not surfacing assumptions in the draft → **Right**: reviewer can't tell what was decided vs invented

## See Also

- [Input: User Stories](ai-testgen-input-user-stories.md)
- [Hybrid Inputs](ai-testgen-hybrid-inputs.md)
- [Targeted Scope](ai-testgen-targeted-scope.md)
