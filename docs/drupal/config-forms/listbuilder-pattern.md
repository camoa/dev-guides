---
description: Build entity collection admin pages with ListBuilder
drupal_version: "11.x"
---

# ListBuilder Pattern

## When to Use

> Use ListBuilder when building entity collection admin pages with standard CRUD operations.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Config entity collection | ConfigEntityListBuilder | For config entities, automatic enable/disable |
| Content entity collection | EntityListBuilder | For content entities, supports bulk operations |
| Draggable ordering | DraggableListBuilder | Weight-based ordering built-in |
| Custom operations only | Override getDefaultOperations() | Keep automatic features, add custom links |

## Pattern

**Entity Annotation** (src/Entity/MyConfigEntity.php):
```php
/**
 * @ConfigEntityType(
 *   id = "my_config_entity",
 *   label = @Translation("My Config Entity"),
 *   handlers = {
 *     "list_builder" = "Drupal\mymodule\MyConfigEntityListBuilder",
 *     "form" = {
 *       "add" = "Drupal\mymodule\Form\MyConfigEntityForm",
 *       "edit" = "Drupal\mymodule\Form\MyConfigEntityForm",
 *       "delete" = "Drupal\Core\Entity\EntityDeleteForm"
 *     }
 *   },
 *   config_prefix = "my_config_entity",
 *   entity_keys = {
 *     "id" = "id",
 *     "label" = "label",
 *   },
 *   links = {
 *     "collection" = "/admin/config/mymodule/entities",
 *     "add-form" = "/admin/config/mymodule/entities/add",
 *     "edit-form" = "/admin/config/mymodule/entities/{my_config_entity}/edit",
 *     "delete-form" = "/admin/config/mymodule/entities/{my_config_entity}/delete"
 *   }
 * )
 */
```

**ListBuilder** (src/MyConfigEntityListBuilder.php):
```php
namespace Drupal\mymodule;

use Drupal\Core\Config\Entity\ConfigEntityListBuilder;
use Drupal\Core\Entity\EntityInterface;

class MyConfigEntityListBuilder extends ConfigEntityListBuilder {

  public function buildHeader() {
    $header['label'] = $this->t('Label');
    $header['status'] = $this->t('Status');
    return $header + parent::buildHeader(); // Adds Operations column
  }

  public function buildRow(EntityInterface $entity) {
    $row['label'] = $entity->label();
    $row['status'] = $entity->status() ? $this->t('Enabled') : $this->t('Disabled');
    return $row + parent::buildRow($entity); // Adds operations dropbutton
  }

  public function getDefaultOperations(EntityInterface $entity) {
    $operations = parent::getDefaultOperations($entity); // Edit, Delete, Enable, Disable

    // Add custom operation
    if ($entity->hasLinkTemplate('duplicate')) {
      $operations['duplicate'] = [
        'title' => $this->t('Duplicate'),
        'url' => $entity->toUrl('duplicate'),
        'weight' => 15,
      ];
    }

    return $operations;
  }
}
```

**Routing** (mymodule.routing.yml):
```yaml
entity.my_config_entity.collection:
  path: '/admin/config/mymodule/entities'
  defaults:
    _entity_list: 'my_config_entity'
    _title: 'My Config Entities'
  requirements:
    _permission: 'administer mymodule'
```

## Common Mistakes

- **Wrong**: Using _controller instead of _entity_list in routing → **Right**: List builder won't be invoked
- **Wrong**: Overriding render() instead of buildRow/buildHeader → **Right**: Loses automatic features
- **Wrong**: Not calling parent::buildRow/buildHeader → **Right**: Operations column missing
- **Wrong**: Hardcoding operations instead of using getDefaultOperations() → **Right**: Can't be altered by other modules
- **Wrong**: Forgetting to add link templates in entity annotation → **Right**: Operations won't work

## See Also

- [FormBase vs ListBuilder](formbase-vs-listbuilder.md)
- [Operations Implementation](operations-implementation.md)
- Reference: [Creating a Configuration Entity Type](https://www.drupal.org/docs/drupal-apis/configuration-api/creating-a-configuration-entity-type)
- Reference: core/modules/menu_link_content/src/MenuLinkContentListBuilder.php
