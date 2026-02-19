---
description: Views Integration — ComponentRow and ComponentStyle plugins, entity context
drupal_version: "11.x"
---

# Views Integration

**Sub-module:** `ui_patterns_views`
**Dependencies:** `views`, `ui_patterns`

## When to Use

> Use `ui_patterns_views` when you want Views results rows or the whole result set rendered through SDC components, with entity field sources available per row.

## Decision

| Plugin Type | Class | Purpose |
|-------------|-------|---------|
| **Row** | `ComponentRow` | Renders each Views result row using a component |
| **Style** | `ComponentStyle` | Wraps the collection of rendered rows in a component |

| Need | Use |
|------|-----|
| Per-row component rendering with entity field sources | `ComponentRow` (row plugin) |
| Wrapping all rows in a container component (card grid, carousel) | `ComponentStyle` (style plugin) |

## Pattern

### Configuration in Views UI

```
1. Set Format to "Component (UI Patterns)" for style plugin
2. Set Show to "Component (UI Patterns)" for row plugin
3. Configure the component, mapping entity fields to props and slots
```

### Row plugin entity context

```php
$context['entity'] = EntityContext::fromEntity($row->_entity);
$context['bundle'] = new Context(ContextDefinition::create('string'), $bundle);
$context['ui_patterns_views:row:index'] = new Context(new ContextDefinition('integer'), $row->index);
```

Entity field sources are available because entity context is injected per row.

## Common Mistakes

- **Wrong**: Using row plugin without entity-based views → **Right**: Field property sources require an entity base table; non-entity views will not have field sources
- **Wrong**: Expecting row-level sources in the style plugin → **Right**: The style plugin operates on the collection of rows; entity-level sources are only in the row plugin
- **Wrong**: Expecting Fields plugin options to carry over → **Right**: Component rendering replaces the fields display; only `hide_empty` is preserved

## See Also

- [Source Plugins](source-plugins.md)
- Reference: `modules/contrib/ui_patterns/modules/ui_patterns_views/`
