---
description: Understand how Drupal tracks config dependencies — modules, themes, config entities — and how they affect import order and deletion.
---

# Config Dependencies

## When to Use

When you need to understand how Drupal tracks which modules, themes, and config entities depend on each other, and how dependencies affect import order and deletion.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Automatic dependency calculation | ConfigEntityBase | Dependencies calculated from plugins, entity references |
| Manual dependency declaration | `dependencies` key in YAML | For enforced or non-calculable dependencies |
| Prevent deletion when in use | Dependency system | Drupal prevents deleting config with dependents |
| Import order guarantee | Dependency system | Config imported in dependency order |
| Uninstall cleanup | Dependency system | Dependent config deleted when dependency uninstalled |

## Dependency Types

**Module Dependencies** — Config depends on module being installed
```yaml
dependencies:
  module:
    - node
    - views
```

**Theme Dependencies** — Config depends on theme being installed
```yaml
dependencies:
  theme:
    - bartik
```

**Config Dependencies** — Config depends on other config existing
```yaml
dependencies:
  config:
    - node.type.article
    - field.storage.node.body
```

**Content Dependencies** — Config depends on content entities (soft dependency)
```yaml
dependencies:
  content:
    - taxonomy_term:tags:1
```

**Enforced Dependencies** — Non-calculable dependencies, must be declared
```yaml
dependencies:
  enforced:
    module:
      - forum
```

**Reference:** `/core/lib/Drupal/Core/Config/Entity/ConfigDependencyManager.php`

## Pattern: Automatic Dependency Calculation

```php
// Config entity automatically calculates dependencies
namespace Drupal\mymodule\Entity;

use Drupal\Core\Config\Entity\ConfigEntityBase;

class Example extends ConfigEntityBase implements ExampleInterface {

  // Entity references automatically create config dependencies
  protected $target_entity_type;
  protected $target_bundle;

  // Plugin collections automatically create module dependencies
  public function getPluginCollections() {
    return [
      'plugin_config' => new DefaultPluginCollection($this->pluginManager, $this->plugin_config),
    ];
  }
}
```

## Pattern: Manual Dependency Declaration

```yaml
# mymodule.example.my_example.yml
id: my_example
label: 'My Example'
# Manual dependencies for special cases
dependencies:
  # Module must be installed
  module:
    - node
    - mymodule
  # Config must exist
  config:
    - node.type.article
  # Enforced — not recalculated on save
  enforced:
    module:
      - mymodule
```

**Reference:** `/core/modules/forum/config/install/node.type.forum.yml` — example with enforced dependency

## Dependency Workflow

**On Config Import:**
1. **Validate dependencies** — Check all dependencies exist or will be imported
2. **Sort by dependencies** — Build dependency graph, topological sort
3. **Import in order** — Dependencies imported before dependents
4. **Fail on circular** — Circular dependencies cause import failure

**On Module Uninstall:**
1. **Find dependents** — Query all config depending on module
2. **Delete dependents first** — Cascade delete in reverse dependency order
3. **Uninstall module** — Remove module config last

**On Config Delete:**
1. **Check for dependents** — Config with dependents can't be deleted
2. **User confirmation** — UI shows dependent config, requires confirmation
3. **Cascade delete** — Delete dependents first (if confirmed)

## Checking Dependencies Programmatically

```php
// Get entity dependencies
$entity = \Drupal::entityTypeManager()
  ->getStorage('example')
  ->load('my_example');
$dependencies = $entity->getDependencies();
// Returns: ['module' => [...], 'config' => [...], ...]

// Find config depending on a specific config
$config_manager = \Drupal::service('config.manager');
$dependents = $config_manager->findConfigEntityDependents('config', ['node.type.article']);

// Check if config has dependents (can't delete)
$has_dependents = !empty($dependents);
```

## Common Mistakes

- Not declaring enforced dependencies — Config not deleted on module uninstall
- Circular dependencies — Import fails, can't deploy config
- Missing module dependencies — Config imports before module enabled, fails
- Deleting config with dependents — Orphaned references, broken site
- Not checking dependencies before delete — User deletes, dependents broken
- Using content dependencies for config — Content dependencies are soft, not enforced

## See Also

- [Config Entities](config-entities.md) — config entity dependencies
- [Config Synchronization](config-synchronization.md) — dependency-aware import
- [Config Installer](config-installer.md) — dependency handling on module install
- Reference: [Configuration Entity Dependencies](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-entity-dependencies)
- Reference: [Config Dependencies Can Optionally Be Enforced](https://www.drupal.org/node/2404447)
