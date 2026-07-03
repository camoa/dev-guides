---
# Routing block — an orchestrator reads to here and decides.
name: content_moderation_workflow
capability: content-moderation-workflow-provisioning
description: Use when a content type needs an editorial workflow via core content_moderation + workflows — authoring the states and transitions, enabling moderation on bundles through the add_moderation config action, backfilling existing content, and emitting transition IDs for the roles recipe to grant.
# Metadata — read only after a match.
label: Content moderation workflow
recipe_schema_version: 1.0.0
version: 0.1.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/editorial-workflow/content-moderation-state-machine
  - drupal/editorial-workflow/content-moderation-existing-content-migration
  - drupal/recipes/config-actions-entity-specific
drupal_compatibility: "^10.4 || ^11"
requires_modules:
  - content_moderation
  - workflows
authors:
  - name: Palcera
license: GPL-2.0-or-later
---

## Goal

Provision an editorial workflow with core `content_moderation` + `workflows` — a state machine (`workflows.workflow.{id}`) with the right states and transitions, moderation enabled on the target bundle(s) via the `add_moderation` config action, and existing content backfilled — then emit the transition IDs as a contract for the roles recipe to grant. The workflow owns states/transitions/bundles; it does **not** grant permissions.

## Opinion

**Do not hardcode one canonical state set.** Core's `editorial` (draft/published/archived, five transitions) and Drupal CMS's `basic_editorial` (draft/published/unpublished, three transitions) are both real, shipped shapes. Default to the leaner three-state variant and add `archived` only when the site needs a distinct terminal archive. Never assume `archived` exists. Source: guide `drupal/editorial-workflow/content-moderation-state-machine`.

**Enable moderation on bundles via the `add_moderation` config action, not raw `entity_types`.** The action (derived per entity type as `addNodeTypes`, `addTaxonomyVocabularies`, …) wires the moderation handlers; hand-editing `type_settings.entity_types` bypasses that wiring. Source: guide `drupal/editorial-workflow/content-moderation-state-machine`.

**`published` and `default_revision` are distinct flags.** `published` controls public visibility; `default_revision` controls which revision is canonical. An unpublished `archived` state still sets `default_revision: true`. Get both right per state. Source: guide `drupal/editorial-workflow/content-moderation-state-machine`.

**Enabling moderation on existing content requires a backfill.** `moderation_state` is a computed field backed by separate `content_moderation_state` entities; there is no automatic backfill. Existing revisions read as un-moderated until resaved — batch-resave them and map publish status to the correct state, or the workflow is not truly live. Source: guide `drupal/editorial-workflow/content-moderation-existing-content-migration`.

**Permissions are emitted, not granted here.** The workflow produces `use {workflow} transition {id}` IDs; the `editorial_roles_permissions` recipe grants them. This keeps `workflows.workflow.*` (this recipe) cleanly separated from `user.role.*`. Source: guide `drupal/editorial-workflow/content-moderation-state-machine`.

### What this recipe refuses

