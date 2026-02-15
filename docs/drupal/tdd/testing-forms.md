---
description: Test Drupal form structure, validation, submission, and AJAX behaviors across test types.
---

# Testing Forms

## When to Use
Verifying form structure, validation, submission, and AJAX behaviors.

## Decision
| Aspect to test | Test type | Method |
|---|---|---|
| Form structure (fields, defaults) | Kernel | FormBuilder::getForm() |
| Validation logic | Kernel or Browser | submitForm() with invalid data |
| Submit handler logic | Kernel | submitForm() |
| User-facing messages | Browser | assertSession()->pageTextContains() |
| AJAX callbacks | WebDriverTestBase | Trigger AJAX, wait, assert |

## Pattern
**Testing form structure (Kernel)**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;

class MyFormTest extends KernelTestBase {

  protected static $modules = ['system', 'my_module'];

  public function testFormStructure(): void {
    $form_builder = $this->container->get('form_builder');
    $form = $form_builder->getForm('Drupal\my_module\Form\MyForm');

    $this->assertArrayHasKey('name', $form);
    $this->assertEquals('textfield', $form['name']['#type']);
    $this->assertEquals('Enter name', $form['name']['#title']);
  }
}
```

**Testing form validation (Browser)**:
```php
namespace Drupal\Tests\my_module\Functional;

use Drupal\Tests\BrowserTestBase;

class MyFormValidationTest extends BrowserTestBase {

  protected $defaultTheme = 'stark';
  protected static $modules = ['my_module'];

  public function testValidationError(): void {
    $this->drupalGet('my-form');
    $this->submitForm(['name' => ''], 'Submit');

    $this->assertSession()->pageTextContains('Name field is required');
  }

  public function testValidSubmission(): void {
    $this->drupalGet('my-form');
    $this->submitForm(['name' => 'John'], 'Submit');

    $this->assertSession()->pageTextContains('Form submitted successfully');
  }
}
```

**Testing AJAX callback (WebDriverTestBase)**:
```php
namespace Drupal\Tests\my_module\FunctionalJavascript;

use Drupal\FunctionalJavascriptTests\WebDriverTestBase;

class AjaxFormTest extends WebDriverTestBase {

  protected $defaultTheme = 'stark';
  protected static $modules = ['my_module'];

  public function testAjaxUpdate(): void {
    $this->drupalGet('my-form');
    $page = $this->getSession()->getPage();

    $page->fillField('category', 'electronics');
    $this->assertSession()->waitForElement('css', '.subcategory-field');

    $this->assertSession()->fieldExists('subcategory');
  }
}
```

Reference: `/core/modules/system/tests/src/Functional/Form/`

## Common Mistakes
- Not testing validation separately from submission -- can't distinguish which failed
- Hardcoding form element keys -- breaks when form structure changes (use FormBuilder to get form array in Kernel tests)
- Not waiting for AJAX in JS tests -- intermittent failures
- Testing form rendering in Kernel tests -- forms need HTTP context (use Browser test)
- Not testing access control -- form accessible to users who shouldn't see it

## See Also
- [Testing Plugins](testing-plugins.md)
- [Testing Entities](testing-entities.md)
- Example: `/core/modules/system/tests/src/Functional/Form/FormTest.php`
