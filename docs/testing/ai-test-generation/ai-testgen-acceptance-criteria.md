---
description: Writing acceptance criteria in test plans — observable present-tense assertions the Generator maps to expect() calls.
tldr: Write each criterion as an observable present-tense state ("The success message is visible") — one fact per bullet, independently checkable. The Generator emits one expect() per bullet. A scenario with 7+ criteria probably contains multiple concerns; split it. Never write code or vague prose in criteria bullets.
---

# Acceptance Criteria

## When to Use

> Use this guide when writing the "what should be true at the end" section of any scenario in a test plan.

## Decision

| Count | When |
|---|---|
| 1–3 | Simple flows; tight focus |
| 4–6 | Typical |
| 7+ | Probably two scenarios — split |

A scenario with 10 expected results usually has multiple concerns smuggled in.

## Pattern

Observable present-tense assertions:

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

### Given-When-Then mental model (without keywords)

- **Preconditions** section = Given
- **Steps** section = When
- **Expected results** section = Then

Don't write `Given/When/Then` literally unless committing to playwright-bdd or Cucumber.

## Common Mistakes

- **Wrong**: "It should work" → **Right**: "The success message is visible"
- **Wrong**: `` `expect(page.locator('.alert-success')).toBeVisible()` `` → **Right**: "The success message is visible" (that's already code — let the Generator write it)
- **Wrong**: "Form succeeds without errors" → **Right**: "No error toast is visible AND a confirmation toast is visible" (split into two bullets)
- **Wrong**: "User can proceed" → **Right**: "The 'Continue' button becomes enabled"
- **Wrong**: One mega-assertion (`page.toMatchSnapshot()`) → **Right**: one bullet per fact
- **Wrong**: No expected results on a "happy path" scenario → **Right**: every scenario has at least one assertable fact

## See Also

- [Negative Assertions](ai-testgen-negative-assertions.md)
- [Test Plan Format](ai-testgen-plan-format.md)
- [Plan vs Code Boundary](ai-testgen-plan-vs-code.md)
