---
description: Collect input values interactively via CLI or web forms before applying recipe
tldr: "Use input collection when you need to gather user-provided values interactively before applying a recipe."
drupal_version: "11.x"
---

# Input Collection & Forms

## When to Use

> Use input collection when you need to gather user-provided values interactively before applying a recipe.

Collect input values interactively via CLI or web forms before applying recipe.

## Steps: Collect Values via CLI, Custom Collector or Form

1. **CLI collection via Drush** — Drush prompts for inputs automatically
   ```bash
   drush recipe recipes/my_recipe
   # Prompts for each input defined in recipe.yml
   ```

2. **Custom CLI collector** — Implement InputCollectorInterface
   ```php
   use Drupal\Core\Recipe\InputCollectorInterface;

   class CustomCollector implements InputCollectorInterface {
     public function collectValue(string $name, DataDefinitionInterface $definition, mixed $default): mixed {
       // Custom logic to collect value
       return $this->askUser($definition->getDescription(), $default);
     }
   }
   ```

3. **Web form collection** — Use RecipeInputFormTrait
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

4. **Input substitution in config actions** — Values replace `${input_name}` placeholders
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

## Decision Points: Choosing a Collection Path

| At this step... | If... | Then... |
|---|---|---|
| Applying via CLI | Drush available | Use `drush recipe`; auto-prompts for inputs |
| Applying via CLI | No Drush | Use `php core/scripts/drupal recipe`; prompts via Symfony Console |
| Applying via web | Custom workflow needed | Implement form with RecipeInputFormTrait |
| Validating inputs | Constraints defined | Validation happens after collection, before application |

## Common Mistakes

- Not implementing InputCollectorInterface correctly → Must return value matching data_type; validation errors are cryptic
- Forgetting inputs are recursive → Recipe dependencies' inputs also collected; can overwhelm users
- Using inputs in config import → Inputs only work in config actions, not config file names
- Not handling validation failures → ConstraintViolationList exceptions throw if input violates constraints
- Assuming inputs persist → Input values only available during recipe application; not stored anywhere

## See Also

- Previous: ← [Input System - Default Sources](input-default-sources.md)
- Next: [Default Content - Overview](default-content-overview.md) →
- Reference: `core/lib/Drupal/Core/Recipe/InputConfigurator.php` (collectAll method)
