---
description: "AI contribution overview — Drupal's disclose-and-verify position, the 4 disclosure levels, and how the community treats AI-assisted code"
tldr: "Drupal's position is disclose-and-verify: AI is welcome with mandatory disclosure and the human contributor takes full responsibility. Four disclosure levels exist; the responsible path is AI Assisted Code with thorough human review."
drupal_version: "11.x"
---

# AI Contribution Overview

## When to Use

> When you are about to contribute to any Drupal project (core, contrib, or custom) using AI coding tools and need to understand the landscape of AI contribution policies, why disclosure matters, and how the Drupal community approaches this.

## Decision: Where Does Drupal Stand?

| Project | Position | Policy |
|---|---|---|
| QEMU | Ban | AI-generated code prohibited entirely (June 2025, DCO rationale) |
| Gentoo | Ban | AI-generated code banned (April 2024, 6-0 council vote) |
| Linux kernel | Disclose | Co-developed-by trailer required, same review standards apply |
| Apache | Disclose | Generated-by convention, AI welcome with attribution |
| **Drupal** | **Disclose and verify** | **AI welcome with mandatory disclosure, human responsibility** |

## Pattern: Drupal's "Disclose and Verify" Position

Drupal does not ban AI tools. It requires transparency. The core principles:

1. **Disclosure is mandatory** — Issues and merge requests must disclose AI involvement when AI generated a significant portion of the work
2. **The human is responsible** — Regardless of how code was produced, the contributor takes full responsibility for quality, correctness, and security
3. **Review expectations scale with AI involvement** — "AI Assisted Code" gets normal review; "Vibe Coded" triggers maximum scrutiny
4. **Policy is adopted and codified** — Drupal has a published *Policy on the use of AI when contributing to Drupal* (last updated 2026-04-23); see [Drupal AI Policy](drupal-ai-policy.md) for the rules

Drupal.org provides 4 disclosure levels on the issue template:
- **AI Assisted Issue** — AI helped research or write the issue
- **AI Assisted Code** — Human wrote code with AI suggestions, reviewed every line
- **AI Generated Code** — AI generated substantial code, human reviewed and tested
- **Vibe Coded** — AI generated most/all code with minimal human review

The responsible path: **AI Assisted Code** with thorough human review.

## Common Mistakes

- **Not disclosing at all** — Even minor AI usage (autocomplete, suggestions) should be disclosed. When in doubt, disclose.
- **Treating disclosure as optional** — The community expects honesty. Undisclosed AI usage erodes trust and may lead to credit revocation.
- **Assuming "Vibe Coded" is acceptable** — Contributors who cannot explain their own code face maximum scrutiny and likely rejection.
- **Confusing Drupal's openness with permissiveness** — "AI welcome" does not mean "anything goes." Quality standards are the same or higher for AI contributions.

## See Also

- [Drupal AI Policy](drupal-ai-policy.md) — adopted policy rules and enforcement
- [Disclosure Checkboxes](disclosure-checkboxes.md) — when to check each box
- [Industry Context](industry-context.md) — how other projects handle this
- [Supervised AI Workflow](supervised-ai-workflow.md) — why supervision matters
- Reference: [Adopted AI policy](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/policy-on-the-use-of-ai-when-contributing-to-drupal)
