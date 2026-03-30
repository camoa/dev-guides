---
description: Human review requirements for AI-generated code — what review IS vs IS NOT, minimum standards by disclosure level, and the six-question senior developer test
drupal_version: "11.x"
---

# Human Review Requirements

## When to Use

> Use this when you need to understand what "human review" actually means for AI-generated code — the minimum standard before you can honestly say you've reviewed the code.

## Decision

| Human Review IS | Human Review IS NOT |
|----------------|---------------------|
| Understanding the problem being solved | Running the code and seeing if it works |
| Reading every line and knowing why it's there | Scanning code quickly for obvious errors |
| Verifying API calls against Drupal documentation | Trusting AI's assertion that "this is correct" |
| Testing edge cases and error conditions | Running it once with test data |
| Questioning whether the approach is simplest | Accepting the first solution that works |
| Being able to defend every technical choice | Saying "the AI chose this approach" |

**Minimum review standard by disclosure level:**

| Disclosure Level | Minimum Review Standard |
|-----------------|------------------------|
| AI Assisted Code | Read all code, verify API usage, run tests, ensure you understand everything |
| AI Generated Code | All of the above + verify every API call exists, test edge cases thoroughly, question the approach |
| Vibe Coded | All of the above + consider rewriting from scratch; if you can't review at "AI Generated" level, don't submit |

## Pattern

The "Senior Developer" Test — ask these six questions:

1. **"What does this code do?"** — Explain in your own words, not the AI's words
2. **"Why this approach?"** — Know the alternatives and why this one was chosen
3. **"What happens if [input] is [edge case]?"** — Know the behavior for unexpected inputs
4. **"What would a malicious user try?"** — Consider security implications
5. **"Is there a simpler way?"** — AI frequently over-engineers; apply the "isn't CSS simpler?" test
6. **"What breaks if this code is wrong?"** — Understand the blast radius

If you can answer all six confidently, you've reviewed the code.

## Common Mistakes

- **Wrong**: Confusing "it works" with "it's correct" → **Right**: Working code can still create unnecessary technical debt and maintenance burden
- **Wrong**: Trusting AI's confidence → **Right**: AI presents solutions as "production ready" regardless of correctness; you must be the skeptic
- **Wrong**: Reviewing AI code less carefully than human code → **Right**: AI code deserves MORE scrutiny because it may contain subtle issues that look correct but aren't
- **Wrong**: Not starting fresh when confused → **Right**: If you've been going back and forth with AI and things aren't making sense, start a new session — context poisoning is real

## See Also

- [Supervised AI Workflow](supervised-ai-workflow.md)
- [AI Code Review Checklist](ai-code-review-checklist.md)
- [Issue Review Guidelines](issue-review-guidelines.md)
