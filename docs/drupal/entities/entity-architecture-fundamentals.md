---
description: Entity architecture — two-layer system separating configuration from content
drupal_version: "11.x"
---

# Entity Architecture Fundamentals

## When to Use

When starting any Drupal entity or field development work, you need to understand the two-layer architecture that separates configuration from content and how entity types relate to bundles.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Store user-facing content | Content entities (Node, User, etc.) | Fieldable, translatable, versionable database records |
| Store site configuration | Config entities (NodeType, View, etc.) | Exportable YAML, version control friendly, deployment safe |
| Define content type structure | Bundle config entity | Defines which fields are available for a content entity bundle |
| Store actual field data | Content entity with fields | Uses field storage layer for flexible data modeling |

## Pattern

Drupal uses a two-layer system:

**Configuration Layer** (YAML files exported to sync):
```yaml
# node.type.article.yml
type: article
name: 'Article'
description: 'Use articles for time-sensitive content.'
```

**Implementation Layer** (PHP classes):
```php
#[ContentEntityType(
  id: 'node',
  bundle_entity_type: 'node_type',  // Links to config layer
  entity_keys: ['bundle' => 'type'],
)]
class Node extends ContentEntityBase {}
```

Key principles:
- **Separation of concerns**: Field storage defines technical specs (cardinality, type), field instances define bundle usage (label, required, settings)
- **Immutability**: Core properties locked after creation to prevent data corruption
- **Dependency tracking**: Config dependencies ensure correct install/uninstall order

Reference: `/core/lib/Drupal/Core/Entity/EntityType.php`, `/core/modules/node/src/Entity/Node.php`

## Common Mistakes

- **Wrong**: Creating content entities without a bundle system → **Right**: Use bundle_entity_type for flexible content modeling
- **Wrong**: Modifying locked field storage properties → **Right**: These are immutable after data exists; create new field instead
- **Wrong**: Missing config dependencies → **Right**: Always declare module and config dependencies or you'll get broken installs
- **Wrong**: Using Entity::load() in OOP code → **Right**: Inject entity_type.manager service and use getStorage() for testability

## See Also

- [Content Type Configuration](content-type-configuration.md) for YAML-based content type setup
- Reference: [Entity API documentation](https://www.drupal.org/docs/drupal-apis/entity-api)
