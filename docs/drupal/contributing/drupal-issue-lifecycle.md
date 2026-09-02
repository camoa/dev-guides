---
description: The Drupal issue lifecycle — classic queue status workflow, GitLab scoped label taxonomy, the RTBC gap on GitLab, finding and claiming issues, and the standard issue summary template
tldr: "Detect whether a project uses the classic queue or GitLab by following the Issues link on the project page. RTBC has no single standardized GitLab equivalent — ask the maintainer. Triage access on GitLab requires Planner role or higher."
drupal_version: "11.x"
---

# The Drupal Issue Lifecycle: drupal.org & GitLab Dual-Mode

## When to Use

> Use this when navigating the issue queue — whether finding an issue to work on, updating its status, or understanding what label/status to set on a GitLab-migrated project.

## Detecting Which System a Project Uses

On the project page (`drupal.org/project/<name>`), follow the **"Issues"** link:

- Target `drupal.org/project/<name>/issues` → **classic queue** (status field workflow)
- Target `git.drupalcode.org/project/<name>/-/issues` → **GitLab** (scoped label workflow)

As of May 2026, GitLab migration is an **opt-in pilot**. Both systems run in parallel with no mandatory migration deadline. Old drupal.org issue URLs redirect server-side on migrated projects.

## Classic Issue Status Workflow

| Status | Meaning |
|---|---|
| **Active** | New issue; no MR attached. Default state. |
| **Needs work** | An MR exists but needs changes per review feedback. |
| **Needs review** | An MR exists and is ready for peer review and testing. |
| **Reviewed & tested by the community (RTBC)** | Community reviewers consider it ready to commit. |
| **Patch (to be ported)** | Committed on one branch; needs porting to another. |
| **Fixed** | Resolved by committing the MR. |
| **Postponed** | Valid but blocked or temporarily deferred. |
| **Postponed (maintainer needs more info)** | Insufficient information to proceed. |
| **Closed (Duplicate / Won't fix / Works as designed / Cannot reproduce / Outdated / Fixed)** | Terminal states. Closed (Fixed) is auto-set ~2 weeks after Fixed. |

## GitLab Scoped Label Taxonomy

GitLab-migrated projects replace the Status field with **scoped labels** (`state::`, `priority::`, `category::`, `why::`):

| Classic status | GitLab equivalent |
|---|---|
| Active | `state::accepted` (or in-progress; no specific label) |
| Needs work | `state::needsWork` + MR marked **draft** |
| Needs review | `state::needsReview` + MR marked **ready** |
| RTBC | `state::rtbc` + MR approvals — *not yet standardized; see below* |
| Fixed | `state::fixed` (auto → `state::closed` after ~2 weeks) |
| Closed (duplicate/won't fix/…) | `state::closed` + matching `why::*` label |

**Label taxonomy:**

- `priority::critical|major|normal|minor`
- `category::bug|feature|plan|support|task`
- `why::duplicate|wontFix|workAsDesigned|needsInfo|outdated|cannotReproduce`
- `component::*` (per-project, non-scoped)
- `version::*` (per-project scoped; naming only, no link to Git tags)

**Triage access gap:** applying or editing labels on GitLab requires the **Planner role or higher** — a regression from the classic queue where any logged-in user could triage. A contributor-facing label UI is in development (no launch date). Until it ships, non-Planner contributors may need maintainer help to change labels.

## The RTBC Gap on GitLab

RTBC has **no single standardized GitLab equivalent** — the migration docs call it "the biggest missing piece." In practice it is approximated by a combination:

- `state::rtbc` label
- GitLab **MR approvals** (count configurable per project)
- Optionally an issue-board RTBC column

The exact workflow varies per project. For a GitLab-migrated project, ask the maintainer what their RTBC signal is.

## Finding and Claiming Issues

**Finding:**

- Search the **"Novice"** tag — Drupal's equivalent of "good first issue."
- Filter by "Needs review / Needs tests / Needs documentation / Needs screenshots."
- Use Contributor Guide task pages for curated entry points.
- Join **mentored contribution days** at DrupalCons and local camps.
- Join initiatives (e.g., Bug Smash Initiative) for coordinated triage.

**Claiming:**

- **Core:** self-assignment is discouraged — post a comment stating what part you are taking and update it periodically; people forget to un-assign, blocking others.
- **Contrib:** follow the project's policy; self-assignment is fine for a single large task if the maintainer allows it.
- **Never** self-assign security advisories.

## Issue Summary — The Standard Template

The bare issue summary template sections (these carry over to GitLab markdown templates):

1. Problem/Motivation
2. Steps to reproduce
3. Proposed resolution
4. Remaining tasks
5. User interface changes
6. API changes
7. Data model changes
8. Release notes snippet

Keep the summary **current** — when it drifts from consensus, maintainers set *Needs work* and tag "Needs issue summary update." Updating the summary is a shared responsibility: author, reviewers, and committers all own it.

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

## Common Mistakes

- Setting RTBC on a GitLab-migrated project without checking how the maintainer configures MR approvals — the signal is per-project.
- Editing a GitLab issue description when you are not the author or a maintainer — GitLab will deny the edit.
- Not updating issue notifications email on GitLab — the no-reply default means you miss all notifications.
- Commenting in closed issues — the etiquette is to open a new related issue instead.

## See Also

- [Issue Forks & Merge Requests, Step by Step](issue-forks-merge-requests.md)
- [Contribution Etiquette, RTBC & Credit](contribution-etiquette-rtbc-credit.md)
- AI overlay: [Contributing with AI — Issue Creation](../contributing-with-ai/issue-creation.md)
- Reference: [drupal.org/docs/develop/issues/issue-procedures-and-etiquette/issue-etiquette](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/issue-etiquette)
- Reference: [drupal.org/drupalorg/blog/gitlab-issue-migration-how-to-use-the-new-workflow](https://www.drupal.org/drupalorg/blog/gitlab-issue-migration-how-to-use-the-new-workflow)
