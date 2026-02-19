---
description: Field Formatters — ComponentFormatter and ComponentFormatterSingle, granularity
drupal_version: "11.x"
---

# Field Formatters

**Sub-module:** `ui_patterns_field_formatters`
**Dependencies:** `ui_patterns`

## When to Use

> Use `ui_patterns_field_formatters` to render field output through SDC components in Manage Display. Choose the formatter based on whether the component handles all values at once or one at a time.

## Decision

| Formatter | Plugin ID | Cardinality | Context | Best For |
|-----------|-----------|-------------|---------|----------|
| `ComponentFormatter` | `ui_patterns_component` | Multi-value (>1 or unlimited) | `field_granularity:items` | List components receiving all items (image gallery, link list) |
| `ComponentFormatterSingle` | `ui_patterns_component_per_item` | Any | `field_granularity:item` | Simple formatters where each value gets its own component instance |

## Pattern

### Setup in Manage Display

```
1. Select "Component (UI Patterns)" as the field formatter
2. Choose a component from the component selector
3. Map the field's properties to component props and slots
```

### Context available in formatters

- Entity context
- Bundle context
- Field items context
- Field index context (for per-item rendering)

Both formatters use `ComponentSettingsFormBuilderTrait` for the standard configuration form.

## Common Mistakes

- **Wrong**: Using `ComponentFormatter` (multi-value) on single-cardinality fields → **Right**: It requires cardinality >1 or unlimited; use `ComponentFormatterSingle` for single-value fields
- **Wrong**: Expecting non-field sources to be absent — they are still available → **Right**: Global sources (menus, paths) remain available; entity + field sources are the primary context

## See Also

- [Source Plugins](source-plugins.md)
- Reference: `modules/contrib/ui_patterns/modules/ui_patterns_field_formatters/`
