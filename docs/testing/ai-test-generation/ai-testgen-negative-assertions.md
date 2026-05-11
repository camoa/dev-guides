---
description: Negative assertions in test plans — the countermeasure to the encode-current-behavior gotcha where AI commits to existing bugs as expected behavior.
tldr: Include a "Negative checks" subsection in every scenario. The AI Planner encodes what it observes — if the site has a bug, the generated assertion enshrines it. Explicit negative checks (no error messages, no console errors, no unexpected redirects) force the Planner and reviewer to think about what should NOT happen, catching the bug before it ships as ground truth.
---

# Negative Assertions

## When to Use

> Include in every scenario. This is the countermeasure to the encode-current-behavior gotcha — the most common way AI-generated tests silently approve regressions.

## The Gotcha (Why This Section Exists)

AI test generation tools observe the site as it currently is. If the site has a bug — a broken empty state showing "Undefined", a 302 redirect that shouldn't happen, a cache-tag mistake producing stale content — the Planner sees that as "expected behavior" and writes an assertion encoding it.

Once committed, the assertion becomes ground truth. The suite passes on day one. The bug ships forever.

## Pattern: explicit "Negative checks" subsection

```markdown
#### 1.1 Submit valid contact message

**Steps:**
1. Navigate to `/contact`
2. Fill the form with valid values
3. Click "Send message"

**Expected results:**
- The success message is visible.
- One email appears in the Mailpit inbox.

**Negative checks:**
- No "error" class messages are visible on the result page.
- Browser console contains zero error-level messages during the flow.
- `watchdog` has no new PHP notices or warnings for this request.
- The submission does NOT appear in the public contact list.
```

## Pattern: boundary tables for input validation

```markdown
**Invalid inputs:**

| Input | Field | Expected error |
|---|---|---|
| empty | Name | "Name field is required" |
| `not-an-email` | Email | "Enter a valid email address" |
| 10,001 chars | Message | "Message must be 10000 characters or less" |
```

Tables diff cleanly in PRs; the Generator emits one parameterized test per row.

## Pattern: counter-scenarios as siblings

For every "happy path" scenario, include a sibling named `<scenario> — invalid input`:

```markdown
#### 1.1 Submit valid contact message
#### 1.2 Submit contact message — invalid email
#### 1.3 Submit contact message — empty required field
```

The sibling pattern surfaces coverage in the plan TOC. Reviewers see the negative cases without hunting.

## Common Mistakes

- **Wrong**: Skipping negative checks → **Right**: universal first-month failure; suite passes; bugs ship
- **Wrong**: Generic negatives ("no errors") → **Right**: specific observable — "No `.messages--error` regions are visible"
- **Wrong**: Mixing happy-path and negative in one scenario → **Right**: when it fails, you can't tell which path broke

## See Also

- [Acceptance Criteria](ai-testgen-acceptance-criteria.md)
- [Anti-Patterns](ai-testgen-anti-patterns.md)
- [Drupal & ATK Notes](ai-testgen-drupal-atk-notes.md) — Drupal-specific negative checks
