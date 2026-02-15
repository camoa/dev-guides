---
description: Drupal entity type hierarchy follows LSP - subtypes can substitute for base types
drupal_version: "11.x"
---

# Entity Type Hierarchy - Liskov Substitution (LSP)

## When to Use

Drupal's entity system follows LSP -- any ContentEntityBase subclass (Node, User, Term) can be used wherever ContentEntityBase is expected. Behavioral contracts must be preserved.

## Decision

| Entity type | Extends | Behavioral contract |
|---|---|---|
| All content entities | ContentEntityBase | Field API, translations, revisions |
| All config entities | ConfigEntityBase | Config storage, dependencies |
| Node, User, Term | ContentEntityBase | Can be used interchangeably where ContentEntityBase expected |
| Custom entity | ContentEntityBase OR ConfigEntityBase | Must honor parent contract |

## Pattern

**GOOD: Following entity LSP**

```php
// Any function accepting ContentEntityInterface works with Node, User, Term
function processEntity(ContentEntityInterface $entity) {
  $entity->setNewRevision(TRUE);              // All content entities support revisions
  $entity->set('field_name', 'value');        // All support Field API
  $entity->addTranslation('es', ['title' => 'Titulo']);  // All support translations
}

// Works with any content entity
processEntity($node);   // Node extends ContentEntityBase
processEntity($user);   // User extends ContentEntityBase
processEntity($term);   // Term extends ContentEntityBase
```

**BAD: Violating entity LSP**

```php
function processEntity(ContentEntityInterface $entity) {
  // Assuming specific entity type breaks LSP
  $title = $entity->title->value;  // Fails for entities without 'title' field
  $entity->setPublished(TRUE);     // Not all entities have published status
}
```

Reference:

- `/core/lib/Drupal/Core/Entity/ContentEntityBase.php` -- base class defining contract
- `/core/modules/node/src/Entity/Node.php` -- honors ContentEntityBase contract

## Common Mistakes

- Type-hinting specific entity class (Node) when EntityInterface would work -- use interface. **WHY:** Can't reuse code for User, Term; tight coupling to implementation
- Assuming all entities have specific fields (title, status) -- check field existence. **WHY:** Custom entities may not have title; causes fatal errors
- Not calling parent methods in entity overrides -- call parent::method(). **WHY:** Breaks entity lifecycle, validation, access control
- Violating entity behavioral contracts (e.g., save() not updating DB) -- honor expected behavior. **WHY:** Entity API expects save() to persist; breaking this breaks entity system

## See Also

- [Form Hierarchy](form-hierarchy-lsp.md) for form LSP patterns
- [Entity Interfaces](entity-interfaces-isp.md) for interface contracts
- Reference: `/core/lib/Drupal/Core/Entity/EntityInterface.php`
