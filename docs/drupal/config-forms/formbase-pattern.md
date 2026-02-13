---
description: Build custom admin forms with FormBase
drupal_version: "11.x"
---

# FormBase Pattern

## When to Use

> Use FormBase when building custom admin forms that don't fit ConfigFormBase (bulk operations, complex workflows, non-config data).

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Custom admin table with operations | FormBase + #type table | Full control over table structure |
| Bulk operations form | FormBase with checkboxes | Process multiple items in one submission |
| Multi-step wizard | FormBase with form state storage | Maintain state across steps |
| Non-config data management | FormBase + custom storage | Config API not appropriate |

## Pattern

```php
namespace Drupal\mymodule\Form;

use Drupal\Core\Form\FormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Url;

class ManageItemsForm extends FormBase {

  public function getFormId() {
    return 'mymodule_manage_items_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $items = $this->loadItems(); // Custom data loading

    $form['items'] = [
      '#type' => 'table',
      '#header' => [$this->t('Name'), $this->t('Status'), $this->t('Operations')],
      '#empty' => $this->t('No items found.'),
      '#attributes' => ['class' => ['mymodule-items-table']],
    ];

    foreach ($items as $id => $item) {
      $row = [];

      $row['name'] = ['#markup' => $item->getName()];
      $row['status'] = ['#markup' => $item->getStatus() ? $this->t('Active') : $this->t('Inactive')];

      // Operations using standard pattern
      $operations = [
        'edit' => [
          'title' => $this->t('Edit'),
          'url' => Url::fromRoute('mymodule.item.edit', ['id' => $id]),
        ],
        'delete' => [
          'title' => $this->t('Delete'),
          'url' => Url::fromRoute('mymodule.item.delete', ['id' => $id]),
        ],
      ];

      $row['operations'] = [
        '#type' => 'operations',
        '#links' => $operations,
        '#prefix' => '<div class="mymodule-dropbutton">',
        '#suffix' => '</div>',
      ];

      $form['items'][$id] = $row;
    }

    $form['actions'] = [
      '#type' => 'actions',
      'submit' => [
        '#type' => 'submit',
        '#value' => $this->t('Save'),
      ],
    ];

    return $form;
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Custom save logic
    $this->messenger()->addStatus($this->t('Items saved.'));
  }
}
```

## Common Mistakes

- **Wrong**: Using #markup for operations → **Right**: Use #type operations for proper dropbutton rendering
- **Wrong**: Not adding #attributes class to table → **Right**: CSS won't apply, dropbutton FOUC occurs
- **Wrong**: Forgetting #empty for empty tables → **Right**: No user feedback when no data exists
- **Wrong**: Not using Url::fromRoute() → **Right**: Hard-coded paths break on alias/language changes
- **Wrong**: Missing CSRF protection on operations → **Right**: Security vulnerability, use routes with tokens

## See Also

- [FormBase vs ListBuilder](formbase-vs-listbuilder.md)
- [Operations Implementation](operations-implementation.md)
- [Dependency Injection](dependency-injection.md)
- Reference: [Drupal Form API Introduction](https://www.drupal.org/docs/drupal-apis/form-api/introduction-to-form-api)
- Reference: modules/contrib/webform/src/Form/WebformEntityHandlersForm.php
