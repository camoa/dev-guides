---
description: Issue forks and merge requests step by step — creating an issue fork, branch naming, target branch rules, drupalorg-cli commands, and draft vs. ready MR states
tldr: "Create an issue fork via the drupal.org UI or `drupalorg issue:branch <issue-number>`. Branch name must include the issue number. Always target the most recent development branch (`main` for core). Mark MR ready when you set the issue to Needs review."
drupal_version: "11.x"
---

# Issue Forks & Merge Requests, Step by Step

## When to Use

> Use this when you have identified an issue to work on and need to create the fork, branch, and merge request.

## Steps

1. **Review what is already done** — read existing comments, MRs, and current status before starting. Duplicate or conflicting MRs waste everyone's time.

2. **Create the issue fork** — on the issue page, click "Create issue fork." Or use `drupalorg-cli`:
   ```bash
   drupalorg issue:get-fork <issue-number>
   drupalorg issue:branch <issue-number>
   ```

3. **Clone and branch** — the branch name **must include the issue number**:
   ```bash
   drupalorg issue:checkout <issue-number>
   git checkout -b '1234567-fix-short-description'
   ```

4. **Make changes** — run `phpcs` and `phpunit` locally before pushing.

5. **Push and open the MR:**
   ```bash
   git push origin 1234567-fix-short-description
   ```
   MR title: `Issue #1234567: Fix short description`. Check **"Allow commits from members who can merge"**.

6. **Set the issue status** — set to "Needs review" (or apply `state::needsReview` on GitLab). Switch MR from draft to ready.

## Decision — Target Branch Rule

| Contribution target | Branch to target |
|---|---|
| Core — new feature or improvement | `main` |
| Core — 11.x-specific bug | `11.x` |
| Core — critical fix only | `10.x` (EOL Dec 2026) |
| Contrib — new feature | Project's active development branch |
| Contrib — bug fix | Same as feature (maintainer backports later) |

## Draft vs. Ready MR

| State | Meaning | When to use |
|---|---|---|
| **Draft** | Work in progress; cannot be merged | While actively developing |
| **Ready** | Prepared for review | When you set the issue to Needs review |

Do not leave an MR in draft and set the issue to Needs review — the MR state is the primary signal on GitLab.

## Pattern — drupalorg-cli Commands

`mglaman/drupalorg-cli` (**v0.10.2**) — install `drupalorg.phar` from GitHub releases → `/usr/local/bin/drupalorg`. The `composer global require` route is deprecated.

```bash
drupalorg issue:show <issue-number>
drupalorg issue:branch <issue-number>
drupalorg issue:checkout <issue-number>
drupalorg mr:list
drupalorg mr:status <mr-id>
drupalorg mr:logs <mr-id>
drupalorg mr:diff <mr-id>
```

## Common Mistakes

- **Wrong**: Using a branch name without the issue number → **Right**: CI and maintainers expect it; some tooling requires it
- **Wrong**: Targeting the wrong branch → **Right**: Always target the development branch; maintainers backport
- **Wrong**: Leaving "Allow commits from members who can merge" unchecked → **Right**: It lets maintainers push small fixes
- **Wrong**: Not reviewing existing MRs before opening a new one → **Right**: Duplicate MRs waste review capacity
- **Wrong**: Posting an MR without setting the issue to Needs review → **Right**: The maintainer has no signal to look at it

## See Also

- [The Drupal Issue Lifecycle](drupal-issue-lifecycle.md)
- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Contribution Etiquette, RTBC & Credit](contribution-etiquette-rtbc-credit.md)
- AI overlay: [Contributing with AI — Merge Request Workflow](../contributing-with-ai/merge-request-workflow.md)
- Reference: [drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/creating-merge-requests](https://www.drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/creating-merge-requests)
- Reference: [github.com/mglaman/drupalorg-cli](https://github.com/mglaman/drupalorg-cli)
