---
description: AI contribution overview — Drupal's disclose-and-verify position, the 4 disclosure levels, and how the community treats AI-assisted code
tldr: "Drupal's position is disclose-and-verify: AI is welcome with mandatory disclosure and the human contributor takes full responsibility. Four disclosure levels exist; the responsible path is AI Assisted Code with thorough human review."
drupal_version: "11.x"
---

# AI Contribution Overview

## When to Use

> Use this when you are about to contribute to any Drupal project using AI coding tools and need to understand the landscape, why disclosure matters, and how Drupal's "disclose and verify" position works.

## Decision

| Project | Position | Policy |
|---------|----------|--------|
| QEMU | Ban | AI-generated code prohibited entirely (June 2025, DCO rationale) |
| Gentoo | Ban | AI-generated code banned (April 2024, 6-0 council vote) |
| Linux kernel | Disclose | Co-developed-by trailer required, same review standards apply |
| Apache | Disclose | Generated-by convention, AI welcome with attribution |
| **Drupal** | **Disclose and verify** | **AI welcome with mandatory disclosure, human responsibility** |

## Pattern

Drupal's four disclosure levels:

| Level | Definition |
|-------|-----------|
| AI Assisted Issue | AI helped research or write the issue |
| AI Assisted Code | Human wrote code with AI suggestions, reviewed every line |
| AI Generated Code | AI generated substantial code, human reviewed and tested |
| Vibe Coded | AI generated most/all code with minimal human review |

The responsible path: **AI Assisted Code** with thorough human review.

Core principles:
1. **Disclosure is mandatory** — Issues and MRs must disclose AI involvement when AI generated a significant portion
2. **The human is responsible** — Contributor takes full responsibility regardless of how code was produced
3. **Review expectations scale with AI involvement** — Vibe Coded triggers maximum scrutiny
4. **Policy is adopted and codified** — Drupal has a published *Policy on the use of AI when contributing to Drupal* (last updated 2026-04-23); see [Drupal AI Policy](drupal-ai-policy.md)

## Common Mistakes

- **Wrong**: Not disclosing at all → **Right**: Even minor AI usage should be disclosed; when in doubt, disclose
- **Wrong**: Treating disclosure as optional → **Right**: Undisclosed AI usage erodes trust and may lead to credit revocation
- **Wrong**: Assuming "Vibe Coded" is acceptable → **Right**: Contributors who cannot explain their own code face maximum scrutiny and likely rejection
- **Wrong**: Confusing Drupal's openness with permissiveness → **Right**: "AI welcome" does not mean "anything goes" — quality standards are the same or higher

## See Also

- [Drupal AI Policy](drupal-ai-policy.md)
- [Disclosure Checkboxes](disclosure-checkboxes.md)
- [Industry Context](industry-context.md)
- [Supervised AI Workflow](supervised-ai-workflow.md)
- Reference: [Adopted AI policy](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/policy-on-the-use-of-ai-when-contributing-to-drupal)
