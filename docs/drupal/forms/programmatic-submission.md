---
description: Programmatic form submission — batch operations, testing, security
drupal_version: "11.x"
---

# Programmatic Form Submission

### When to Use

**Appropriate Use Cases:**
- Batch operations processing items
- Migration/import scripts
- Automated testing (programmatic, not browser)
- Cron jobs creating/updating content
- Drush commands
- Admin operations (bulk updates)

**When NOT to Use:**
- User-submitted forms (security risk)
- Forms requiring user interaction
- When form validation should block
- Public-facing operations

### Security Implications

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

### Basic Pattern

**Simple Submission:**
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

### Advanced Patterns

**Bypass Access Checks:**
```php
$form_state->setProgrammedBypassAccessCheck(TRUE); // Use with caution
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

**Get Return Value:**
```php
$result = $form_builder->submitForm('Drupal\mymodule\Form\MyForm', $form_state);
// $result = form render array (usually not useful for programmatic)
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

### Batch Integration

**Form Submission in Batch:**
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
  // Programmatically submit form for each item
  $form_state = new FormState();
  $form_state->setValues(['item_id' => $item['id']]);
  $form_state->setProgrammed(TRUE);

  \Drupal::formBuilder()->submitForm('Drupal\mymodule\Form\ProcessForm', $form_state);

  $context['results'][] = $item['id'];
  $context['message'] = $this->t('Processed @id', ['@id' => $item['id']]);
}
```

**Reference:**
- Tutorial: [Drupal 11: Batch API Introduction](https://www.hashbangcode.com/article/drupal-11-introduction-batch-processing-batch-api)
- Core: `/web/core/lib/Drupal/Core/Form/form.api.php` lines 56-95

### Testing Pattern

**PHPUnit Kernel Test:**
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

### Common Mistakes

**Not Setting Programmed Flag:**
```php
// WRONG - will fail token validation
$form_state->setValues([...]);
\Drupal::formBuilder()->submitForm(...);

// CORRECT
$form_state->setProgrammed(TRUE);
```

**Using Raw Form Array:**
```php
// WRONG
$form = \Drupal::formBuilder()->getForm('Drupal\mymodule\Form\MyForm');
// Can't submit $form array

// CORRECT - use class name/object
\Drupal::formBuilder()->submitForm('Drupal\mymodule\Form\MyForm', $form_state);
```

**Bypassing Access Inappropriately:**
```php
// DANGEROUS - only for trusted admin operations
$form_state->setProgrammedBypassAccessCheck(TRUE);
```

**See Also:**
- Batch API Guide
- Testing Forms Guide
- FormBuilder Service
- Official: [Batch API Overview](https://www.drupal.org/docs/drupal-apis/batch-api/batch-api-overview)
