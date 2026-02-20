---
description: Write automated AJAX tests with WebDriverTestBase — assertWaitOnAjaxRequest, session interaction, and common pitfalls
drupal_version: "11.x"
---

# Testing AJAX

## When to Use

> Use WebDriverTestBase (FunctionalJavascript namespace) for AJAX tests — it drives a real browser. Use BrowserTestBase only for non-JavaScript tests.

## Pattern

```php
namespace Drupal\Tests\my_module\FunctionalJavascript;

use Drupal\FunctionalJavascriptTests\WebDriverTestBase;

class AjaxFormTest extends WebDriverTestBase {
  protected static $modules = ['my_module'];
  protected $defaultTheme = 'stark';  // Required in Drupal 11+

  public function testDependentFields() {
    $this->drupalGet('/my-module/ajax-form');

    $page = $this->getSession()->getPage();
    $assert = $this->assertSession();

    // Verify initial state
    $assert->fieldExists('subcategory');
    $this->assertEmpty($page->findField('subcategory')->getValue());

    // Trigger AJAX
    $page->selectFieldOption('category', 'electronics');

    // Wait for AJAX to complete (always required)
    $assert->assertWaitOnAjaxRequest();

    // Verify outcome
    $assert->optionExists('subcategory', 'Laptops');
  }

  public function testAjaxErrors() {
    $this->drupalGet('/my-module/ajax-form');
    $this->getSession()->getPage()->pressButton('Submit');
    $this->assertSession()->assertWaitOnAjaxRequest();
    $this->assertSession()->pageTextContains('Email field is required');
  }
}
```

Reference: `core/tests/Drupal/FunctionalJavascriptTests/Ajax/AjaxFormPageCacheTest.php`

## Common Mistakes

- **Wrong**: Extending BrowserTestBase for AJAX tests → **Right**: Use WebDriverTestBase from FunctionalJavascriptTests namespace
- **Wrong**: Not calling `assertWaitOnAjaxRequest()` → **Right**: Tests check DOM before AJAX completes; always wait
- **Wrong**: Not setting `$defaultTheme` → **Right**: Tests fail in Drupal 11+; explicitly set a theme
- **Wrong**: Testing only the happy path → **Right**: Test validation errors, access control, edge cases, and error states
- **Wrong**: Not cleaning up test data → **Right**: Use transactions or manual cleanup to avoid state leaking between tests

## See Also

- [Debugging Techniques](debugging-techniques.md)
- [Frontend Framework Integration](frontend-framework-integration.md)
- Reference: [JavaScript testing documentation](https://www.drupal.org/docs/automated-testing/javascript-testing-using-nightwatch)
