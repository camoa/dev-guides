---
description: GroupRelationType plugin — attribute syntax, derivers, handler system, and enforced plugins
tldr: "Read this when creating a custom group relation type plugin to allow a new entity type (or bundle) to be added to groups."
drupal_version: "11.x"
---

# Plugin System

## When to Use

> Read this when creating a custom group relation type plugin to allow a new entity type (or bundle) to be added to groups.

## Decision

| Situation | Choose | Why |
|---|---|---|
| One specific bundle | Single plugin with `entity_bundle: 'article'` | Simple, direct |
| All bundles of an entity type | Deriver class | Creates one plugin per bundle automatically |
| Plugin on every group type | `enforced: TRUE` | Auto-installs; use sparingly |
| Hide from admin UI | `code_only: TRUE` | Install via code/config only |

## Pattern

```php
use Drupal\group\Plugin\Attribute\GroupRelationType;
use Drupal\group\Plugin\Group\Relation\GroupRelationBase;

#[GroupRelationType(
  id: 'my_module_article',
  entity_type_id: 'node',
  entity_bundle: 'article',        // FALSE to handle all bundles
  label: new TranslatableMarkup('Group article'),
  entity_access: TRUE,             // TRUE = generates CRUD permissions + entity access
  enforced: FALSE,
  pretty_path_key: 'article',
)]
class MyModuleArticle extends GroupRelationBase {
  public function defaultConfiguration() {
    $config = parent::defaultConfiguration();
    $config['entity_cardinality'] = 1; // 0 = unlimited
    return $config;
  }
}
```

To override a handler (e.g., permissions):

```yaml
# mymodule.services.yml
group.relation_handler.permission_provider.my_module_article:
  class: 'Drupal\mymodule\Plugin\Group\RelationHandler\ArticlePermissionProvider'
  arguments: ['@group.relation_handler.permission_provider']
  shared: false
```

## Derivers: One Plugin per Bundle

When you need one plugin per node type (like gnode does), use a deriver:

```php
// Deriver reads all node types and creates a derivative per bundle.
#[GroupRelationType(
  id: 'group_node',
  entity_type_id: 'node',
  entity_access: TRUE,
  deriver: GroupNodeDeriver::class,
)]
class GroupNode extends GroupRelationBase {}

// GroupNodeDeriver:
class GroupNodeDeriver extends DeriverBase {
  public function getDerivativeDefinitions($base_plugin_definition) {
    foreach (NodeType::loadMultiple() as $name => $node_type) {
      $this->derivatives[$name] = clone $base_plugin_definition;
      $this->derivatives[$name]->set('entity_bundle', $name);
      $this->derivatives[$name]->set('label', t('Group node (@type)', ['@type' => $node_type->label()]));
    }
    return $this->derivatives;
  }
}
// Resulting plugin IDs: group_node:article, group_node:page, etc.
```

Invalidate plugin definitions when bundles are created: call `$this->pluginManager->clearCachedDefinitions()` in `hook_ENTITY_TYPE_insert()` for the bundle config entity.

## Plugin Handler System

Rather than cramming all functionality into one class, Group 4.x splits plugin behavior across **handler services**. Every plugin gets six handlers, each with a default implementation and a decorator pattern for overrides.

| Handler Type | Service ID pattern | Interface | Purpose |
|---|---|---|---|
| `access_control` | `group.relation_handler.access_control.{plugin_id}` | `AccessControlInterface` | Entity and relationship access |
| `entity_reference` | `group.relation_handler.entity_reference.{plugin_id}` | `EntityReferenceInterface` | Entity reference field settings |
| `operation_provider` | `group.relation_handler.operation_provider.{plugin_id}` | `OperationProviderInterface` | UI operations (add, edit, delete links) |
| `permission_provider` | `group.relation_handler.permission_provider.{plugin_id}` | `PermissionProviderInterface` | Generate plugin permissions |
| `post_install` | `group.relation_handler.post_install.{plugin_id}` | `PostInstallInterface` | Tasks after plugin is installed |
| `ui_text_provider` | `group.relation_handler.ui_text_provider.{plugin_id}` | `UiTextProviderInterface` | UI labels |

To override a handler, register a service in your module's `services.yml`:

```yaml
# mymodule.services.yml
group.relation_handler.permission_provider.my_module_article:
  class: 'Drupal\mymodule\Plugin\Group\RelationHandler\ArticlePermissionProvider'
  arguments: ['@group.relation_handler.permission_provider']
```

The constructor receives the default handler as a decorator (outer wraps inner). This is the same decorator pattern as Drupal's access control handlers.

## Enforced Plugins

Set `enforced: TRUE` to have the plugin automatically installed on every group type when Group is installed or when `group_rebuild()` fires. The `group_membership` plugin is enforced, which is why every group type always has membership capabilities.

