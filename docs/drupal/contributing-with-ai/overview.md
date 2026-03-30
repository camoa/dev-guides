---
description: AI contribution overview — Drupal's disclose-and-verify position, the 4 disclosure levels, and how the community treats AI-assisted code
drupal_version: "11.x"
---

# AI Contribution Overview

## When to Use

> Read this first. It maps the landscape of AI contribution policies, why disclosure matters, and how Drupal's "disclose and verify" position works before you touch any issue or merge request.

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
1. Disclosure is mandatory — every issue and MR must indicate AI involvement
2. The human is responsible — contributor takes full responsibility regardless of how code was produced
3. Review expectations scale with AI involvement — Vibe Coded triggers maximum scrutiny
4. Policy is evolving — check drupal.org for the latest governance decisions

## Common Mistakes

- **Wrong**: Not disclosing at all → **Right**: Even minor AI usage (autocomplete) should be disclosed; when in doubt, disclose
- **Wrong**: Treating disclosure as optional → **Right**: Undisclosed AI usage erodes trust and may lead to credit revocation
- **Wrong**: Assuming "Vibe Coded" is acceptable → **Right**: Contributors who cannot explain their own code face maximum scrutiny and likely rejection
- **Wrong**: Confusing Drupal's openness with permissiveness → **Right**: "AI welcome" does not mean "anything goes" — quality standards are the same or higher

## See Also

- [Drupal AI Policy](drupal-ai-policy.md)
- [Disclosure Checkboxes](disclosure-checkboxes.md)
- [Industry Context](industry-context.md)
- [Supervised AI Workflow](supervised-ai-workflow.md)
- Reference: [drupal.org governance issue #3565917](https://www.drupal.org/project/governance/issues/3565917)
