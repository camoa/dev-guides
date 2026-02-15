---
description: Write Drupal browser tests with BrowserTestBase for full user workflows, form submission, and access control.
---

# Browser Tests with BrowserTestBase

## When to Use
Testing complete user workflows: page rendering, form submission, access control, multi-step processes requiring HTTP.

## Decision
| If you need to test... | Use BrowserTestBase? | Notes |
|---|---|---|
| Form submission and validation | YES | Full form API + HTTP |
| Page access control | YES | Simulates user login + permissions |
| Rendered HTML output | YES | Can assert on CSS selectors |
| Multi-step workflows | YES | Maintains session between requests |
| JavaScript interactions | NO | Use WebDriverTestBase |
| Service logic only | NO | Use KernelTestBase (10x faster) |

## Pattern
**Basic browser test structure**:
```php
namespace Drupal\Tests\my_module\Functional;

use Drupal\Tests\BrowserTestBase;

class MyFeatureTest extends BrowserTestBase {

  protected $defaultTheme = 'stark';
  protected static $modules = ['node', 'my_module'];

  protected function setUp(): void {
    parent::setUp();
    // Drupal fully installed, database populated
    $this->drupalCreateContentType(['type' => 'article']);
  }

  public function testNodeCreation(): void {
    $user = $this->drupalCreateUser(['create article content']);
    $this->drupalLogin($user);

    $this->drupalGet('node/add/article');
    $this->assertSession()->statusCodeEquals(200);

    $edit = ['title[0][value]' => 'Test Article'];
    $this->submitForm($edit, 'Save');

    $this->assertSession()->pageTextContains('Test Article has been created');
  }
}
```

**Common assertion patterns**:
```php
// HTTP response
$this->assertSession()->statusCodeEquals(200);
$this->assertSession()->addressEquals('user/login');

// Page content
$this->assertSession()->pageTextContains('Welcome');
$this->assertSession()->elementExists('css', '.messages--status');
$this->assertSession()->linkExists('Edit');

// Form fields
$this->assertSession()->fieldExists('title[0][value]');
$this->assertSession()->buttonExists('Save');
```

**File location**: `modules/my_module/tests/src/Functional/MyFeatureTest.php`

Reference: `/core/tests/Drupal/Tests/BrowserTestBase.php`

## Common Mistakes
- Not setting `$defaultTheme` -- test failures in Drupal 10+ (no default theme assumption)
- Using real HTTP calls instead of `drupalGet()` -- breaks test isolation
- Testing without user context -- permission denials that hide real bugs (always `drupalLogin()` with appropriate permissions)
- Asserting on HTML structure instead of behavior -- brittle tests that break on template changes
- Not using traits (NodeCreationTrait, UserCreationTrait) -- reinventing helper methods

## See Also
- Reference: `/core/tests/Drupal/Tests/BrowserTestBase.php`
- Example: `/core/modules/node/tests/src/Functional/NodeCreationTest.php`
