---
description: ConfirmFormBase — confirmation step before destructive actions
drupal_version: "11.x"
---

# ConfirmFormBase

## When to Use

> Use ConfirmFormBase when you need an "Are you sure?" step before a destructive or irreversible action (delete, reset, purge). Never skip confirmation for data-destroying operations.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Delete entity/content | ConfirmFormBase | User must confirm destruction |
| Reset configuration | ConfirmFormBase | Irreversible change |
| Bulk operation with consequences | ConfirmFormBase | Prevents accidental mass action |
| Simple data entry | FormBase | No destructive action |

## Pattern

```php
namespace Drupal\my_module\Form;

use Drupal\Core\Form\ConfirmFormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Url;

class DeleteForm extends ConfirmFormBase {

  public function getFormId() {
    return 'my_module_delete_confirm';
  }

  public function getQuestion() {
    return $this->t('Are you sure you want to delete this item?');
  }

  public function getCancelUrl() {
    return new Url('my_module.list');
  }

  public function getDescription() {
    return $this->t('This action cannot be undone.');
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Perform the destructive action.
    $this->messenger()->addStatus($this->t('Item deleted.'));
    $form_state->setRedirectUrl($this->getCancelUrl());
  }

}
```

## Required Methods

| Method | Purpose |
|--------|---------|
| `getFormId()` | Unique form identifier |
| `getQuestion()` | The confirmation question shown to user |
| `getCancelUrl()` | Where "Cancel" button redirects |
| `submitForm()` | Performs the action after confirmation |

## Common Mistakes

- **Wrong**: Using FormBase with a manual "confirm" checkbox (ConfirmFormBase handles this)
- **Wrong**: Forgetting `getCancelUrl()` (required, will fatal)
- **Right**: Always redirect after submit — user should land somewhere meaningful

## See Also

- [FormBase](form-base.md) — for non-destructive forms
