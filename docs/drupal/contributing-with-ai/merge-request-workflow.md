---
description: "Merge request workflow with AI disclosure — the full drupal.org contribution flow, MR description template, issue fork commands, CI pipeline interpretation, and common AI mistakes"
tldr: "When submitting AI-assisted code to drupal.org: disclose in both the issue checkboxes and the MR description, use ISSUE_NUMBER-description branch naming, target the lowest active supported branch, and always run phpcs locally — linting jobs in drupalci are non-blocking so a green pipeline does not mean standards pass."
drupal_version: "11.x"
---

# Merge Request Workflow

## When to Use

> When you are ready to submit code to a drupal.org project and need to follow the full contribution workflow with AI disclosure at each step.

## Decision: Contribution Workflow Steps

| Step | Action | AI Disclosure Point |
|---|---|---|
| 1 | Find or create issue | Check AI disclosure boxes on issue |
| 2 | Create issue fork on GitLab | Use `drupalorg-cli` or the issue page "Create issue fork" button |
| 3 | Write code (with AI assistance) | Follow coding standards, review all AI output |
| 4 | Run local tests | Verify AI code passes phpcs, phpstan, phpunit |
| 5 | Create merge request | Add AI disclosure in MR description |
| 6 | CI pipeline runs | Fix any failures — AI code often fails phpcs; linting jobs are non-blocking by default |
| 7 | Request review | Reviewers see AI flags from issue |
| 8 | Address feedback | Iterate, provide interdiffs |
| 9 | Maintainer commits | Credit assigned |

## Pattern: Merge Request Description

Include an AI disclosure section in your MR description:

```
## Summary
[What this MR does and why]

## AI Usage
- **Disclosure level**: AI Assisted Code
- **Tools used**: Claude Code
- **What AI helped with**: Suggested the approach for the form alter, helped write the test
- **What I did manually**: Reviewed all code, wrote the access check logic, tested edge cases

## Testing
- [ ] phpcs passes
- [ ] phpunit tests pass
- [ ] Manual testing completed
```

## Pattern: Issue Fork Workflow

**Branch naming:** Use `ISSUE_NUMBER-brief-description` (e.g., `3565917-add-disclosure-comment`). The issue number must be the first component — drupalci uses it to associate the pipeline with the issue.

**Target branch:** Target the lowest active supported branch for the project (e.g., `5.0.x` not `main` unless the project uses only `main`). Core contributors: target `11.x` for current work. Targeting the wrong branch is a common reason for maintainer push-back.

**Using `mglaman/drupalorg-cli`:**
```bash
# Install once
composer global require mglaman/drupalorg-cli

# Check out an existing issue fork
drupalorg-cli issue:checkout 3565917

# Create a new issue fork branch
drupalorg-cli issue:branch 3565917
```

`drupalorg-cli` handles the remote setup, branch naming convention, and fork URL automatically — avoiding the manual `git remote add` step.

**Manual flow (without drupalorg-cli):**
1. Navigate to the issue on drupal.org
2. Click "Create issue fork" — creates a branch on GitLab
3. Clone or add the remote: `git remote add drupal git@git.drupal.org:issue/PROJECT-NNNNNNN.git`
4. Create your changes on the correctly named branch
5. Push to the issue fork: `git push drupal HEAD:NNNNNNN-brief-description` — the `HEAD:<branch>` refspec pushes the current branch to the correctly named remote branch without renaming it locally
6. The merge request is created automatically

Provide interdiffs for each revision so reviewers can see incremental changes.

## Pattern: CI Pipeline — What "Green" Actually Means

A passing drupalci pipeline can hide problems. Know the difference:

| Job | Blocking? | What it means |
|---|---|---|
| `phpcs` (coding standards) | **Non-blocking by default** (`allow_failure: true` in `gitlab_templates`) | A red phpcs job does NOT fail the pipeline — your green pipeline may have coding standard violations |
| `phpstan` (static analysis) | **Non-blocking by default** | Same — a green pipeline with phpstan failures is common |
| `phpunit` | **Blocking** | Red phpunit = real failure |
| Manual / opt-in jobs | **Not auto-run** (v1.15.0+) | Version matrix jobs require explicit manual trigger; an unrun job is not a passing job |

**Implication for AI-generated code:** Always run phpcs locally before pushing. Do not interpret a green pipeline as "standards pass" — check the individual job status for phpcs and phpstan. A maintainer reviewing your AI-assisted MR will check those jobs even if the overall pipeline is green.

## Common Mistakes

- **Skipping the MR description AI section** — Even if the issue has checkboxes, describe AI usage in the MR too
- **Not providing interdiffs** — Reviewers need to see what changed between revisions, especially for AI-assisted code where large rewrites are common
- **Relying on pipeline green = standards pass** — Linting jobs are non-blocking. Check phpcs and phpstan job results individually.
- **Wrong branch naming or target branch** — Use `ISSUE_NUMBER-description` and target the correct supported branch. AI tools frequently suggest wrong branch names.
- **Submitting without local testing** — Always run tests locally before pushing. CI is a safety net, not a substitute.

## See Also

- [Issue Creation](issue-creation.md) — creating the issue
- [Coding Standards](coding-standards.md) — what AI gets wrong
- [AI Code Review Checklist](ai-code-review-checklist.md) — pre-submission verification
- [Evidence Over Assertion](evidence-over-assertion.md) — why a green pipeline is not evidence that linting passed
- [Issue Forks & Merge Requests](../contributing/issue-forks-merge-requests.md) — full issue-fork and MR mechanics (this guide covers the AI-specific angle only)
- Reference: [Drupal git workflow](https://www.drupal.org/docs/develop/git)
- Reference: [drupalorg-cli](https://github.com/mglaman/drupalorg-cli)
