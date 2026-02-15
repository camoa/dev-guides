---
description: Implement only the entity interfaces your Drupal entity actually needs
drupal_version: "11.x"
---

# Entity Interfaces - Interface Segregation (ISP)

## When to Use

Drupal provides role-specific entity interfaces. Implement only the interfaces your entity needs -- don't implement EntityPublishedInterface if your entity can't be published.

## Decision

| Interface | Implement when entity... | Provides |
|---|---|---|
| EntityInterface | Is any entity | Base entity contract |
| ContentEntityInterface | Has fields | Field API methods |
| ConfigEntityInterface | Is configuration | Config-specific methods |
| EntityOwnerInterface | Has an owner | getOwner(), setOwner() |
| EntityPublishedInterface | Can be published/unpublished | isPublished(), setPublished() |
| RevisionableInterface | Supports revisions | Revision methods |
| TranslatableInterface | Supports translations | Translation methods |

## Pattern

**GOOD: Implementing only needed interfaces (ISP)**

```php
// Node needs owner, published, revisions
class Node extends ContentEntityBase implements
  NodeInterface,
  EntityOwnerInterface,
  EntityPublishedInterface,
  RevisionLogInterface {

  use EntityOwnerTrait;
  use EntityPublishedTrait;

  // Only implement methods for interfaces we need
}

// Simple custom entity - no owner, no published
class CustomEntity extends ContentEntityBase implements CustomEntityInterface {
  // No unnecessary interfaces
}
```

**BAD: Fat interface forcing unused methods (violates ISP)**

```php
// Hypothetical bad design
interface EntityInterface {
  public function getOwner();          // Not all entities have owner
  public function isPublished();       // Not all entities publishable
  public function getRevisionId();     // Not all entities revisionable
  // 50 more methods most entities don't need
}

// Forces fake implementations
class SimpleEntity implements EntityInterface {
  public function getOwner() {
    throw new \Exception('No owner');  // Fake implementation
  }
}
```

Reference:

- `/core/lib/Drupal/Core/Entity/EntityInterface.php` -- minimal base
- `/core/lib/Drupal/Core/Entity/EntityOwnerInterface.php` -- focused on ownership
- `/core/lib/Drupal/user/EntityOwnerTrait.php` -- trait implementing interface

## Common Mistakes

- Implementing EntityOwnerInterface without storing owner -- don't implement. **WHY:** Interface contract requires functional getOwner(); fake implementation breaks ownership system
- Creating one interface with all entity methods -- create role interfaces. **WHY:** Forces entities to implement methods they don't need; bloats simple entities
- Not using EntityOwnerTrait when implementing EntityOwnerInterface -- use trait. **WHY:** Reinventing wheel; trait provides tested implementation
- Implementing interfaces without understanding contract -- read interface docs. **WHY:** Interface promises specific behavior; violating breaks dependent code

## See Also

- [Injection Interfaces](injection-interfaces-isp.md) for dependency injection ISP
- [Entity Hierarchy](entity-hierarchy-lsp.md) for entity architecture
- Reference: `/core/lib/Drupal/Core/Entity/` (entity interfaces)
