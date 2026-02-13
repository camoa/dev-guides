---
description: Entity reference fields for relationships with referential integrity
drupal_version: "11.x"
---

# Entity Reference Patterns

## When to Use

When creating relationships between entities (nodes ↔ taxonomy, nodes ↔ users, nodes ↔ nodes), requiring referential integrity and access-controlled relationships.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Reference single entity type | entity_reference with target_type | Simple, enforced type constraint |
| Reference multiple entity types | entity_reference with dynamic handler | Flexible but complex queries |
| Reference with revisions | entity_reference_revisions | Track specific revision of target |
| Auto-create referenced entities | auto_create: true in handler settings | Users can create terms/entities on the fly |
| Restrict by bundle | target_bundles in handler settings | Performance and UX improvement |

## Pattern

Entity reference field storage:

```yaml
# field.storage.node.field_related.yml
type: entity_reference
settings:
  target_type: node
```

Field instance with restrictions:

```yaml
# field.field.node.article.field_related.yml
settings:
  handler: 'default:node'
  handler_settings:
    target_bundles:
      article: article
      page: page
    sort:
      field: title
      direction: ASC
    auto_create: false
    auto_create_bundle: null
```

Reference with revisions:

```php
BaseFieldDefinition::create('entity_reference_revisions')
  ->setSetting('target_type', 'paragraph')
  ->setSetting('handler', 'default');
```

Reference: `/core/modules/field/src/Plugin/Field/FieldType/EntityReferenceItem.php`

## Common Mistakes

- **Wrong**: Not restricting target_bundles → **Right**: Performance hit loading all possible targets; poor UX
- **Wrong**: Using auto_create without access control → **Right**: Users create entities bypassing permissions
- **Wrong**: Missing target_type validation → **Right**: Referencing wrong entity type; data corruption
- **Wrong**: Not checking entity access before rendering → **Right**: Security issue; users see content they shouldn't
- **Wrong**: Forgetting to clear entity cache → **Right**: Stale references after entity updates

**Security**:
- ALWAYS validate entity access when rendering references. Use entity.repository service.
- auto_create: true allows users to create entities. Validate permissions in hook_entity_create_access().
- Check both field access AND referenced entity access. Field access isn't enough.
- Use handler_settings validation to prevent privilege escalation via reference manipulation.

**Performance**:
- Restrict target_bundles to avoid loading all entities of a type.
- Use Views-based selection handler for complex filtering (avoid loading thousands of options).
- Entity reference fields trigger entity loads. Use entity query for large result sets, not field loading.
- Set cardinality wisely. Unlimited entity references can create N+1 query problems.

**Recent improvements** (Drupal 10.5/11.2):
- Performance regression fix for sites with large revision counts when calculating latest revision
- Optimized entity reference queries save hundreds of queries on complex pages
- See: https://www.drupal.org/project/drupal/releases/11.2.6

## See Also

- [View Mode Development](view-mode-development.md)
- [File and Image Field Patterns](file-and-image-field-patterns.md)
- Reference: [Entity reference field](https://www.drupal.org/docs/drupal-apis/entity-api/entity-types)
