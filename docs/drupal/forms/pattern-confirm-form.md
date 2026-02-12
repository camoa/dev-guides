---
description: ConfirmFormBase — confirmation dialogs for destructive actions
drupal_version: "11.x"
---

# Pattern: Confirmation Form (ConfirmFormBase)

## When to Use

> Use ConfirmFormBase for delete operations and destructive actions. Use FormBase for multi-field forms.

## Decision

| Use Case | Form Type | Why |
|----------|-----------|-----|
| Delete operations | ConfirmFormBase | Standard pattern |
| Destructive actions | ConfirmFormBase | User confirmation |
| Yes/no decision | ConfirmFormBase | Simple dialog |
| Multi-field forms | FormBase | Need additional inputs |

## Pattern

```php
<?php

namespace Drupal\mymodule\Form;

use Drupal\Core\Form\ConfirmFormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\Core\Url;

class DeleteForm extends ConfirmFormBase {

  public function getFormId() {
    return 'mymodule_delete_form';
  }

  public function getQuestion() {
    return $this->t('Are you sure you want to delete this item?');
  }

  public function getCancelUrl() {
    return Url::fromRoute('mymodule.collection');
  }

  public function getConfirmText() {
    return $this->t('Delete');
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    // Perform deletion
    $form_state->setRedirectUrl($this->getCancelUrl());
  }
}
```

Reference: `/web/core/modules/dblog/src/Form/DblogClearLogConfirmForm.php`

## Required Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `getQuestion()` | TranslatableMarkup | Main confirmation question |
| `getCancelUrl()` | Url object | Destination if user cancels |
| `getConfirmText()` | TranslatableMarkup | Submit button text (default: "Confirm") |
| `getDescription()` | String (optional) | Additional warning/info text |

## Form Structure

Automatically provides:
- Question text (from getQuestion())
- Confirm button (from getConfirmText())
- Cancel link (from getCancelUrl())
- Standard confirmation form styling

## Custom Confirm Text

Different from "Confirm":
- "Delete" for delete operations
- "Remove" for remove operations
- "Reset" for reset operations

## Common Mistakes

- **Wrong**: Forgetting to implement required methods → **Right**: Implement getQuestion, getCancelUrl, getConfirmText
- **Wrong**: Returning string instead of Url object from getCancelUrl() → **Right**: Return `Url::fromRoute()`
- **Wrong**: Adding complex form elements (defeats purpose) → **Right**: Keep it simple, just confirm/cancel
- **Wrong**: Using generic "Confirm" text → **Right**: Use descriptive text ("Delete", "Remove")

## See Also

- [Standard Form Pattern](pattern-standard-form.md)
- [URL Generation](https://www.drupal.org/docs/drupal-apis/routing-system/url-generation)
- Reference: `/web/core/lib/Drupal/Core/Form/ConfirmFormBase.php`
