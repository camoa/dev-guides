---
description: AI test generation anti-patterns — ranked list and the encode-current-behavior gotcha that causes AI tests to permanently enshrine bugs.
tldr: "The top anti-pattern is encode-current-behavior: the AI Planner observes the site as-is and asserts that bugs are expected behavior, causing the suite to pass forever while shipping the bug. Mitigations are mandatory plan review, negative assertions in every scenario, draft-only status until human edits, and Healer auto-commit disabled. The triple-review rule (plan intent, generated code, every Healer patch) applies without exception."
---

# Anti-Patterns

## The Big One: Encode-Current-Behavior

**AI-generated tests look like tests, but they encode the current behavior rather than the intended behavior — so they pass on day one and silently rubber-stamp regressions forever.**

A model crawling your site sees what *is*, not what *should be*. It will happily assert that a broken empty state shows "Undefined", that a 302 to `/user/login` is the "expected" response after submit, or that a Drupal cache-tag mistake produces stale content "as designed". Once committed, that assertion becomes ground truth and the suite can no longer detect the bug.

**Mitigations:**

1. Review the Planner's Markdown plan before code generation — that's the entire reason Playwright split planner from generator
2. Negative assertions in every scenario — see [Negative Assertions](ai-testgen-negative-assertions.md)
3. Treat AI output as a draft fixture, not a finished test — `*.draft.spec.ts`, exclude from CI until a human edits
4. Don't let the Healer auto-commit — every locator change reviewed

## Other Anti-Patterns (Ranked)

- **Wrong**: Skipping the plan stage and generating tests directly → **Right**: Plan → Review → Generate, every time
- **Wrong**: Letting the Healer modify assertions → **Right**: Healer fixes locators only; assertion changes mean plan changes
- **Wrong**: Treating an assertion change as a routine edit because it is small → **Right**: an assertion change is a contract change whoever makes it, and needs a recorded reason — see [Changing Existing Tests](https://camoa.github.io/dev-guides/development/tdd-spec-driven/changing-existing-tests/)
- **Wrong**: Editing tests after generation instead of editing the plan → **Right**: plan is source of truth; regenerate code
- **Wrong**: Putting selectors in plans → **Right**: plans stay behavioral
- **Wrong**: One mega-test asserting 20 things → **Right**: one scenario, one purpose; split
- **Wrong**: AI-generated tests with no negative assertions → **Right**: every plan has a Negative checks block
- **Wrong**: Crawling the whole site and generating a test per page → **Right**: scope explicit and narrower than input
- **Wrong**: No Clarifications block on ambiguous prompts → **Right**: surface unknowns; don't invent
- **Wrong**: Plan and code reviewed by the same person who wrote them → **Right**: separate reviewers, separate gates
- **Wrong**: AI as final reviewer → **Right**: human signs off on plan and code

## The Triple-Review Rule

Every AI test generation cycle has **three** mandatory review gates:

1. The plan (intent review)
2. The generated code (technical review)
3. Every Healer patch (drift review)

Skip any gate → the suite drifts away from the plan. Skip all three → you've outsourced your spec to whatever the AI happened to find.

## See Also

- [Negative Assertions](ai-testgen-negative-assertions.md)
- [The Four-Phase Pattern](ai-testgen-four-phase-pattern.md)
- [End-to-End Workflow](ai-testgen-end-to-end-workflow.md)
