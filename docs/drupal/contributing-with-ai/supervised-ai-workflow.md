---
description: "Supervised AI workflow — the four failure modes of unsupervised AI contribution (no memory, context poisoning, confident-but-wrong, training data bias) and guardrails for each"
tldr: "Use this when you want to understand why unsupervised AI contribution fails and how to build guardrails into your AI-assisted development workflow. This guide explains the failure modes and prevention strategies."
drupal_version: "11.x"
---

# Supervised AI Workflow

## When to Use

> When you want to understand why unsupervised AI contribution fails and how to build guardrails into your AI-assisted development workflow. This guide explains the failure modes and prevention strategies.

## Decision: Failure Modes and Guardrails

| Failure Mode | What Happens | Guardrail |
|---|---|---|
| No persistent memory | AI starts fresh every session, forgets project patterns, repeats mistakes | Load coding standards and guides at session start |
| Context poisoning | Previous errors compound, AI builds on wrong foundation | Start fresh sessions when confused |
| Confident-but-wrong | AI presents incorrect solutions with full confidence | Question every choice, verify independently |
| Training data bias | AI defaults to Stack Overflow patterns, mixes Drupal versions | Use authoritative reference docs, not AI's "knowledge" |

## Pattern: Failure Mode 1 — No Persistent Memory

AI does not form new memories between sessions. Every conversation starts from zero. It doesn't remember:
- Your project's established patterns
- Previous corrections you made
- Conventions your team follows
- What it got wrong last time

**Impact on contribution:** AI may write a patch that contradicts a pattern established two sessions ago. It may suggest an approach you already tried and rejected. It may ignore project conventions documented in files it didn't read.

**Guardrail:** Load context explicitly at the start of every session. Point AI to coding standards, dev-guides for the relevant API, project-specific conventions. Use CLAUDE.md files, skills, or other mechanism to embed best practices. Even then, verify — AI doesn't always read or follow loaded context.

## Pattern: Failure Mode 2 — Context Poisoning

In long sessions, the conversation history IS the AI's context. Everything said — including mistakes, wrong approaches, failed attempts — stays in that context. AI doesn't read the full history top-to-bottom; it scans for relevant fragments. Earlier errors become the foundation for later decisions.

**Impact on contribution:** You ask AI to fix a bug. It tries approach A (wrong). You correct it to approach B (still wrong). By attempt C, the context is polluted with two wrong approaches, and the AI is building on confusion. The final patch may look right but carries subtle assumptions from the wrong approaches.

**Guardrail:** When things go sideways — you've corrected the same thing twice, the AI is going in circles — start a fresh session. Let the AI analyze the code without the poisoned history. The clean context often finds the solution immediately.

## Pattern: Failure Mode 3 — Confident-but-Wrong (AI Dunning-Kruger)

AI presents every solution with equal confidence. "This is done, production ready!" It never says "I'm uncertain about this approach" or "maybe we should reconsider." That false confidence enters the context and makes subsequent corrections harder — the AI has already declared it correct.

**Impact on contribution:** You receive a patch that AI says is "complete and follows all Drupal coding standards." You trust the confidence, submit it, and it gets rejected in review for using deprecated APIs. The AI's confidence was not correlated with correctness.

**Guardrail:** Be the skeptic. Apply the "isn't CSS simpler?" test to every solution. Ask: is there a simpler approach? Does this use the right APIs for this Drupal version? Is this over-engineered? Never accept "this is done" — verify independently.

## Pattern: Failure Mode 4 — Training Data Bias

AI learned from Stack Overflow answers, blog posts, tutorials, and public code. This training data skews toward:
- Older Drupal versions (more Drupal 7/8 content online than Drupal 11)
- Complex solutions (developers share complex work, not simple CSS fixes)
- Popular but sometimes incorrect patterns

**Impact on contribution:** AI suggests Drupal 7 patterns in a Drupal 11 module. It creates a custom module with preprocess functions when CSS would suffice. It adds unnecessary abstractions because "that's what the training data does."

**Guardrail:** Use dev-guides and official API documentation as authoritative sources, not AI's training-derived suggestions. When AI suggests an approach, check it against current documentation for the target Drupal version. Prefer the simplest solution that works.

## Pattern: The Supervised Workflow

1. **Understand the problem deeply before involving AI** — Read the issue, reproduce the bug, understand the expected behavior
2. **Load context** — Point AI to relevant coding standards, dev-guides, existing patterns
3. **Guide the direction** — Tell AI what approach to take, don't let it choose freely
4. **Review every output** — Apply the human review requirements (see [Human Review Requirements](human-review-requirements.md))
5. **Question every choice** — "Is this the simplest approach?" "Does this API exist in Drupal 11?"
6. **Start fresh when stuck** — Don't let context poisoning waste your time
7. **Verify independently** — Run phpcs, phpstan, tests. Don't trust AI's "this passes all standards"
8. **Disclose honestly** — Your disclosure level should reflect the actual workflow, not what sounds best

## Common Mistakes

- **Letting AI drive the conversation** — You should be directing; AI should be assisting. If AI is making all the decisions, you're in "Vibe Coded" territory.
- **Not starting fresh when confused** — Stubbornly continuing a poisoned session wastes time. Fresh context is often the fastest fix.
- **Thinking more tools means better results** — Guardrails (guides, checklists, standards) matter more than the AI tool itself. A cheap AI with good guardrails outperforms an expensive AI with no oversight.
- **Skipping verification because "AI already checked"** — AI saying "I verified this" is meaningless. YOU must verify.

## See Also

- [Human Review Requirements](human-review-requirements.md) — what review means in practice
- [AI Toolchain for Contribution](ai-toolchain-for-contribution.md) — practical tool setup
- [AI Code Review Checklist](ai-code-review-checklist.md) — pre-submission verification
- [Overview](overview.md) — Drupal's disclose-and-verify position
