---
description: Custom bundle entity classes for programmatic content type creation
drupal_version: "11.x"
---

# Bundle Entity Implementation

## When to Use

When building custom content entity types that need bundle support (multiple subtypes with different field configurations), requiring programmatic bundle creation or custom bundle behavior.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Standard node bundles | NodeType entity | Built-in, field UI integrated, well supported |
| Custom entity bundles | Custom ConfigEntityBundleBase | Full control over bundle properties and behavior |
| Dynamic bundle creation | EntityTypeManager::create() | Runtime bundle creation without config files |

## Pattern

Bundle entity class with PHP 8 attributes:

```php
namespace Drupal\my_module\Entity;

use Drupal\Core\Config\Entity\ConfigEntityBundleBase;
use Drupal\Core\Entity\Attribute\ConfigEntityType;

#[ConfigEntityType(
  id: 'my_content_type',
  label: new TranslatableMarkup('My Type'),
  config_prefix: 'type',
  bundle_of: 'my_content',      // Links to content entity
  entity_keys: ['id' => 'id', 'label' => 'label'],
  config_export: ['id', 'label', 'description'],
  admin_permission: 'administer my content types',
)]
class MyContentType extends ConfigEntityBundleBase {
  protected string $id;
  protected string $label;
  protected string $description = '';
}
```

Reference: `/core/modules/node/src/Entity/NodeType.php`

## Common Mistakes

- **Wrong**: Missing bundle_of attribute → **Right**: Content entity won't link to bundles; field UI won't work
- **Wrong**: Not extending ConfigEntityBundleBase → **Right**: You'll lose bundle-specific functionality like bundle classes
- **Wrong**: Forgetting config_export → **Right**: Bundle properties won't save to YAML; lost on config export
- **Wrong**: Missing admin_permission → **Right**: No access control on bundle management
- **Wrong**: Using wrong entity keys → **Right**: Must include at minimum 'id' and 'label' for proper display

## See Also

- [Content Type Configuration](content-type-configuration.md)
- [Base Field Definitions](base-field-definitions.md) for adding fields to bundles
- Reference: [Creating a content entity type](https://www.drupal.org/docs/drupal-apis/entity-api/creating-a-content-entity-type)
