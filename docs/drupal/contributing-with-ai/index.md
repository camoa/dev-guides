---
description: Contributing to Drupal with AI — disclosure requirements, merge request workflow, coding standards, human review, and responsible AI-assisted development practices
tracks: []
guide-meta:
  concepts:
    - AI contribution
    - disclosure checkboxes
    - AI Assisted Code
    - AI Generated Code
    - Vibe Coded
    - AI contribution policy
    - drupal.org AI policy
    - disclose and verify
    - human review
    - pre-commit hooks
    - phpcs Drupal standards
    - context poisoning
    - supervised AI workflow
    - AI attribution
    - Co-Authored-By
    - merge request AI disclosure
    - credit system
    - contribution workflow
    - evidence over assertion
    - ai_best_practices
    - Drupal Eval Commons
    - evals
  not:
    - Drupal AI module
    - AI Automators
    - AI chatbot
    - vector search
    - AI content generation
    - AI provider configuration
  requires: []
  complements:
    - drupal/security
    - drupal/tdd
    - drupal/forms
    - drupal/services
    - development/security-practices
  specializes: ""
  category: drupal
---

# Contributing to Drupal with AI

> Responsible AI-assisted contribution to Drupal projects. Drupal's position: AI is welcome with mandatory disclosure and human responsibility. The contributor takes full accountability for every line submitted, regardless of how it was produced.

## Policy & Landscape

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand AI contribution landscape and Drupal's position | [Overview](overview.md) | Drupal's position is disclose-and-verify: AI is welcome with mandatory disclosure and the human contributor takes full responsibility. Four disclosure levels exist; the responsible path is AI Assisted Code with thorough human review. |
| Know the current drupal.org AI policy and active governance issues | [Drupal AI Policy](drupal-ai-policy.md) | The adopted Policy on the use of AI when contributing to Drupal (last updated 2026-04-23) is live and enforced. Core rules: full contributor responsibility, disclose significant AI use, verify all output, fix problems before submitting. Copyright/licensing is the one unresolved area. |
| Choose the right AI disclosure checkboxes | [Disclosure Checkboxes](disclosure-checkboxes.md) | Check the box matching your actual AI involvement level: AI Assisted Issue, AI Assisted Code, AI Generated Code, or Vibe Coded. Multiple boxes can apply. When significant code was generated, also add an AI-Generated: Yes (...) comment. |
| Understand how other projects handle AI contributions | [Industry Context](industry-context.md) | Use this when you want to understand how Drupal's approach compares to other major open source projects, or when you need to make arguments for or against specific AI policies in governance discussions. |

## Contribution Workflow

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Create a drupal.org issue with AI disclosure | [Issue Creation](issue-creation.md) | Use this when creating a new issue on drupal.org and AI tools were used in any part of the process — researching the problem, writing the summary, analyzing code, or drafting a patch. |
| Know how reviewers evaluate AI-flagged issues | [Issue Review Guidelines](issue-review-guidelines.md) | Use this when you are reviewing an AI-flagged issue, or when you want to understand how your AI-assisted contribution will be evaluated by maintainers. |
| Understand credits and AI contributions | [Credit System](credit-system.md) | Use this when you need to understand how drupal.org credits work in the context of AI-assisted contributions, or when you have questions about credit attribution. |
| Follow the merge request workflow with AI disclosure | [Merge Request Workflow](merge-request-workflow.md) | When submitting AI-assisted code to drupal.org: disclose in both the issue checkboxes and the MR description, use ISSUE_NUMBER-description branch naming, target the lowest active supported branch, and always run phpcs locally — linting jobs in drupalci are non-blocking so a green pipeline does not mean standards pass. |

## Code Quality

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Avoid coding standards violations AI tools make | [Coding Standards](coding-standards.md) | Use this when submitting AI-assisted code to drupal.org and you need to verify it meets Drupal coding standards. AI tools commonly produce code that looks correct but violates specific Drupal conventions. |
| Format commit messages for AI-assisted work | [Commit Messages](commit-messages.md) | Use this when committing AI-assisted code and you want to properly attribute AI involvement, whether to drupal.org or your own contrib/custom project. |
| Run through a pre-submission checklist | [AI Code Review Checklist](ai-code-review-checklist.md) | Use this before submitting any AI-assisted code to drupal.org or any Drupal project. Run through this checklist every time. |

## Responsible AI Practice

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Know what "human review" really means | [Human Review Requirements](human-review-requirements.md) | Use this when you need to understand what "human review" actually means for AI-generated code — the minimum standard before you can honestly say you've reviewed the code. |
| Understand why unsupervised AI fails | [Supervised AI Workflow](supervised-ai-workflow.md) | Use this when you want to understand why unsupervised AI contribution fails and how to build guardrails into your AI-assisted development workflow. |
| Set up AI tools for responsible contribution | [AI Toolchain for Contribution](ai-toolchain-for-contribution.md) | Use this when setting up your AI development environment for Drupal contribution and you want to configure tools for responsible, well-guarded AI-assisted development. |
| Test AI-generated contributions properly | [Testing AI Code](testing-ai-code.md) | Use this when writing or reviewing tests for AI-generated Drupal contributions and you need to ensure adequate test coverage. |
| Check for AI-specific security risks | [Security Considerations](security-considerations.md) | Use this when reviewing AI-generated code for security issues, or when you want to understand the security risks specific to AI-assisted Drupal development. |

## Quick Reference & Advanced

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Know when gates pass on artifacts vs. AI claims | [Evidence Over Assertion](evidence-over-assertion.md) | Every contribution gate must be satisfied by a produced artifact — captured phpcs/phpunit output, verified API docs, actual pipeline status. AI saying "this passes" or "this is secure" is never sufficient. Any code change after a gate passed requires that gate to be re-run. |
| Understand Drupal's AI best practices and the eval landscape | [AI Best Practices and Evals](ai-best-practices-and-evals.md) | The ai_best_practices drupal.org project (pre-MVP as of 2026-05-21) will become the canonical Drupal AI guidance; watch it but don't hard-depend yet. The policy axis (disclosure) and quality axis (evals) are separate. promptfoo is dead — do not adopt it. |
| Make quick decisions with flowcharts | [Decision Trees](decision-trees.md) | Use this when you need quick answers to common AI contribution questions without reading the full guides. |
| Find policy docs and references | [Resources](resources.md) | Use this when you need links to drupal.org governance issues, contribution workflow documentation, coding standards, or industry AI policies. |
