---
description: Merge request workflow with AI disclosure — the full drupal.org contribution flow, MR description template, issue fork commands, CI pipeline interpretation, and common AI mistakes
tldr: "When submitting AI-assisted code to drupal.org: disclose in both the issue checkboxes and the MR description, use ISSUE_NUMBER-description branch naming, target the lowest active supported branch, and always run phpcs locally — linting jobs in drupalci are non-blocking so a green pipeline does not mean standards pass."
drupal_version: "11.x"
---

# Merge Request Workflow

## When to Use

> Use this when you are ready to submit code to a drupal.org project and need to follow the full contribution workflow with AI disclosure at each step.

## Decision

| Step | Action | AI Disclosure Point |
|------|--------|---------------------|
| 1 | Find or create issue | Check AI disclosure boxes on issue |
| 2 | Create issue fork on GitLab | Use `drupalorg-cli` or issue page "Create issue fork" button |
| 3 | Write code (with AI assistance) | Follow coding standards, review all AI output |
| 4 | Run local tests | Verify AI code passes phpcs, phpstan, phpunit |
| 5 | Create merge request | Add AI disclosure in MR description |
| 6 | CI pipeline runs | Fix any failures — AI code often fails phpcs; linting jobs are non-blocking by default |
| 7 | Request review | Reviewers see AI flags from issue |
| 8 | Address feedback | Iterate, provide interdiffs |
| 9 | Maintainer commits | Credit assigned |

## Pattern: MR Description

```markdown
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

**Branch naming:** Use `ISSUE_NUMBER-brief-description` (e.g., `3565917-add-disclosure-comment`). The issue number must be first — drupalci uses it to associate the pipeline with the issue.

**Target branch:** Target the lowest active supported branch (e.g., `5.0.x` not `main`). Core contributors: target `11.x`. Wrong target branch is a common reason for maintainer push-back.

**Using `mglaman/drupalorg-cli`:**
```bash
composer global require mglaman/drupalorg-cli

# Check out an existing issue fork
drupalorg-cli issue:checkout 3565917

# Create a new issue fork branch
drupalorg-cli issue:branch 3565917
```

**Manual flow:**
```bash
git remote add drupal git@git.drupal.org:issue/PROJECT-NNNNNNN.git
# create branch, make changes, then:
git push drupal HEAD:NNNNNNN-brief-description
```

Provide interdiffs for each revision so reviewers can see incremental changes.

## Pattern: CI Pipeline — What "Green" Actually Means

| Job | Blocking? | What it means |
|-----|-----------|---------------|
| `phpcs` (coding standards) | **Non-blocking** (`allow_failure: true`) | A red phpcs job does NOT fail the pipeline — your green pipeline may have coding standard violations |
| `phpstan` (static analysis) | **Non-blocking** | Same — a green pipeline with phpstan failures is common |
| `phpunit` | **Blocking** | Red phpunit = real failure |
| Manual / opt-in jobs | **Not auto-run** | Version matrix jobs require explicit manual trigger |

Always run phpcs locally before pushing. A maintainer reviewing your AI-assisted MR will check those jobs even if the overall pipeline is green.

## Common Mistakes

- **Wrong**: Skipping the MR description AI section → **Right**: Even if the issue has checkboxes, describe AI usage in the MR too
- **Wrong**: Not providing interdiffs → **Right**: Reviewers need to see what changed between revisions, especially for AI-assisted code where large rewrites are common
- **Wrong**: Relying on pipeline green = standards pass → **Right**: Linting jobs are non-blocking; check phpcs and phpstan job results individually
- **Wrong**: Wrong branch naming or target branch → **Right**: Use `ISSUE_NUMBER-description` and target the correct supported branch; AI tools frequently suggest wrong branch names
- **Wrong**: Submitting without local testing → **Right**: Always run tests locally before pushing; CI is a safety net, not a substitute

## See Also

- [Issue Creation](issue-creation.md)
- [Coding Standards](coding-standards.md)
- [AI Code Review Checklist](ai-code-review-checklist.md)
- [Evidence Over Assertion](evidence-over-assertion.md) — why "pipeline green" is not sufficient evidence
- [Issue Forks & Merge Requests](../contributing/issue-forks-merge-requests.md) — full issue-fork and MR mechanics (this guide covers the AI-specific angle only)
- Reference: [Drupal git workflow](https://www.drupal.org/docs/develop/git)
- Reference: [drupalorg-cli](https://github.com/mglaman/drupalorg-cli)
