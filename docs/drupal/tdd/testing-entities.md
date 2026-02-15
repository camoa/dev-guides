---
description: Test Drupal entity CRUD operations, field values, entity references, and validation constraints.
---

# Testing Entities

## When to Use
Testing entity CRUD, field values, entity references, computed fields, validation.

## Decision
| Operation | Minimum test type | Notes |
|---|---|---|
| Entity CRUD (create/load/update/delete) | Kernel | Database required |
| Field value storage/retrieval | Kernel | Field system required |
| Entity access control | Kernel or Browser | Browser if UI matters |
| Entity rendering | Browser | Needs view modes, themes |

## Pattern
**Testing entity CRUD (Kernel)**:
```php
namespace Drupal\Tests\my_module\Kernel;

use Drupal\KernelTests\KernelTestBase;
use Drupal\node\Entity\Node;

class EntityCrudTest extends KernelTestBase {

  protected static $modules = ['system', 'user', 'node', 'field'];

  protected function setUp(): void {
    parent::setUp();
    $this->installEntitySchema('user');
    $this->installEntitySchema('node');
    $this->installSchema('node', ['node_access']);
    $this->installConfig(['node']);
  }

  public function testNodeCreation(): void {
    $node = Node::create([
      'type' => 'page',
      'title' => 'Test Node',
    ]);
    $node->save();

    $this->assertNotNull($node->id());
    $loaded_node = Node::load($node->id());
    $this->assertEquals('Test Node', $loaded_node->getTitle());
  }
}
```

**Testing field values**:
```php
public function testFieldValue(): void {
  $node = Node::create([
    'type' => 'article',
    'title' => 'Test',
    'body' => ['value' => 'Content', 'format' => 'plain_text'],
  ]);
  $node->save();

  $this->assertEquals('Content', $node->body->value);
  $this->assertEquals('plain_text', $node->body->format);
}
```

**Testing entity reference fields**:
```php
public function testEntityReference(): void {
  $user = $this->createUser();
  $node = Node::create([
    'type' => 'page',
    'title' => 'Test',
    'uid' => $user->id(),
  ]);
  $node->save();

  $this->assertEquals($user->id(), $node->getOwnerId());
  $this->assertEquals($user->label(), $node->getOwner()->label());
}
```

Reference: `/core/modules/node/tests/src/Kernel/`

## Common Mistakes
- Not installing entity schema -- "Table doesn't exist"
- Forgetting `node_access` schema for nodes -- access checks fail
- Not saving entity after modification -- changes lost
- Testing entity rendering in Kernel tests -- no theme system (use Browser test)
- Not testing validation constraints -- invalid data accepted

## See Also
- Reference: `/core/modules/node/tests/src/Kernel/NodeAccessTest.php`
- Example: `/core/modules/system/tests/modules/entity_test/`
