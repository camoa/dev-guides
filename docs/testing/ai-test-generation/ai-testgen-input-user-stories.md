---
description: Translating user stories, Jira tickets, and PRD excerpts into test plans — deterministic rewrite rules and scope-control patterns.
tldr: "Map \"As an X, I want Y so that Z\" to: Preconditions = X, scenario title = imperative \"X does Y\", first criterion = Z made observable. When pulling from Jira, extract Acceptance Criteria and Description only — tell the Planner explicitly not to add criteria from the comment thread or related tickets."
---

# Input: User Stories

## When to Use

> Translating Jira tickets, PRD excerpts, design docs, or Markdown user stories into test plans.

## Decision

| Input type | Key action |
|---|---|
| User story (`As an X...`) | Map each part to plan section (see Pattern below) |
| Jira epic with multiple stories | One H2 epic, one H3 per story, shared preconditions hoisted |
| PRD prose | Identify functional claims, convert each to observable criterion, surface ambiguities in Clarifications block |
| Ambiguous ticket | Add `## Clarifications needed` block at top of draft plan |

## Pattern: deterministic rewrite

```
As an X, I want Y so that Z
```

| Story part | Plan part |
|---|---|
| `As an X` | Preconditions: "Logged in as `<X>`" |
| `I want Y` | Scenario title (imperative): "X does Y" |
| `so that Z` | First acceptance criterion: "Z is observable as ..." |

## Pattern: multiple stories per input

If a single Jira epic contains five stories:
- One H2 epic in the plan
- One H3 scenario per story under the epic
- Shared preconditions hoisted to the plan level if they apply to all stories

## Pattern: extracting from Jira

Jira tickets contain noise (comments, status changes that become acceptance criteria, Slack-quote pastes). Tell the Planner explicitly:

```
Extract the Acceptance Criteria block and the Description only.
Do not generate criteria from the comment thread.
Do not add criteria I didn't list.
```

The "do not add criteria I didn't list" line prevents scope creep — a recurring failure mode where the AI invents requirements based on related tickets it can see.

## Pattern: from PRD excerpts

PRDs have prose, not enumerated AC. The Planner should:
1. Identify each functional claim in the prose
2. Convert each to an acceptance criterion (observable, present-tense)
3. Surface ambiguities as `## Clarifications needed` at the top of the plan

## Anti-Patterns

- **Pasting the whole Jira ticket with comments** — stale AC from comments override canonical AC
- **Translating "should be fast" literally** — non-functional criteria need different assertions (Lighthouse, performance traces), not E2E asserts
- **One scenario per user story regardless of size** — large stories split into multiple scenarios; sometimes one story = one epic

## Common Mistakes

- **No Clarifications block** when the story is ambiguous — Planner invents an interpretation; reviewer rubber-stamps it
- **Story title becomes plan title verbatim** without imperative rewriting — "User Login Story" instead of "User logs in"
- **Acceptance criteria copied as bullets without translation** — keeping "User should be able to log in" instead of "Logged-in user reaches dashboard"

## See Also

- [Input: Raw Prompt](ai-testgen-input-raw-prompt.md)
- [Hybrid Inputs](ai-testgen-hybrid-inputs.md)
- [Test Plan Format](ai-testgen-plan-format.md)
