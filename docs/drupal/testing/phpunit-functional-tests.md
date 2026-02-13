---
description: Write PHPUnit Functional tests for complete user workflows, admin forms, and HTTP request/response testing
drupal_version: "11.x"
---

# PHPUnit Functional Tests

## When to Use

Write Functional tests for complete user workflows: admin configuration forms, content creation/editing, user registration/login, permission testing, and any feature requiring HTTP requests and responses.

## Decision

| If you need... | Use Functional Tests | Why |
|----------------|----------------------|-----|
| Test admin configuration forms | Yes | Full form rendering and submission |
| Test user workflows | Yes | Complete HTTP request/response cycle |
| Test permissions and access control | Yes | Full user authentication system |
| Test routing and menu system | Yes | Full Drupal bootstrap with routing |
| Test JavaScript interactions | No, use FunctionalJavascript | No browser JavaScript execution |
| Faster test execution | No, use Unit/Kernel | Functional tests are slower |

## Pattern

```php
<?php
namespace Drupal\Tests\my_module\Functional;

use Drupal\Tests\BrowserTestBase;

/**
 * Tests the my_module admin configuration interface.
 *
 * @group my_module
 */
class AdminConfigurationTest extends BrowserTestBase {

  protected $defaultTheme = 'stark';
  protected static $modules = ['my_module', 'node'];

  protected function setUp(): void {
    parent::setUp();

    // Create admin user with specific permissions
    $this->adminUser = $this->drupalCreateUser([
      'administer my module',
      'access administration pages',
    ]);
  }

  public function testConfigurationForm(): void {
    $this->drupalLogin($this->adminUser);

    // Visit configuration page
    $this->drupalGet('admin/config/my-module/settings');
    $this->assertSession()->statusCodeEquals(200);
    $this->assertSession()->pageTextContains('My Module Settings');
    $this->assertSession()->fieldExists('api_key');

    // Test form submission
    $edit = [
      'api_key' => 'test_key_123',
      'timeout' => '60',
      'enabled' => TRUE,
    ];
    $this->submitForm($edit, 'Save configuration');

    // Verify success message
    $this->assertSession()->pageTextContains('configuration options have been saved');
    
    // Verify configuration was saved
    $config = $this->config('my_module.settings');
    $this->assertEquals('test_key_123', $config->get('api_key'));
    $this->assertEquals(60, $config->get('timeout'));
    $this->assertTrue($config->get('enabled'));
  }

  public function testPermissionDenied(): void {
    // Create user without admin permission
    $user = $this->drupalCreateUser(['access content']);
    $this->drupalLogin($user);

    $this->drupalGet('admin/config/my-module/settings');
    $this->assertSession()->statusCodeEquals(403);
    $this->assertSession()->pageTextContains('Access denied');
  }

  public function testFormValidation(): void {
    $this->drupalLogin($this->adminUser);
    $this->drupalGet('admin/config/my-module/settings');

    // Submit invalid data
    $edit = [
      'api_key' => '', // Empty required field
      'timeout' => 'invalid', // Non-numeric value
    ];
    $this->submitForm($edit, 'Save configuration');

    // Verify validation errors
    $this->assertSession()->pageTextContains('API key field is required');
    $this->assertSession()->pageTextContains('Timeout must be a number');
  }
}
```

**File Location**: `modules/my_module/tests/src/Functional/AdminConfigurationTest.php`

## Common Mistakes

- **Wrong**: Not setting `$defaultTheme` → **Right**: Always set `$defaultTheme = 'stark'` or another stable theme
- **Wrong**: Not logging in before accessing protected pages → **Right**: Call `drupalLogin()` before accessing admin pages
- **Wrong**: Using JavaScript methods like `getSession()->getPage()` → **Right**: Use FunctionalJavascript for JavaScript interactions
- **Wrong**: Creating users with wrong permissions → **Right**: Create users with exact permissions needed for test
- **Wrong**: Not checking status codes → **Right**: Verify both HTTP status and page content

## See Also

- [PHPUnit Kernel Tests](phpunit-kernel-tests.md)
- [PHPUnit FunctionalJavascript Tests](phpunit-functionaljavascript-tests.md)
- Reference: [Run Functional JavaScript Tests - Drupalize.me](https://drupalize.me/tutorial/run-functional-javascript-tests)
- Reference: `/core/tests/Drupal/Tests/BrowserTestBase.php`
