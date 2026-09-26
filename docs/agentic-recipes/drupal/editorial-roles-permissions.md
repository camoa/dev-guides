---
# Routing block — an orchestrator reads to here and decides.
name: editorial_roles_permissions
capability: editorial-roles-permissions-provisioning
description: Use when a site needs its editorial content roles — deciding a single content_editor vs a two-tier author/editor split, granting own-vs-any content permissions (and any workflow-transition permissions) per bundle through recipe config actions, never via is_admin.
# Metadata — read only after a match.
label: Editorial roles & permissions
recipe_schema_version: 1.0.0
version: 0.2.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/editorial-workflow/editorial-role-permission-model
  - drupal/security/permissions-and-roles
  - drupal/recipes/config-actions-entity-specific
drupal_compatibility: "^10.4 || ^11"
requires_modules:
  - user
  - node
authors:
  - name: Palcera
license: GPL-2.0-or-later
---

## Goal

Provision a site's editorial roles (`user.role.*`) and their content permissions — choosing a single `content_editor` or a two-tier `author`/`editor` split, granting the correct own-vs-any permission set per content bundle (and, when a workflow exists, its transition permissions) through idempotent recipe config actions — so editors can do exactly their job and nothing more, and the grants survive config export/import.

## Opinion

**Compose roles from own/any permission pairs.** The author tier gets the *own* side (`create`, `edit own`, `delete own`, `view own unpublished`); the editor tier gets the *any* side plus publishing. This own/any split — not a special module — is what separates the tiers. Source: guide `drupal/editorial-workflow/editorial-role-permission-model`.

**Cite a shipped reference, don't invent roles.** Drupal CMS ships a single `content_editor`; the core `demo_umami` profile ships the two-tier `author`/`editor`. Match whichever fits the site and diverge only with a reason. Note there is no `content_author` role in Drupal CMS — do not cite one. Source: guide `drupal/editorial-workflow/editorial-role-permission-model`.

**Grant through config actions, never bake permissions into role YAML.** Use `grantPermissions` (and `grantPermissionsForEachNodeType` for per-bundle scaling) with `strict: false`, so grants compose across recipes and re-apply cleanly. Source: guides `drupal/editorial-workflow/editorial-role-permission-model`, `drupal/recipes/config-actions-entity-specific`.

**Editorial roles are never `is_admin`.** `is_admin: true` bypasses all permission checks — that is the administrator posture. An editorial role keeps `is_admin: false` and enumerates exactly the permissions it needs. Source: guide `drupal/editorial-workflow/editorial-role-permission-model`.

**Workflow-transition permissions are consumed, not authored here.** When a moderation workflow exists, the editor tier receives its `use {workflow} transition {id}` permissions — but this recipe does not create the workflow; it takes the transition IDs as input. Source: guide `drupal/editorial-workflow/editorial-role-permission-model`.

### What this recipe refuses

- Granting the author tier `edit any` / `delete any` permissions.
- Granting `bypass node access` or `administer nodes` to an author- or editor-tier role.
- Setting `is_admin: true` on an editorial role.
- Baking the permission list into `user.role.*.yml` by hand instead of via config actions.
- Citing a `content_author` role as a Drupal standard (it does not ship).
- Granting a `use {workflow} transition {id}` permission before that workflow/transition exists.

## Preconditions

- Drupal 10.4+ or 11.x; the core `user` and `node` modules.
- The content bundles the roles will act on exist.
- If transition permissions are in scope, the moderation workflow exists first (see the content-moderation recipe).
- Config export is in use, so the roles and grants are deployable.
- DDEV runs the site; the verifier's commands go through `ddev`.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
roles:
  - id: string                 # e.g. content_editor, author, editor
    label: string
    tier: string               # author (own) | editor (any + publish) | custom
    bundles:                   # content types this role acts on
      - string
    extra_permissions:         # subsystem grants beyond content (media, taxonomy…)
      - string

workflow_transitions:          # optional; consumed, not created here
  workflow_id: string
  grant_to_role: string        # usually the editor tier
  transition_ids:
    - string
