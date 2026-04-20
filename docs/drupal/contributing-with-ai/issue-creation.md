---
description: Creating drupal.org issues with AI disclosure — when to check which boxes, the full issue creation workflow, and what AI can and cannot reliably help with
tldr: "Use this when creating a new issue on drupal.org and AI tools were used in any part of the process — researching the problem, writing the summary, analyzing code, or drafting a patch."
drupal_version: "11.x"
---

# Issue Creation

## When to Use

> Use this when creating a new issue on drupal.org and AI tools were used in any part of the process — researching the problem, writing the summary, analyzing code, or drafting a patch.

## Decision

| Issue Activity | AI Involvement | Required Disclosure |
|---------------|----------------|---------------------|
| Researched the bug using AI | AI analyzed a backtrace or suggested cause | Check "AI Assisted Issue" |
| Drafted issue summary with AI | AI helped write the description | Check "AI Assisted Issue" |
| Created steps to reproduce with AI | AI suggested test scenarios | Check "AI Assisted Issue" |
| Attached a patch written with AI | AI generated or assisted with code | Check appropriate code checkbox too |
| No AI used in the issue | Entirely human-written | No AI checkboxes needed |

## Pattern

Issue creation workflow:
1. **Research the problem** — If AI helps analyze code, backtraces, or suggest root causes, note this for disclosure
2. **Write the issue title** — Clear, specific, descriptive. AI can help draft but you must verify accuracy
3. **Set metadata** — Component, priority, category, version. These must be accurate regardless of who researched them
4. **Write the description** — Problem statement, steps to reproduce, expected vs actual behavior. If AI drafted any part, disclose
5. **Check AI disclosure boxes** — Be honest about which parts AI helped with
6. **Verify steps to reproduce** — Even if AI drafted them, YOU must verify they actually reproduce the issue

| Good Use | Caution Required |
|----------|-----------------|
| Analyzing a backtrace to identify the failing component | AI may misidentify the root cause — verify |
| Drafting a clear issue summary from your notes | AI may add assumptions not in your notes — review |
| Suggesting related issues or documentation | AI may hallucinate issue numbers — verify every link |
| Helping format the issue with proper markdown | Low risk — still review |

## Common Mistakes

- **Wrong**: Submitting AI-drafted steps to reproduce without testing them → **Right**: Steps must actually work; AI frequently generates plausible but incorrect reproduction steps
- **Wrong**: Letting AI set the priority → **Right**: AI cannot assess ecosystem impact; set priority based on your understanding
- **Wrong**: Using AI-hallucinated issue numbers → **Right**: AI may reference issues that don't exist; verify every cross-reference
- **Wrong**: Forgetting to disclose AI involvement in issue text → **Right**: If AI helped write any part of the issue, check "AI Assisted Issue"

## See Also

- [Disclosure Checkboxes](disclosure-checkboxes.md)
- [Issue Review Guidelines](issue-review-guidelines.md)
- [Merge Request Workflow](merge-request-workflow.md)
- Reference: [Drupal issue workflow](https://www.drupal.org/docs/develop/issues)
