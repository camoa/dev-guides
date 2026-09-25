---
description: Markdown test plan format — the schema Playwright Test Agents emit and parse, with canonical section structure and detail-level rules.
tldr: "Plans use a specific Markdown hierarchy: H2 = epic/area, H3 = scenario group (test.describe), H4 = single test, numbered Steps, bulleted Expected results, bulleted Negative checks. Each section has a correct detail level — steps are behavioral actions, not selector instructions. Free-form prose breaks the Generator."
---

# Test Plan Format

## When to Use

> Authoring or reviewing a Markdown test plan.

## Two Anti-Patterns That Recur

- **Too vague** ("test the form works") — Generator invents its own success criteria; Healer can't distinguish regression from ambiguity
- **Too detailed / imperative** (selectors, literal copy, exact wait times) — every UI tweak forces a plan rewrite; defeats the regenerable-code premise

## Decision: The De Facto Schema

Playwright Test Agents emit and parse a specific Markdown shape. Heading hierarchy maps to test code:

| Markdown level | Maps to |
|---|---|
| `## Epic / Area` (H2) | Top-level grouping (file or `test.describe()`) |
| `### N. Scenario group` (H3) | `test.describe()` block |
| `#### N.M Specific test` (H4) | A single `test()` |
| `**Steps:**` numbered list | `test.step()` calls in order |
| `**Expected results:**` bullets | `expect()` assertions, one per bullet |
| `**Negative checks:**` bullets | `expect(...).not.X()` or `toHaveCount(0)` assertions |

### Detail Level by Section

| Section | Right level | Anti-pattern |
|---|---|---|
| Title | One scenario, one verb — "User submits contact form" | "Test contact form" (no scenario) |
| Preconditions | State only, not how to get there | Listing every Drush command |
| Steps | "Fill the Name field with a valid name" | "Type 'John' into `input[name=name]`" |
| Expected | One assertable fact per bullet | "Form works correctly" |
| Negative | Specific observable | "Nothing bad happens" |

## Pattern: Canonical Section Structure

For each scenario, in this order:

1. **Title** — one short imperative sentence
2. **Seed reference** — pointer to the seed test that bootstraps state
3. **Preconditions / Starting state** — what's true before the test runs
4. **Steps** — numbered, behavioral, 3–10 items
5. **Expected results** — bulleted, each independently checkable
6. **Negative checks** — bulleted, what should NOT happen
7. **Out-of-scope notes** — explicit exclusions

Plan-level header template:

```markdown
# Contact form — public submission flow

**Seed:** `tests/seed.drupal.spec.ts`
**Codebase under test:** `web/modules/custom/site_contact`
**Plan version:** 2026-05-11

## Scope

Anonymous user submits the default contact form at `/contact`,
receives confirmation, and the submission is logged.

## Out of scope

- Authenticated submissions (covered in `specs/contact-auth.md`)
- Email delivery (asserted only at queue level)
- Spam protection (Honeypot, reCAPTCHA) — separate plan
- Admin-side review UI
```

Plan-level scope is the contract. The Generator respects this header on regeneration.

## Common Mistakes

- **No version line in the header** — can't tell which plan was reviewed if multiple were drafted
- **Free-form prose without numbered steps** — Generator can't map prose to step calls
- **Plan that mixes happy-path and edge-case in the same scenario** — split into siblings

## See Also

- [Plan vs Code Boundary](ai-testgen-plan-vs-code.md)
- [Acceptance Criteria](ai-testgen-acceptance-criteria.md)
- [Negative Assertions](ai-testgen-negative-assertions.md)
- [The Four-Phase Pattern](ai-testgen-four-phase-pattern.md)
