---
# Routing block — an orchestrator reads to here and decides.
name: content_moderation_workflow
capability: content-moderation-workflow-provisioning
description: Use when a content type needs an editorial workflow via core content_moderation + workflows — authoring the states and transitions, enabling moderation on bundles through the add_moderation config action, backfilling existing content, and emitting transition IDs for the roles recipe to grant.
# Metadata — read only after a match.
label: Content moderation workflow
recipe_schema_version: 1.0.0
version: 0.2.0
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
- DDEV runs the site; the verifier's commands go through `ddev`.

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

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only; a non-interactive `ddev drush` keeps Drush's messages on standard error. A stopped DDEV project prints its start-up text on standard output, so start the site before the verify run. Entries that call `.aida/content-moderation-workflow/verify.php` run the script in `## Files`. It prints one line per violation and exits non-zero when it printed any.

verifier:
  - id: workflow-shape
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/content-moderation-workflow/verify.php -- workflow {workflow:json}
    pass: stdout empty
  - id: moderation-on-bundles
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/content-moderation-workflow/verify.php -- bundles {workflow.id} {enable_on.entity_type} {enable_on.bundles}
    pass: stdout empty
  - id: backfill-complete
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/content-moderation-workflow/verify.php -- backfill {workflow.id} {enable_on.entity_type} {enable_on.bundles} {backfill_existing:json}
    pass: stdout empty
  - id: active-equals-export
    kind: config-assert
    run: ddev drush config:status
    pass: stdout empty

What the entries do not prove, and where the proof is:

- `workflow-shape` always checks the type, that every published state is also the default revision, and that `default_moderation_state` names a state. It compares states, transitions and the default state with the input only where the input gives them. When the input leaves `states` out, the summary carries the resolved model.
- `moderation-on-bundles` and `backfill-complete` run once per bundle in `enable_on.bundles`, and `*` checks every bundle of the entity type. An empty list reads unknown, not pass.
- `moderation-on-bundles` proves the bundle is moderated by this workflow. It cannot tell the `add_moderation` action from a raw `entity_types` edit, because both leave the same config.
- `backfill-complete` reads content, not config, and names up to 20 entities with no moderation state. An absent `backfill_existing` counts as true, its default. When it is false, the entry checks nothing, and the summary carries the operator flag.
- The transition-permission list handed to the roles recipe is not checked here. It is in the summary, and the roles recipe's `transition-permissions` entry checks the grants.
- `active-equals-export` proves the export is current after Sequence step 7. The state-awareness contract makes a second apply a no-op on that state.

## Files

One script, which the consumer writes before the verifier runs and removes after it. Do not edit it or commit it. Drush runs it with Drupal booted and passes the words after `--` in `$extra`.

