---
description: Write automated AJAX tests with WebDriverTestBase — assertWaitOnAjaxRequest, session interaction, and common pitfalls
tldr: "Use WebDriverTestBase (FunctionalJavascript namespace) for AJAX tests — it drives a real browser. Use BrowserTestBase only for non-JavaScript tests."
drupal_version: "11.x"
---

# Testing AJAX

## When to Use

You need automated tests for AJAX functionality to prevent regressions.

## Pattern

```php
// Functional test for AJAX (BrowserTestBase)
namespace Drupal\Tests\my_module\FunctionalJavascript;

use Drupal\FunctionalJavascriptTests\WebDriverTestBase;

class AjaxFormTest extends WebDriverTestBase {
  protected static $modules = ['my_module'];
  protected $defaultTheme = 'stark';

  public function testDependentFields() {
    // Visit form
    $this->drupalGet('/my-module/ajax-form');

    // Wait for page load
    $page = $this->getSession()->getPage();
    $assert = $this->assertSession();

    // Initially subcategory should be empty
    $assert->fieldExists('subcategory');
    $this->assertEmpty($page->findField('subcategory')->getValue());

    // Select category
    $page->selectFieldOption('category', 'electronics');

    // Wait for AJAX to complete
    $assert->assertWaitOnAjaxRequest();

    // Verify subcategory populated
    $subcategory_field = $page->findField('subcategory');
    $this->assertNotEmpty($subcategory_field->getValue());

    // Verify specific option exists
    $assert->optionExists('subcategory', 'Laptops');
  }

  public function testAjaxContentUpdate() {
    $this->drupalGet('/my-module/ajax-page');

    $page = $this->getSession()->getPage();
    $assert = $this->assertSession();

    // Click AJAX button
    $page->pressButton('Load Content');

    // Wait for AJAX
    $assert->assertWaitOnAjaxRequest();

    // Verify content updated
    $assert->elementContains('css', '#content-wrapper', 'New content loaded');
  }

  public function testAjaxErrors() {
    $this->drupalGet('/my-module/ajax-form');

    $page = $this->getSession()->getPage();
    $assert = $this->assertSession();

    // Trigger AJAX without required field
    $page->pressButton('Submit');

    $assert->assertWaitOnAjaxRequest();

    // Verify error message appears
    $assert->pageTextContains('Email field is required');
  }
}
```

Reference: `core/tests/Drupal/FunctionalJavascriptTests/Ajax/AjaxFormPageCacheTest.php`

## Common Mistakes

- Not extending WebDriverTestBase → Use FunctionalJavascriptTests namespace for AJAX tests, not BrowserTestBase
- Forgetting `assertWaitOnAjaxRequest()` → Tests check before AJAX completes; always wait
- Not setting `$defaultTheme` → Tests fail in Drupal 11+; set theme explicitly
- Testing only happy path → Test validation errors, access control, edge cases
- Not cleaning up test data → Tests leave database changes; use transactions or manual cleanup

## See Also

- ← Previous: [Debugging Techniques](debugging-techniques.md) | Next: [Frontend Framework Integration](frontend-framework-integration.md)
- Reference: [JavaScript testing documentation](https://www.drupal.org/docs/develop/automated-testing/javascript-testing-using-nightwatch)
