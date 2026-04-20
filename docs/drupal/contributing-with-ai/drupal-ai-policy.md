---
description: Drupal AI policy — current state of drupal.org AI contribution rules, active governance issues, enforcement, and the tool-vs-author distinction
tldr: "Use this when you need to understand the current state of drupal.org's AI contribution policy — what rules exist, what's being proposed, and how enforcement works."
drupal_version: "11.x"
---

# Drupal AI Policy

## When to Use

> Use this when you need to understand the current state of drupal.org's AI contribution policy — what rules exist, what's being proposed, and how enforcement works.

## Decision

| Aspect | Status | Details |
|--------|--------|---------|
| Disclosure checkboxes | Active | 4 checkboxes on issue template, honor-system |
| Formal written policy | In progress | Governance issue #3565917 — active discussion, no final decision |
| MR template AI section | Proposed | #3570498 — adding AI disclosure to merge request descriptions |
| AI label for issues | Proposed | #3568936 — tagging system for AI-involved contributions |
| Reviewer guidelines | In discussion | #3576537, #3569240 — how maintainers should review AI patches |
| Automated detection | None | No tooling to detect undisclosed AI usage |

## Pattern

**AI as Tool vs AI as Author:**

| Dimension | AI as Tool (Assisted) | AI as Author (Generated/Vibe) |
|-----------|-----------------------|-------------------------------|
| Who drives decisions | Human | AI |
| Code understanding | Full | Partial to none |
| Review expectation | Normal | Enhanced to full audit |
| Disclosure level | AI Assisted Code | AI Generated / Vibe Coded |
| Community reception | Generally positive | Cautious to skeptical |

**Active governance issues:**
- **#3565917** — primary policy debate, no consensus yet
- **#3574093** — specific rules discussion, some advocate stricter requirements
- **#3569240** — reviewer guidance from the Drupal AI module project

**Enforcement:** Currently honor-system. Consequences of non-disclosure: trust erosion, potential credit revocation, increased scrutiny, reputation damage.

## Common Mistakes

- **Wrong**: Waiting for "final" policy before disclosing → **Right**: Disclosure is expected now, regardless of whether the formal policy is finalized
- **Wrong**: Assuming one governance issue represents community consensus → **Right**: Multiple issues with different perspectives exist; read broadly
- **Wrong**: Ignoring the tool vs author distinction → **Right**: How you used AI matters as much as whether you used it
- **Wrong**: Thinking enforcement means detection → **Right**: No automated detection doesn't mean no consequences; reviewers notice patterns

## See Also

- [Overview](overview.md)
- [Disclosure Checkboxes](disclosure-checkboxes.md)
- [Issue Review Guidelines](issue-review-guidelines.md)
- [Credit System](credit-system.md)
- Reference: [#3565917 AI Policy Proposal](https://www.drupal.org/project/governance/issues/3565917)
- Reference: [#3574093 AI Contribution Guidelines](https://www.drupal.org/project/governance/issues/3574093)
- Reference: [#3569240 AI Issue Review Guidelines](https://www.drupal.org/project/ai/issues/3569240)
