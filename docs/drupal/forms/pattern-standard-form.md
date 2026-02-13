---
description: FormBase pattern for general-purpose forms with dependency injection
drupal_version: "11.x"
---

# Pattern: Standard Form (FormBase)

## When to Use

> Use FormBase for general-purpose forms with custom business logic. Use ConfigFormBase for settings, EntityForm for entities, ConfirmFormBase for confirmations.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Authentication, calculations, integrations | FormBase | Full control, service injection |
| Configuration management | ConfigFormBase | Auto config sync |
| Entity create/edit | EntityForm | Entity-specific features |
| Confirmation dialogs | ConfirmFormBase | Standard UI |

## Pattern

Dependency injection via `create()` method:

```php
use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

class MyForm extends FormBase {
  protected $entityTypeManager;

  public function __construct(EntityTypeManagerInterface $entity_type_manager) {
    $this->entityTypeManager = $entity_type_manager;
  }

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('entity_type.manager')
    );
  }

  public function getFormId() {
    return 'my_module_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $form['field'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Field'),
      '#required' => TRUE,
    ];
    return $form;
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    $value = $form_state->getValue('field');
    $form_state->setRedirect('route.name');
  }
}
```

## Value Storage

| Phase | Pattern | Purpose |
|-------|---------|---------|
| Build | `$form['field']['#default_value'] = $value` | Initial display value |
| Submit | `$value = $form_state->getValue('field')` | Submitted value |
| Cross-rebuild | `$form_state->set('data', $value)` | Persist across rebuilds |

## Common Mistakes

- **Wrong**: Not implementing unique `getFormId()` → **Right**: Unique ID per form
- **Wrong**: Using `$_POST` directly → **Right**: Use `$form_state->getValue()` (CSRF-protected)
- **Wrong**: No dependency injection → **Right**: Use `create()` for services
- **Wrong**: Forgetting `parent::buildForm()` → **Right**: Call parent when needed

## See Also

- [Form Lifecycle](architecture-lifecycle.md)
- [Validation Architecture](validation-architecture.md)
- [Submission Architecture](submission-architecture.md)
- Reference: `/web/core/modules/user/src/Form/UserLoginForm.php`
