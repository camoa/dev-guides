---
description: Write PHPUnit FunctionalJavascript tests for AJAX interactions, autocomplete, modals, and client-side JavaScript
drupal_version: "11.x"
---

# PHPUnit FunctionalJavascript Tests

## When to Use

Write FunctionalJavascript tests only when testing features that require JavaScript execution: AJAX form elements, autocomplete fields, modal dialogs, drag-and-drop interfaces, or client-side validation.

## Decision

| If you need... | Use FunctionalJavascript | Why |
|----------------|--------------------------|-----|
| Test AJAX interactions | Yes | Real browser executes JavaScript |
| Test autocomplete fields | Yes | Requires JavaScript event handling |
| Test modal dialogs | Yes | JavaScript-driven UI components |
| Test drag-and-drop | Yes | Browser DOM manipulation needed |
| Test server-rendered forms | No, use Functional | Faster without browser overhead |
| Test pure logic | No, use Unit/Kernel | No UI needed |

## Pattern

```php
<?php
namespace Drupal\Tests\my_module\FunctionalJavascript;

use Drupal\FunctionalJavascriptTests\WebDriverTestBase;

/**
 * Tests the my_module AJAX form interactions.
 *
 * @group my_module
 */
class AjaxFormTest extends WebDriverTestBase {

  protected $defaultTheme = 'stark';
  protected static $modules = ['my_module', 'node'];

  public function testAjaxDependentDropdown(): void {
    $this->drupalLogin($this->drupalCreateUser(['access content']));

    $session = $this->getSession();
    $page = $session->getPage();
    $assert_session = $this->assertSession();

    $this->drupalGet('my-module/ajax-form');

    // Trigger AJAX request by selecting option
    $page->selectFieldOption('category', 'electronics');
    
    // CRITICAL: Wait for AJAX to complete
    $assert_session->assertWaitOnAjaxRequest();

    // Verify AJAX-loaded content
    $assert_session->elementExists('css', '#subcategory-wrapper');
    $assert_session->fieldExists('subcategory');
    $assert_session->optionExists('subcategory', 'smartphones');
    
    // Test cascading AJAX
    $page->selectFieldOption('subcategory', 'smartphones');
    $assert_session->assertWaitOnAjaxRequest();
    
    $assert_session->elementExists('css', '#brand-wrapper');
    $assert_session->fieldExists('brand');
  }

  public function testModalDialog(): void {
    $this->drupalLogin($this->drupalCreateUser(['access content']));

    $page = $this->getSession()->getPage();
    $assert_session = $this->assertSession();

    $this->drupalGet('my-module/content-list');

    // Open modal via AJAX
    $page->clickLink('Add New Item');
    
    // Wait for modal to appear
    $assert_session->waitForElement('css', '.ui-dialog');
    $assert_session->elementExists('css', '.ui-dialog-title');
    $assert_session->elementTextContains('css', '.ui-dialog-title', 'Add Item');

    // Fill and submit modal form
    $page->fillField('title', 'Test Item');
    $page->fillField('description', 'Test description');
    $page->pressButton('Save');
    
    // Wait for AJAX submission
    $assert_session->assertWaitOnAjaxRequest();
    
    // Verify modal closed and item added
    $assert_session->elementNotExists('css', '.ui-dialog');
    $assert_session->pageTextContains('Test Item');
  }

  public function testAutocomplete(): void {
    $this->drupalLogin($this->drupalCreateUser(['access content']));

    $page = $this->getSession()->getPage();
    $assert_session = $this->assertSession();

    $this->drupalGet('my-module/autocomplete-form');

    // Type to trigger autocomplete
    $page->fillField('user_search', 'adm');
    
    // Wait for autocomplete results
    $assert_session->waitForElement('css', '.ui-autocomplete');
    $assert_session->elementExists('css', '.ui-autocomplete li');
    $assert_session->elementTextContains('css', '.ui-autocomplete', 'admin');

    // Select autocomplete result
    $page->find('css', '.ui-autocomplete li:first-child')->click();
    
    // Verify selection
    $this->assertEquals('admin', $page->findField('user_search')->getValue());
  }
}
```

**File Location**: `modules/my_module/tests/src/FunctionalJavascript/AjaxFormTest.php`

## Common Mistakes

- **Wrong**: Not calling `assertWaitOnAjaxRequest()` after AJAX triggers → **Right**: Always wait for AJAX to complete
- **Wrong**: Using `drupalGet()` and immediately checking for AJAX content → **Right**: Wait for elements to appear
- **Wrong**: Not configuring ChromeDriver/WebDriver → **Right**: Start ChromeDriver before running tests
- **Wrong**: Writing FunctionalJavascript tests for non-JavaScript features → **Right**: Use Functional tests when no JavaScript needed
- **Wrong**: Using `sleep()` instead of proper waits → **Right**: Use `waitForElement()` or `assertWaitOnAjaxRequest()`

## See Also

- [PHPUnit Functional Tests](phpunit-functional-tests.md)
- [Gander Performance Testing](gander-performance-testing.md)
- [Running and Debugging Tests](running-debugging-tests.md)
- Reference: [Creating FunctionalJavascript tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/creating-functionaljavascript-tests-real-browser)
- Reference: [Running PHPUnit JavaScript tests - Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-javascript-tests)
- Reference: `/core/tests/Drupal/FunctionalJavascriptTests/WebDriverTestBase.php`
