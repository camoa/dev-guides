---
description: Views integration — row and style plugins for rendering Views results as components
drupal_version: "10.3+ / 11"
---

## Views Integration

**Sub-module:** `ui_patterns_views`
**Dependencies:** `views`, `ui_patterns`

### What It Does

Provides two Views plugins:

| Plugin Type | Class | Purpose |
|---|---|---|
| **Row** | `ComponentRow` | Renders each Views result row using a component |
| **Style** | `ComponentStyle` | Wraps the collection of rendered rows in a component |

### Row Plugin

The `ComponentRow` extends Views' `Fields` row plugin. For each row, it:

1. Gets the entity from the view result (`$row->_entity`)
2. Builds entity context + bundle context + row index context
3. Calls `buildComponentRenderable()` with the configured component

Entity field sources are available because entity context is injected:

```php
$context['entity'] = EntityContext::fromEntity($row->_entity);
$context['bundle'] = new Context(ContextDefinition::create('string'), $bundle);
$context['ui_patterns_views:row:index'] = new Context(new ContextDefinition('integer'), $row->index);
```

### Style Plugin

The `ComponentStyle` wraps rows in a wrapper component. The rendered rows are passed as context via `ui_patterns_views:rows`. This is useful for list-style components (card grids, carousels) where individual rows need to be wrapped in a container component.

### Configuration

In Views UI:
1. Set the **Format** to "Component (UI Patterns)" for style
2. Set the **Show** to "Component (UI Patterns)" for row
3. Configure the component, mapping entity fields to props and slots

### Config YAML

Views configuration with UI Patterns row and style plugins is stored in `views.view.{view_name}.yml`. After `drush config:export`, the relevant sections under each display's `display_options`:

```yaml
# In views.view.article_cards.yml
display:
  default:
    display_options:
      # Style plugin wraps all rows in a container component
      style:
        type: ui_patterns
        options:
          ui_patterns:
            ui_patterns:
              component_id: 'ui_suite_daisyui:grid_cols'
              variant_id:
                source_id: select
                source:
                  value: ''
              props:
                grid_cols:
                  source_id: number
                  source:
                    value: '1'
                grid_cols_md:
                  source_id: number
                  source:
                    value: '2'
                grid_cols_lg:
                  source_id: number
                  source:
                    value: '3'
                gap:
                  source_id: number
                  source:
                    value: '4'
              slots: {}
      # Row plugin renders each result as a component
      row:
        type: ui_patterns
        options:
          hide_empty: false
          ui_patterns:
            component_id: 'ui_suite_daisyui:card'
            variant_id:
              source_id: select
              source:
                value: default
            props:
              heading_level:
                source_id: select
                source:
                  value: '3'
              url:
                source_id: 'entity_link:node'
                source:
                  template: canonical
            slots:
              title:
                sources:
                  - source_id: 'field_property:node:article:title'
                    source:
                      type: value
                    _weight: '0'
              text:
                sources:
                  - source_id: 'field_property:node:article:body'
                    source:
                      type: text_processed
                    _weight: '0'
              image:
                sources:
                  - source_id: 'field_property:node:article:field_image'
                    source:
                      type: entity
                    _weight: '0'
```

Key observations:
- The style plugin has **double nesting**: `options.ui_patterns.ui_patterns` (the outer `ui_patterns` is the Views sub-key, the inner is the `ui_patterns_component` schema). This matches the `views.ui_patterns_configuration` schema.
- The row plugin has **single nesting**: `options.ui_patterns` maps directly to `ui_patterns_component`.
- Row-level entity field sources use derived source IDs like `field_property:node:article:title` because entity context is available per row.
- The style plugin wraps all rows; the rendered rows are injected into the component's slot via the `ui_patterns_views:rows` context.

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Using row plugin without entity-based views | Field property sources require an entity base table. Non-entity views will not have field sources available. |
| Expecting row-level sources in the style plugin | The style plugin operates on the collection of rows, not individual rows. Entity-level sources are available only in the row plugin. |
| Not enabling "Hide empty" | The `hide_empty` option from the Fields row plugin is preserved. Other Fields options are stripped since component rendering replaces the fields display. |

### See Also

- Drupal Views Guide
- [Source Plugins](#source-plugins)