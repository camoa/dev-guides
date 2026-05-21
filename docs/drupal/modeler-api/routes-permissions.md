---
description: Modeler API auto-generated routes and permissions — naming scheme, permission keys, and access patterns
tldr: "Routes and permissions are generated dynamically at container rebuild; you write no route YAML. configEntityBasePath() must return a non-NULL string for CRUD routes to be generated. Use ModelerApiPermissions::getPermissionKey() to build permission strings programmatically — never hardcode them."
drupal_version: "11.x"
---

# Routes and Permissions

## When to Use

> Use this when setting up access control for a new Model Owner, when debugging a 403 on a modeler route, or when understanding how the auto-generated route scheme is named.

## Decision

Routes and permissions are generated dynamically at container rebuild time by `Routing\Routes::routes()` and `ModelerApiPermissions::permissions()`. You do not write route YAML for Modeler API routes.

**Prerequisite:** `configEntityBasePath()` must return a non-`NULL` string for routing to be generated.

## Pattern

**Auto-generated route names** (for entity type `my_workflow`, base path `admin/config/workflow`):

| Route | URL pattern | Generated when |
|---|---|---|
| `entity.my_workflow.collection` | `/{basePath}` | Always |
| `entity.my_workflow.edit` | `/{basePath}/{id}/edit` | Always |
| `entity.my_workflow.delete_form` | `/{basePath}/{id}/delete` | Entity has `delete` form handler |
| `entity.my_workflow.clone` | `/{basePath}/{id}/clone` | Always |
| `entity.my_workflow.import` | `/{basePath}/import` | Always |
| `entity.my_workflow.export` | `/{basePath}/{id}/export` | Always |
| `entity.my_workflow.export_recipe` | `/{basePath}/{id}/recipe` | Always |
| `entity.my_workflow.enable/disable` | `/{basePath}/{id}/enable\|disable` | Entity type has `status` key |
| `entity.my_workflow.settings` | `/{basePath}/settings` | `settingsForm()` returns a class |
| `modeler_api.add.{owner}.{modeler}` | `/{basePath}/add/{modelerId}` | Per installed modeler |
| `entity.my_workflow.edit_with.{modeler}` | `/{basePath}/{id}/edit_with/{modelerId}` | Per installed modeler |

**Internal API routes** (no base path required):

| Route | URL | Purpose |
|---|---|---|
| `entity.{type}.save` | `/admin/modeler_api/{type}/{modeler_id}/save` | Save endpoint (CSRF-protected) |
| `entity.{type}.config` | `/admin/modeler_api/{type}/{modeler_id}/config` | Config form endpoint |
| `entity.{type}.replay` | `/admin/modeler_api/{type}/replay` | Replay data (if supported) |
| `entity.{type}.test` | `/admin/modeler_api/{type}/test` | Testing (if supported) |

**Permission keys:**

| Operation | Key example | Notes |
|---|---|---|
| `administer` | `modeler api administer my_workflow` | `restrict access: TRUE` |
| `collection` | `modeler api collection my_workflow` | View model list |
| `edit` | `modeler api edit my_workflow` | Edit any model |
| `delete` | `modeler api delete my_workflow` | Delete models |
| `view` | `modeler api view my_workflow` | View in read-only mode |
| `edit` with modeler | `modeler api edit my_workflow with workflow_modeler` | Modeler-specific edit |

```php
use Drupal\modeler_api\ModelerApiPermissions;

$key = ModelerApiPermissions::getPermissionKey('edit', 'my_workflow');
// → 'modeler api edit my_workflow'

$key = ModelerApiPermissions::getPermissionKey('edit', 'my_workflow', 'workflow_modeler');
// → 'modeler api edit my_workflow with workflow_modeler'
```

## Common Mistakes

- **Wrong**: Hardcoding route names or permission strings → **Right**: Use `ModelerApiPermissions::getPermissionKey()` for permissions and the `entity.{type}.{op}` pattern for routes.
- **Wrong**: Granting only `edit` without `view` → **Right**: The `config` and `replay` routes check combined permissions (`edit + view`).
- **Wrong**: Expecting `administer` to appear in role assignment forms by default → **Right**: `restrict access: TRUE` means it does not appear there and requires explicit configuration.

## See Also

- [Registering a Model Owner](registering-model-owner.md)
- Reference: `src/Routing/Routes.php`, `src/ModelerApiPermissions.php`
