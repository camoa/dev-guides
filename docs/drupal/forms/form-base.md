---
description: FormBase — custom input forms that process data without saving to config
drupal_version: "11.x"
---

# FormBase

## When to Use

> Use FormBase when your form collects and processes user input but does NOT save to Drupal config. Use ConfigFormBase for module settings.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Contact or feedback form | FormBase | Processes input, sends email or saves to DB |
| Search or filter form | FormBase | Processes input, redirects with query |
| Import/upload form | FormBase | Processes file, no config involved |
| Module settings | ConfigFormBase | Needs config save/load |

## Pattern

```php
namespace Drupal\my_module\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;

class SearchForm extends FormBase {

  public function getFormId() {
    return 'my_module_search';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $form['query'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Search'),
      '#required' => TRUE,
    ];

    $form['submit'] = [
      '#type' => 'submit',
      '#value' => $this->t('Search'),
    ];

    return $form;
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    $query = $form_state->getValue('query');
    $form_state->setRedirect('my_module.results', [], [
      'query' => ['q' => $query],
    ]);
  }

}
```

## Injecting Services

```php
use Drupal\Core\Form\FormBase;
use Symfony\Component\DependencyInjection\ContainerInterface;

class MyForm extends FormBase {

  public function __construct(
    protected readonly EntityTypeManagerInterface $entityTypeManager,
  ) {}

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('entity_type.manager'),
    );
  }

}
```

## Common Mistakes

- **Wrong**: Extending ConfigFormBase for non-config forms (unnecessary overhead)
- **Wrong**: Forgetting `#type => 'submit'` (no submit button)
- **Wrong**: Using `\Drupal::service()` in forms (use `create()` + constructor injection)
- **Right**: Use `$form_state->setRedirect()` not `RedirectResponse` for POST-redirect-GET

## See Also

- [ConfigFormBase](config-form-base.md) — for module settings
- [Validation](validation.md) — adding validation
- [AJAX](ajax.md) — dynamic form behavior
