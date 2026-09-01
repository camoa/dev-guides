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

### Group Type Config Schema

```yaml
# config/install/group.type.project.yml
langcode: en
status: true
dependencies: {}
id: project
label: 'Project'
description: 'A project group'
new_revision: true
creator_membership: true   # Group creator auto-gets a membership (form-created groups only)
creator_roles:
  - project-manager        # Role IDs assigned to creator on group creation
```

> **3.x:** Group 3.x group types also had a `creator_wizard` boolean controlling whether the creator had to complete a second membership-config step. The two-step wizard was removed in 4.x, so `creator_wizard` no longer exists — drop it from any config being migrated to 4.x.

### Group Role Config Schema

```yaml
# config/install/group.role.project-manager.yml
langcode: en
status: true
dependencies:
  config:
    - group.type.project
id: project-manager
label: 'Project Manager'
weight: 0
admin: false             # TRUE = bypass all permission checks
scope: individual        # outsider | insider | individual
# global_role: ''        # required for outsider/insider scope only
group_type: project
permissions:
  - 'edit group'
  - 'manage features'
  - 'create group_node:article entity'
  - 'update any group_node:article entity'
  - 'delete any group_node:article entity'
```

#### Synchronized Role Example (insider scope)

```yaml
# group.role.project-insider_authenticated.yml
id: project-insider_authenticated
scope: insider
global_role: authenticated    # Applies when user has Drupal 'authenticated' role AND is a member
group_type: project
permissions:
  - 'view group'
  - 'view group_node:article entity'
```

### Relationship Type Config Schema

```yaml
# config/install/group.relationship_type.project-group_node__article.yml
langcode: en
status: true
dependencies:
  config:
    - group.type.project
    - node.type.article
  module:
    - gnode
id: project-group_node__article
group_type: project
relation_type: 'group_node:article'
plugin_config:
  group_cardinality: 0      # 0 = unlimited
  entity_cardinality: 1     # 1 = a node can only be in this group once
```

ID convention: `{group_type_id}-{plugin_id}` where `:` in plugin IDs is replaced with `__`.

> **The key is `relation_type` as of `4.0.0-alpha2`.** It was `content_plugin` at `4.0.0-alpha1`; the rename (issue #3604203) landed on the dev branch on 2026-06-19 and shipped in `4.0.0-alpha2` on 2026-08-21. `GroupRelationshipType::$content_plugin` became `::$relation_type` with no back-compatible alias, and `group_update_11401()` rewrites existing `group.relationship_type.*` config on update. Verified by reading `src/Entity/GroupRelationshipType.php` at both tags. A site still on `alpha1` keeps `content_plugin` — match the key to your installed tag, and run database updates after the upgrade.

> **3.x:** Group 3.x relationship-type `plugin_config` also accepted a `use_creation_wizard` key (skip/show the two-step creation wizard). It was removed in 4.x along with the wizard. The base `GroupRelationBase::defaultConfiguration()` in 4.x defines only `group_cardinality` and `entity_cardinality`.

## Global Settings

```yaml
# config/install/group.settings.yml
use_admin_theme: false    # Use admin theme for group edit/create forms
```

## Plugin Config Schema Requirements

For every key in `GroupRelationBase::defaultConfiguration()`, you must add a schema entry:

```yaml
# config/schema/mymodule.schema.yml
group_relation.config.my_setting:
  type: 'boolean'
  label: 'My custom setting label'
```

## Common Mistakes

- **Wrong**: Group type IDs longer than 22 characters → **Right**: `GroupTypeInterface::ID_MAX_LENGTH = 22` enforces this. Role IDs append `-anonymous` and must stay under 32 characters total.
- **Wrong**: Forgetting to clear caches after installing new plugin-generated config → **Right**: Relationship types are bundles, and Drupal caches bundle info aggressively — clear caches after install.
- **Wrong**: Deploying relationship type config without the dependent module's entity config → **Right**: Include `node.type.article` (or equivalent) in the same config import batch, or config dependencies will fail during import.
- **Wrong**: Keeping `creator_wizard` in `group.type.*` config when upgrading to 4.x → **Right**: The 4.x config schema no longer defines it; config validation will flag it.
- **Wrong**: Keeping `use_creation_wizard` in `plugin_config` of relationship type config for 4.x → **Right**: The two-step wizard was removed in 4.x; drop this key from all relationship type config.
- **Wrong**: Writing `content_plugin` as the plugin key on `4.0.0-alpha2` → **Right**: The key is `relation_type` as of `4.0.0-alpha2` (renamed in issue #3604203, no back-compatible alias). Only a site still on `4.0.0-alpha1` uses `content_plugin`; run database updates after upgrading so `group_update_11401()` rewrites existing config.

## See Also

- [Plugin System](plugin-system.md)
- [Migration from v1/v2](migration-from-v1v2.md)
- Reference: https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/group
