# Design: Drupal AI Contribution Guide

## Location

`docs/drupal/ai-contribution/` — 18 atomic decision guides

## Purpose

How to contribute to Drupal projects using AI tools — disclosure requirements, attribution, workflow, quality standards, and community norms. The guide is objectively useful for any contributor but informed by a supervised-AI philosophy: AI is productive under human oversight, dangerous without it.

## Audience

Drupal developers who use AI coding tools (Claude Code, Copilot, Cursor, etc.) and want to contribute patches, modules, or issues to drupal.org while following community norms and policies.

## Key Sources

- Drupal.org AI disclosure checkboxes (4 levels: AI Assisted Issue, AI Assisted Code, AI Generated Code, Vibe Coded)
- Governance issues: #3565917 (AI policy proposal), #3574093 (AI contribution guidelines), #3570498 (MR template), #3568936 (AI label), #3576537 (AI reviewer guidelines), #3569240 (review process)
- Industry: Linux kernel Co-developed-by trailer, Apache Generated-by, QEMU/Gentoo bans, DCO implications
- Drupal contribution workflow: issue forks, GitLab MRs, coding standards, CI, credit system

## Guide Structure (18 guides)

### Layer 1 — Overview & Policy

| # | File | Summary |
|---|------|---------|
| 1 | `overview.md` | AI contribution landscape — why disclosure matters, spectrum from ban to embrace, Drupal's "disclose and verify" position |
| 2 | `drupal-ai-policy.md` | Current drupal.org policy — governance issues, enforcement rules, what happens if you don't disclose, how policy is evolving |
| 3 | `disclosure-checkboxes.md` | The 4 AI disclosure levels on drupal.org issue template — exact wording, when to check each, examples of each level |
| 4 | `industry-context.md` | How other projects handle AI — Linux kernel Co-developed-by, Apache Generated-by, QEMU/Gentoo bans, DCO and copyright, legal landscape |

### Layer 2 — Issue Workflow

| # | File | Summary |
|---|------|---------|
| 5 | `issue-creation.md` | Creating issues with AI disclosure — metadata, component/priority, AI-specific fields, when AI helps with issue research |
| 6 | `issue-review-guidelines.md` | How reviewers evaluate AI-flagged issues — extra scrutiny triggers, what reviewers look for, the #3569240 review process |
| 7 | `credit-system.md` | Drupal credit system — how credits work, credit abuse policy for AI, whether AI tools get credited |

### Layer 3 — Code Contribution

| # | File | Summary |
|---|------|---------|
| 8 | `merge-request-workflow.md` | Issue forks → GitLab MR → CI pipeline → review — the full contribution workflow with AI disclosure at each step |
| 9 | `coding-standards.md` | Drupal coding standards that AI tools commonly violate — deprecated APIs, wrong patterns, hallucinated functions, namespace issues |
| 10 | `commit-messages.md` | Commit message format for AI contributions — Co-Authored-By, Generated-by, Co-developed-by trailers, drupal.org conventions |
| 11 | `ai-code-review-checklist.md` | Pre-submission checklist — what to verify before submitting AI-generated code, minimum quality bar |

### Layer 4 — Quality & Best Practices

| # | File | Summary |
|---|------|---------|
| 12 | `human-review-requirements.md` | What "human review" means — understand every line, verify API correctness, test edge cases, not just "it works" |
| 13 | `supervised-ai-workflow.md` | The case for supervised AI — failure modes (no memory, context poisoning, confident-but-wrong, training bias), guardrail strategies, when to start fresh, "isn't CSS simpler?" principle |
| 14 | `ai-toolchain-for-contribution.md` | Setting up AI tools for Drupal contribution — reference guides for standards, context management, checklists, mapping tools to disclosure levels |
| 15 | `testing-ai-code.md` | Testing AI-generated contributions — avoiding mock-heavy tests, testing what AI typically gets wrong, coverage expectations |
| 16 | `security-considerations.md` | AI-specific security risks — hallucinated APIs, insecure defaults, missing sanitization, supply chain concerns |

### Layer 5 — Reference

| # | File | Summary |
|---|------|---------|
| 17 | `decision-trees.md` | Quick flowcharts — Should I disclose? Which checkbox? How to attribute? Is my code ready to submit? |
| 18 | `resources.md` | Links to governance issues, policy docs, coding standards, contribution guide, key drupal.org pages |

## Design Decisions

### Why `drupal/` not `development/`
The guide is deeply tied to drupal.org-specific policies, issue templates, GitLab workflow, and credit system. A generic "AI contribution" guide would lose the actionable specifics. Industry context is covered in one guide (`industry-context.md`) rather than being the organizing principle.

### Why `supervised-ai-workflow.md` exists
Most AI contribution guides say "use AI, disclose it." This guide goes deeper into WHY unsupervised AI contribution fails — drawing from documented failure modes (no persistent memory, context poisoning, Dunning-Kruger confidence, biased training data). It maps these problems to contribution risks and shows how guardrails prevent them. This is the guide that differentiates "AI Assisted Code" (supervised, reviewed, understood) from "Vibe Coded" (generated and submitted).

### Why `ai-toolchain-for-contribution.md` exists
Bridges the gap between "I want to contribute with AI" and "how do I set up my tools responsibly." Covers: loading coding standards into context, using dev-guides for patterns, clearing context when confused, pre-submission checklists. Practical counterpart to the philosophical `supervised-ai-workflow.md`.

### Format
Each guide follows the standard atomic decision guide format:
- YAML frontmatter (description, drupal_version: "11.x")
- H1 title
- When to Use this guide
- Decision table or checklist
- Pattern/implementation details
- Common Mistakes
- See Also (cross-references)

## What This Does NOT Cover

- How to build AI-powered Drupal modules (see `drupal/ai-module/`)
- AI content generation within Drupal (see `drupal/ai-content/`)
- General coding standards (see `drupal/` topic guides for specific APIs)
- Claude Code or specific tool configuration (tool-agnostic principles)
