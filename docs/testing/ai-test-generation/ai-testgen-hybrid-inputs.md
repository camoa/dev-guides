---
description: Combining multiple input modalities — precedence rule for when user story, code analysis, live exploration, and crawl conflict.
tldr: When inputs conflict, user-story constraints win (define what's in/out), code analysis fills vocabulary (exact labels, routes, required fields), live exploration validates (the rendered DOM is authoritative), and crawl only fills gaps inside scope. The Planner's job is reduction, not expansion — output that covers more surface than the input requested is a Planner failure.
---

# Hybrid Inputs

## When to Use

> Use this for realistic plan generation — most good plans benefit from multiple input sources combined with an explicit precedence rule.

## Decision

When inputs conflict, use this precedence (highest first):

1. **Scope / user-story constraints win** — define what's in/out
2. **Code analysis fills in vocabulary** — exact field labels, route paths, required fields
3. **Live exploration validates** — Planner opens the page to confirm the form matches what code suggests
4. **Crawl only fills gaps the user-story didn't cover** — and only inside scope

## Pattern: the unifying principle

**Scope must be explicit and narrower than the input.** The Planner's job is *reduction*, not expansion. If the output plan covers more surface than the input asked about, the Planner failed even if every scenario is individually well-written.

## Pattern: example hybrid prompt

```
Generate a test plan for the new contact form work tracked in JIRA-1234.

Inputs:
1. User story: web/specs/jira-1234.md (use as primary scope)
2. Code: web/modules/custom/site_contact/ (vocabulary only)
3. Existing style: specs/example-form.md (style reference)
4. Live URL: https://my-site.ddev.site/contact (validate)

Do NOT extrapolate beyond the story's acceptance criteria.
Do NOT add scenarios for related features visible in the codebase
but not in the story.

Out of scope: spam protection, admin review UI, email delivery
verification beyond queue insertion.
```

## Common Mistakes

- **Wrong**: No precedence rule → **Right**: code analysis discoveries silently expand scope past the user story
- **Wrong**: Live exploration without code analysis → **Right**: Planner uses imprecise field labels
- **Wrong**: Code analysis without live exploration → **Right**: Planner misses Ajax-added or `#states`-conditional fields

## See Also

- [Input: Code Analysis](ai-testgen-input-code.md)
- [Input: User Stories](ai-testgen-input-user-stories.md)
- [Crawled Site](ai-testgen-crawled-site.md)
- [Targeted Scope](ai-testgen-targeted-scope.md)
