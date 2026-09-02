---
description: "Human review requirements for AI-generated code — what review IS vs IS NOT, minimum standards by disclosure level, and the six-question senior developer test"
tldr: "Use this when you need to understand what \"human review\" actually means for AI-generated code — the minimum standard before you can honestly say you've reviewed the code."
drupal_version: "11.x"
---

# Human Review Requirements

## When to Use

> When you need to understand what "human review" actually means for AI-generated code — the minimum standard before you can honestly say you've reviewed the code.

## Decision: What Review IS vs IS NOT

| Human Review IS | Human Review IS NOT |
|---|---|
| Understanding the problem being solved | Running the code and seeing if it works |
| Reading every line and knowing why it's there | Scanning code quickly for obvious errors |
| Verifying API calls against Drupal documentation | Trusting AI's assertion that "this is correct" |
| Testing edge cases and error conditions | Running it once with test data |
| Questioning whether the approach is simplest | Accepting the first solution that works |
| Being able to defend every technical choice | Saying "the AI chose this approach" |

## Decision: Review Depth by Disclosure Level

| Disclosure Level | Minimum Review Standard |
|---|---|
| AI Assisted Code | Read all code, verify API usage, run tests, ensure you understand everything |
| AI Generated Code | All of the above + verify every API call exists, test edge cases thoroughly, question the approach |
| Vibe Coded | All of the above + consider rewriting from scratch with understanding. If you can't review at the "AI Generated" level, don't submit. |

## Pattern: The "Senior Developer" Test

Ask yourself these questions about the code:

1. **"What does this code do?"** — You should be able to explain in your own words, not the AI's words
2. **"Why this approach?"** — You should know the alternatives and why this one was chosen
3. **"What happens if [input] is [edge case]?"** — You should know the behavior for unexpected inputs
4. **"What would a malicious user try?"** — You should have considered security implications
5. **"Is there a simpler way?"** — The AI frequently over-engineers. Apply the "isn't CSS simpler?" test
6. **"What breaks if this code is wrong?"** — You should understand the blast radius

If you can answer all six confidently, you've reviewed the code.

## Common Mistakes

- **Confusing "it works" with "it's correct"** — All three solutions in the laollita.es example worked. Only one was right. Working code can still create unnecessary technical debt and maintenance burden.
- **Trusting AI's confidence** — AI presents solutions as "production ready" or "this is done, perfect!" It never says "I'm confused, maybe we should start over." You must be the skeptic.
- **Reviewing AI code less carefully than human code** — AI code deserves MORE scrutiny because it may contain subtle issues that look correct but aren't (hallucinated APIs, deprecated patterns, unnecessary complexity)
- **Not starting fresh when confused** — If you've been going back and forth with AI and things aren't making sense, start a new session. Context poisoning is real.

## See Also

- [Supervised AI Workflow](supervised-ai-workflow.md) — why these review standards matter
- [AI Code Review Checklist](ai-code-review-checklist.md) — actionable checklist
- [Issue Review Guidelines](issue-review-guidelines.md) — how maintainers apply these standards
