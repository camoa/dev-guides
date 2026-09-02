---
description: "Drupal AI best practices and evals — the ai_best_practices project, Drupal Eval Commons, the eval/policy distinction, and what to track vs. ignore"
tldr: "The ai_best_practices drupal.org project (pre-MVP as of 2026-05-21) will become the canonical Drupal AI guidance; watch it but don't hard-depend yet. The policy axis (disclosure) and quality axis (evals) are separate. promptfoo is dead — do not adopt it. Refresh this section quarterly."
drupal_version: "11.x"
---

# AI Best Practices and Evals

> **Confidence label:** This section describes a fast-moving area. The `ai_best_practices` project and Drupal Eval Commons are both pre-MVP as of 2026-05-21. Treat findings here as current-state orientation, not settled reference. **Refresh cadence: quarterly, or whenever `ai_best_practices` releases a new version.**

## When to Use

> When you want to understand the canonical Drupal AI guidance ecosystem — where authoritative Drupal AI best-practice guidance will live, what the eval infrastructure is, and what tools are and are not appropriate for Drupal contribution quality assurance.

## Decision: The Drupal AI Guidance Landscape

| Resource | What it is | Status | Use it? |
|---|---|---|---|
| **`ai_best_practices`** drupal.org project | Canonical, opinionated Drupal AI guidance for AI agents and their humans; `anthropics/skills`-format skill files + `evals/evals.json`; maintained by webchick, Dries, 19+ contributors | **Pre-MVP** (`1.0.x-dev`); MVP roadmap in progress (#3585542) | Watch it — it will become the authoritative source; do not hard-depend yet |
| Adopted AI contribution policy | The live policy (disclosure, responsibility, enforcement) | **Adopted** 2026-04-23 | Yes — this is current, enforced guidance |
| **Drupal Eval Commons** | Five-layer eval infrastructure proposal: cases/rubrics, result envelope, registry, browser, domain extensions | **Proof of concept** (built by Angie Byron with Claude); proposal at #3586445 — not independently confirmed | Orientation only — not a dependency |
| **"Every Eval Ever" envelope** | Standardized eval result format (EvalEval-Coalition external standard); per-eval UUIDs, aggregate JSON + instance JSONL, HuggingFace hosting | **Stable format** (external standard); Drupal's binding to it is not yet designed | The envelope format is stable; Drupal's registry is not |
| **`promptfoo`** | Eval tooling formerly used in the community | **Dead** — acquired by OpenAI March 2026, open-source project closed | Do not adopt |

## Pattern: `ai_best_practices` — What It Is and Why It Matters

The `ai_best_practices` project (`drupal.org/project/ai_best_practices`) is positioned as the **canonical, opinionated source of truth for how AI agents and their humans should write Drupal code**. It is not documentation — it is an active, executable guidance system:

- **Skill files** (e.g., `hook-implementations.md`, `issue-creation.md`) — guidance organized in `anthropics/skills` format, each with an `evals.json`
- **Evaluation framework** (#3581832) — an `evals.json` spec and a grader script that checks PHP lint, phpcs, diff validation, security patterns, and report structure; runs **offline, no API key required**
- **Policy framework** — disclosure rules, conduct, enforcement aligned with the adopted policy

When the MVP ships, it becomes the primary reference for AI-assisted Drupal contribution quality. Until then, the adopted policy (see [Drupal AI Policy](drupal-ai-policy.md)) is the enforced rule; `ai_best_practices` is the guidance in progress.

## Pattern: The Eval Axis vs. the Policy Axis

These are two separate concerns that are often conflated:

| Axis | What it measures | Where it lives |
|---|---|---|
| **Policy** (see [Drupal AI Policy](drupal-ai-policy.md)) | Disclosure, responsibility, conduct — whether AI use was acceptable | Adopted policy doc; enforced via credit/abuse rules |
| **Quality / Evals** (`ai_best_practices`) | Whether AI-generated code follows Drupal best practices — phpcs passes, correct APIs, security patterns | `ai_best_practices` `evals.json` + grader |

Passing the policy axis (disclosing correctly) does not guarantee passing the quality axis. Both matter. The policy is enforced today; the eval infrastructure is being built.

## Pattern: What to Track, What to Ignore

**Track** (check quarterly):
- `ai_best_practices` releases — when the MVP ships, update [Drupal AI Policy](drupal-ai-policy.md) and this section to point to it
- Drupal Eval Commons #3586445 — when the registry design is finalized, evals become a usable contribution gate
- Governance issue #3565917 — if it un-postpones and adopts, it may add to or modify the current policy

**Ignore / do not adopt**:
- `promptfoo` — dead (March 2026 acquisition by OpenAI)
- Any eval registry or `evals.json` schema as a hard dependency — both are `[DRAFT]` and subject to breaking change
- Unconfirmed Eval Commons work items — `#3586445` could not be independently confirmed as of 2026-05-21

## Common Mistakes

- **Treating `ai_best_practices` as stable reference** — It is pre-MVP. Skill file content and `evals.json` schema are actively changing. Pin to a specific release if you depend on it; otherwise reference by project URL.
- **Using `promptfoo`** — It is no longer maintained. Do not adopt it for any Drupal eval workflow.
- **Conflating the policy gate with the quality gate** — Disclosing AI use correctly does not mean the AI-generated code passes Drupal's quality bar. Both checks are needed.
- **Treating a passing eval as a policy substitute** — The eval grader checks code quality; it does not verify that you disclosed AI use appropriately or understood the issue before submitting.

## See Also

- [Drupal AI Policy](drupal-ai-policy.md) — the adopted policy (the enforced rule today)
- [Evidence Over Assertion](evidence-over-assertion.md) — why gates must pass on artifacts, not claims
- [AI Code Review Checklist](ai-code-review-checklist.md) — the practical pre-submission checklist
- Reference: [ai_best_practices](https://www.drupal.org/project/ai_best_practices) | [webchick Eval Commons article](https://webchick.tech/toward-a-shared-eval-infrastructure-for-drupal-ai-a-proof-of-concept) | [Every Eval Ever](https://evalevalai.com/projects/every-eval-ever/)
