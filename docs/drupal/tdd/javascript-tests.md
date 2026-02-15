---
description: Write Drupal JavaScript tests with WebDriverTestBase for AJAX, DOM manipulation, and real browser interactions.
---

# JavaScript Tests with WebDriverTestBase

## When to Use
Testing JavaScript interactions, AJAX callbacks, dynamic DOM manipulation requiring a real browser.

## Decision
| Feature | BrowserTestBase | WebDriverTestBase |
|---|---|---|
| HTTP simulation | Yes (BrowserKit) | Yes (Real browser) |
| JavaScript execution | No | Yes |
| AJAX/fetch requests | No | Yes |
| DOM events (click, hover, etc.) | No | Yes |
| Speed (seconds per test) | 10-30 | 20-60 |
| Setup complexity | Low | High (requires chromedriver) |

**Use WebDriverTestBase when**: JavaScript behavior is essential to test, AJAX interactions, complex UI widgets.

## Pattern
**Basic JavaScript test structure**:
```php
namespace Drupal\Tests\my_module\FunctionalJavascript;

use Drupal\FunctionalJavascriptTests\WebDriverTestBase;

class AjaxFormTest extends WebDriverTestBase {

  protected $defaultTheme = 'stark';
  protected static $modules = ['my_module'];

  public function testAjaxCallback(): void {
    $this->drupalLogin($this->rootUser);
    $this->drupalGet('my-form');

    $page = $this->getSession()->getPage();
    $assert = $this->assertSession();

    // Trigger AJAX
    $page->selectFieldOption('category', 'books');
    $assert->waitForElement('css', '.subcategory-wrapper');

    // Assert AJAX result
    $assert->fieldExists('subcategory');
    $assert->optionExists('subcategory', 'Fiction');
  }
}
```

**Waiting for JavaScript operations**:
```php
// Wait for element to appear
$this->assertSession()->waitForElement('css', '#ajax-result');

// Wait for element to disappear
$this->assertSession()->waitForElementRemoved('css', '.loading-spinner');

// Wait for text
$this->assertSession()->waitForText('Operation complete');

// Custom wait condition
$this->getSession()->wait(5000, "jQuery('.target').length > 0");
```

**File location**: `modules/my_module/tests/src/FunctionalJavascript/AjaxFormTest.php`

Reference: `/core/tests/Drupal/FunctionalJavascriptTests/WebDriverTestBase.php`

## Common Mistakes
- Not starting chromedriver before running tests -- "Could not connect to host" failure
- Using https:// in SIMPLETEST_BASE_URL -- "invalid cookie domain" exception (use http://)
- Not waiting for AJAX operations -- test runs ahead of browser, assertions fail intermittently
- Hardcoding wait times `sleep(2)` -- flaky tests (use `waitForElement()` instead)
- Disabling CSS animations with `$disableCssAnimations = FALSE` without reason -- tests fail on timing issues

## See Also
- Reference: `/core/tests/Drupal/FunctionalJavascriptTests/WebDriverTestBase.php`
- Setup guide: `/core/tests/README.md` lines 81-89
- Official documentation: [Running PHPUnit JavaScript tests | Drupal.org](https://www.drupal.org/docs/develop/automated-testing/phpunit-in-drupal/running-phpunit-javascript-tests)
