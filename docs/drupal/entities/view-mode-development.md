---
description: Custom view modes for specialized display contexts
drupal_version: "11.x"
---

# View Mode Development

## When to Use

When creating custom display contexts beyond default/teaser (e.g., 'card', 'embed', 'json_api'), requiring entity-specific formatter configurations.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| New display context | Custom view mode | Distinct formatter/field configurations |
| Entity type specific | View mode for single entity type | Scoped to one entity type |
| Shared across entities | Cross-entity view mode | Reuse 'card' for nodes, users, terms |

## Pattern

View mode config in `config/install/core.entity_view_mode.node.card.yml`:

```yaml
langcode: en
status: true
dependencies:
  module:
    - node
id: node.card
label: 'Card'
targetEntityType: node
cache: true
```

Programmatic creation:

```php
use Drupal\Core\Entity\Entity\EntityViewMode;

EntityViewMode::create([
  'id' => 'node.card',
  'label' => 'Card',
  'targetEntityType' => 'node',
  'cache' => TRUE,
])->save();
```

Then configure view display for the mode:
`core.entity_view_display.node.article.card.yml`

Reference: `/core/lib/Drupal/Core/Entity/EntityViewMode.php`

## Common Mistakes

- **Wrong**: Not enabling view mode on entity type → **Right**: View mode exists but not usable; enable in Field UI
- **Wrong**: Missing cache: true → **Right**: No render caching; performance issues
- **Wrong**: Creating view mode without view display config → **Right**: Mode exists but uses default display
- **Wrong**: Wrong targetEntityType → **Right**: View mode won't appear for entity type
- **Wrong**: Forgetting module dependencies → **Right**: Config import failures

**Performance**:
- ALWAYS set cache: true. View modes without caching bypass render cache.
- Use view modes to create cacheable variations of content for different contexts.

**Development Standards**:
- Use semantic names (card, embed, summary) not layout names (sidebar, homepage)
- Create view display configs for each bundle that needs the mode
- Document expected usage in module README

## See Also

- [View Display Configuration](view-display-configuration.md)
- [Entity Reference Patterns](entity-reference-patterns.md)
- Reference: [Display modes](https://www.drupal.org/docs/drupal-apis/entity-api/display-modes-view-modes-and-form-modes)
