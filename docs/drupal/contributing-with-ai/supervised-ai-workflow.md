---
description: Supervised AI workflow — the four failure modes of unsupervised AI contribution (no memory, context poisoning, confident-but-wrong, training data bias) and guardrails for each
tldr: "Use this when you want to understand why unsupervised AI contribution fails and how to build guardrails into your AI-assisted development workflow."
drupal_version: "11.x"
---

# Supervised AI Workflow

## When to Use

> Use this when you want to understand why unsupervised AI contribution fails and how to build guardrails into your AI-assisted development workflow.

## Decision

| Failure Mode | What Happens | Guardrail |
|-------------|-------------|-----------|
| No persistent memory | AI starts fresh every session, forgets project patterns, repeats mistakes | Load coding standards and guides at session start |
| Context poisoning | Previous errors compound, AI builds on wrong foundation | Start fresh sessions when confused |
| Confident-but-wrong | AI presents incorrect solutions with full confidence | Question every choice, verify independently |
| Training data bias | AI defaults to Stack Overflow patterns, mixes Drupal versions | Use authoritative reference docs, not AI's "knowledge" |

## Pattern

**Failure Mode 1 — No Persistent Memory:** AI doesn't remember previous corrections, project conventions, or what it got wrong last session. Load context explicitly at the start of every session: coding standards, dev-guides for the relevant API, project-specific conventions. Verify — AI doesn't always follow loaded context.

**Failure Mode 2 — Context Poisoning:** In long sessions, mistakes accumulate in context. AI builds on wrong approaches. When you've corrected the same thing twice or things go in circles, start a fresh session. Clean context often finds the solution immediately.

**Failure Mode 3 — Confident-but-Wrong:** AI presents every solution with equal confidence. It never says "I'm uncertain." Apply the "isn't CSS simpler?" test. Ask: is there a simpler approach? Does this use the right APIs for this Drupal version? Is this over-engineered?

**Failure Mode 4 — Training Data Bias:** AI training data skews toward older Drupal versions (more Drupal 7/8 content online than 11) and complex solutions. Use dev-guides and official API documentation as authoritative sources, not AI's training-derived suggestions.

**The Supervised Workflow:**
1. Understand the problem deeply before involving AI
2. Load context — point AI to relevant coding standards, dev-guides, existing patterns
3. Guide the direction — tell AI what approach to take, don't let it choose freely
4. Review every output — apply human review requirements
5. Question every choice — "Is this the simplest approach?" "Does this API exist in Drupal 11?"
6. Start fresh when stuck — don't let context poisoning waste time
7. Verify independently — run phpcs, phpstan, tests; don't trust AI's "this passes all standards"
8. Disclose honestly — disclosure level should reflect the actual workflow

## Common Mistakes

- **Wrong**: Letting AI drive the conversation → **Right**: You should be directing; AI should be assisting; if AI makes all decisions, you're in "Vibe Coded" territory
- **Wrong**: Not starting fresh when confused → **Right**: Stubbornly continuing a poisoned session wastes time; fresh context is often the fastest fix
- **Wrong**: Thinking more tools means better results → **Right**: Guardrails (guides, checklists, standards) matter more than the AI tool itself
- **Wrong**: Skipping verification because "AI already checked" → **Right**: AI saying "I verified this" is meaningless; YOU must verify

## See Also

- [Human Review Requirements](human-review-requirements.md)
- [AI Toolchain for Contribution](ai-toolchain-for-contribution.md)
- [AI Code Review Checklist](ai-code-review-checklist.md)
- [Overview](overview.md)
