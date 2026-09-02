---
description: "Use ECA traits for form fields, entity saving, lists, and YAML config to avoid code duplication"
tldr: "Use ECA's built-in traits to avoid duplicating complex logic that's already implemented and tested. Traits encapsulate patterns like form field lookup, entity saving, list operations, and YAML configuration."
drupal_version: "11.x"
---

# Reusable Traits

## When to Use

> Use ECA's built-in traits to avoid duplicating complex logic that's already implemented and tested. Traits encapsulate patterns like form field lookup, entity saving, list operations, and YAML configuration.

## Decision

| Need to... | Use Trait | Benefit |
|------------|-----------|---------|
| Find/modify form fields | `FormFieldPluginTrait` | ~300 lines of field lookup logic |
| Save entities with original tracking | `EntitySaveTrait` + `EntityOriginalTrait` | Proper change detection |
| Count list items | `ListCountTrait` | List/array counting patterns |
| Traverse nested data | `PropertyPathTrait` | Safe nested access |
| Accept YAML config | `FormFieldYamlTrait` | YAML textarea + validation |
| Filter by entity type/bundle | `EntityApplianceTrait` | Entity type matching logic |

## Pattern

```php
use Drupal\eca\Plugin\FormFieldPluginTrait;
use Drupal\eca\Plugin\EntitySaveTrait;
use Drupal\eca_base\Plugin\ListCountTrait;

class MyFormAction extends FormFieldActionBase {

  use FormFieldPluginTrait;  // Provides findFormElement(), getFormElement()
  use EntitySaveTrait;       // Provides saveEntity() with change tracking

  public function execute(): void {
    // Use trait method to find form field
    $field = $this->findFormElement(
      $this->configuration['field_name'],
      $form,
      $form_state
    );

    if ($field) {
      // Modify field value
      $field['#default_value'] = 'New value';
    }

    // Use trait method to save with original tracking
    $entity = $this->getEntity();
    $entity->set('title', 'Updated Title');
    $this->saveEntity($entity);  // Tracks original for comparison
  }
}

class MyListCondition extends ConditionBase {

  use ListCountTrait;  // Provides getListCount()

  public function evaluate(): bool {
    $list_data = $this->tokenService->getTokenData($this->configuration['list_token']);
    $count = $this->getListCount($list_data);
    $result = $count > 5;

    return $this->negationCheck($result);
  }
}
```

## Common Mistakes

- Duplicating trait logic in your plugin → Maintenance nightmare when ECA updates
- Using wrong trait for the job → FormFieldPluginTrait requires FormFieldActionBase
- Not reading trait source code → Missing useful methods the trait provides
- Trait method name conflicts → Use `use TraitName { method as renamedMethod; }`
- Reimplementing what traits provide → Wasted effort, bugs

## See Also

- [Action Plugin Basics](action-plugin-basics.md) for base classes
- [Service Injection](service-injection.md) for services vs traits
- [Common Pitfalls](common-pitfalls.md) for trait usage errors

**References:**
- Traits: `/modules/contrib/eca/src/Plugin/` (FormFieldPluginTrait, FormFieldYamlTrait, etc.)
- Trait: `/modules/contrib/eca/modules/content/src/Plugin/EntitySaveTrait.php`
- Traits: `/modules/contrib/eca/modules/base/src/Plugin/` (ListCountTrait)
