---
description: Test Drupal permission checks, role-based access, entity access, and route access control.
---

# Testing Access & Permissions

## When to Use
Verifying permission checks, role-based access, entity access, route access.

## Decision
| Access type | Test approach | Test type |
|---|---|---|
| Route access (can user visit path?) | drupalGet() + statusCodeEquals() | Browser |
| Entity access (can user view/edit/delete?) | node_access() or entity access API | Kernel |
| Permission existence | Role::load()->hasPermission() | Kernel |
| Field access | Field access API | Kernel |

## Pattern
**Testing route access (Browser)**:
```php
namespace Drupal\Tests\my_module\Functional;

use Drupal\Tests\BrowserTestBase;

class AccessTest extends BrowserTestBase {

  protected $defaultTheme = 'stark';
  protected static $modules = ['node', 'my_module'];

  public function testAdminAccess(): void {
    $user = $this->drupalCreateUser(['access administration pages']);
    $this->drupalLogin($user);

    $this->drupalGet('admin/config');
    $this->assertSession()->statusCodeEquals(200);
  }

  public function testAccessDenied(): void {
    $user = $this->drupalCreateUser();
    $this->drupalLogin($user);

    $this->drupalGet('admin/config');
    $this->assertSession()->statusCodeEquals(403);
  }
}
```

**Testing entity access (Kernel)**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Drupal\node\Entity\Node;

class EntityAccessTest extends KernelTestBase {

  use UserCreationTrait;

  protected static $modules = ['system', 'user', 'node'];

  protected function setUp(): void {
    parent::setUp();
    $this->installEntitySchema('user');
    $this->installEntitySchema('node');
    $this->installSchema('node', ['node_access']);
  }

  public function testNodeAccess(): void {
    $node = Node::create(['type' => 'page', 'status' => 0]);
    $node->save();

    $user = $this->createUser(['access content']);
    $this->assertFalse($node->access('view', $user));

    $admin = $this->createUser(['bypass node access']);
    $this->assertTrue($node->access('view', $admin));
  }
}
```

**Testing custom permissions**:
```php
public function testCustomPermission(): void {
  $user = $this->createUser(['my_module do_special_thing']);
  $service = $this->container->get('my_module.special_service');

  $this->setCurrentUser($user);
  $this->assertTrue($service->canDoThing());
}
```

Reference: `/core/modules/node/tests/src/Kernel/NodeAccessTest.php`

## Common Mistakes
- Not installing `node_access` schema -- access checks return unexpected results
- Testing with anonymous user when user 0/1 doesn't exist -- undefined behavior
- Using `bypass node access` for all tests -- masks permission bugs
- Not testing edge cases (unpublished content, different ownership) -- false positives
- Forgetting to call `node_access_rebuild()` when access rules change -- stale access grants

## See Also
- Reference: `/core/modules/node/tests/src/Kernel/NodeAccessTest.php`
- Example: `/core/modules/user/tests/src/Unit/PermissionAccessCheckTest.php`
