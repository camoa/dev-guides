---
description: Issue review guidelines for AI-flagged contributions — review depth by disclosure level, red flags for AI-generated patches, and how to evaluate contributor understanding
drupal_version: "11.x"
---

# Issue Review Guidelines

## When to Use

> Use this when you are reviewing an AI-flagged issue, or when you want to understand how your AI-assisted contribution will be evaluated by maintainers.

## Decision

| Disclosure Level | Review Approach | Time Estimate |
|-----------------|----------------|---------------|
| AI Assisted Issue (text only) | Normal review — evaluate issue quality, not AI usage | Standard |
| AI Assisted Code | Normal code review — assume contributor understands the code | Standard |
| AI Generated Code | Enhanced review — probe understanding, test edge cases, verify API correctness | 1.5-2x standard |
| Vibe Coded | Full audit — question every line, verify contributor can explain choices, consider rejection | 2-3x standard |

## Pattern

**What reviewers look for:**

Understanding of the problem:
- Can the contributor explain what the bug is and why the fix works?
- Does the issue demonstrate understanding beyond "AI told me"?
- Are the steps to reproduce verified and accurate?

**Red flags for AI-generated patches:**
1. Contributor can't explain their own patch
2. Tests only cover happy path — no edge cases or error conditions
3. Code uses non-existent APIs — hallucinated function names or method signatures
4. Over-engineered solution — complex abstraction where a simple approach would suffice
5. Style inconsistencies — mix of coding styles suggesting copy-paste from AI without review

**Reviewer guidance (from #3569240):**
- Treat AI-flagged contributions with appropriate scrutiny, not hostility
- Ask contributors to explain their technical choices
- If in doubt about code understanding, ask specific questions about implementation details
- Consider requiring additional test coverage for AI-generated code
- Document your review concerns in the issue for transparency

## Common Mistakes

- **Wrong**: Rejecting solely because AI was used → **Right**: Drupal's policy is disclose-and-verify, not ban; judge the code quality
- **Wrong**: Skipping review because "it's just AI Assisted" → **Right**: All code gets reviewed; the disclosure level affects depth, not whether review happens
- **Wrong**: Not asking the contributor to explain → **Right**: The simplest test: "Why did you choose this approach?" If they can't answer, the contribution needs more work
- **Wrong**: Being generous with vibe-coded patches → **Right**: If a vibe-coded patch would take longer to review than to rewrite, close and rewrite

## See Also

- [Drupal AI Policy](drupal-ai-policy.md)
- [AI Code Review Checklist](ai-code-review-checklist.md)
- [Human Review Requirements](human-review-requirements.md)
- Reference: [#3569240 AI Issue Review Guidelines](https://www.drupal.org/project/ai/issues/3569240)
