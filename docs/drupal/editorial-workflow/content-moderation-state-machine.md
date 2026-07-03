---
description: The content_moderation + workflows state machine — the workflows.workflow.* config shape, states vs transitions, the core editorial vs Drupal CMS basic_editorial variants, and enabling moderation on bundles via the add_moderation config action rather than raw entity_types edits.
tldr: "A moderation workflow is workflows.workflow.{id} with type content_moderation: states (published + default_revision flags), transitions (from[]/to), and entity_types (the moderated bundles). Enable moderation on a bundle with the add_moderation config action (addNodeTypes), never by hand-editing entity_types. Do not assume 'archived' exists — Drupal CMS ships a 3-state variant."
drupal_version: "11.x"
---

# Content Moderation State Machine

## When to Use

> When you are provisioning an editorial workflow with core `content_moderation` + `workflows`, and need the exact config shape: what a state is, what a transition is, how permissions are derived, and how moderation gets switched on for a content type. Read this before authoring a `workflows.workflow.*` object or enabling moderation on a bundle that may already hold content.

## Foundation

`content_moderation` is a `workflows` plugin. The config object is `workflows.workflow.{id}` with `type: content_moderation` and a `type_settings` block:

- **`states`** — each keyed by a machine name with `label`, `weight`, and the two moderation flags: `published` (does content in this state show to the public?) and `default_revision` (does entering this state make this revision the canonical one?). `content_moderation.state` extends the base `workflows.state` with exactly those two flags.
- **`transitions`** — each with `label`, `from` (a list of state ids), `to` (one state id), and `weight`. Transitions are the edges; permissions gate them.
- **`entity_types`** — a map of `entity_type_id: [bundle, …]`; the bundles moderation is enabled on.
- **`default_moderation_state`** — the state a brand-new entity starts in (typically `draft`).

Transition permissions are **generated**, one per transition, as `use {workflow_id} transition {transition_id}`, and checked when a user tries to move content across that edge. This recipe/guide emits those IDs; a role recipe grants them (see [Editorial Role & Permission Model](editorial-role-permission-model.md)).

## Decision

Do not hardcode one canonical state set — two real, shipped variants differ:

| Variant | States | Transitions | Where it ships |
|---|---|---|---|
| Core `editorial` | `draft` (unpublished), `published`, `archived` (unpublished, default_revision) | `create_new_draft`, `publish`, `archive`, `archived_draft`, `archived_published` | `core/recipes/editorial_workflow`, Standard profile, demo_umami |
| Drupal CMS `basic_editorial` | `draft`, `published`, `unpublished` (no `archived`) | `create_new_draft`, `publish`, `unpublish` | `drupal_cms_content_type_base` |

Pick the leaner `basic_editorial` shape for most sites; add `archived` only when the site genuinely needs a distinct terminal archive state separate from "unpublished." **Never assume `archived` is present** when writing transitions or verifiers.

## Pattern

A minimal three-state workflow, config-first, with `entity_types` left empty at authoring time:

```yaml
# workflows.workflow.editorial.yml
id: editorial
label: Editorial
type: content_moderation
type_settings:
  states:
    draft:
      label: Draft
      weight: -5
      published: false
      default_revision: false
    published:
      label: Published
      weight: 0
      published: true
      default_revision: true
    archived:
      label: Archived
      weight: 5
      published: false
      default_revision: true
  transitions:
    create_new_draft: { label: 'Create New Draft', from: [draft, published], to: draft, weight: 0 }
    publish:          { label: 'Publish',          from: [draft, published], to: published, weight: 1 }
    archive:          { label: 'Archive',          from: [published],        to: archived, weight: 2 }
  default_moderation_state: draft
  entity_types: {}
```

Enable moderation on a bundle through the **`add_moderation` config action**, not by hand-editing `entity_types`. The action is derived per entity type (`addNodeTypes`, `addTaxonomyVocabularies`, …); each call wires the handlers and adds the bundle to the workflow:

```yaml
# In a recipe.yml
config:
  actions:
    workflows.workflow.editorial:
      addNodeTypes: [article, page]   # or '*' for all node bundles
```

Hand-editing `type_settings.entity_types` bypasses the handler wiring the action performs and is treated as a smell by the paired recipe verifier.

## Common Mistakes

- **Wrong**: Assuming every workflow has a `draft → published → archived` shape → **Right**: Drupal CMS's `basic_editorial` has no `archived`; read the target workflow before writing transitions
- **Wrong**: Adding bundles by editing `type_settings.entity_types` directly → **Right**: Use the `add_moderation` config action (`addNodeTypes`) so moderation handlers are wired correctly
- **Wrong**: Confusing `published` and `default_revision` → **Right**: `published` controls public visibility; `default_revision` controls which revision is canonical (an unpublished `archived` state still sets `default_revision: true`)
- **Wrong**: Granting transition permissions inside the workflow config → **Right**: The workflow emits transition IDs; a role recipe grants `use {workflow} transition {id}` (separation of concerns)
- **Wrong**: Enabling moderation on a bundle that already has content and calling it done → **Right**: Existing revisions have no moderation state until resaved — see [Enabling Moderation on Existing Content](content-moderation-existing-content-migration.md)

## See Also

- [Enabling Moderation on Existing Content](content-moderation-existing-content-migration.md) — the backfill gotcha
- [Editorial Role & Permission Model](editorial-role-permission-model.md) — who gets each `use {workflow} transition {id}` permission
- Reference: [Content Moderation](https://www.drupal.org/docs/administering-a-drupal-site/managing-content/content-moderation)
