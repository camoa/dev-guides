---
description: "FormBase pattern for general-purpose forms with dependency injection"
tldr: "Use FormBase for general-purpose forms with custom business logic. Use ConfigFormBase for settings, EntityForm for entities, ConfirmFormBase for confirmations."
drupal_version: "11.x"
---

# Pattern: Standard Form (FormBase)

## When to Use

> Use FormBase for general-purpose forms with custom business logic. Use ConfigFormBase for settings, EntityForm for entities, ConfirmFormBase for confirmations.

**Appropriate Use Cases:**

- General-purpose forms not tied to entities
- Custom business logic (authentication, calculations, integrations)
- API integration forms
- Administrative operations (cache clear, imports)

**When NOT to Use:**

- Configuration management → Use ConfigFormBase
- Entity create/edit → Use EntityForm
- Confirmation dialogs → Use ConfirmFormBase

## Pattern: Implementation

**Core Example:**

- File: `/web/core/modules/user/src/Form/UserLoginForm.php`
- Pattern: Dependency injection, custom validation chains, FormState storage
- Study: Authentication logic, flood control integration

**Dependency Injection:**

```
Inject services via:
1. Add properties to class
2. Constructor receives services
3. static create() method instantiates with container
4. Use injected services in methods
```

**Reference:** `/web/core/lib/Drupal/Core/Form/FormBase.php` shows base DI pattern

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
    return new static($container->get('entity_type.manager'));
  }

  public function getFormId() {
    return 'my_module_example_form';
  }
}
```

## Decision: Key Decisions

| Decision Point | Recommendation | Example |
|----------------|----------------|---------|
| Service injection | Use `create()` method | UserLoginForm lines 50-70 |
| Multiple validators | Add to `$form['#validate']` array | UserLoginForm lines 90-95 |
| Intermediate data | Use `$form_state->set()`/`get()` | Multi-step pattern |
| Post-submit routing | `$form_state->setRedirect()` | All submit handlers |

**Value Storage:**

```
Build phase: $form['field']['#default_value'] = $initial_value;
Submit phase: $value = $form_state->getValue('field');
Cross-rebuild: $form_state->set('stored_data', $data);
```

**Validation Chain:**

```
Element validators run first (#element_validate)
Then form validators ($form['#validate'] array)
Then class validateForm() method
Error on any → no submit handlers run
```

## Common Mistakes

- Not implementing `getFormId()` with unique ID
    - **WHY BAD:** Form ID collisions break form caching, alter hooks fail, form_build_id validation breaks
- Using `$_POST` instead of `$form_state->getValue()`
    - **WHY BAD:** Bypasses CSRF protection, no sanitization, validation skipped, direct security vulnerability
- Forgetting to call `parent::buildForm()` when needed
    - **WHY BAD:** Breaks form caching setup, CSRF token not added, form structure incomplete
- Not using dependency injection for services
    - **WHY BAD:** Can't unit test (mocking impossible), breaks service substitution, creates hidden dependencies

## See Also

- [Dependency Injection Guide](../services/index.md)
- [Validation Architecture](validation-architecture.md) (dedicated section)
- [Submission Architecture](submission-architecture.md) (dedicated section)
- Reference: `/web/core/modules/user/src/Form/UserLoginForm.php`