```

## Sequence

If invoked in dry-run mode, perform all reads and derivations but emit a preview instead of writing config. Dry-run is required.

1. **Resolve the role model.** Decide single `content_editor` vs two-tier `author`/`editor` from input; map each role to a shipped reference where one fits. See `drupal/editorial-workflow/editorial-role-permission-model`.

2. **Create each role if absent** — `user.role.{id}` with `id`/`label`/`weight` and `is_admin: false`; if present, skip creation. See `drupal/security/permissions-and-roles`.

3. **Derive the per-bundle permission set by tier.** Author tier → own-scoped grants; editor tier → any-scoped grants plus publish, where publish means the workflow's transition permissions from step 5. Without a workflow the editor tier does not publish, because core then needs `administer nodes`, which this recipe refuses. Expand across `bundles`. See `drupal/editorial-workflow/editorial-role-permission-model`.

4. **Grant via config actions** — `grantPermissions` (or `grantPermissionsForEachNodeType` for all-bundle scaling) with `strict: false`; add `extra_permissions` to the tier that needs them. Never hand-edit the role's permission list. See `drupal/recipes/config-actions-entity-specific`.

5. **Grant workflow-transition permissions if supplied** — add `use {workflow_id} transition {id}` for each `transition_ids` entry to `grant_to_role`. Do not create the workflow. See `drupal/editorial-workflow/editorial-role-permission-model`.

6. **Export configuration, rebuild caches, and emit a summary** of roles created/no-op and the permissions granted per role, flagging any requested permission that does not exist (e.g. a transition whose workflow is absent).

## Data flow

```
input: roles[] (id, label, tier, bundles[], extra_permissions[])
       workflow_transitions (workflow_id, grant_to_role, transition_ids[])

reads project state:
       user.role.*               (existing roles + current grants)
       node type list            (bundles to expand own/any grants across)
       workflows.workflow.*       (to validate transition IDs, when supplied)

applies opinion (guardrails):
       own/any-by-tier · cite-shipped-reference · grant-via-config-actions ·
       never-is_admin · transitions-are-consumed-not-authored

references atomic detail (guides):
       drupal/editorial-workflow/editorial-role-permission-model
       drupal/security/permissions-and-roles
       drupal/recipes/config-actions-entity-specific

emits:
       user.role.<id>            (is_admin: false; permissions via grantPermissions)
       per-bundle content grants (own for author, any+publish for editor)
       use <workflow> transition <id>  (on the editor tier, when supplied)
```

## State-awareness contract

The recipe reads existing state before writing. For each role: absent → create; present and matching → skip, log no-op; present and differing in identity (label/weight/is_admin) → conflict, do not overwrite, request operator review. Permission grants are **additive** — granting a permission a role lacks is a create; the recipe never revokes a permission implicitly.

Granting a `use {workflow} transition {id}` permission whose workflow or transition does not exist is a **conflict**, surfaced for review, not silently written — it depends on the content-moderation recipe having run first.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run.

## Verifier

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only; a non-interactive `ddev drush` keeps Drush's messages on standard error. A stopped DDEV project prints its start-up text on standard output, so start the site before the verify run. Entries that call `.aida/editorial-roles-permissions/verify.php` run the script in `## Files`. It prints one line per violation and exits non-zero when it printed any.

verifier:
  - id: roles-exist-not-admin
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/editorial-roles-permissions/verify.php -- roles {roles:json}
    pass: stdout empty
  - id: tier-permissions
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/editorial-roles-permissions/verify.php -- tiers {roles:json}
    pass: stdout empty
  - id: transition-permissions
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/editorial-roles-permissions/verify.php -- transitions {workflow_transitions:json}
    pass: stdout empty
  - id: active-equals-export
    kind: config-assert
    run: ddev drush config:status
    pass: stdout empty

What the entries do not prove, and where the proof is:

- `tier-permissions` requires, per bundle, `create`, `edit own` and `delete own` on the author tier, and `edit any` and `delete any` on the editor tier. It refuses `edit any` and `delete any` on the author tier, and `bypass node access` and `administer nodes` on both. It skips the `custom` tier. It does not check that `extra_permissions` were granted, but the refusal reads every permission the role holds, so `bypass node access` or `administer nodes` granted as an extra still fails it.
- Core has no per-bundle node permission to publish. The editor tier's publishing is its transition permissions, which `transition-permissions` checks. Without a workflow, publishing is not checked.
- `transition-permissions` checks nothing when `workflow_transitions` is absent. When it is given, `grant_to_role` must hold each requested transition permission and no other of that workflow's, and each must be a permission the site defines.
- `active-equals-export` proves the export is current after Sequence step 6. The state-awareness contract makes a second apply a no-op on that state.

