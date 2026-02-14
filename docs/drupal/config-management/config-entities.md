---
description: Create user-manageable config entity types with CRUD operations, dependencies, and admin UI.
---

# Config Entities

## When to Use

When you need to create user-manageable lists of configuration items (like views, image styles, vocabularies) with CRUD operations, dependencies, and admin UI.

## Steps

1. **Define entity type** — Create `MODULE.entity_type.yml` annotation
2. **Create entity class** — Extend `ConfigEntityBase`
3. **Define entity schema** — In `config/schema/MODULE.schema.yml`
4. **Add entity keys** — `id`, `label`, `uuid`, `status`
5. **Create handlers** — Storage, list builder, forms (add, edit, delete)
6. **Define routes** — Collection, add, edit, delete forms
7. **Export default config** — `config/install/MODULE.ENTITY_TYPE.MACHINE_NAME.yml`
8. **Test CRUD** — Create, read, update, delete via UI and API

## Example: Entity Type Definition

```yaml
# mymodule/mymodule.entity_type.yml
example:
  id: example
  label: Example
  label_singular: example
  label_plural: examples
  label_count:
    singular: '@count example'
    plural: '@count examples'
  entity_keys:
    id: id
    label: label
    uuid: uuid
    status: status
  config_prefix: example
  admin_permission: administer examples
  handlers:
    storage: Drupal\Core\Config\Entity\ConfigEntityStorage
    list_builder: Drupal\mymodule\ExampleListBuilder
    form:
      add: Drupal\mymodule\Form\ExampleForm
      edit: Drupal\mymodule\Form\ExampleForm
      delete: Drupal\Core\Entity\EntityDeleteForm
  links:
    collection: /admin/structure/example
    add-form: /admin/structure/example/add
    edit-form: /admin/structure/example/{example}/edit
    delete-form: /admin/structure/example/{example}/delete
  config_export:
    - id
    - label
    - description
    - weight
    - status
```

## Example: Entity Class

```php
namespace Drupal\mymodule\Entity;

use Drupal\Core\Config\Entity\ConfigEntityBase;

/**
 * Defines the Example entity.
 *
 * @ConfigEntityType(
 *   id = "example",
 *   label = @Translation("Example"),
 *   config_prefix = "example",
 *   admin_permission = "administer examples",
 *   entity_keys = {
 *     "id" = "id",
 *     "label" = "label",
 *     "uuid" = "uuid",
 *     "status" = "status"
 *   },
 *   links = {
 *     "collection" = "/admin/structure/example",
 *     "add-form" = "/admin/structure/example/add",
 *     "edit-form" = "/admin/structure/example/{example}/edit",
 *     "delete-form" = "/admin/structure/example/{example}/delete"
 *   }
 * )
 */
class Example extends ConfigEntityBase implements ExampleInterface {

  protected $id;
  protected $label;
  protected $description;
  protected $weight = 0;

  public function getDescription() {
    return $this->description;
  }

  public function getWeight() {
    return $this->weight;
  }
}
```

**Reference:** `/core/lib/Drupal/Core/Config/Entity/ConfigEntityBase.php`, `/core/lib/Drupal/Core/Config/Entity/ConfigEntityInterface.php`

## Common Mistakes

- No config schema defined — Entity won't validate, import/export fails
- Missing entity keys — `id`, `label`, `uuid` required for proper entity handling
- Not setting `config_prefix` — Defaults to module name, causes naming conflicts
- Hardcoded permissions — Use `admin_permission` or dynamic permissions
- No `config_export` list — All properties exported, including internal state
- Not extending ConfigEntityBase — Missing critical methods (save, delete, dependencies)

## See Also

- [Simple Config vs Config Entities](simple-config-vs-config-entities.md) — when to use config entities
- [Config Entity Schema Definition](config-entity-schema-definition.md) — defining entity schema
- [Config Dependencies](config-dependencies.md) — entity dependency management
- Reference: [Creating a Configuration Entity Type](https://www.drupal.org/docs/drupal-apis/configuration-api/creating-a-configuration-entity-type)