- Assuming an `archived` state exists when writing transitions or verifiers.
- Adding bundles by hand-editing `type_settings.entity_types` instead of the `add_moderation` action.
- Declaring the workflow live on a bundle with pre-existing content without backfilling that content.
- Granting `use {workflow} transition {id}` permissions to roles (that is the roles recipe's job).
- Blindly resaving existing content with the default state, risking unpublishing live pages.

## Preconditions

- Drupal 10.4+ or 11.x; the core `content_moderation` and `workflows` modules.
- The target bundle(s) exist.
- Config export is in use, so the workflow is deployable.
- For a bundle with existing content, a backfill mechanism (Batch API / queue) is available.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
workflow:
  id: string                   # e.g. editorial
  label: string
  states:                      # default to a 3-state model unless specified
    - id: string               # draft | published | unpublished | archived …
      label: string
      weight: integer
      published: boolean
      default_revision: boolean
  transitions:
    - id: string               # e.g. create_new_draft, publish
      label: string
      from: [string]
      to: string
  default_moderation_state: string

enable_on:                     # bundles to moderate
  entity_type: string          # node | taxonomy_term …
  bundles:                     # bundle ids, or '*' for all
    - string

backfill_existing: boolean     # resave existing content to seed state (default true)
```

## Sequence

If invoked in dry-run mode, perform all reads and derivations but emit a preview instead of writing config. Dry-run is required.

1. **Validate preconditions** — `content_moderation` + `workflows` enabled; target bundle(s) exist. See `drupal/editorial-workflow/content-moderation-state-machine`.

2. **Resolve the state model** — from input, or default to a three-state (draft/published/archived or draft/published/unpublished) shape; set `published`/`default_revision` per state and `default_moderation_state`. Do not assume `archived`. See `drupal/editorial-workflow/content-moderation-state-machine`.

3. **Author the workflow config-first** — `workflows.workflow.{id}` with `type: content_moderation`, the states, transitions, and `default_moderation_state`; leave `entity_types` empty at this step.

4. **Enable moderation on each target bundle via the `add_moderation` action** (`addNodeTypes` / `addTaxonomyVocabularies`, or `*`) — never by hand-editing `entity_types`. See `drupal/editorial-workflow/content-moderation-state-machine`, `drupal/recipes/config-actions-entity-specific`.

5. **Detect pre-existing content on the bundle(s).** If present and `backfill_existing`, batch-resave each entity, mapping publish status to the correct moderation state; if backfill is deferred, raise an operator-visible flag. See `drupal/editorial-workflow/content-moderation-existing-content-migration`.

6. **Emit the transition-permission contract** — the list of `use {workflow_id} transition {id}` strings — as input for `editorial_roles_permissions`. Do not grant them here.

7. **Export configuration, rebuild caches, and emit a summary** — states/transitions created, bundles enabled, backfill performed or flagged, and the transition IDs handed off.

## Data flow

```
input: workflow (id, label, states[], transitions[], default_moderation_state)
       enable_on (entity_type, bundles[])
       backfill_existing

reads project state:
       workflows.workflow.*       (existing workflow for the id/bundles)
       node type / bundle list
       existing content on the target bundles (to decide backfill)

applies opinion (guardrails):
       no-hardcoded-states · add_moderation-action-not-raw-entity_types ·
       published≠default_revision · backfill-existing-content ·
       emit-transitions-do-not-grant

references atomic detail (guides):
       drupal/editorial-workflow/content-moderation-state-machine
       drupal/editorial-workflow/content-moderation-existing-content-migration
       drupal/recipes/config-actions-entity-specific

emits:
       workflows.workflow.<id>    (states, transitions, default_moderation_state)
       type_settings.entity_types (via add_moderation action, not raw edit)
       content_moderation_state entities (backfill for existing content)
       transition IDs: use <workflow> transition <id>  → editorial_roles_permissions
```

## State-awareness contract

The recipe reads existing state before writing. For the workflow config: absent → create; present and matching the resolved spec → skip, log no-op; present and differing → conflict, do not overwrite, request operator review. Adding a bundle to an existing workflow via `add_moderation` is a create; removing states/transitions from a workflow already in use is a conflict (it can strand content in a deleted state) and is never applied silently.

Enabling moderation on a bundle with existing content is not complete until that content is backfilled — the recipe treats an un-backfilled bundle as a raised flag, not a finished state. Backfill maps each entity's publish status to a moderation state deliberately, so a resave never flips live content's visibility.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run (no duplicate states, no re-backfill of already-stated content).

## Verifier

After the recipe runs, verify:

1. `workflows.workflow.{id}` exists with `type: content_moderation` and the expected states, transitions, and `default_moderation_state`.
2. Each target bundle appears in `type_settings.entity_types.{entity_type}`, and was added via the `add_moderation` action (handlers wired), not a raw `entity_types` edit.
3. Each state's `published`/`default_revision` flags match the intended model.
4. On a bundle that had pre-existing content, every existing entity now has a `content_moderation_state` (backfill complete), or the deferral was flagged for the operator.
5. The emitted `use {workflow} transition {id}` list is correctly formed and handed to the roles recipe (this recipe grants no permissions itself).
6. A second apply produces no config changes (idempotent).

The recipe ships no verifier *script*, but every check is **agent-runnable**. Checks 1–3, 5, 6 are `config-assert` (drush + config reads). Check 4 is `self-fixture` — it seeds a pre-moderation revision, runs the backfill, and asserts a `content_moderation_state` entity now exists, cleaning up the fixture afterward; it does not assume an operator fixture.

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/editorial-workflow/content-moderation-state-machine` | Workflow config shape, state/transition model, `add_moderation` action, transition-permission IDs |
| `drupal/editorial-workflow/content-moderation-existing-content-migration` | The existing-content backfill gotcha and safe resave |
| `drupal/recipes/config-actions-entity-specific` | The config-action mechanism for enabling moderation on bundles |

### Related recipes

- `editorial_roles_permissions` — grants the `use {workflow} transition {id}` permissions this recipe emits, to the editor tier.
