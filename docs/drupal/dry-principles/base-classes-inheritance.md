---
description: Extend Drupal core base classes and create project-specific base classes to eliminate duplication across entities, forms, and blocks.
---

# Base Classes and Inheritance

## When to Use

When you have multiple classes of the same type (entities, forms, blocks, controllers) that share common patterns or need to override specific base functionality.

## Core Base Classes

| Base Class | Extends From | Use When |
|-----------|--------------|----------|
| `ContentEntityBase` | `EntityBase` | Creating content entity types (nodes, users, custom entities) |
| `ConfigEntityBase` | `EntityBase` | Creating config entity types (views, field configs) |
| `FormBase` | - (implements `FormInterface`) | Creating forms (uses traits for common services) |
| `ConfigFormBase` | `FormBase` | Creating admin forms that save to config |
| `BlockBase` | `PluginBase` | Creating block plugins |
| `PluginBase` | - | Creating any plugin type |
| `ControllerBase` | - | Creating controllers (uses traits) |

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Custom content entity | Extend `ContentEntityBase` | Field API support, revisions, translations |
| Custom admin form | Extend `ConfigFormBase` | Built-in config save/load methods |
| Custom block | Extend `BlockBase` | Context, caching, plugin scaffolding |
| Multiple similar custom forms | Create shared base class extending `FormBase` | Reuse common methods, eliminate duplication |
| Override parent constructor | Call `parent::__construct()` AND override `create()` | Maintain proper DI chain |

## Pattern

```php
// Extending core base class
namespace Drupal\mymodule\Entity;

use Drupal\Core\Entity\ContentEntityBase;
use Drupal\Core\Entity\EntityTypeInterface;
use Drupal\Core\Field\BaseFieldDefinition;

class MyEntity extends ContentEntityBase {

  public static function baseFieldDefinitions(EntityTypeInterface $entity_type) {
    $fields = parent::baseFieldDefinitions($entity_type);

    $fields['name'] = BaseFieldDefinition::create('string')
      ->setLabel(t('Name'))
      ->setRequired(TRUE);

    return $fields;
  }
}
```

```php
// Creating project-specific base class
namespace Drupal\mymodule\Form;

use Drupal\Core\Form\FormBase;

abstract class MyProjectFormBase extends FormBase {

  // Shared validation logic
  protected function validateEmail(string $email): bool {
    return filter_var($email, FILTER_VALIDATE_EMAIL);
  }

  // Shared submission patterns
  protected function logFormSubmission(string $form_id): void {
    $this->getLogger('mymodule')->info('Form @id submitted', ['@id' => $form_id]);
  }
}
```

Reference: `core/lib/Drupal/Core/Entity/ContentEntityBase.php`, `core/lib/Drupal/Core/Form/FormBase.php`, `core/lib/Drupal/Core/Block/BlockBase.php`

## Common Mistakes

- **Deep inheritance hierarchies** — Keep inheritance shallow (2-3 levels max); prefer composition via traits or services
- **Overriding constructors without calling parent** — Always call `parent::__construct()` and override `create()` method for DI
- **Creating base classes prematurely** — Wait until you have 3+ similar classes before creating a shared base class
- **God base classes with too many methods** — Keep base classes focused; use traits for orthogonal concerns
- **Forgetting to extend from correct core base** — `FormBase` for forms, `ContentEntityBase` for content entities, `BlockBase` for blocks

## See Also

- [Services for Shared Logic](services-shared-logic.md)
- [Traits for Cross-Cutting Concerns](traits-cross-cutting.md)
- Reference: [Extending Drupal Base Classes Without Overriding Constructors](https://www.hashbangcode.com/article/drupal-9-extending-drupal-base-classes-without-overriding-constructors)
- Reference: `core/lib/Drupal/Core/Entity/ContentEntityBase.php`
