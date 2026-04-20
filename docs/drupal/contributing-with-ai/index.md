---
description: Contributing to Drupal with AI — disclosure requirements, merge request workflow, coding standards, human review, and responsible AI-assisted development practices
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
| Understand AI contribution landscape and Drupal's position | [Overview](overview.md) | Read this first. It maps the landscape of AI contribution policies, why disclosure matters, and how Drupal's "disclose and verify" position works before you touch any issue or merge request. |
| Know the current drupal.org AI policy and active governance issues | [Drupal AI Policy](drupal-ai-policy.md) | Use this when you need to understand the current state of drupal.org's AI contribution policy — what rules exist, what's being proposed, and how enforcement works. |
| Choose the right AI disclosure checkboxes | [Disclosure Checkboxes](disclosure-checkboxes.md) | Use this when creating or updating a drupal.org issue and you need to determine which AI disclosure checkboxes to select. |
| Understand how other projects handle AI contributions | [Industry Context](industry-context.md) | Use this when you want to understand how Drupal's approach compares to other major open source projects, or when you need to make arguments for or against specific AI policies in governance discussions. |

## Contribution Workflow

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Create a drupal.org issue with AI disclosure | [Issue Creation](issue-creation.md) | Use this when creating a new issue on drupal.org and AI tools were used in any part of the process — researching the problem, writing the summary, analyzing code, or drafting a patch. |
| Know how reviewers evaluate AI-flagged issues | [Issue Review Guidelines](issue-review-guidelines.md) | Use this when you are reviewing an AI-flagged issue, or when you want to understand how your AI-assisted contribution will be evaluated by maintainers. |
| Understand credits and AI contributions | [Credit System](credit-system.md) | Use this when you need to understand how drupal.org credits work in the context of AI-assisted contributions, or when you have questions about credit attribution. |
| Follow the merge request workflow with AI disclosure | [Merge Request Workflow](merge-request-workflow.md) | Use this when you are ready to submit code to a drupal.org project and need to follow the full contribution workflow with AI disclosure at each step. |

## Code Quality

| I need to... | Guide |
|-------------|-------|
| Avoid coding standards violations AI tools make | [Coding Standards](coding-standards.md) |
| Format commit messages for AI-assisted work | [Commit Messages](commit-messages.md) |
| Run through a pre-submission checklist | [AI Code Review Checklist](ai-code-review-checklist.md) |

## Responsible AI Practice

| I need to... | Guide |
|-------------|-------|
| Know what "human review" really means | [Human Review Requirements](human-review-requirements.md) |
| Understand why unsupervised AI fails | [Supervised AI Workflow](supervised-ai-workflow.md) |
| Set up AI tools for responsible contribution | [AI Toolchain for Contribution](ai-toolchain-for-contribution.md) |
| Test AI-generated contributions properly | [Testing AI Code](testing-ai-code.md) |
| Check for AI-specific security risks | [Security Considerations](security-considerations.md) |

## Quick Reference

| I need to... | Guide |
|-------------|-------|
| Make quick decisions with flowcharts | [Decision Trees](decision-trees.md) |
| Find policy docs and references | [Resources](resources.md) |
