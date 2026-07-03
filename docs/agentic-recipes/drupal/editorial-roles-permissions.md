---
# Routing block — an orchestrator reads to here and decides.
name: editorial_roles_permissions
capability: editorial-roles-permissions-provisioning
description: Use when a site needs its editorial content roles — deciding a single content_editor vs a two-tier author/editor split, granting own-vs-any content permissions (and any workflow-transition permissions) per bundle through recipe config actions, never via is_admin.
# Metadata — read only after a match.
label: Editorial roles & permissions
recipe_schema_version: 1.0.0
version: 0.1.0
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
- Setting `is_admin: true` on an editorial role.
- Baking the permission list into `user.role.*.yml` by hand instead of via config actions.
- Citing a `content_author` role as a Drupal standard (it does not ship).
- Granting a `use {workflow} transition {id}` permission before that workflow/transition exists.

## Preconditions

- Drupal 10.4+ or 11.x; the core `user` and `node` modules.
- The content bundles the roles will act on exist.
- If transition permissions are in scope, the moderation workflow exists first (see the content-moderation recipe).
- Config export is in use, so the roles and grants are deployable.

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

3. **Derive the per-bundle permission set by tier.** Author tier → own-scoped grants; editor tier → any-scoped grants plus publish. Expand across `bundles`. See `drupal/editorial-workflow/editorial-role-permission-model`.

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

After the recipe runs, verify:

1. Each requested role exists with the expected `id` and `is_admin: false`.
2. The author tier has only *own*-scoped content permissions for its bundles; the editor tier has the *any*-scoped set plus publish — no tier has more than its model allows.
3. No editorial role is `is_admin: true`.
4. When workflow transitions were supplied, the editor tier has exactly the `use {workflow} transition {id}` permissions requested, and no permission references a nonexistent workflow/transition.
5. A second apply produces no config changes (idempotent).

The recipe ships no verifier *script*, but every check is **agent-runnable**. All five are `config-assert` (drush + config reads, no served site needed), so none is fail-closed on the absence of a served site.

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/editorial-workflow/editorial-role-permission-model` | Own/any model, single-vs-two-tier decision, shipped references, grant-via-config-actions |
| `drupal/security/permissions-and-roles` | Role config structure and the permission system |
| `drupal/recipes/config-actions-entity-specific` | `grantPermissions` / `grantPermissionsForEachNodeType` config actions |

### Related recipes

- `content_moderation_workflow` — provisions the workflow and emits the transition IDs this recipe grants to the editor tier.
