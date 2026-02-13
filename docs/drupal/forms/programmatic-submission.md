---
description: Programmatic form submission for batch operations, testing, and automation
drupal_version: "11.x"
---

# Programmatic Form Submission

## When to Use

> Use programmatic submission for batch operations, migrations, automated testing, and cron jobs. Never for user-submitted forms.

## Decision

| Situation | Use Programmatic | Why |
|-----------|------------------|-----|
| Batch operations | Yes | Process items programmatically |
| Migration/import scripts | Yes | Automated data processing |
| Automated testing | Yes | PHPUnit, kernel tests |
| Cron jobs | Yes | Scheduled operations |
| Drush commands | Yes | CLI automation |
| User-submitted forms | No | Security risk |
| Forms requiring user interaction | No | Use normal form flow |

## Security Implications

**Bypasses:**
- CSRF token validation (skipped)
- Access checks (can bypass with setProgrammedBypassAccessCheck)
- Normal user flow (no render, no UI validation)

**Use only in trusted contexts:** CLI, Cron, Admin batch, Migration, Automated tests

## Pattern

```php
use Drupal\Core\Form\FormState;

$form_state = new FormState();
$form_state->setValues([
  'field_name' => 'value',
  'another_field' => 'another value',
]);
$form_state->setProgrammed(TRUE); // REQUIRED

$form_builder = \Drupal::formBuilder();
$form_builder->submitForm('Drupal\mymodule\Form\MyForm', $form_state);

// Check for errors
if ($form_state->hasAnyErrors()) {
  $errors = $form_state->getErrors();
  // Handle errors
} else {
  // Success
}
```

## With Dependency Injection

```php
use Drupal\Core\Form\FormBuilderInterface;
use Drupal\Core\Form\FormState;

class MyService {
  protected $formBuilder;

  public function __construct(FormBuilderInterface $form_builder) {
    $this->formBuilder = $form_builder;
  }

  public function submitForm($data) {
    $form_state = new FormState();
    $form_state->setValues($data);
    $form_state->setProgrammed(TRUE);

    $this->formBuilder->submitForm('Drupal\mymodule\Form\MyForm', $form_state);

    return !$form_state->hasAnyErrors();
  }
}
```

## Batch Integration

```php
public function submitForm(array &$form, FormStateInterface $form_state) {
  $items = $this->getItemsToProcess();

  $operations = [];
  foreach ($items as $item) {
    $operations[] = [[$this, 'batchProcessItem'], [$item]];
  }

  $batch = [
    'title' => $this->t('Processing items...'),
    'operations' => $operations,
    'finished' => [$this, 'batchFinished'],
  ];

  batch_set($batch);
}

public function batchProcessItem($item, &$context) {
  $form_state = new FormState();
  $form_state->setValues(['item_id' => $item['id']]);
  $form_state->setProgrammed(TRUE);

  \Drupal::formBuilder()->submitForm('Drupal\mymodule\Form\ProcessForm', $form_state);

  $context['results'][] = $item['id'];
}
```

## Testing Pattern

```php
namespace Drupal\Tests\mymodule\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Drupal\Core\Form\FormState;

class MyFormTest extends KernelTestBase {
  public function testFormSubmission() {
    $form_state = new FormState();
    $form_state->setValues(['field' => 'value']);
    $form_state->setProgrammed(TRUE);

    $form_builder = $this->container->get('form_builder');
    $form_builder->submitForm('Drupal\mymodule\Form\MyForm', $form_state);

    $this->assertEmpty($form_state->getErrors());
  }
}
```

## Common Mistakes

- **Wrong**: No setProgrammed(TRUE) → **Right**: Required or token validation fails
- **Wrong**: Using raw form array → **Right**: Use class name/object
- **Wrong**: Bypassing access inappropriately → **Right**: Only for trusted operations
- **Wrong**: User-submitted data → **Right**: Only for automated/trusted contexts

## See Also

- [Batch API Guide](https://www.drupal.org/docs/drupal-apis/batch-api/batch-api-overview)
- [Testing Forms](https://www.drupal.org/docs/automated-testing)
- [FormBuilder Service](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Form!FormBuilder.php/class/FormBuilder/11.x)
- Reference: `/web/core/lib/Drupal/Core/Form/form.api.php` lines 56-95
