---
description: "Issue review guidelines for AI-flagged contributions — review depth by disclosure level, red flags for AI-generated patches, and how to evaluate contributor understanding"
tldr: "Use this when you are reviewing an AI-flagged issue, or when you want to understand how your AI-assisted contribution will be evaluated by maintainers."
drupal_version: "11.x"
---

# Issue Review Guidelines

## When to Use

> When you are reviewing an AI-flagged issue, or when you want to understand how your AI-assisted contribution will be evaluated by maintainers.

## Decision: Review Depth by Disclosure Level

| Disclosure Level | Review Approach | Time Estimate |
|---|---|---|
| AI Assisted Issue (text only) | Normal review — evaluate issue quality, not AI usage | Standard |
| AI Assisted Code | Normal code review — assume contributor understands the code | Standard |
| AI Generated Code | Enhanced review — probe understanding, test edge cases, verify API correctness | 1.5-2x standard |
| Vibe Coded | Full audit — question every line, verify contributor can explain choices, consider rejection | 2-3x standard |

## Pattern: What Reviewers Look For

**Understanding of the problem:**
- Can the contributor explain what the bug is and why the fix works?
- Does the issue demonstrate understanding beyond "AI told me"?
- Are the steps to reproduce verified and accurate?

**Code quality signals:**
- Does the code follow Drupal coding standards?
- Are the right APIs used for the Drupal version?
- Is dependency injection used where appropriate?
- Are there access checks where needed?
- Is output properly sanitized?

**Red flags for AI-generated patches:**
1. **Contributor can't explain their own patch** — Asked a question about the code and they don't know the answer
2. **Tests only cover happy path** — No edge cases, error conditions, or boundary testing
3. **Code uses non-existent APIs** — Hallucinated function names, service names, or method signatures
4. **Over-engineered solution** — Complex abstraction where a simple approach would suffice
5. **Style inconsistencies** — Mix of coding styles suggesting copy-paste from AI without review

## Pattern: Reviewer Guidance (#3569240)

From the AI module project's review guidelines:
- Treat AI-flagged contributions with appropriate scrutiny, not hostility
- Ask contributors to explain their technical choices
- If in doubt about code understanding, ask specific questions about implementation details
- Consider requiring additional test coverage for AI-generated code
- Document your review concerns in the issue for transparency

## Common Mistakes

- **Rejecting solely because AI was used** — Drupal's policy is disclose-and-verify, not ban. Judge the code quality.
- **Skipping review because "it's just AI Assisted"** — All code gets reviewed. The disclosure level affects depth, not whether review happens.
- **Not asking the contributor to explain** — The simplest test: "Why did you choose this approach?" If they can't answer, the contribution needs more work.
- **Timeboxing vibe-coded patches generously** — If a vibe-coded patch would take longer to review than to rewrite, it may be more efficient to close and rewrite

## See Also

- [Drupal AI Policy](drupal-ai-policy.md) — policy context for review
- [AI Code Review Checklist](ai-code-review-checklist.md) — checklist for contributors before submission
- [Human Review Requirements](human-review-requirements.md) — what thorough review means
- [Contribution Etiquette, RTBC & Credit](../contributing/contribution-etiquette-rtbc-credit.md) — RTBC discipline and general review etiquette (this guide covers the AI-specific angle only)
- Reference: [#3569240 AI Issue Review Guidelines](https://www.drupal.org/project/ai/issues/3569240)
