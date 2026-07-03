---
description: Drupal editorial workflow — content roles and permissions, and the content_moderation state machine that moves content from draft to published.
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
  specializes: ""
  category: drupal
---

# Drupal Editorial Workflow

> The configuration that lets a team run content: the roles editors log in as, the content permissions those roles carry, and the moderation state machine that moves a page from draft to published. Provision roles and workflow as separate, composable pieces — the workflow emits transition IDs, the role grants the permission to use them.

## Roles & Permissions

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide how many editorial roles and which content permissions each gets | [Editorial Role & Permission Model](editorial-role-permission-model.md) | The own/any permission model, the single-role (`content_editor`) vs two-tier (`author`/`editor`) decision, and provisioning permissions through recipe `grantPermissions` actions rather than baked-in role config or `is_admin`. |

## Content Moderation

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Author a moderation workflow's states and transitions | [Content Moderation State Machine](content-moderation-state-machine.md) | The `workflows.workflow.*` config shape, states vs transitions, the core `editorial` vs Drupal CMS `basic_editorial` variants, and enabling moderation on a bundle via the `add_moderation` config action. |
| Turn on moderation for a content type that already has content | [Enabling Moderation on Existing Content](content-moderation-existing-content-migration.md) | The silent backfill gotcha — existing revisions get no moderation state until resaved — and how to batch-backfill them safely. |
