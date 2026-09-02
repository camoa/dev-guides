---
description: "Industry context for AI contribution — how QEMU, Gentoo, Linux kernel, and Apache handle AI policies compared to Drupal, plus legal landscape and attribution mechanisms"
tldr: "Use this when you want to understand how Drupal's approach compares to other major open source projects, or when you need to make arguments for or against specific AI policies in governance discussions."
drupal_version: "11.x"
---

# Industry Context

## When to Use

> When you want to understand how Drupal's approach compares to other major open source projects, or when you need to make arguments for or against specific AI policies in governance discussions.

## Decision: Project Policies Compared

| Project | Policy | Key Mechanism | Rationale |
|---|---|---|---|
| **QEMU** | Ban | Commit policy prohibits AI-generated code (June 2025) | DCO compliance — cannot certify AI output as your own work |
| **Gentoo** | Ban | Council voted 6-0 to ban (April 2024) | Copyright uncertainty, quality concerns, unable to verify originality |
| **Linux kernel** | Disclose | Co-developed-by trailer proposed (2025), Signed-off-by required for all code | DCO requires personal certification; AI assistance disclosed via trailers |
| **Apache** | Disclose | Generated-by trailer convention, ASF guidance document | AI welcome with attribution; committer takes responsibility |
| **Drupal** | Disclose | Issue template checkboxes, honor system | Transparency-first; human responsible for submitted code |

## Pattern: Attribution Mechanisms

**Git Trailers** (for your own repos and contrib modules you maintain):

```
Co-Authored-By: Claude <noreply@anthropic.com>
```
General-purpose, widely recognized. GitHub renders these in commit UI.

```
Co-developed-by: AI Tool <tool@example.com>
Signed-off-by: Your Name <you@example.com>
```
Linux kernel style. Each Co-developed-by must be followed by a Signed-off-by from the human who verified the work.

```
Generated-by: Claude Sonnet 4
```
Apache style. Indicates AI generated the code; committer takes responsibility.

**On drupal.org**: Attribution is handled via issue checkboxes, not commit trailers. Maintainers write the final commit message. Use trailers in your own projects.

## Pattern: Legal Landscape

**Copyright ownership is unsettled:**
- US Copyright Office: AI-generated content without human creative input may not be copyrightable
- EU AI Act: Requires disclosure of AI-generated content in certain contexts
- Some jurisdictions recognize AI-assisted works where human provides creative direction

**DCO (Developer Certificate of Origin) tension:**
- DCO requires you to certify the contribution is your original work or you have the right to submit it
- Can you certify AI-generated code as "your" work? QEMU says no. Linux kernel says yes if you take responsibility.
- Drupal doesn't use DCO but the principle applies: you are responsible for what you submit

**Practical guidance:** Treat AI-assisted code as your own. You prompted it, you reviewed it, you submit it, you defend it. If you can't do that, don't submit it.

## Common Mistakes

- **Citing QEMU's ban to argue Drupal should ban AI** — Different projects have different governance models, contributor bases, and risk profiles. QEMU's DCO-based argument doesn't apply directly to Drupal's credit-based system.
- **Assuming legal questions are settled** — Copyright law for AI is actively evolving. Don't make definitive legal claims in governance discussions.
- **Ignoring the trend** — Most major projects are moving toward disclosure-based policies. Bans are increasingly the exception.
- **Not considering DCO implications** — Even without formal DCO, the principle that you certify your submission matters

## See Also

- [Overview](overview.md) — Drupal's position
- [Drupal AI Policy](drupal-ai-policy.md) — Drupal-specific policy details
- [Commit Messages](commit-messages.md) — attribution in practice
- Reference: [Apache AI guidance](https://www.apache.org/legal/generative-tooling.html)
- Reference: [Linux kernel patches](https://www.kernel.org/doc/html/latest/process/submitting-patches.html)
- Reference: [Gentoo AI policy](https://wiki.gentoo.org/wiki/Project:Council/AI_policy)
