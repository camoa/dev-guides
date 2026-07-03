---
description: The Drupal editorial role model — own-vs-any content permissions, the single-role (content_editor) vs two-tier (author/editor) split, and provisioning permissions through recipe grantPermissions actions rather than baked-in role config.
tldr: "Editorial roles are composed from own/any permission PAIRS (create, edit own/any, delete own/any, view own/any unpublished). Drupal CMS ships one content_editor role whose permissions accrete across recipes; demo_umami ships a two-tier author/editor split. Grant permissions via config actions, never is_admin."
drupal_version: "11.x"
---

# Editorial Role & Permission Model

## When to Use

> When you are provisioning the content roles a site's editors log in as, and must decide how many roles to create and exactly which content permissions each gets. Drupal does not ship a one-size role; you compose the roles from core permission primitives. This guide gives the model — the own/any pairs, the single-role vs two-tier decision, and the correct provisioning mechanism.

## Foundation

Content-entity access in Drupal is granted through **own/any permission pairs**, generated per bundle:

- `create {bundle} content`
- `edit own {bundle} content` / `edit any {bundle} content`
- `delete own {bundle} content` / `delete any {bundle} content`
- `view own unpublished content` / `view any unpublished content`

An **author** tier gets the *own* side (create and manage their own drafts); an **editor** tier gets the *any* side (act on everyone's content and publish). This own/any distinction — not a special module — is what separates the two editorial tiers.

A role is `user.role.{id}` config: `id`, `label`, `weight`, `is_admin` (bool), and a flat `permissions` list. Setting `is_admin: true` makes the role bypass **all** permission checks — that is the administrator posture, never an editorial one. An editorial role always keeps `is_admin: false` and enumerates exactly the permissions it needs.

## Decision

| Situation | Roles to provision | Reference model |
|---|---|---|
| Simple site, one class of trusted editor | A single `content_editor` (own + any + publish) | Drupal CMS `content_editor` |
| Separate draft-writers from publishers | Two tiers: `author` (own) + `editor` (any + workflow publish) | demo_umami `author` / `editor` |
| Role also needs to move content through a workflow | Add the transition permissions `use {workflow} transition {id}` to the *editor* tier | See [Content Moderation State Machine](content-moderation-state-machine.md) |
| A capability beyond content (media, taxonomy) | Add the subsystem permission to the tier that needs it, per bundle | — |

**Do not invent bespoke role names when a shipped reference fits.** Drupal CMS ships a single `content_editor`; the core `demo_umami` profile ships the two-tier `author` + `editor` split. Cite whichever matches, and only diverge with a reason.

## Pattern

The load-bearing detail: in Drupal CMS the `content_editor` role config ships with an **empty** permission list, and permissions are grafted on afterward by **config actions** in each composing recipe (`strict: false`, so each recipe adds its own slice idempotently):

```yaml
# In a recipe.yml — grant permissions to a role via a config action,
# rather than hand-editing user.role.content_editor.yml.
config:
  actions:
    user.role.content_editor:
      grantPermissions:
        - 'access content overview'
        - 'create article content'
        - 'edit own article content'
        - 'view own unpublished content'
```

For per-bundle grants across every content type, core provides the `grantPermissionsForEachNodeType` action so a role's content permissions scale with the content model instead of being frozen at author time. The editor tier additionally receives the *any*-scoped grants and the workflow transition permissions:

```yaml
    user.role.editor:
      grantPermissions:
        - 'edit any article content'
        - 'delete any article content'
        - 'view any unpublished content'
        - 'use editorial transition publish'
```

This recipe-action path is idempotent, composable across recipes, and survives config export/import — unlike hand-edited permission lists, which fight every re-apply.

## Common Mistakes

- **Wrong**: Setting `is_admin: true` on an editorial role to "give it enough access" → **Right**: `is_admin` bypasses every check; editorial roles enumerate specific permissions and stay `is_admin: false`
- **Wrong**: Giving the author tier `edit any` / `delete any` permissions → **Right**: Authors get the *own* side; *any* is the editor/publisher tier
- **Wrong**: Baking the full permission list into `user.role.*.yml` by hand → **Right**: Grant via recipe `grantPermissions` / `grantPermissionsForEachNodeType` config actions so it composes and re-applies cleanly
- **Wrong**: Inventing a `content_author` role and citing it as a Drupal standard → **Right**: Drupal CMS ships only `content_editor`; the two-tier reference is demo_umami's `author`/`editor`
- **Wrong**: Granting a `use {workflow} transition {id}` permission before the workflow exists → **Right**: Provision the workflow first, then hand its transition IDs to the role recipe

## See Also

- [Content Moderation State Machine](content-moderation-state-machine.md) — where the `use {workflow} transition {id}` permissions come from
- [Permissions & Roles](../security/permissions-and-roles.md) — the module-developer view: defining permissions in `*.permissions.yml`
- Reference: [User roles and permissions](https://www.drupal.org/docs/user_guide/en/user-roles.html)