```php
// Group 4.x: src/Hook/CoreHooks.php — enforced plugins are installed automatically.
#[Hook('modules_installed')]
public function modulesInstalled(array $modules, bool $is_syncing): void {
  if (!$is_syncing) {
    $this->groupRelationTypeManager->installEnforced();
  }
}
```

> **3.x:** Group 3.x did this procedurally in `group.module` as `group_modules_installed()`, calling the `_group_relation_type_manager()` helper. Both the `.module` file and that helper were deleted in 4.x.

## Plugin Handler System

Rather than cramming all functionality into one class, Group 4.x splits plugin behavior across **handler services**. Every plugin gets six handlers, each with a default implementation and a decorator pattern for overrides.

| Handler Type | Service ID pattern | Interface | Purpose |
|---|---|---|---|
| `access_control` | `group.relation_handler.access_control.{plugin_id}` | `AccessControlInterface` | Entity and relationship access |
| `entity_reference` | `group.relation_handler.entity_reference.{plugin_id}` | `EntityReferenceInterface` | Entity reference field settings |
| `operation_provider` | `group.relation_handler.operation_provider.{plugin_id}` | `OperationProviderInterface` | UI operations (add, edit, delete links) |
| `permission_provider` | `group.relation_handler.permission_provider.{plugin_id}` | `PermissionProviderInterface` | Generate plugin permissions |
| `post_install` | `group.relation_handler.post_install.{plugin_id}` | `PostInstallInterface` | Tasks after plugin is installed |
| `ui_text_provider` | `group.relation_handler.ui_text_provider.{plugin_id}` | `UiTextProviderInterface` | UI labels |

To override a handler, register a service in your module's `services.yml`:

```yaml
# mymodule.services.yml
group.relation_handler.permission_provider.my_module_article:
  class: 'Drupal\mymodule\Plugin\Group\RelationHandler\ArticlePermissionProvider'
  arguments: ['@group.relation_handler.permission_provider']
```

The constructor receives the default handler as a decorator (outer wraps inner). This is the same decorator pattern as Drupal's access control handlers.

## Enforced Plugins

Set `enforced: TRUE` to have the plugin automatically installed on every group type when Group is installed or when `group_rebuild()` fires. The `group_membership` plugin is enforced, which is why every group type always has membership capabilities.

```php
// Group 4.x: src/Hook/CoreHooks.php — enforced plugins are installed automatically.
#[Hook('modules_installed')]
public function modulesInstalled(array $modules, bool $is_syncing): void {
  if (!$is_syncing) {
    $this->groupRelationTypeManager->installEnforced();
  }
}
```

> **3.x:** Group 3.x did this procedurally in `group.module` as `group_modules_installed()`, calling the `_group_relation_type_manager()` helper. Both the `.module` file and that helper were deleted in 4.x.

## Derivers: One Plugin per Bundle

When you need one plugin per node type (like gnode does), use a deriver:

```php
// Deriver reads all node types and creates a derivative per bundle.
#[GroupRelationType(
  id: 'group_node',
  entity_type_id: 'node',
  entity_access: TRUE,
  deriver: GroupNodeDeriver::class,
)]
class GroupNode extends GroupRelationBase {}

// GroupNodeDeriver:
class GroupNodeDeriver extends DeriverBase {
  public function getDerivativeDefinitions($base_plugin_definition) {
    foreach (NodeType::loadMultiple() as $name => $node_type) {
      $this->derivatives[$name] = clone $base_plugin_definition;
      $this->derivatives[$name]->set('entity_bundle', $name);
      $this->derivatives[$name]->set('label', t('Group node (@type)', ['@type' => $node_type->label()]));
    }
    return $this->derivatives;
  }
}
// Resulting plugin IDs: group_node:article, group_node:page, etc.
```

Invalidate plugin definitions when bundles are created: call `$this->pluginManager->clearCachedDefinitions()` in `hook_ENTITY_TYPE_insert()` for the bundle config entity.

## Common Mistakes

- **Wrong**: Defining handlers without `shared: false` → **Right**: Always add `shared: false` so each plugin gets its own handler instance.
- **Wrong**: Using the old annotation `@GroupContentEnabler` → **Right**: Use the PHP 8 attribute `#[GroupRelationType(...)]`. The annotation class no longer exists.
- **Wrong**: Not clearing plugin cache when adding new bundles → **Right**: Call `$this->pluginManager->clearCachedDefinitions()` in `hook_ENTITY_TYPE_insert()` for the bundle config entity.
- **Wrong**: Forgetting `calculateDependencies()` → **Right**: Add config dependencies for any config entity the plugin depends on (e.g., a node type).

## See Also

- [Configuration](configuration.md)
- [PHP API](php-api.md)
- Reference: `web/modules/contrib/group/src/Plugin/Group/Relation/GroupRelationBase.php`
