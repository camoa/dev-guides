---
description: Collect input values interactively via CLI or web forms before applying recipe
drupal_version: "11.x"
---

# Input Collection & Forms

## When to Use

> Use input collection when you need to gather user-provided values interactively before applying a recipe.

## Decision

| Context | Tool | Why |
|---------|------|-----|
| Applying via CLI with Drush | `drush recipe` | Auto-prompts for inputs |
| Applying via CLI without Drush | `php core/scripts/drupal recipe` | Prompts via Symfony Console |
| Applying via web with custom workflow | Implement form with RecipeInputFormTrait | Custom form integration |
| Validating inputs with constraints | Validation happens after collection | Before application |

## Pattern

CLI collection via Drush (automatic):

```bash
drush recipe recipes/my_recipe
# Prompts for each input defined in recipe.yml
```

Custom CLI collector (implement InputCollectorInterface):

```php
use Drupal\Core\Recipe\InputCollectorInterface;

class CustomCollector implements InputCollectorInterface {
  public function collectValue(string $name, DataDefinitionInterface $definition, mixed $default): mixed {
    // Custom logic to collect value
    return $this->askUser($definition->getDescription(), $default);
  }
}
```

Web form collection (use RecipeInputFormTrait):

```php
use Drupal\Core\Recipe\RecipeInputFormTrait;

class RecipeApplyForm extends FormBase {
  use RecipeInputFormTrait;

  public function buildForm(array $form, FormStateInterface $form_state, Recipe $recipe = NULL) {
    $form += $this->buildRecipeInputForm($recipe);
    return $form;
  }
}
```

Input substitution in config actions:

```yaml
input:
  theme_name:
    data_type: string
    default: { source: value, value: olivero }
config:
  actions:
    system.theme:
      simpleConfigUpdate:
        default: ${theme_name}
```

## Common Mistakes

- **Wrong**: Not implementing InputCollectorInterface correctly → **Right**: Must return value matching data_type; validation errors are cryptic
- **Wrong**: Forgetting inputs are recursive → **Right**: Recipe dependencies' inputs also collected; can overwhelm users
- **Wrong**: Using inputs in config import → **Right**: Inputs only work in config actions, not config file names
- **Wrong**: Not handling validation failures → **Right**: ConstraintViolationList exceptions throw if input violates constraints
- **Wrong**: Assuming inputs persist → **Right**: Input values only available during recipe application; not stored anywhere

## See Also

- [Input System - Default Sources](input-default-sources.md)
- [Default Content - Overview](default-content-overview.md)
- Reference: `core/lib/Drupal/Core/Recipe/InputConfigurator.php` (collectAll method)
