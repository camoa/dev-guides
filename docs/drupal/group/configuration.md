---
description: Group YAML configuration — group type, group role, relationship type, global settings, and plugin config schema
tldr: "Reference this when writing or exporting configuration YAML for group types, group roles, relationship types, or plugin config. In 4.x, creator_wizard and use_creation_wizard are removed — drop them from any migrated config."
drupal_version: "11.x"
---

# Configuration

## When to Use

> Reference this when writing or exporting configuration YAML for group types, group roles, relationship types, or plugin config.

## Decision

| Config entity | File pattern | Key constraint |
|---|---|---|
| Group type | `group.type.{id}.yml` | ID max 22 characters |
| Group role (individual) | `group.role.{group_type}-{role}.yml` | `scope: individual`, no `global_role` |
| Group role (outsider) | `group.role.{group_type}-outsider_{drupal_role}.yml` | `scope: outsider`, `global_role: authenticated` |
| Group role (insider) | `group.role.{group_type}-insider_{drupal_role}.yml` | `scope: insider`, `global_role: authenticated` |
| Relationship type | `group.relationship_type.{group_type}-{plugin_id__dots_to_double_underscore}.yml` | ID convention: `{group_type}-{plugin_id}` where `:` → `__` |

## Pattern

```yaml
# config/install/group.type.project.yml
id: project
label: 'Project'
new_revision: true
creator_membership: true   # Auto-adds creator as member — form submissions only in 4.x
creator_roles:
  - project-manager
# Note: creator_wizard is removed in 4.x — do not include it
```

```yaml
# config/install/group.role.project-manager.yml
id: project-manager
label: 'Project Manager'
scope: individual
group_type: project
admin: false
permissions:
  - 'edit group'
  - 'create group_node:article entity'
  - 'update any group_node:article entity'
  - 'delete any group_node:article entity'
```

```yaml
# group.role.project-insider_authenticated.yml
id: project-insider_authenticated
scope: insider
global_role: authenticated
group_type: project
permissions:
  - 'view group'
  - 'view group_node:article entity'
```

```yaml
# group.relationship_type.project-group_node__article.yml
id: project-group_node__article
group_type: project
content_plugin: 'group_node:article'
plugin_config:
  group_cardinality: 0
  entity_cardinality: 1
  # Note: use_creation_wizard is removed in 4.x — do not include it
```

Plugin config schema (required for each `defaultConfiguration()` key):

```yaml
# config/schema/mymodule.schema.yml
group_relation.config.my_setting:
  type: 'boolean'
  label: 'My custom setting label'
```

## Common Mistakes

- **Wrong**: Group type IDs longer than 22 characters → **Right**: `GroupTypeInterface::ID_MAX_LENGTH = 22`. Role IDs append `-anonymous` and must stay under 32 characters total.
- **Wrong**: Deploying relationship type config without the dependent entity config → **Right**: Include `node.type.article` (or equivalent) in the same config import batch.
- **Wrong**: Keeping `creator_wizard` in `group.type.*` config when upgrading to 4.x → **Right**: The 4.x config schema no longer defines it; config validation will flag it.
- **Wrong**: Keeping `use_creation_wizard` in `plugin_config` of relationship type config for 4.x → **Right**: The two-step wizard was removed in 4.x; drop this key from all relationship type config.

## See Also

- [Plugin System](plugin-system.md)
- [Migration from v1/v2](migration-from-v1v2.md)
- Reference: https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/group
