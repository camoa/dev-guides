---
description: Issue forks and merge requests step by step — creating an issue fork, branch naming, target branch rules, drupalorg-cli commands, and draft vs. ready MR states
tldr: "Create an issue fork via the drupal.org UI or `drupalorg issue:branch <issue-number>`. Branch name must include the issue number. Always target the most recent development branch (`main` for core). Mark MR ready when you set the issue to Needs review."
drupal_version: "11.x"
---

# Issue Forks & Merge Requests, Step by Step

## When to Use

> Use this when you have identified an issue to work on and need to create the fork, branch, and merge request. This covers the full mechanical flow from issue fork to open MR.

## Steps

1. **Review what is already done** — read existing comments, MRs, and the current status before starting. Duplicate or conflicting MRs waste everyone's time.

2. **Create the issue fork** — on the issue page, click **"Create issue fork"**. This grants push access to a fork under `issue-forks/`. Alternatively, use `drupalorg-cli`:
   ```bash
   drupalorg issue:get-fork <issue-number>    # retrieves an existing fork
   drupalorg issue:branch <issue-number>      # creates a branch on the fork
   ```

3. **Clone and branch** — the branch name **must include the issue number**:
   ```bash
   git clone git@git.drupalcode.org:issue/<project>/<issue-forks-fork-path>.git
   # Or use drupalorg-cli to check out an existing fork/branch:
   drupalorg issue:checkout <issue-number>

   git checkout -b '1234567-fix-short-description'
   ```

4. **Make changes** — follow coding standards (see [Coding Standards](drupal-coding-standards-ci-parity.md)); run `phpcs` and `phpunit` locally before pushing.

5. **Push and open the MR:**
   ```bash
   git push origin 1234567-fix-short-description
   ```
   On GitLab, open a merge request from the pushed branch. MR title: `Issue #1234567: Fix short description`. **Set the target branch** (see rule below). Check **"Allow commits from members who can merge"** — this lets maintainers push fixes directly.

6. **Set the issue status** — on the drupal.org issue, set to *Needs review* (or apply `state::needsReview` on a GitLab-migrated issue). CI runs automatically; new commits to the branch auto-update the MR.

## Target Branch Rule

Make the MR against the **most recent development branch** — `main` for core, or the project's active development branch. Backports to older branches are a later maintainer decision. Features target the development branch only.

| Contribution target | Branch to target |
|---|---|
| Core — new feature or improvement | `main` |
| Core — 11.x-specific bug | `11.x` |
| Core — critical fix only | `10.x` (EOL Dec 2026) |
| Contrib — new feature | Project's active development branch |
| Contrib — bug fix | Same as feature (maintainer backports later) |

## Using drupalorg-cli

`mglaman/drupalorg-cli` (**v0.10.2**, 2026-05-20) is a PHP CLI (`drupalorg.phar`) that wraps the drupal.org + GitLab APIs and auto-detects projects migrated to GitLab work items.

Install: download `drupalorg.phar` from [GitHub releases](https://github.com/mglaman/drupalorg-cli/releases) → place in `/usr/local/bin/drupalorg`. The `composer global require` route is **deprecated**.

Relevant commands:

```bash
drupalorg issue:show <issue-number>        # view issue details
drupalorg issue:branch <issue-number>      # create branch on issue fork
drupalorg issue:checkout <issue-number>    # check out an issue fork branch
drupalorg issue:get-fork <issue-number>    # get the issue fork URL

drupalorg mr:list                          # list merge requests
drupalorg mr:status <mr-id>               # pipeline status of an MR
drupalorg mr:logs <mr-id>                 # failed job traces
drupalorg mr:diff <mr-id>                 # diff for an MR
```

## Draft vs. Ready MR

| State | Meaning | When to use |
|---|---|---|
| **Draft** | Work in progress; cannot be merged | While actively developing; signals "not ready" |
| **Ready** | Prepared for review | When you are ready for review; equivalent to setting "Needs review" |

Mark an MR draft while working; switch to ready when it is ready for review. Do not leave an MR in draft and set the issue to Needs review — the MR state is the primary signal on GitLab.

## Handling an Existing Fork

| Situation | Action |
|---|---|
| Your own existing fork | `drupalorg issue:checkout <issue-number>` to re-use it |
| Someone else's fork/branch | Surface it via an issue comment; coordinate before starting parallel work |
| No existing fork | `drupalorg issue:branch <issue-number>` to create one |

Do not create a competing MR on top of an open MR without coordinating — it creates review confusion and discourages the original contributor.

## Common Mistakes

- Using a branch name without the issue number — CI and maintainers expect it; some tooling requires it.
- Targeting the wrong branch — always target the development branch (`main` for core); maintainers backport, not contributors.
- Leaving "Allow commits from members who can merge" unchecked — it blocks maintainers from pushing small fixes.
- Not reviewing existing MRs before opening a new one — duplicate MRs waste review capacity.
- Posting an MR without setting the issue to Needs review — the maintainer has no signal to look at it.

## See Also

- [The Drupal Issue Lifecycle](drupal-issue-lifecycle.md)
- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Contribution Etiquette, RTBC & Credit](contribution-etiquette-rtbc-credit.md)
- AI overlay: [Contributing with AI — Merge Request Workflow](../contributing-with-ai/merge-request-workflow.md)
- Reference: [drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/creating-merge-requests](https://www.drupal.org/docs/develop/git/using-gitlab-to-contribute-to-drupal/creating-merge-requests)
- Reference: [drupal.org/docs/develop/git/using-git-to-contribute-to-drupal/merge-request-guidelines](https://www.drupal.org/docs/develop/git/using-git-to-contribute-to-drupal/merge-request-guidelines)
- Reference: [github.com/mglaman/drupalorg-cli](https://github.com/mglaman/drupalorg-cli)
