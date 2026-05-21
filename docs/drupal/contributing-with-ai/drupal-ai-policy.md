---
description: Drupal AI policy — the adopted drupal.org AI contribution rules, enforcement escalation, what remains open, and what the policy does NOT cover
tldr: "The adopted Policy on the use of AI when contributing to Drupal (last updated 2026-04-23) is live and enforced. Core rules: full contributor responsibility, disclose significant AI use, verify all output, fix problems before submitting. Copyright/licensing is the one unresolved area."
drupal_version: "11.x"
---

# Drupal AI Policy

## When to Use

> Use this when you need to understand the rules in Drupal's adopted AI contribution policy, how enforcement works, and what areas remain open. This policy applies uniformly to core and contrib.

## Decision

| Rule | Detail |
|------|--------|
| **Full responsibility** | "You are fully responsible for the integrity of your submission." "The AI wrote it" is not a defense. |
| **Understand before submitting** | Read and understand prior issue discussion before adding AI-generated code or comments. |
| **Disclose significant AI use** | Required when AI generated a *significant* portion — whole functions, classes, architectural scaffolding, or extensive documentation blocks. |
| **Review and verify all AI output** | Thoroughly verify all dependencies, logic, and security implications. Submitting failing checks for others to fix is unacceptable. |
| **Fix problems before submitting** | Do not post code without reading prior discussion; do not abandon an issue after requesting feedback. |
| **Engage collaboratively** | Do not propose rewrites without engaging existing contributors; do not add AI-generated code to others' work without permission and disclosure. |
| **Copyright/GPL** | The contributor alone bears responsibility that AI-generated code violates no third-party copyright and is GPL-compatible. |

## Pattern: Unacceptable Practices

The policy explicitly names these as violations:
- Posting bulk AI output without reading what has already been discussed
- Submitting MRs with failing automated checks for others to fix
- Adding AI-generated code to someone else's MR without their permission and disclosure
- Abandoning an issue after requesting and receiving feedback
- Posting unreviewed AI-generated comments/reviews/summaries as your own words
- Ignoring architectural conclusions that prior discussion already reached

## Pattern: Enforcement Escalation

Enforcement is a three-tier escalation — not immediate bans:
1. **Education first** — Explain the policy; help the contributor correct the problem
2. **Temporary ban** — For repeated violations after education
3. **Permanent ban** — For clear disregard for the policy or disrespect toward maintainers

No automated detection tools exist. Enforcement is community-driven and reputation-based.

## Pattern: What Remains Open

| Area | Status |
|------|--------|
| **Copyright / licensing** | **Unresolved** — GPL + AI training-data is an industry-wide open question; Drupal defers it. The contributor bears responsibility, but no court precedent exists. |
| Maintainer review checklist (#3569240) | **In progress** — reviewer guidance from the AI module project |
| `ai_best_practices` Drupal project | **Pre-MVP** — will become the canonical Drupal AI guidance; watch it, don't depend on it yet |

**Historical note:** Governance issue #3565917 is "Postponed (maintainer needs more info)" — stalled specifically over copyright/licensing. The *adopted policy* at the URL below is the live rule; #3565917 is not it.

## Common Mistakes

- **Wrong**: Treating #3565917 as the live policy → **Right**: That issue is Postponed. The adopted policy is a separate published document.
- **Wrong**: Calling the policy "in progress" or "evolving" → **Right**: It is adopted. Copyright/licensing is the one open area, not the policy as a whole.
- **Wrong**: Thinking "no automated detection" means no consequences → **Right**: Maintainers notice patterns; credit can be revoked; repeated violations escalate to bans.
- **Wrong**: Ignoring the "understand before submitting" rule → **Right**: AI-generated code added without reading the prior issue discussion is an explicit violation, even if disclosed.

## See Also

- [Overview](overview.md) — Drupal's position in context
- [Disclosure Checkboxes](disclosure-checkboxes.md) — threshold, format, and when to check each box
- [Issue Review Guidelines](issue-review-guidelines.md) — how reviewers evaluate AI contributions
- [Credit System](credit-system.md) — credit implications of AI usage
- [AI Best Practices and Evals](ai-best-practices-and-evals.md) — the `ai_best_practices` project and eval infrastructure
- Reference: [Adopted AI policy](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/policy-on-the-use-of-ai-when-contributing-to-drupal)
- Reference: [#3565917 — Proposed guidelines (Postponed)](https://www.drupal.org/project/governance/issues/3565917)
- Reference: [#3569240 — AI Issue Review Guidelines](https://www.drupal.org/project/ai/issues/3569240)
