---
description: The Drupal issue lifecycle — classic queue status workflow, GitLab scoped label taxonomy, the RTBC gap on GitLab, finding and claiming issues, and the standard issue summary template
tldr: "Detect whether a project uses the classic queue or GitLab by following the Issues link on the project page. RTBC has no single standardized GitLab equivalent — ask the maintainer. Triage access on GitLab requires Planner role or higher."
drupal_version: "11.x"
---

# The Drupal Issue Lifecycle: drupal.org & GitLab Dual-Mode

## When to Use

> Use this when navigating the issue queue — whether finding an issue to work on, updating its status, or understanding what label/status to set on a GitLab-migrated project.

## Decision

**Detecting which system a project uses:**
- Issues link → `drupal.org/project/<name>/issues` → **classic queue** (status field workflow)
- Issues link → `git.drupalcode.org/project/<name>/-/issues` → **GitLab** (scoped label workflow)

GitLab migration is opt-in as of May 2026 — both systems run in parallel.

**Classic issue status workflow:**

| Status | Meaning |
|---|---|
| **Active** | New issue; no MR attached |
| **Needs work** | MR exists but needs changes |
| **Needs review** | MR exists and ready for review |
| **RTBC** | Community reviewers consider it ready to commit |
| **Patch (to be ported)** | Committed on one branch; needs porting |
| **Fixed** | Resolved by committing the MR |
| **Postponed** | Valid but blocked or deferred |
| **Closed (*)** | Terminal states |

**GitLab scoped label taxonomy:**

| Classic status | GitLab equivalent |
|---|---|
| Active | `state::accepted` |
| Needs work | `state::needsWork` + MR marked **draft** |
| Needs review | `state::needsReview` + MR marked **ready** |
| RTBC | `state::rtbc` + MR approvals (not standardized) |
| Fixed | `state::fixed` |

Other labels: `priority::critical|major|normal|minor`, `category::bug|feature|plan|support|task`, `why::duplicate|wontFix|workAsDesigned|needsInfo|outdated|cannotReproduce`

**Triage access gap:** applying labels on GitLab requires Planner role or higher — a regression from the classic queue. A contributor-facing label UI is in development.

**RTBC on GitLab** has no single standardized equivalent — ask the maintainer how they configure MR approvals.

## Finding and Claiming Issues

- Search the **"Novice"** tag — Drupal's equivalent of "good first issue"
- Filter by "Needs review / Needs tests / Needs documentation / Needs screenshots"
- Join mentored contribution days at DrupalCons and local camps

**Claiming:**
- **Core:** self-assignment is discouraged — post a comment stating what part you are taking
- **Contrib:** follow the project's policy; self-assignment is fine if the maintainer allows
- **Never** self-assign security advisories

## GitLab-Specific Differences

| Aspect | Classic drupal.org | GitLab |
|---|---|---|
| Metadata | Status/Priority/Category form fields | Scoped labels (`state::`, `priority::`, …) |
| Triage access | Any logged-in user | Planner role+ (community UI pending) |
| Issue summary | Mandatory Summary field | Description + repo markdown templates (`.gitlab/issue_templates/`) |
| Editing the summary | Any logged-in user | Author or maintainers only |
| "Ready for review" | Status = Needs review | MR marked **ready** (not draft) |
| RTBC | Status = RTBC | `state::rtbc` + MR approvals (not standardized) |
| Cross-reference | `[#123]` | `#123` in-project; full URL across projects/platforms |
| Notifications | drupal.org subscriptions | GitLab Watch/Mention/Participate settings |

**Notification setup on GitLab:** set a deliverable email at `git.drupalcode.org/profile/notifications` — the default `<username>@<uid>.no-reply.drupal.org` address discards mail.

## Issue Summary Template

Standard sections:
1. Problem/Motivation
2. Steps to reproduce
3. Proposed resolution
4. Remaining tasks
5. User interface changes
6. API changes
7. Data model changes
8. Release notes snippet

Keep the summary current — when it drifts, maintainers set "Needs work" and tag "Needs issue summary update."

## Common Mistakes

- **Wrong**: Setting RTBC on a GitLab-migrated project without checking MR approvals config → **Right**: Ask the maintainer what their RTBC signal is
- **Wrong**: Editing a GitLab issue description when not the author or maintainer → **Right**: GitLab will deny the edit
- **Wrong**: Not updating issue notifications email on GitLab → **Right**: Set a deliverable email at `git.drupalcode.org/profile/notifications`
- **Wrong**: Commenting in closed issues to add a +1 → **Right**: Open a new related issue

## See Also

- [Issue Forks & Merge Requests, Step by Step](issue-forks-merge-requests.md)
- [Contribution Etiquette, RTBC & Credit](contribution-etiquette-rtbc-credit.md)
- AI overlay: [Contributing with AI — Issue Creation](../contributing-with-ai/issue-creation.md)
- Reference: [drupal.org/docs/develop/issues/issue-procedures-and-etiquette/issue-etiquette](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/issue-etiquette)
- Reference: [drupal.org/drupalorg/blog/gitlab-issue-migration-how-to-use-the-new-workflow](https://www.drupal.org/drupalorg/blog/gitlab-issue-migration-how-to-use-the-new-workflow)
