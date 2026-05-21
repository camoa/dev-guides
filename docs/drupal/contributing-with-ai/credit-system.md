---
description: Credit system and AI contributions — who gets credit, credit abuse policy, what counts as genuine contribution, and how organizational credit applies
tldr: "Use this when you need to understand how drupal.org credits work in the context of AI-assisted contributions, or when you have questions about credit attribution."
drupal_version: "11.x"
---

# Credit System

## When to Use

> Use this when you need to understand how drupal.org credits work in the context of AI-assisted contributions, or when you have questions about credit attribution.

## Decision

| Scenario | Who Gets Credit | Notes |
|----------|----------------|-------|
| You contributed AI-assisted code | You (the contributor) | Standard credit — AI tools don't get attributed in the credit system |
| Your organization sponsored the work | You + your organization | Standard organizational credit applies |
| AI generated the code, you submitted it | You | You take responsibility and credit |
| You submitted AI code without disclosure | Risk of credit revocation | Violates community trust and fair credit policy |

## Pattern

Drupal.org tracks contributions via issue credits:
- **Issue credits** — When a maintainer commits code, contributors listed on the issue receive credit
- **Commit credits** — The committer (maintainer) gets credit for the commit
- **Organization credits** — Contributors can attribute their work to their employer/organization

Credits are public, visible on user profiles, and serve as reputation currency in the Drupal community.

**What counts as genuine contribution with AI:**
- You identified the problem, guided the solution, reviewed the code, and verified correctness
- AI was a tool in your workflow, not a replacement for your expertise
- You can defend your contribution in review

**Credit abuse:** Submitting AI-generated code without disclosure to inflate credit counts violates the spirit of the system. Mass AI-generated patches for credit gaming is reportable abuse.

## Common Mistakes

- **Wrong**: Thinking AI tools should be credited → **Right**: AI tools are tools, like an IDE or debugger; the human contributor receives credit
- **Wrong**: Mass-submitting AI patches for credit → **Right**: Quality over quantity — this is credit abuse
- **Wrong**: Not attributing your organization → **Right**: If your employer supports your AI-assisted contribution work, attribute them properly
- **Wrong**: Assuming more AI involvement means less credit → **Right**: The credit is for the contribution, not the effort; a well-reviewed AI-assisted patch deserves the same credit as a manually written one

## See Also

- [Drupal AI Policy](drupal-ai-policy.md)
- [Disclosure Checkboxes](disclosure-checkboxes.md)
- [Merge Request Workflow](merge-request-workflow.md)
- [Contribution Etiquette, RTBC & Credit](../contributing/contribution-etiquette-rtbc-credit.md) — how the Contribution Records system works in full (this guide covers the AI-specific angle only)
- Reference: [Fair credit policy](https://www.drupal.org/drupalorg/blog/ensuring-a-fair-drupal-contribution-credit-system)
