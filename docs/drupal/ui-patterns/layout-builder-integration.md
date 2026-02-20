---
description: Layout Builder integration — exposing components as layout plugins with slot regions
drupal_version: "10.3+ / 11"
---

## Layout Builder Integration

**Sub-module:** `ui_patterns_layouts`
**Dependencies:** `layout_discovery`, `ui_patterns`

### What It Does

`ui_patterns_layouts` exposes every SDC component (that has slots) as a Drupal Layout plugin. Each component's slots become layout **regions**, and its props become configurable via the Layout Builder section configuration form.

### How It Works

`ComponentLayout` extends `LayoutDefault` and uses the `ComponentFormBuilderTrait`. A deriver (`ComponentLayout` deriver) creates one layout derivative per component, mapping slots to regions:

```
Component: my_theme:two-column
  Slots: main, sidebar

Layout Plugin: ui_patterns:my_theme:two-column
  Regions: main, sidebar
```

The `build()` method merges Layout Builder regions into component slots:

```php
public function build(array $regions) {
    $build = $this->buildComponentRenderable($componentId, $contexts);
    foreach ($regionNames as $region_name) {
        $build['#slots'][$region_name] = $regions[$region_name];
        $build[$region_name] = &$build['#slots'][$region_name];
    }
    return $build;
}
```

### Configuration Form

When configuring a Layout Builder section using a UI Patterns layout, the form exposes:
- **Props**: Each prop displays its source selector and widget
- **Variant**: If the component has variants, a variant selector appears
- **Slots are not configurable** in the layout form -- they are filled by blocks placed in regions

### Entity Context

The layout automatically resolves entity context through `ChainContextEntityResolver`, making entity field sources available for props.

### Workflow

```
1. Enable ui_patterns_layouts
2. Components with slots appear in Layout Builder's "Add section" dialog
3. Choosing a component layout shows props configuration
4. Place blocks into the component's slot regions
5. Props can pull from entity fields, manual input, or other sources
```

### Config YAML

When you enable Layout Builder on an entity display and add a UI Patterns layout section, the configuration is stored in the entity view display. After `drush config:export`, find it in `core.entity_view_display.{entity_type}.{bundle}.{view_mode}.yml`:

```yaml
# In core.entity_view_display.node.page.default.yml
third_party_settings:
  layout_builder:
    enabled: true
    allow_custom: false
    sections:
      - layout_id: 'ui_patterns:ui_suite_daisyui:grid_2_regions'
        layout_settings:
          label: 'Two Column Layout'
          ui_patterns:
            component_id: 'ui_suite_daisyui:grid_2_regions'
            variant_id:
              source_id: select
              source:
                value: ''
            props:
              container_type:
                source_id: select
                source:
                  value: 'container mx-auto'
              gap:
                source_id: number
                source:
                  value: '4'
              gap_lg:
                source_id: number
                source:
                  value: '8'
            slots: {}
        components:
          550e8400-e29b-41d4-a716-446655440000:
            uuid: 550e8400-e29b-41d4-a716-446655440000
            region: col_first
            configuration:
              id: 'ui_patterns:ui_suite_daisyui:card'
              label: 'Article Card'
              label_display: '0'
              provider: ui_patterns_blocks
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
                slots:
                  title:
                    sources:
                      - source_id: textfield
                        source:
                          value: 'Section Title'
                        _weight: '0'
            weight: 0
            additional: {}
```

Key observations:
- The `layout_id` uses the format `ui_patterns:{provider}:{component}`.
- `layout_settings.ui_patterns` follows the `ui_patterns_component` schema: `component_id`, `variant_id`, `props`, `slots`.
- Layout **slots are empty** in the layout config because they are filled by `components` placed in regions.
- Components nested inside regions follow the block config schema (`block.settings.ui_patterns:*:*`).
- The `layout_plugin.settings.*` schema adds the `ui_patterns` mapping to the standard layout settings.

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Expecting components without slots to appear as layouts | Layout plugins require at least one region. Components with only props and no slots will not be exposed as layouts. |
| Configuring slots in the layout form | Slots in layouts are filled by blocks in regions, not by the layout configuration form. Props are configured; slots receive blocks. |
| Using `ckeditor_layouts` with UI Patterns layouts | Incompatible because `ckeditor_layouts` loads layouts through the theme manager, but SDC does not pass through the theme manager. |

### See Also

- Drupal Layout Builder Guide
- [Blocks Integration](#blocks-integration)