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

## Common Mistakes

- **Wrong**: Defining handlers without `shared: false` → **Right**: Always add `shared: false` so each plugin gets its own handler instance.
- **Wrong**: Using the old annotation `@GroupContentEnabler` → **Right**: Use the PHP 8 attribute `#[GroupRelationType(...)]`. The annotation class no longer exists.
- **Wrong**: Not clearing plugin cache when adding new bundles → **Right**: Call `$this->pluginManager->clearCachedDefinitions()` in `hook_ENTITY_TYPE_insert()` for the bundle config entity.
- **Wrong**: Forgetting `calculateDependencies()` → **Right**: Add config dependencies for any config entity the plugin depends on (e.g., a node type).

## See Also

- [Configuration](configuration.md)
- [PHP API](php-api.md)
- Reference: `web/modules/contrib/group/src/Plugin/Group/Relation/GroupRelationBase.php`
