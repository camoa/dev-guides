---
description: Writing acceptance criteria in test plans — observable present-tense assertions the Generator maps to expect() calls.
tldr: Write each criterion as an observable present-tense state ("The success message is visible") — one fact per bullet, independently checkable. The Generator emits one expect() per bullet. A scenario with 7+ criteria probably contains multiple concerns; split it. Never write code or vague prose in criteria bullets.
---

# Acceptance Criteria

## When to Use

> Writing the "what should be true at the end" section of a scenario.

## Decision

| Count | When |
|---|---|
| 1–3 | Simple flows; tight focus |
| 4–6 | Typical |
| 7+ | Probably two scenarios — split |

A scenario with 10 expected results usually has multiple concerns smuggled in.

## Pattern: observable present-tense assertions

The phrasing that works for both humans and AI:

```markdown
**Expected results:**
- The success message "Thanks, we'll be in touch" is visible.
- The URL changes to `/contact/thank-you`.
- A new entry appears in the contact log within 5 seconds.
```

Each bullet is:
- **Observable** (a manual tester could verify)
- **Present-tense state** (not action)
- **Independently checkable** (Generator emits one `expect()` per bullet)

### Pattern: Given-When-Then mental model (without keywords)

Use the structure without writing the keywords explicitly:

- **Preconditions** section is the *Given*
- **Steps** section is the *When*
- **Expected results** section is the *Then*

Don't paste `Given/When/Then` literally unless you're committing to playwright-bdd or Cucumber — they become redundant with the section names.

## Anti-Patterns

| Bad | Why | Better |
|---|---|---|
| "It should work" | No observable | "The success message is visible" |
| "`expect(page.locator('.alert-success')).toBeVisible()`" | Already code — demote to Generator | "The success message is visible" |
| "Form succeeds without errors" | Negative without specificity | "No error toast is visible AND a confirmation toast is visible" |
| "User can proceed" | Non-observable | "The 'Continue' button becomes enabled" |
| "Performance is acceptable" | Non-functional, wrong tool | Use Lighthouse or performance traces, not E2E asserts |

## Common Mistakes

- **One mega-assertion** (`page.toMatchSnapshot()`) — hides what changed; use one bullet per fact
- **No expected results at all** on a "happy path" scenario — defaulting to "page loaded" misses the actual behavior
- **Expected results that overlap with steps** — if the step is "click submit," don't also assert "user clicked submit"

## See Also

- [Negative Assertions](ai-testgen-negative-assertions.md)
- [Test Plan Format](ai-testgen-plan-format.md)
- [Plan vs Code Boundary](ai-testgen-plan-vs-code.md)
