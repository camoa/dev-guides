---
description: Use Drupal test traits for creating users, nodes, content types, blocks, and random test data.
---

# Test Traits & Utilities

## When to Use
Reusing common test setup patterns: creating users, nodes, content types, blocks, etc.

## Reference Catalog

### UserCreationTrait
**Description:** Creates users, roles, and manages authentication in tests.

| Method | Purpose | Returns |
|--------|---------|---------|
| `createUser($permissions, $name, $admin, $values)` | Create user with permissions | UserInterface |
| `createRole($permissions, $rid, $name)` | Create role with permissions | Role ID string |
| `createAdminRole($rid, $name)` | Create admin role (bypass node access) | Role ID string |
| `setUpCurrentUser($values, $permissions, $admin)` | Create user and set as current | UserInterface |
| `drupalLogin($account)` | Log in user (BrowserTestBase only) | void |

**Usage Example (Kernel test)**:
```php
use Drupal\Tests\user\Traits\UserCreationTrait;

class MyTest extends KernelTestBase {
  use UserCreationTrait;

  public function testUserPermissions(): void {
    $user = $this->createUser(['access content', 'create article content']);
    $this->setCurrentUser($user);
    // Test permission-dependent logic
  }
}
```

**Gotchas:**
- `createUser()` returns user with `pass_raw` property -- use for `drupalLogin()` if needed
- In Kernel tests, must call `setCurrentUser()` to set active user (no automatic session)
- `createAdminRole()` bypasses ALL access checks -- use sparingly, creates false positives

**Source:** `/core/modules/user/tests/src/Traits/UserCreationTrait.php`

### NodeCreationTrait
**Description:** Creates nodes with default values for testing.

| Method | Purpose | Returns |
|--------|---------|---------|
| `createNode($values)` | Create node entity with defaults | NodeInterface |
| `getNodeByTitle($title, $reset)` | Load node by title | NodeInterface or FALSE |
| `drupalCreateNode($values)` | Alias for createNode in BrowserTestBase | NodeInterface |

**Usage Example (Browser test)**:
```php
use Drupal\Tests\node\Traits\NodeCreationTrait;

class MyTest extends BrowserTestBase {
  use NodeCreationTrait;

  public function testNodeDisplay(): void {
    $node = $this->drupalCreateNode([
      'type' => 'article',
      'title' => 'Test Article',
      'status' => 1,
    ]);
    $this->drupalGet('node/' . $node->id());
    $this->assertSession()->pageTextContains('Test Article');
  }
}
```

**Gotchas:**
- Automatically populates title, type ('page'), uid (current user or anonymous)
- If node has 'body' field, auto-fills with random content unless provided
- Created nodes are NOT automatically deleted in Kernel tests (use Browser tests for auto-cleanup)

**Source:** `/core/modules/node/tests/src/Traits/NodeCreationTrait.php`

### ContentTypeCreationTrait
**Description:** Creates content types (node bundles) for testing.

| Method | Purpose | Returns |
|--------|---------|---------|
| `createContentType($values)` | Create node type entity | NodeTypeInterface |
| `drupalCreateContentType($values)` | Alias in BrowserTestBase | NodeTypeInterface |

**Usage Example:**
```php
$this->createContentType([
  'type' => 'landing_page',
  'name' => 'Landing Page',
]);
```

**Source:** `/core/modules/node/tests/src/Traits/ContentTypeCreationTrait.php`

### BlockCreationTrait
**Description:** Places blocks in regions for testing.

| Method | Purpose | Returns |
|--------|---------|---------|
| `placeBlock($plugin_id, $settings)` | Place block in theme region | BlockInterface |
| `drupalPlaceBlock($plugin_id, $settings)` | Alias in BrowserTestBase | BlockInterface |

**Usage Example:**
```php
$this->drupalPlaceBlock('system_branding_block', [
  'region' => 'header',
  'theme' => 'stark',
]);
```

**Source:** `/core/modules/block/tests/src/Traits/BlockCreationTrait.php`

### RandomGeneratorTrait
**Description:** Generates random data for test fixtures.

| Method | Purpose | Example Output |
|--------|---------|----------------|
| `randomMachineName($length)` | Lowercase alphanumeric | "abc123xyz" |
| `randomString($length)` | Mixed case + special chars | "Xy9$aB!c" |
| `randomObject($size)` | stdClass with random props | Object with $prop0..$propN |

**Usage Example:**
```php
$title = $this->randomMachineName(16);
$email = $this->randomMachineName() . '@example.com';
```

**Source:** `/core/tests/Drupal/Tests/RandomGeneratorTrait.php`

## Common Mistakes
- Using traits without understanding cleanup behavior -- database clutter in Kernel tests
- Creating users with insufficient permissions -- false negatives in tests
- Not importing trait namespace -- "Trait not found" error
- Calling `drupalLogin()` in Kernel tests -- method doesn't exist (use `setCurrentUser()` instead)
- Over-relying on traits for complex setup -- abstracts away what test is actually doing (be explicit when clarity matters)

## See Also
- [JavaScript Tests with WebDriverTestBase](javascript-tests.md)
- [Test Modules](test-modules.md)
- Reference: `/core/modules/*/tests/src/Traits/`
- [PHPUnit and Drupal Test Traits](https://www.drupalatyourfingertips.com/dtt)
