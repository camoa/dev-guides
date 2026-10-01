---
description: "Use the drupal/tool_belt catalog of 58 ready-made Tool API tools, and avoid its entity_save validation trap"
tldr: "Check tool_belt 1.0.0-alpha6 before writing a tool for a common core task; it ships 58 tools in eight submodules. Gotcha: tool_belt:entity_save saves without entity validation; use entity_create or entity_update."
drupal_version: "^10.5 || ^11"
---

# Tool Belt Catalog

## When to Use

> Use this before writing a Tool API plugin for a common core task. `drupal/tool_belt` 1.0.0-alpha6 ships 58 tool plugins in eight submodules; check it first, and know its `entity_save` trap.
>
> **Version:** applies to `drupal/tool_belt` 1.0.0-alpha6 (alpha; no security advisory coverage) on `drupal/tool` 1.0.0-beta10 or later. Paths are under `modules/contrib/tool_belt/`.

## What It Is

Facts from tool_belt 1.0.0-alpha6: core `^10.5 || ^11 || ^12`, requires `drupal/tool ^1.0.0-beta10`. Every tool ID starts with `tool_belt:`. No tool declares a `permission:`; each uses a `checkAccess()` override.

| Submodule | Tools | Examples |
|---|---|---|
| `tool_belt_content` | 15 | `entity_create`, `entity_update`, `entity_save`, `entity_delete`, `entity_list`, `entity_load_by_id`, `entity_stub`, `field_set_value`, `text_format_preview` |
| `tool_belt_entity` | 14 | `entity_bundle_add`, `field_storage_add`, `field_add`, `field_delete`, `entity_type_list` |
| `tool_belt_workspace` | 10 | `workspace_create`, `workspace_publish`, `workspace_revert` |
| `tool_belt_image_style` | 6 | `image_style_add`, `image_effect_add` |
| `tool_belt_content_moderation` | 4 | `moderation_state_get`, `moderation_state_set` |
| `tool_belt_user` | 4 | `user_block`, `user_add_role` |
| `tool_belt_system` | 4 | `send_email`, `log_message`, `system_status` |
| `tool_belt_content_translation` | 1 | `entity_translation_get` |

Nine tools set `destructive: TRUE`: `entity_delete`, `entity_bundle_delete`, `field_delete`, `field_storage_delete`, `image_style_delete`, `image_effect_remove`, `workspace_delete`, `workspace_publish`, `workspace_revert`.

## The entity_save Trap

`tool_belt:entity_save` saves without validating the entity:

```php
// tool_belt 1.0.0-alpha6 modules/tool_belt_content/src/Plugin/tool/Tool/EntitySave.php
try {
  $op = $entity->isNew() ? $this->t('created') : $this->t('updated');
  $entity->save();
```

`save()` does not run entity validation. Entity-level constraints, and field constraints on fields the caller did not touch, are skipped. `field_set_value` validates only the one field it sets. So the chain `entity_stub → field_set_value → entity_save` can store an entity that `$entity->validate()` would reject. `entity_create` and `entity_update` call a `validateEntity()` helper that runs `$entity->validate()` before `save()` (tool_belt 1.0.0-alpha6 `modules/tool_belt_content/src/OneShotEntityFieldsTrait.php`).

## Decision

| If you need to... | Use... |
|---|---|
| Create or update content in one call, with validation | `tool_belt:entity_create` or `tool_belt:entity_update` |
| Build an entity across several calls | `entity_stub` + `field_set_value`, then a tool that validates before saving, or your own save tool |
| Delete or restructure config | The `tool_belt_entity` tools, behind tight access and `destructive` handling |
| A tool Tool Belt lacks | Write one; see [Defining a Tool](defining-a-tool.md) |

## Common Mistakes

- Exposing `entity_save` to an agent and trusting entity constraints to hold → they do not run
- Enabling all eight submodules → enable only what callers need; each tool is another callable surface
- Calling `entity_save` from Drush → its `entity` input needs a handle-capable caller; see [Entity Inputs and Handles](entity-inputs-and-handles.md)
- Assuming Tool Belt failure messages are safe for LLMs → several return `$e->getMessage()`
- Trusting `entity_field_values` field access for a passed account → it checks the current user; see [Access Control](access-control.md)

## See Also

- [Entity Inputs and Handles](entity-inputs-and-handles.md) → why entity tools need handles
- [Security Checklist](security-best-practices.md)
- Reference: `modules/contrib/tool_belt/modules/tool_belt_content/src/Plugin/tool/Tool/EntitySave.php`, `modules/contrib/tool_belt/modules/tool_belt_content/src/OneShotEntityFieldsTrait.php`, https://www.drupal.org/project/tool_belt