## Files

One script, which the consumer writes before the verifier runs and removes after it. Do not edit it or commit it. Drush runs it with Drupal booted and passes the words after `--` in `$extra`.

```php .aida/editorial-roles-permissions/verify.php
<?php

use Drupal\user\Entity\Role;

// Verifier checks for editorial-roles-permissions.
// $extra: roles <roles JSON> | tiers <roles JSON> | transitions <workflow_transitions JSON>
// Prints one line per violation, then throws so Drush exits non-zero.
$check = $extra[0] ?? '';
$input = json_decode($extra[1] ?? 'null', TRUE, 512, JSON_THROW_ON_ERROR);
$v = [];

if ($check === 'roles' || $check === 'tiers') {
  if (!is_array($input) || !$input) {
    $v[] = "$check: the roles input is missing or empty";
  }
  foreach ((array) $input as $spec) {
    $id = $spec['id'] ?? '';
    $role = $id === '' ? NULL : Role::load($id);
    if (!$role) {
      $v[] = "role '$id' does not exist";
      continue;
    }
    if ($check === 'roles') {
      if ($role->isAdmin()) {
        $v[] = "role $id has is_admin: true";
      }
      continue;
    }
    $tier = $spec['tier'] ?? '';
    if ($tier === 'custom') {
      continue;
    }
    if (!in_array($tier, ['author', 'editor'], TRUE)) {
      $v[] = "role $id has tier '$tier', not author, editor or custom";
      continue;
    }
    $must = [];
    $must_not = ['bypass node access', 'administer nodes'];
    foreach ($spec['bundles'] ?? [] as $b) {
      if ($tier === 'author') {
        array_push($must, "create $b content", "edit own $b content", "delete own $b content");
        array_push($must_not, "edit any $b content", "delete any $b content");
      }
      else {
        array_push($must, "edit any $b content", "delete any $b content");
      }
    }
    $held = $role->getPermissions();
    foreach (array_diff($must, $held) as $permission) {
      $v[] = "role $id ($tier) lacks '$permission'";
    }
    foreach (array_intersect($must_not, $held) as $permission) {
      $v[] = "role $id ($tier) holds '$permission'";
    }
  }
}
elseif ($check === 'transitions') {
  if ($input !== NULL) {
    $workflow = $input['workflow_id'] ?? '';
    $grantee = $input['grant_to_role'] ?? '';
    $role = $grantee === '' ? NULL : Role::load($grantee);
    $want = [];
    foreach ($input['transition_ids'] ?? [] as $transition) {
      $want[] = "use $workflow transition $transition";
    }
    if ($workflow === '' || !$want) {
      $v[] = 'transitions: the workflow id or transition ids are missing';
    }
    elseif (!$role) {
      $v[] = "role '$grantee' does not exist";
    }
    else {
      $defined = \Drupal::service('user.permissions')->getPermissions();
      $held = array_filter($role->getPermissions(), fn($p) => str_starts_with($p, "use $workflow transition "));
      foreach (array_diff($want, $held) as $permission) {
        $v[] = "role $grantee lacks '$permission'";
      }
      foreach (array_diff($held, $want) as $permission) {
        $v[] = "role $grantee holds '$permission', which was not requested";
      }
      foreach ($want as $permission) {
        if (!isset($defined[$permission])) {
          $v[] = "'$permission' is not a permission this site defines";
        }
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
| `drupal/editorial-workflow/editorial-role-permission-model` | Own/any model, single-vs-two-tier decision, shipped references, grant-via-config-actions |
| `drupal/security/permissions-and-roles` | Role config structure and the permission system |
| `drupal/recipes/config-actions-entity-specific` | `grantPermissions` / `grantPermissionsForEachNodeType` config actions |

### Related recipes

- `content_moderation_workflow` — provisions the workflow and emits the transition IDs this recipe grants to the editor tier.
