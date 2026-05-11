---
description: Scoping test plans to a single flow, page, or viewport — three-constraint pattern and when narrow scope becomes a coverage gap.
tldr: A scope-narrow prompt expresses three things: feature ("password reset"), surface ("mobile viewport 375×667, iOS Safari"), and explicit exclusions ("do not test login after reset"). Viewport goes in Preconditions (becomes test.use), not in Steps. Always plan a sibling desktop scenario — targeting only mobile misses responsive issues.
---

# Targeted Scope

## When to Use

> Use this when you need a plan limited to a single flow, page, or viewport — "Test only the password reset flow on mobile."

## Decision

| Scope | When |
|---|---|
| One scenario, one viewport, one role | Tight — the focused case |
| One feature, all viewports, one role | Normal — most scope decisions |
| All features, one viewport | Too broad — make per-feature scope decisions |

## Pattern: three constraints

A scope-narrow prompt expresses:

1. **Feature** — "password reset"
2. **Surface** — "mobile viewport (375×667), iOS Safari user agent"
3. **Exclusions** — "do not test login after reset; do not test desktop"

## Pattern: viewport in Preconditions, not Steps

```markdown
## Preconditions

- Viewport: mobile (375×667)
- User agent: iOS Safari
- Anonymous visitor
- Email address exists in the system with username "ada@example.com"
```

Preconditions become `test.use({ viewport: ... })`. Steps become noisy with `setViewportSize` calls if you put surface there.

## Pattern: when the Planner should refuse or ask

- The feature isn't reachable from the seed test's state
- "Mobile" isn't specified (responsive CSS only? native app webview? PWA?)
- The surface implies tools not present (a native iOS test needs a different runner)

## Common Mistakes

- **Wrong**: "Test only X" without saying what to skip → **Right**: out-of-scope must be explicit; Generator extrapolates anyway
- **Wrong**: Surface constraint in the steps instead of Preconditions → **Right**: pollutes every step with viewport noise
- **Wrong**: Targeted scope that's also the only scope → **Right**: if you target mobile, plan a desktop scenario in a sibling spec

## See Also

- [Input: Raw Prompt](ai-testgen-input-raw-prompt.md)
- [Crawled Site](ai-testgen-crawled-site.md)
- [Test Plan Format](ai-testgen-plan-format.md)
