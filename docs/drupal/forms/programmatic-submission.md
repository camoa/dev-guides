---
description: Programmatic form submission — batch operations, testing, security
drupal_version: "11.x"
---

# Programmatic Form Submission

## When to Use

> Use programmatic submission for batch operations, cron jobs, and automated testing. Only in trusted contexts (CLI, admin operations).

## Decision

| Use Case | Appropriate | Why |
|----------|-------------|-----|
| Batch operations | Yes | Trusted context |
| Migration/import | Yes | Automated process |
| Cron jobs | Yes | Server-side |
| Drush commands | Yes | CLI context |
| User-submitted forms | NO | Security risk |
| Public operations | NO | Bypass CSRF |

## Security Implications

**Bypasses:**
```
CSRF token validation - Skipped
Access checks - Can bypass with setProgrammedBypassAccessCheck()
Normal user flow - No render, no UI validation
```

**Use Only In Trusted Contexts:**
- CLI (Drush, Console)
- Cron operations
- Admin-initiated batch operations
- Migration processes
- Automated tests

## Pattern

**Basic Submission:**
```php
use Drupal\Core\Form\FormState;

$form_state = new FormState();
$form_state->setValues([
  'field_name' => 'value',
  'another_field' => 'another value',
]);
$form_state->setProgrammed(TRUE);

$form_builder = \Drupal::formBuilder();
$form_builder->submitForm('Drupal\mymodule\Form\MyForm', $form_state);
```

**With Dependency Injection:**
```php
use Drupal\Core\Form\FormBuilderInterface;

class MyService {
  protected $formBuilder;

  public function __construct(FormBuilderInterface $form_builder) {
    $this->formBuilder = $form_builder;
  }

  public function submitFormProgrammatically($data) {
    $form_state = new FormState();
    $form_state->setValues($data);
    $form_state->setProgrammed(TRUE);

    $this->formBuilder->submitForm('Drupal\mymodule\Form\MyForm', $form_state);
  }
}
```

## Advanced Patterns

**Bypass Access Checks (Use with Caution):**
```php
$form_state->setProgrammedBypassAccessCheck(TRUE);
```

**Check for Errors:**
```php
$form_builder->submitForm('Drupal\mymodule\Form\MyForm', $form_state);

if ($form_state->hasAnyErrors()) {
  $errors = $form_state->getErrors();
  // Handle errors
}
else {
  // Success
}
```

**Nested Values:**
```php
$form_state->setValues([
  'container' => [
    'field1' => 'value1',
    'field2' => 'value2',
  ],
]);
```

## Batch Integration

```php
public function submitForm(array &$form, FormStateInterface $form_state) {
  $items = $this->getItemsToProcess();

  $operations = [];
  foreach ($items as $item) {
    $operations[] = [
      [$this, 'batchProcessItem'],
      [$item],
    ];
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
  $context['message'] = $this->t('Processed @id', ['@id' => $item['id']]);
}
```

Reference: [Batch API Introduction](https://www.hashbangcode.com/article/drupal-11-introduction-batch-processing-batch-api)

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

- **Wrong**: Not setting programmed flag → **Right**: `$form_state->setProgrammed(TRUE)`
- **Wrong**: Using raw form array → **Right**: Use class name/object
- **Wrong**: Bypassing access inappropriately → **Right**: Only for trusted admin operations
- **Wrong**: Using for user-submitted forms → **Right**: Only for automated/trusted contexts

## See Also

- [Batch API](https://www.drupal.org/docs/drupal-apis/batch-api/batch-api-overview)
- [Form State Methods](form-state-methods.md)
- Reference: `/web/core/lib/Drupal/Core/Form/form.api.php` lines 56-95
- Reference: `/web/core/lib/Drupal/Core/Form/FormBuilder.php`
