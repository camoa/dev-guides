---
description: "Credit system and AI contributions — who gets credit, credit abuse policy, what counts as genuine contribution, and how organizational credit applies"
tldr: "Use this when you need to understand how drupal.org credits work in the context of AI-assisted contributions, or when you have questions about credit attribution."
drupal_version: "11.x"
---

# Credit System

## When to Use

> When you need to understand how drupal.org credits work in the context of AI-assisted contributions, or when you have questions about credit attribution.

## Decision: Credit and AI

| Scenario | Who Gets Credit | Notes |
|---|---|---|
| You contributed AI-assisted code | You (the contributor) | Standard credit — AI tools don't get attributed in the credit system |
| Your organization sponsored the work | You + your organization | Standard organizational credit applies |
| AI generated the code, you submitted it | You | You take responsibility and credit |
| You submitted AI code without disclosure | Risk of credit revocation | Violates community trust and fair credit policy |

## Pattern: How Credits Work

Drupal.org tracks contributions via issue credits:
- **Issue credits** — When a maintainer commits code, contributors listed on the issue receive credit
- **Commit credits** — The committer (maintainer) gets credit for the commit
- **Organization credits** — Contributors can attribute their work to their employer/organization

Credits are public and visible on user profiles. They serve as reputation currency in the Drupal community.

## Pattern: Credit Abuse Policy

Drupal.org maintains a fair contribution credit system policy. Key points relevant to AI:

- Credits should reflect genuine human contribution to the project
- Submitting AI-generated code without disclosure to inflate credit counts violates the spirit of the system
- Gaming credits through mass AI-generated patches is considered abuse
- Maintainers may report suspected credit abuse

**What counts as genuine contribution with AI:**
- You identified the problem, guided the solution, reviewed the code, and verified correctness
- AI was a tool in your workflow, not a replacement for your expertise
- You can defend your contribution in review

## Common Mistakes

- **Thinking AI tools should be credited** — AI tools are tools, like an IDE or debugger. The human contributor receives credit.
- **Mass-submitting AI patches for credit** — This is credit abuse. Quality over quantity.
- **Not attributing your organization** — If your employer supports your AI-assisted contribution work, attribute them properly
- **Assuming more AI = less credit** — The credit is for the contribution, not the effort. A well-reviewed AI-assisted patch deserves the same credit as a manually written one.

## See Also

- [Drupal AI Policy](drupal-ai-policy.md) — policy context
- [Disclosure Checkboxes](disclosure-checkboxes.md) — proper disclosure
- [Merge Request Workflow](merge-request-workflow.md) — how contributions are submitted
- [Contribution Etiquette, RTBC & Credit](../contributing/contribution-etiquette-rtbc-credit.md) — how the Contribution Records system works in full (this guide covers the AI-specific angle only)
- Reference: [Fair credit policy](https://www.drupal.org/drupalorg/blog/ensuring-a-fair-drupal-contribution-credit-system)
