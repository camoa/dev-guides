---
description: ConfirmFormBase pattern for delete operations and destructive actions
drupal_version: "11.x"
---

# Pattern: Confirmation Form (ConfirmFormBase)

## When to Use

> Use ConfirmFormBase for delete operations and irreversible actions. Use FormBase for forms with additional input fields.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Delete operations | ConfirmFormBase | Standard confirm UI |
| Destructive actions (purge, reset) | ConfirmFormBase | Clear confirmation |
| Yes/no decisions | ConfirmFormBase | Simple binary choice |
| Multi-field forms | FormBase | More than yes/no |
| Confirmations with inputs | FormBase | Custom styling needed |

## Pattern

Minimal form with automatic confirm UI:

```php
use Drupal\Core\Form\ConfirmFormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Url;

class DeleteConfirmForm extends ConfirmFormBase {
  public function getFormId() {
    return 'mymodule_delete_confirm';
  }

  public function getQuestion() {
    return $this->t('Are you sure you want to delete this item?');
  }

  public function getCancelUrl() {
    return new Url('entity.node.collection');
  }

  public function getConfirmText() {
    return $this->t('Delete'); // Default: "Confirm"
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Perform deletion
    $this->messenger()->addStatus($this->t('Item deleted.'));
    $form_state->setRedirectUrl($this->getCancelUrl());
  }
}
```

## Required Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `getQuestion()` | TranslatableMarkup | Main confirmation question |
| `getCancelUrl()` | Url object | Destination if canceled |
| `getConfirmText()` | TranslatableMarkup | Submit button text (default: "Confirm") |
| `getDescription()` | String (optional) | Additional warning/info |

## Customization

Add elements in buildForm() but call parent:

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['extra_option'] = [
    '#type' => 'checkbox',
    '#title' => $this->t('Also delete related items'),
  ];
  return parent::buildForm($form, $form_state);
}
```

## Common Mistakes

- **Wrong**: Missing required methods → **Right**: Implement getQuestion() and getCancelUrl()
- **Wrong**: getCancelUrl() returns string → **Right**: Return Url object
- **Wrong**: Complex form elements → **Right**: Keep simple (defeats purpose)
- **Wrong**: Generic "Confirm" text → **Right**: Descriptive action ("Delete", "Remove")

## See Also

- [URL Generation Guide](https://www.drupal.org/docs/drupal-apis/routing-system)
- [User Experience Guidelines](https://www.drupal.org/docs/develop/user-interface-standards)
- Reference: `/web/core/modules/dblog/src/Form/DblogClearLogConfirmForm.php`