```php .aida/content-moderation-workflow/verify.php
<?php

// Verifier checks for content-moderation-workflow.
// $extra: workflow <workflow JSON> | bundles <id> <entity type> <bundle>
//   | backfill <id> <entity type> <bundle> <backfill_existing JSON>
// Prints one line per violation, then throws so Drush exits non-zero.
$check = $extra[0] ?? '';
$v = [];

if ($check === 'workflow') {
  $input = json_decode($extra[1] ?? 'null', TRUE, 512, JSON_THROW_ON_ERROR);
  $id = $input['id'] ?? '';
  $config = \Drupal::config("workflows.workflow.$id");
  if ($id === '') {
    $v[] = 'workflow: the workflow id is missing';
  }
  elseif ($config->isNew()) {
    $v[] = "workflows.workflow.$id does not exist";
  }
  else {
    $settings = $config->get('type_settings');
    $states = $settings['states'] ?? [];
    $transitions = $settings['transitions'] ?? [];
    $default = $settings['default_moderation_state'] ?? '';
    if ($config->get('type') !== 'content_moderation') {
      $v[] = "workflows.workflow.$id has type '" . $config->get('type') . "', not 'content_moderation'";
    }
    foreach ($states as $state_id => $state) {
      if (!empty($state['published']) && empty($state['default_revision'])) {
        $v[] = "state $state_id is published but not the default revision";
      }
    }
    if (!isset($states[$default])) {
      $v[] = "default_moderation_state '$default' is not a state of $id";
    }
    if (isset($input['default_moderation_state']) && $input['default_moderation_state'] !== $default) {
      $v[] = "default_moderation_state is '$default', not '{$input['default_moderation_state']}'";
    }
    if (isset($input['states'])) {
      $want = array_column($input['states'], NULL, 'id');
      if (array_diff_key($want, $states) || array_diff_key($states, $want)) {
        $v[] = 'states are ' . implode(',', array_keys($states)) . ', not ' . implode(',', array_keys($want));
      }
      foreach (array_intersect_key($want, $states) as $state_id => $state) {
        foreach (['published', 'default_revision'] as $flag) {
          if ((bool) ($state[$flag] ?? FALSE) !== (bool) ($states[$state_id][$flag] ?? FALSE)) {
            $v[] = "state $state_id has $flag " . var_export((bool) ($states[$state_id][$flag] ?? FALSE), TRUE) . ', not as the input says';
          }
        }
      }
    }
    if (isset($input['transitions'])) {
      $want = array_column($input['transitions'], NULL, 'id');
      if (array_diff_key($want, $transitions) || array_diff_key($transitions, $want)) {
        $v[] = 'transitions are ' . implode(',', array_keys($transitions)) . ', not ' . implode(',', array_keys($want));
      }
      foreach (array_intersect_key($want, $transitions) as $transition_id => $transition) {
        $from = (array) ($transition['from'] ?? []);
        $have = $transitions[$transition_id]['from'] ?? [];
        sort($from);
        sort($have);
        if ($from !== $have) {
          $v[] = "transition $transition_id goes from " . implode(',', $have) . ', not ' . implode(',', $from);
        }
        if (($transition['to'] ?? '') !== ($transitions[$transition_id]['to'] ?? '')) {
          $v[] = "transition $transition_id goes to '" . ($transitions[$transition_id]['to'] ?? '') . "', not '" . ($transition['to'] ?? '') . "'";
        }
      }
    }
  }
}
elseif ($check === 'bundles' || $check === 'backfill') {
  [, $id, $type, $bundle] = array_pad($extra, 4, '');
  $backfill = json_decode($extra[4] ?? 'null', TRUE, 512, JSON_THROW_ON_ERROR) ?? TRUE;
  if ($id === '' || $type === '' || $bundle === '') {
    $v[] = "$check: the workflow id, entity type or bundle argument is missing";
  }
  elseif ($check === 'bundles' || $backfill) {
    $bundles = $bundle === '*' ? array_keys(\Drupal::service('entity_type.bundle.info')->getBundleInfo($type)) : [$bundle];
    if (!$bundles) {
      $v[] = "$type has no bundles";
    }
    foreach ($bundles as $b) {
      if ($check === 'bundles') {
        $workflow = \Drupal::service('content_moderation.moderation_information')->getWorkflowForEntityTypeAndBundle($type, $b);
        if ($workflow?->id() !== $id) {
          $v[] = "$type bundle $b is moderated by '" . ($workflow?->id() ?? 'no workflow') . "', not '$id'";
        }
        continue;
      }
      $bundle_key = \Drupal::entityTypeManager()->getDefinition($type)->getKey('bundle');
      $query = \Drupal::entityTypeManager()->getStorage($type)->getQuery()->accessCheck(FALSE);
      if ($bundle_key) {
        $query->condition($bundle_key, $b);
      }
      $missing = [];
      $state_storage = \Drupal::entityTypeManager()->getStorage('content_moderation_state');
      foreach (array_chunk(array_values($query->execute()), 500) as $chunk) {
        $state_ids = $state_storage->getQuery()->accessCheck(FALSE)
          ->condition('workflow', $id)
          ->condition('content_entity_type_id', $type)
          ->condition('content_entity_id', $chunk, 'IN')
          ->execute();
        $stated = [];
        foreach ($state_storage->loadMultiple($state_ids) as $state) {
          $stated[] = (int) $state->get('content_entity_id')->value;
        }
        $missing = array_merge($missing, array_diff(array_map('intval', $chunk), $stated));
      }
      if ($missing) {
        $v[] = count($missing) . " $type of bundle $b have no moderation state in $id, including " . implode(',', array_slice($missing, 0, 20));
      }
    }
  }
}
else {
  throw new \InvalidArgumentException("unknown check '$check'");
}

if ($v) {
  echo implode(PHP_EOL, $v) . PHP_EOL;
  throw new \RuntimeException(count($v) . ' violation(s)');
}
```

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/editorial-workflow/content-moderation-state-machine` | Workflow config shape, state/transition model, `add_moderation` action, transition-permission IDs |
| `drupal/editorial-workflow/content-moderation-existing-content-migration` | The existing-content backfill gotcha and safe resave |
| `drupal/recipes/config-actions-entity-specific` | The config-action mechanism for enabling moderation on bundles |

### Related recipes

- `editorial_roles_permissions` — grants the `use {workflow} transition {id}` permissions this recipe emits, to the editor tier.
