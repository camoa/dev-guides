---
description: Drupal editorial workflow — content roles and permissions, and the content_moderation state machine that moves content from draft to published.
tracks:
  - project: drupal
    channel: stable
    verified: 2026-07-03
guide-meta:
  concepts:
    - editorial roles
    - content permissions
    - own vs any permissions
    - content moderation
    - workflows
    - moderation state
    - editorial workflow
  not:
    - module-developer permission definitions
    - access control internals
  requires: []
  complements:
    - drupal/security
    - drupal/recipes
  category: drupal
---

# Drupal Editorial Workflow

> The configuration that lets a team run content: the roles editors log in as, the content permissions those roles carry, and the moderation state machine that moves a page from draft to published. Provision roles and workflow as separate, composable pieces — the workflow emits transition IDs, the role grants the permission to use them.

## Roles & Permissions

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide how many editorial roles and which content permissions each gets | [Editorial Role & Permission Model](editorial-role-permission-model.md) | Editorial roles are composed from own/any permission PAIRS (create, edit own/any, delete own/any, view own/any unpublished). Drupal CMS ships one content_editor role whose permissions accrete across recipes; demo_umami ships a two-tier author/editor split. Grant permissions via config actions, never is_admin. |

## Content Moderation

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Author a moderation workflow's states and transitions | [Content Moderation State Machine](content-moderation-state-machine.md) | The `workflows.workflow.*` config shape, states vs transitions, the core `editorial` vs Drupal CMS `basic_editorial` variants, and enabling moderation on a bundle via the `add_moderation` config action. |
| Turn on moderation for a content type that already has content | [Enabling Moderation on Existing Content](content-moderation-existing-content-migration.md) | The silent backfill gotcha — existing revisions get no moderation state until resaved — and how to batch-backfill them safely. |
